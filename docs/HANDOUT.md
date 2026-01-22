# Project handover document

**Website:** [https://hahuy.site](https://hahuy.site)
**Purpose:** Personal portfolio site with simple backend and ML demo endpoints

---

## 1. High level architecture

* Single EC2 instance on AWS
* Static public IP via Elastic IP
* Nginx as reverse proxy
* Backend app served by Gunicorn on localhost
* HTTPS via Let’s Encrypt Certbot
* DNS managed at Namecheap

Traffic flow:

```
User → hahuy.site → Elastic IP → Nginx (80/443) → Gunicorn (127.0.0.1:8000)
```

---

## 2. AWS resources

### EC2

* OS: Amazon Linux
* Instance type: small instance suitable for portfolio use
* Public access via Elastic IP
* SSH access restricted by Security Group

### Elastic IP

* Attached to the EC2 instance
* Must remain attached to avoid charges and DNS breakage

### Security Group (critical)

Inbound rules:

* SSH 22, source limited to owner IP
* HTTP 80, open to all
* HTTPS 443, open to all

Do not expose backend ports publicly.

---

## 3. Domain and DNS

* Domain registrar: Namecheap
* Domain: hahuy.site
* DNS records:

  * A record `@` → Elastic IP
  * A record `www` → Elastic IP

Any IP change requires updating Namecheap DNS.

---

## 4. Web server configuration

### Nginx

Config file:

```
/etc/nginx/conf.d/myapp.conf
```

Structure:

* One server block on port 80

  * Serves ACME challenge
  * Redirects all traffic to HTTPS
* One server block on port 443

  * Terminates SSL
  * Proxies traffic to backend on 127.0.0.1:8000

After editing Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

## 5. HTTPS and certificates

* Managed by Certbot with Nginx plugin
* Certificate path:

```
/etc/letsencrypt/live/hahuy.site/
```

Check certificate status:

```bash
sudo certbot certificates
```

Test renewal:

```bash
sudo certbot renew --dry-run
```

Do not manually edit files inside `/etc/letsencrypt`.

---

## 6. Backend application

* Runs on localhost only
* Port: 8000
* Served via Gunicorn
* Entry point and framework depend on project codebase

Expected behavior:

* App must bind to `127.0.0.1:8000`
* App must not bind to `0.0.0.0` directly

If backend changes port, Nginx config must be updated.

---

## 7. Deployment workflow

Current model:

* Code pulled directly onto EC2
* Backend restarted after changes

Recommended commands:

```bash
sudo systemctl restart myapp
sudo systemctl status myapp
```

Note: The systemd service is named `myapp` (not `gunicorn`). This service manages the Gunicorn process.

---

## 8. Safe change rules

Before making changes:

* Confirm SSH access works
* Backup Nginx config
* Run `nginx -t` before reload

Never:

* Delete Elastic IP
* Open backend ports publicly
* Edit certbot managed SSL files manually
* Stop instance without checking Elastic IP attachment

---

## 9. Cost awareness

* EC2 billed hourly
* Elastic IP is free only while attached
* No Route 53 usage
* HTTPS is free

If the instance is stopped long term, Elastic IP must be released to avoid charges.

---

## 10. Known future improvements

Optional but recommended:

* Add systemd service for Gunicorn if missing
* Add basic monitoring and alarms
* Add simple CI based deployment
* Add request rate limiting in Nginx
* Separate ML heavy workloads if traffic increases

---

## 11. Contact and ownership

* Original owner responsible for AWS billing and domain ownership
* Code ownership transferred separately from AWS account
* Any infrastructure change should be documented before execution

