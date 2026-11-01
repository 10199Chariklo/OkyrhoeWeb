# OkyrhoeWeb_server.py - Central State Daemon & Extended Request Orchestrator
import http.server
import json
import os
import re
import sys
import time
from collections import deque
import threading
from OkyrhoeWeb import OkyrhoeWebEngine

PORT = 5909
DEFAULT_SUBSYSTEM = "_UNCONFIGURED_caller_source_unknown_bot_behaviour_warning_"
MAX_LOOP_RETRIES = 2  # Tier 4.6 Safety ceiling threshold limit for looping failures

if getattr(sys, 'frozen', False):
    BIN_DIR = os.path.dirname(sys.executable)
else:
    BIN_DIR = os.path.dirname(os.path.abspath(__file__))

CACHE_DIR = os.path.abspath(os.path.join(BIN_DIR, "cache"))
os.makedirs(CACHE_DIR, exist_ok=True)

request_queue = deque()
queue_lock = threading.Lock()
cache_index = {}
cache_ttl_seconds = 3600

class AdaptiveLimiter:
    def __init__(self):
        self.last_request_time = 0.0
        self.current_delay = 0.0
        self.min_delay = 0.0
        self.max_delay = 8.0
        self.backoff_step = 2.0
        self.recovery_step = 1.0

    def maximize_delay(self):
        """Forces the pacing system instantly to its highest latency ceiling."""
        self.current_delay = self.max_delay
        print(f"[*] Limiter Alert: Infrastructure control block caught. Pacing spiked to {self.max_delay}s.")

    def calculate_wait_gate(self):
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < 10.0:
            self.current_delay = min(self.max_delay, self.current_delay + self.backoff_step)
        else:
            intervals_passed = int(time_since_last / 15.0)
            self.current_delay = max(self.min_delay, self.current_delay - (intervals_passed * self.recovery_step))
        self.last_request_time = now + self.current_delay
        return self.current_delay

limiter = AdaptiveLimiter()

def clean_query_for_filename(query: str) -> str:
    sanitized = re.sub(r'[^a-zA-Z0-9_\-]', '_', query.strip())
    return f"_duckduckgo.com_{sanitized}.json"

def process_queue_worker():
    """Background consumer extracting elements from central thread pool."""
    while True:
        task = None
        with queue_lock:
            if request_queue:
                task = request_queue.popleft()
        
        if task:
            # Unpack expanded context parameters bubbling up from wrapper scripts
            query, subsystem, options, response_box, execution_flag = task
            filename = clean_query_for_filename(query)
            cache_filepath = os.path.join(CACHE_DIR, filename)
            
            # --- FUTURE PATHWAYS TARGET HOOKS ---
            # Extract configuration primitives safely (Acknowledged and held for future Tier 4 processing)
            max_results = int(options.get("max_results", 3))
            page_limit = int(options.get("page_limit", 1))
            
            # Cache lookup gate
            if query in cache_index and (time.time() - cache_index[query]) < cache_ttl_seconds:
                if os.path.exists(cache_filepath):
                    try:
                        with open(cache_filepath, "r", encoding="utf-8") as cache_file:
                            response_box["data"] = json.load(cache_file)
                            execution_flag.set()
                            continue
                    except Exception:
                        pass

            retry_count = 0
            current_target_query = query
            final_output_array = []
            
            # Stateful extraction processing wrapper loop
            while retry_count <= MAX_LOOP_RETRIES:
                # Scale-dependent throttle engine gate
                calculated_wait = limiter.calculate_wait_gate()
                if calculated_wait > 0:
                    time.sleep(calculated_wait)
                
                engine = OkyrhoeWebEngine(subsystem_name=subsystem)
                extracted_array = engine.extract(current_target_query)
                
                # Evaluation processing path targeting infrastructure flag states
                if isinstance(extracted_array, list) and len(extracted_array) == 1 and extracted_array[0].get("type") == "control":
                    control_signals = extracted_array[0]
                    
                    # Flag 1 processing: Maximize rate pacing delay
                    if control_signals.get("__action_flag__") == "MAXIMIZE_DELAY":
                        limiter.maximize_delay()
                    
                    # Flag 2 processing: Payload retry validation check
                    if control_signals.get("__retry_flag__") is True and retry_count < MAX_LOOP_RETRIES:
                        retry_count += 1
                        current_target_query = control_signals.get("retry_query", current_target_query)
                        print(f"[!] Captcha Rejection intercepted. Pipeline executing retry step ({retry_count}/{MAX_LOOP_RETRIES}).")
                        continue
                    else:
                        # Safety ceiling hit without clearing: Convert flags to terminal error data block
                        final_output_array = [{
                            "index": 1,
                            "title": "Pipeline Execution Halted",
                            "url": "https://duckduckgo.com",
                            "snippet": f"Extraction blocked via infrastructure boundaries: {control_signals.get('error_context')}",
                            "type": "halt"
                        }]
                        break
                else:
                    # Clean response array captured
                    final_output_array = extracted_array
                    break

            # Commit to cache loop arrays if standard text entries exist
            if any(item.get("type") == "standard" for item in final_output_array):
                try:
                    with open(cache_filepath, "w", encoding="utf-8") as cache_file:
                        json.dump(final_output_array, cache_file, indent=4)
                    cache_index[query] = time.time()
                    
                    with open(os.path.join(CACHE_DIR, "_LATEST_RETURN.log"), "w", encoding="utf-8") as latest_log:
                        json.dump(final_output_array, latest_log, indent=4)
                except Exception:
                    pass
            
            response_box["data"] = final_output_array
            execution_flag.set()
        else:
            time.sleep(0.1)

class OkyrhoeProtocolRouter(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/search":
            content_length = int(self.headers['Content-Length'])
            payload = json.loads(self.rfile.read(content_length).decode('utf-8'))
            
            # Extract Structured Contract Layers
            query = payload.get("query", "latest news")
            subsystem = payload.get("subsystem", DEFAULT_SUBSYSTEM)
            
            # Safe default fallbacks for integer parameter dictionary objects
            options = payload.get("options", {})
            if not isinstance(options, dict):
                options = {}
                
            response_box = {"data": None}
            execution_flag = threading.Event()
            
            # Register extended context frames straight into the transaction Deque
            with queue_lock:
                request_queue.append((query, subsystem, options, response_box, execution_flag))
                
            execution_flag.wait()
            
            response_bytes = json.dumps(response_box["data"]).encode('utf-8')
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response_bytes)))
            self.end_headers()
            self.wfile.write(response_bytes)
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args): return

if __name__ == "__main__":
    worker = threading.Thread(target=process_queue_worker, daemon=True)
    worker.start()
    
    server = http.server.HTTPServer(('127.0.0.1', PORT), OkyrhoeProtocolRouter)
    print("==================================================")
    print(f"🪐 OkyrhoeWeb Stateful Daemon Operational")
    print(f" -> Loopback Listening Port Interconnect: {PORT}")
    print(f" -> Infrastructure Guard Framework: Enabled")
    print("==================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nHalting daemon process tree.")
