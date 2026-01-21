# LLM ASSISTANT HANDOUT

**System Name:** hahuy.site portfolio platform
**Role:** Autonomous or semi autonomous technical assistant
**Primary Objective:** Rapid experimentation with ML backed demos while maintaining a stable, low cost public website

---

## 0. Operating mode

**Priority order**

1. Experimentation speed
2. System stability
3. Cost efficiency
4. Clean but minimal design

You are not optimizing for enterprise scale.
You are optimizing for iteration, clarity, and showcase value.

---

## 1. System invariants (must never be violated)

These are hard constraints. Any proposed action that risks breaking them must be rejected or staged safely.

* Domain `hahuy.site` must remain publicly reachable
* HTTPS must always be valid and auto renewing
* Elastic IP must remain attached to the running instance
* Backend services must never be publicly exposed directly
* DNS must always point to the Elastic IP
* Single EC2 instance architecture must be preserved unless explicitly instructed otherwise

---

## 2. Current architecture model

### Infrastructure

* One EC2 instance
* OS: Amazon Linux
* One Elastic IP attached
* One Security Group

### Networking

* Public entry points: ports 80 and 443 only
* Reverse proxy: Nginx
* Backend: Gunicorn on `127.0.0.1:8000`
* No public backend ports

### Traffic flow

```
Client
  ↓
DNS (Namecheap)
  ↓
Elastic IP
  ↓
Nginx (80/443)
  ↓
Gunicorn (localhost)
  ↓
Application
```

---

## 3. Domain and DNS authority

* Domain: `hahuy.site`
* Registrar and DNS authority: Namecheap
* DNS records:

  * A `@` → Elastic IP
  * A `www` → Elastic IP

Rules:

* Do not move DNS to AWS or other providers
* Do not introduce root CNAMEs
* Do not remove `www` without redirect logic
* Any IP change requires DNS update

---

## 4. Web server contract

### Nginx responsibilities

* TLS termination
* ACME challenge handling
* HTTP to HTTPS redirection
* Reverse proxy to backend

### Config location

```
/etc/nginx/conf.d/myapp.conf
```

### Structural rules

* Exactly one HTTP server block
* Exactly one HTTPS server block
* No duplicate `server_name` on same port
* No conditional host logic
* Never manually edit certificate files

Validation before reload:

```bash
nginx -t
```

Reload, not restart:

```bash
systemctl reload nginx
```

---

## 5. TLS lifecycle

* Certificate authority: Let’s Encrypt
* Tooling: certbot with nginx plugin
* Domains covered: `hahuy.site`, `www.hahuy.site`

Rules:

* Do not manually touch `/etc/letsencrypt`
* Do not re issue certificates unless invalid or expiring
* Validate renewals with:

```bash
certbot renew --dry-run
```

---

## 6. Backend service contract

### Runtime expectations

* Runs on localhost only
* Port: `8000`
* Managed independently of Nginx
* Can be restarted without touching Nginx

### ML workload expectations

* Model size range: 2MB to 2GB
* Multiple frameworks supported
* Backend must not depend directly on framework internals

---

## 7. ML workload strategy

### General rule

Backend orchestrates inference, not ML compute.

### Local inference

Use when:

* Model < ~200MB
* CPU inference acceptable
* Low concurrent usage

### Remote inference

Use when:

* Model > ~200MB
* GPU required
* Cold starts or memory pressure appear

Preferred remote service:

* Hugging Face inference endpoints or Spaces

### Hybrid rule

Design inference behind an abstraction so local and remote providers are interchangeable without frontend changes.

---

## 8. Interaction patterns

### Synchronous inference

Default.

* Request blocks until result
* Simple UX
* Use for fast models

### Asynchronous inference

Use only when latency exceeds UX tolerance.

* Job based
* Polling or streaming

Do not introduce async complexity prematurely.

---

## 9. Deployment model

Current assumptions:

* Code lives directly on EC2
* No containerization
* No CI enforced

Safe change sequence:

1. Update code
2. Validate locally
3. Restart backend
4. Verify endpoint
5. Leave Nginx untouched unless required

---

## 10. Containerization policy

Containerization is **explicitly deferred**.

Do not introduce Docker unless:

* Environment drift becomes painful
* Multiple services appear
* CI becomes a priority

Until then, bare metal operation is preferred.

---

## 11. Cost constraints

* EC2 cost is accepted baseline
* Elastic IP is free while attached
* No Route 53 usage
* No managed load balancers
* External ML services allowed only when justified

Any recurring cost increase must be surfaced explicitly.

---

## 12. Failure handling order

If site is unreachable:

1. DNS resolution
2. Elastic IP association
3. Security Group rules
4. Nginx status
5. Backend status

If HTTPS fails:

* Verify port 80 reachability
* Check certbot logs
* Do not immediately re issue certificates

---

## 13. Allowed extensions

Permitted:

* New ML demos
* New inference adapters
* Frontend UI variations
* Streaming responses when justified
* Monitoring and logging

Disallowed without instruction:

* Multi instance architectures
* Public backend exposure
* Manual TLS handling
* DNS migration
* Heavy AWS managed services

---

## 14. Decision making principle for the LLM

Prefer:

* Simple over clever
* Explicit over implicit
* Reversible over irreversible
* Local changes over global refactors

Reject any action that:

* Slows experimentation unnecessarily
* Introduces fragile coupling
* Obscures system behavior

---

## 15. Clarifying assumptions for future work

Unless told otherwise, assume:

* Solo developer
* Portfolio audience
* ML quality is primary, infra is secondary
* Changes should be explainable in plain language
