# Decision tree: Local vs Hugging Face inference

This decision tree must be applied **per model**, not globally.

### Step 1: Model size

* If model size ≤ 200 MB → go to Step 2
* If model size > 200 MB → use **Hugging Face inference**

Reason: EC2 memory pressure and cold start risk grow sharply past this point.

---

### Step 2: Compute requirements

* If CPU inference is sufficient → go to Step 3
* If GPU is required → use **Hugging Face inference**

Reason: GPU on EC2 is not cost effective for a portfolio site.

---

### Step 3: Inference latency

* If typical inference time < 2 seconds → go to Step 4
* If inference time ≥ 2 seconds → prefer **Hugging Face**, or mark as async candidate

Reason: blocking backend workers degrades UX and experimentation speed.

---

### Step 4: Concurrency expectation

* If expected concurrent users ≤ 2 → go to Step 5
* If expected concurrent users > 2 → prefer **Hugging Face**

Reason: single instance CPU contention.

---

### Step 5: Development phase

* If experimenting, iterating, or debugging → **Local inference**
* If demo is stable and public facing → **Hugging Face inference**

Reason: local favors speed, remote favors stability.

---

### Final decision summary

| Condition                       | Decision     |
| ------------------------------- | ------------ |
| Large model or GPU needed       | Hugging Face |
| Small model, fast, low traffic  | Local        |
| Prototype phase                 | Local        |
| Public demo, stability critical | Hugging Face |
| Memory pressure observed        | Hugging Face |

---

### Mandatory abstraction rule

Regardless of decision:

* Backend must call inference through an adapter interface
* Frontend must not know or care where inference runs
* Switching provider must not change API contracts
