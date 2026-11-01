# OkyrhoeWeb_PS.py - PowerShell Client Adaptor Pipe (Structured Envelope)
import sys
import json
import urllib.request

PORT = 5909
SUBSYSTEM_TAG = "PowerShell_CLI_Environment"

def main():
    if len(sys.argv) < 2:
        print("[!] Input Fault: Empty query parameter received. Usage: python OkyrhoeWeb_PS.py <your query>")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    
    # Construct structured contract container block
    transaction_envelope = {
        "query": user_query,
        "subsystem": SUBSYSTEM_TAG,
        "options": {
            "max_results": 3,   # Acknowledged parameters ready for scaling tiers
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
        with urllib.request.urlopen(req, timeout=120) as response:
            server_response = response.read().decode('utf-8')
            
            # Unpack the server transaction envelope directly for pure CLI view
            data_array = json.loads(server_response)

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
