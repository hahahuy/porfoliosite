(function () {
    // Get configuration from the current script tag
    var hasPageview = false;
    var locationObj = window.location;
    var documentObj = window.document;
    var currentScript = documentObj.currentScript;
    var apiUrl =
      currentScript.getAttribute("data-api") ||
      new URL(currentScript.src).origin + "/api/event";
    var domain = currentScript.getAttribute("data-domain");
  
    // Helper: Ignore an event and optionally log a reason
    function ignoreEvent(eventName, reason, callbackObj) {
      if (reason) {
        console.warn("Ignoring Event: " + reason);
      }
      if (callbackObj && callbackObj.callback) {
        callbackObj.callback();
      }
      if (eventName === "pageview") {
        hasPageview = true;
      }
    }
  
    // Variables used for engagement tracking
    var engagementStart = null; // Time when engagement started
    var accumulatedTime = 0;    // Time accumulated while page was visible
    var currentUrl = locationObj.href;
    var props = {};
    var lastScrollPos = -1;     // Last recorded scroll position
    var hasVisibilityListener = false;
    var isEngaging = false;
  
    // Get the maximum height of the document
    function getDocumentHeight() {
      var body = documentObj.body || {};
      var docElem = documentObj.documentElement || {};
      return Math.max(
        body.scrollHeight || 0,
        body.offsetHeight || 0,
        body.clientHeight || 0,
        docElem.scrollHeight || 0,
        docElem.offsetHeight || 0,
        docElem.clientHeight || 0
      );
    }
  
    // Get the current scroll position plus viewport height,
    // or return the document height if the viewport is taller.
    function getScrollPosition() {
      var body = documentObj.body || {};
      var docElem = documentObj.documentElement || {};
      var viewportHeight = window.innerHeight || docElem.clientHeight || 0;
      var scrollY = window.scrollY || docElem.scrollTop || body.scrollTop || 0;
      return getDocumentHeight() <= viewportHeight ? getDocumentHeight() : scrollY + viewportHeight;
    }
  
    var documentHeight = getDocumentHeight();
    var maxScrollPos = getScrollPosition();
  
    // Check if user engagement should trigger an event.
    function sendEngagementEvent() {
      var elapsedTime = engagementStart ? accumulatedTime + (Date.now() - engagementStart) : accumulatedTime;
      // If not currently engaging, no pageview yet, and either we scrolled further or 3000ms have passed:
      if (!isEngaging && !hasPageview && (lastScrollPos < maxScrollPos || elapsedTime >= 3000)) {
        lastScrollPos = maxScrollPos;
        // Reset engagement state after 300ms
        setTimeout(function () {
          isEngaging = false;
        }, 300);
        var eventData = {
          n: "engagement",
          sd: Math.round((maxScrollPos / documentHeight) * 100), // scroll depth percentage
          d: domain,
          u: currentUrl,
          p: props,
          e: elapsedTime
        };
        engagementStart = null;
        accumulatedTime = 0;
        sendEvent(apiUrl, eventData);
      }
    }
  
    // Main tracking function for events (pageviews, custom events, etc.)
    function trackEvent(eventName, options) {
      var isPageview = eventName === "pageview";
  
      // Ignore events on local environments
      if (
        /^localhost$|^127(\.[0-9]+){0,2}\.[0-9]+$|^\[::1?\]$/.test(locationObj.hostname) ||
        locationObj.protocol === "file:"
      ) {
        return ignoreEvent(eventName, "localhost", options);
      }
      // Ignore events if running in headless browsers or testing frameworks (unless overridden)
      if (
        (window._phantom || window.__nightmare || window.navigator.webdriver || window.Cypress) &&
        !window.__plausible
      ) {
        return ignoreEvent(eventName, null, options);
      }
      try {
        if (window.localStorage.plausible_ignore === "true") {
          return ignoreEvent(eventName, "localStorage flag", options);
        }
      } catch (err) {}
  
      // Build the event payload
      var payload = {
        n: eventName,
        u: locationObj.href,
        d: domain,
        r: documentObj.referrer || null
      };
      if (options && options.meta) {
        payload.m = JSON.stringify(options.meta);
      }
      if (options && options.props) {
        payload.p = options.props;
      }
  
      // For pageview events, initialize engagement tracking
      if (isPageview) {
        hasPageview = false;
        currentUrl = payload.u;
        props = payload.p;
        lastScrollPos = -1;
        accumulatedTime = 0;
        engagementStart = Date.now();
        if (!hasVisibilityListener) {
          documentObj.addEventListener("visibilitychange", function () {
            if (documentObj.visibilityState === "hidden") {
              accumulatedTime += Date.now() - engagementStart;
              engagementStart = null;
              sendEngagementEvent();
            } else {
              engagementStart = Date.now();
            }
          });
          hasVisibilityListener = true;
        }
      }
      sendEvent(apiUrl, payload, options);
    }
  
    // Helper to send the event payload via fetch
    function sendEvent(url, data, callbackObj) {
      if (window.fetch) {
        fetch(url, {
          method: "POST",
          headers: { "Content-Type": "text/plain" },
          keepalive: true,
          body: JSON.stringify(data)
        }).then(function (response) {
          if (callbackObj && callbackObj.callback) {
            callbackObj.callback({ status: response.status });
          }
        });
      }
    }
  
    // Update document height periodically on load
    window.addEventListener("load", function () {
      documentHeight = getDocumentHeight();
      var count = 0;
      var intervalId = setInterval(function () {
        documentHeight = getDocumentHeight();
        if (++count === 15) {
          clearInterval(intervalId);
        }
      }, 200);
    });
  
    // Update the maximum scroll position on scroll
    documentObj.addEventListener("scroll", function () {
      documentHeight = getDocumentHeight();
      var currentPos = getScrollPosition();
      if (maxScrollPos < currentPos) {
        maxScrollPos = currentPos;
      }
    });
  
    // Process any queued events if the plausible object was used before the script loaded
    var queuedEvents = (window.plausible && window.plausible.q) || [];
    window.plausible = trackEvent;
    for (var i = 0; i < queuedEvents.length; i++) {
      trackEvent.apply(this, queuedEvents[i]);
    }
  
    // Handle SPA navigation and pageviews
    var previousPathname;
    function triggerPageview(forceTrigger) {
      if (forceTrigger && previousPathname === locationObj.pathname) return;
      if (forceTrigger && hasVisibilityListener) {
        sendEngagementEvent();
        documentHeight = getDocumentHeight();
        maxScrollPos = getScrollPosition();
      }
      previousPathname = locationObj.pathname;
      trackEvent("pageview");
    }
    function triggerPageviewCallback() {
      triggerPageview(true);
    }
    var historyObj = window.history;
    if (historyObj.pushState) {
      var originalPushState = historyObj.pushState;
      historyObj.pushState = function () {
        originalPushState.apply(this, arguments);
        triggerPageviewCallback();
      };
      window.addEventListener("popstate", triggerPageviewCallback);
    }
    if (documentObj.visibilityState === "prerender") {
      documentObj.addEventListener("visibilitychange", function () {
        if (!previousPathname && documentObj.visibilityState === "visible") {
          triggerPageview();
        }
      });
    } else {
      triggerPageview();
    }
    window.addEventListener("pageshow", function (event) {
      if (event.persisted) {
        triggerPageview();
      }
    });
  })();
  