# OkyrhoeWeb Architecture 🪐

This document defines the decoupled engineering architecture of OkyrhoeWeb. The system is split into two primary layers: a stateless extraction engine and a stateful request orchestrator daemon. By separating network extraction from session-state governance, the architecture ensures absolute predictability, predictable pacing control, and easy client interoperability.

---

## 1. Core Extraction Engine (`OkyrhoeWeb.py`)

The Extraction Engine acts as the stateless data provider for the system. Its single responsibility is to safely execute HTTP handshakes with upstream layout matrices and transform raw markup into uniform structured data primitives.

### Primary Responsibilities
* **Strict Namespace Enforcement:** Validates calling signatures upon instantiation to eliminate anonymous unconfigured system operations.
* **Stream Safety Ceilings:** Enforces strict inbound payload bounds, truncating responses at a maximum ceiling of 5MB to guarantee local buffer protection.
* **Layout Parsing:** Direct targets low-bandwidth, text-friendly layout matrices. It processes fields using fast regular expressions rather than bulky browser object models (DOM).
* **Visualization Layer:** Independent from the JSON payload data return, this module paints a local visual Markdown asset for quick shell/terminal rendering.

### Implementation Notes
* **Standard Library Boundary:** Constructed purely within the standard Python tier using `urllib.request` for networking, `re` for structural capture, and `html` for unescaping entities.
* **Quote-Agnostic Block Slicing:** Uses regex compilation targeting the table structures (`result-table`) seamlessly supporting both single and double quotes to handle upstream structural adjustments.
* **Failure Interception:** Catches and translates infrastructure signals (like HTTP `403` or `429`) into standardized internal control structures that direct the upstream daemon to alter its state.

---

## 2. Central State Daemon (`OkyrhoeWeb_server.py`)

The State Daemon acts as the asynchronous transaction manager, pacing valve, and local cache authority for the entire system lifecycle. It isolates external clients from interacting directly with the network layer.

### Primary Responsibilities
* **Client Protocol Boundary:** Runs an HTTP loopback interface that digests inbound query contracts wrapped inside standard structural envelopes.
* **Stateful Pacing Regulation:** Governs outbound network latency through a dynamic pacing calculator that dynamically scales delays based on transaction intervals.
* **Transaction Ordering:** Serializes all inbound network traffic requests onto a single, isolated execution timeline to prevent concurrent connection bursts.
* **Response Caching:** Maps repeat queries locally inside an explicit isolation folder to slash repetitive outbound traffic volume.

### Implementation Notes
* **Standard Deque Collection:** Utilizes a native `collections.deque` object protected by a threading lock (`threading.Lock`) to create a thread-safe, high-performance First-In, First-Out (FIFO) background task consumer.
* **Pacing Metrics Matrix:** The stateful `AdaptiveLimiter` operates a discrete tracking matrix:
  * *Base Latency Bounds:* Evaluates the time delta since the previous outbound query. Short intervals spike pacing latency by predictable math steps (`2.0s`), capping at an explicit maximum threshold (`8.0s`).
  * *Infrastructure Control Handling:* If the engine intercepts a `MAXIMIZE_DELAY` control signal, the pacing mechanism instantly overrides the calculation loops and snaps latency directly to its maximum protective ceiling.
* **File-System Caching Cache:** Stores clean standard returns as structured `.json` primitives indexed by filename-sanitized query profiles with an explicit Time-To-Live (TTL) ceiling of 1 hour (3600 seconds).

---

## 🔍 Further Reading & Extension
For details on extending the network stack, adding new pipeline endpoints, or reviewing an active integration pattern, please consult the [CONTRIBUTING.md](CONTRIBUTING.md) documentation. The contribution guide includes a complete breakdown of the client-side pipeline architecture (`OkyrhoeWeb_PS.py`) which acts as the reference blueprint for building downstream client adapters.
