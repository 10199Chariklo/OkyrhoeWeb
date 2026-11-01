# CONTRIBUTING 🪐
Welcome to the OkyrhoeWeb project! This project is intentionally designed to be a **hands-on learning playground** for developers interested in pure standard-library automation, structured protocol routing, and clean API design. 

To maintain the project's foundational commitment to transparency, predictability, and simplicity, all codebase adjustments must comply with a few structural rules.


---
## 🗺️ Finding Your Way Around
Depending on what you want to build, here is how to dive in:
* **Working on the Core Engine or Server?** Please review the [ARCHITECTURE.md](ARCHITECTURE.md) document first to understand how the stateless parser and stateful queue daemon isolate responsibilities.
* **Looking for Ideas or the Current Roadmap?** Check out the active `TODO` markers inside the code files or open placeholders (like `placeholder.x`) to see where the platform scaling tiers are heading next.
* **Want to build an adapter for your favorite environment?** Review our reference implementation pattern below to see how easy it is to pipe data into other environments (like Bash, Python tools, or terminal viewers).


---
## 1. Architectural Invariants
* **Zero External Dependencies:** External package inclusions (e.g., `requests`, `beautifulsoup4`, `lxml`) will be strictly rejected. The framework must remain bound to the pure Python standard library layer (`urllib`, `re`, `html`).
* **No Profile Spoofing:** Modifications that obscure or randomize request signatures, spoof browser canvases, or rotate spoofed fingerprints run counter to the project’s goal and will not be merged. Honesty is a rigid system invariant.
* **Predictable Timing:** Keep timing mechanisms transparent. Do not introduce randomized behavior; the `AdaptiveLimiter` handles rate limits reliably using predictable math intervals.


---
## 2. Header and Tracking Requirements
* Every functional engine path must leave the custom transparent identification metadata intact. 
* If you introduce new extraction parameters, ensure they inherit the active `X-Chariklo-Subsystem` context passed down from the root invocation layer to prevent validation halts.


---
## 3. Blueprint Template: The Client Adapter Layer (`OkyrhoeWeb_PS.py`)
If you want to contribute a wrapper or a new platform module for a unique environment (e.g., Bash, CMD, or a desktop widget), use the following structured blueprint from our PowerShell client adapter. 

This client adaptor shows how to package a user query into a structured contract envelope, post it to the state daemon loopback port, and decode the payload array into raw terminal row strings:

```python
# OkyrhoeWeb_PS.py - Reference Client Adaptor Template
import sys
import json
import urllib.request

PORT = 5909
SUBSYSTEM_TAG = "PowerShell_CLI_Environment"

def main():
    # 1. Gracefully reject empty query fragments
    if len(sys.argv) < 2:
        print("[!] Input Fault: Empty query parameter received. Usage: python OkyrhoeWeb_PS.py <your query>")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    
    # 2. Construct the structured contract transaction envelope
    transaction_envelope = {
        "query": user_query,
        "subsystem": SUBSYSTEM_TAG,
        "options": {
            "max_results": 3,
            "page_limit": 1
        }
    }
    
    payload = json.dumps(transaction_envelope).encode('utf-8')
    req = urllib.request.Request(
        f"http://127.0.0.1:{PORT}/search", 
        data=payload, 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        # 3. Handle loopback network transaction
        with urllib.request.urlopen(req, timeout=120) as response:
            server_response = response.read().decode('utf-8')
            data_array = json.loads(server_response)

            # 4. Unpack and unpack array text elements cleanly for individual CLI rows
            for item in data_array:
                itype = item.get("type")
                if itype == "standard":
                    print(f"[{item['index']}] {item['title']}")
                    print(f"  URL     : {item['url']}")
                    print(f"  SNIPPET : {item['snippet']}\n")
                elif itype in ("fallback", "halt", "error"):
                    print(f"[!] {item.get('title', 'ERROR').upper()}")
                    print(f"  {item.get('snippet')}\n")
                elif itype == "attribution":
                    print(f"--- {item['snippet']} ---")
                    
    except Exception as e:
        print(f"[!] Local Host Interface Disconnect (Target Port: {PORT})")
        print(f"    Could not route pipe transaction. Ensure OkyrhoeWeb_server.py is running.")
        print(f"    Context: {str(e)}")

if __name__ == "__main__":
    main()
```


---
## 4. Submission Protocol
We want this project to be a welcoming workspace! Submissions don't need to be intimidating or overly rigorous:
1. Fork the repository and build your feature patch or client wrapper in an independent branch.
2. Run a quick query test to ensure any text improvements decode cleanly into standard terminal outputs.
3. Submit a clear Pull Request detailing the specific parsing improvement, bug fix, or new client adapter platform you have added.
