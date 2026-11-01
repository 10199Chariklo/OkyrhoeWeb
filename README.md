# OkyrhoeWeb 🪐

An ultra-lightweight, zero-dependency Python search extraction engine designed to provide transparent, completely detached, and pre-parsed text extraction for console and automated environments. 

This engine is architected to act as a robust universal data provider. By outputting highly optimized text structures stripped of JavaScript, heavy visual styling, and tracking scripts, it serves as a high-efficiency pipeline adapter for diverse environments:
* **Virtual Ecosystems & Terminal Emulators:** Clean ASCII text rendering for local CLI workspaces.
* **Frameworks & Plugins:** Minimal-token, text-only corpus feeds for automation engines.
* **Data Layout Engines:** Seamless integration into spreadsheet functions, document pipelines, or offline archival scripts.

This project is entirely open-source, publicly auditable, and built on absolute transparency.


---
## 🛠️ The Architecture of Transparency

This engine strictly rejects the adversarial paradigms of traditional scrapers. It does not attempt to mimic human browser profiles, spoof hardware signatures, or rotate proxy pools to bypass infrastructure traffic controls. Instead, it relies on a completely honest footprint and queries endpoints explicitly designed for low-bandwidth, text-based clients.

The core codebase strictly mandates that downstream scripts explicitly initialize their calling subsystem namespace. To protect the integrity of the project's digital signature, the architecture implements rigid safeguards:
* **No Unconfigured Broadcasting:** The implementation bars silent, anonymous operation. 
* **Internal Structural Gate:** An unconfigured fallback string (`_UNCONFIGURED_caller_source_unknown_bot_behaviour_warning_`) exists solely as an internal programmatic fail-safe. If a downstream runtime fails to supply its namespace, the engine immediately throws a terminal architecture validation error.

> **Engineering Note on Future Roadmap:** The fallback signature currently acts strictly as a local execution gate and is *not* broadcasted in the active HTTP header package. Future iterations will re-introduce automated network signature broadcasts using a custom User-Agent entry that dynamically truncates/abbreviates the user's subsystem, or fully overwrites the User-Agent header with the fallback identifier if an invalid runtime is detected.


---
### File Structure
    📦 OkyrhoeWeb Repository Root
        ├─ placeholder.x                # TODO: pyInstaller Automated build orchestration for self-compiling
        ├─ src/ 
        │   ├── OkyrhoeWeb.py           # Platform Agnostic core extraction engine
        │   ├── OkyrhoeWeb_PS.py        # Powershell platform .py wrapper
        |   └── OkyrhoeWeb_server.py    # Server instance - Receives requests from wrapper binaries, (cont.)
        |                                   # preserves states, and manages the core primitives
        ├─ release/platformX/           # Planned release platforms in TODO: Tier 3 (EG; POSIX)
        │   └── bin/                    # Contains pre-compiled release binaries
        |
        └── README.md (And ect)         # The project documents - You are here


---
## ☕ A Message to Network & SysAdmin Engineers

If you have traced an HTTP traffic log or automated alert profile directly to this repository: **Welcome!**

This engine is deliberately engineered to protect host infrastructure, respect server resources, and fail gracefully rather than attempting to aggressively pierce network safety boundaries.
* **Permissive Targeting:** The core engine targets the DuckDuckGo Lite endpoint, which is explicitly maintained by the upstream host for low-bandwidth, non-JS, and scripted contexts.
* **Generously Rate-Limited by Default:** Outbound requests are governed by a predictable, stateful `AdaptiveLimiter` pacing engine rather than utilizing volatile, randomized timings.
* **Hard Back-Off Controls:** If the engine intercepts an infrastructure control block like an HTTP `403 Forbidden` or rate-limiting state, it immediately halts traffic, spikes its internal limiter latency to its maximum ceiling, and gracefully executes structured retry/back-off boundaries.

---
## 💾 Structural Features

* **Zero External Dependencies:** Operating exclusively on the Python standard library tier (`urllib`, `re`, `html`).
* **Isolated Stateful Daemon:** A central background queue worker handles client traffic synchronously, preventing parallel connection bursts to upstream servers.
* **Unified Layout Schema:** Returns clean, predictable dictionary arrays completely isolated from display logic, enabling arbitrary translation into JSON wrappers, CLI string lines, or markdown documents.


---
## 📊 Project Deployment Profiles

| Attribute | Profile Specification |
| :--- | :--- |
| **Primary Code Repository** | https://github.com/10199Chariklo/OkyrhoeWeb |
| **Licensing Framework** | MIT Permissive (Zero Cost / Open Distribution) |
| **Fail-Safe Internal Sign** | `_UNCONFIGURED_caller_source_unknown_bot_behaviour_warning_` |
| **Target Engine Matrix** | DuckDuckGo Lite Endpoint API (`/lite/`) |
| **Response Interceptors** | `429 Rate Limit` (Dynamic Pacing Back-off) & `403 CAPTCHA` (Maximize Pacing Delay & Halt) |
