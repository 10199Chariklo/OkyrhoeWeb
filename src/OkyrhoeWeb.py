# OkyrhoeWeb.py - Pure Core Extraction Engine
import html
import re
import urllib.request
import urllib.parse
import urllib.error

FALLBACK_SIGN = "_UNCONFIGURED_caller_source_unknown_bot_behaviour_warning_"
ATTRIBUTION_STRING = "Powered By DuckDuckGo - https://duckduckgo.com"

RAW_HTML_FILE = "_LATEST_RESPONSE.html"
RENDER_MD_FILE = "Okyrhoe_Browser_View.md"

class OkyrhoeWebEngine:
    def __init__(self, subsystem_name: str = FALLBACK_SIGN):
        """Initializes isolated extraction engine with strict identity rules."""
        if not subsystem_name or subsystem_name == FALLBACK_SIGN:
            raise ValueError(
                f"Architecture Violation: Downstream scripts must explicitly initialize their calling namespace. "
                f"Using default fallback flag '{FALLBACK_SIGN}' is barred."
            )
        self.subsystem = subsystem_name
        self.headers = {
            "User-Agent": "OkyrhoeWebEngine/0.1 (+https://github.com/10199Chariklo/OkyrhoeWeb) CustomBrowserBackend/1.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

    def extract(self, query: str) -> list:
        """Queries upstream layout layers and extracts a uniform structured data array."""
        if isinstance(query, list):
            query = query[0] if len(query) > 0 else "latest news"
        
        clean_query = str(query if query is not None else "latest news").lstrip('/')
        encoded_query = urllib.parse.urlencode({'q': clean_query})
        
        url = f"https://duckduckgo.com/lite/?{encoded_query}"
        req = urllib.request.Request(url, headers=self.headers)
        
        try:
            # Enforce Tier 2 inbound byte-size safety ceiling (5MB maximum)
            with urllib.request.urlopen(req, timeout=6) as response:
                html_content = response.read(5 * 1024 * 1024).decode('utf-8', errors='ignore')

            with open(RAW_HTML_FILE, "w", encoding="utf-8") as raw_file:
                raw_file.write(html_content)
            
            # Refactored for the clean table blocks used by the Lite layout
            blocks = re.findall(r"<table[^>]*class=['\"]result-table['\"][^>]*>(.*?)</table>", html_content, re.DOTALL)
            if not blocks:
                blocks = re.findall(r'td valign="top"[^>]*>(.*?)td valign="top"[^>]*>', html_content, re.DOTALL)
                
            compiled_array = []
            
            for index, block in enumerate(blocks[:3]):
                title_m = re.search(r"class='result-link'[^>]*>(.*?)</a>", block, re.DOTALL)
                snippet_m = re.search(r"td class='result-snippet'[^>]*>(.*?)</td>", block, re.DOTALL)
                url_m = re.search(r"<span class='link-text'[^>]*>(.*?)</span>", block, re.DOTALL)

                if title_m and snippet_m and url_m:
                    title = re.sub(r'<[^>]+>', '', title_m.group(1)).strip()
                    snippet = re.sub(r'<[^>]+>', '', snippet_m.group(1)).strip()
                    url = re.sub(r'<[^>]+>', '', url_m.group(1)).strip()
                    
                    compiled_array.append({
                        "index": index + 1,
                        "title": html.unescape(title),
                        "url": url,
                        "snippet": html.unescape(re.sub(r'\s+', ' ', snippet)),
                        "type": "standard"
                    })
            
            if not compiled_array:
                # Fallback to loose snippets if link parsing was missed
                snippets = re.findall(r"td class='result-snippet'[^>]*>(.*?)</td>", html_content, re.DOTALL)
                for idx, snip in enumerate(snippets[:3]):
                    clean_snip = html.unescape(re.sub(r'<[^>]+>', '', snip).strip())
                    compiled_array.append({
                        "index": idx + 1,
                        "title": "Unmapped Fragment",
                        "url": "https://duckduckgo.com",
                        "snippet": re.sub(r'\s+', ' ', clean_snip),
                        "type": "fallback"
                    })
                    
            if not compiled_array:
                compiled_array.append({
                    "index": 1,
                    "title": "Extraction Alert",
                    "url": "https://duckduckgo.com",
                    "snippet": "No text primitives parsed. Structural shifting detected.",
                    "type": "error"
                })
                
        except urllib.error.HTTPError as e:
            if e.code == 403:
                # Infrastructure Control Block Flag Mapping
                return [{
                    "type": "control",
                    "__action_flag__": "MAXIMIZE_DELAY",
                    "__retry_flag__": True,
                    "retry_query": clean_query,
                    "error_context": "HTTP 403 Forbidden (Infrastructure CAPTCHA/Firewall Gate)"
                }]
                
            status_desc = "Rate Limit (429) Triggered" if e.code == 429 else f"Access Blocked ({e.code})"
            compiled_array = [{
                "index": 1,
                "title": "Network Transport Guard",
                "url": "https://duckduckgo.com",
                "snippet": f"Pipeline extraction suspended via infrastructure boundaries: {status_desc}",
                "type": "halt"
            }]
        except Exception as e:
            compiled_array = [{
                "index": 1,
                "title": "System Layer Error",
                "url": "https://duckduckgo.com",
                "snippet": f"Local pipeline isolation fault: {str(e)}",
                "type": "error"
            }]
            
        # Tier 2 Mandatory Provenance Invariant Injection
        compiled_array.append({
            "index": len(compiled_array) + 1,
            "title": "Data Source Provenance",
            "url": "https://duckduckgo.com",
            "snippet": ATTRIBUTION_STRING,
            "type": "attribution"
        })
        
        # --- THE MARKDOWN RENDER LAYER ---
        # Generate the visual page output used by your terminal/OS viewer application
        self._generate_markdown_view(clean_query, compiled_array)
        
        return compiled_array

    def _generate_markdown_view(self, query: str, dataset: list):
        """Paints a highly expressive, static ASCII Markdown document for terminal viewing."""
        try:
            md = []
            md.append(f"# OKYRHOE BROWSER // INTERNET PORTAL")
            md.append(f"**Subsystem Context:** `{self.subsystem}` | **Target Target Matrix:** `DuckDuckGo API`  ")
            md.append(f"**Active Lens Query:** *\"{query}\"*")
            md.append(f"\n" + "="*72 + "\n")
            
            for item in dataset:
                itype = item.get("type", "unknown")
                if itype == "standard":
                    md.append(f"## [{item['index']}] {item['title']}")
                    md.append(f"- **Resource Locator:** {item['url']}")
                    md.append(f"- **Abstract Frame:** {item['snippet']}")
                    md.append(f"")
                elif itype in ("fallback", "halt", "error"):
                    md.append(f"### {item['title'].upper()}")
                    md.append(f"> {item['snippet']}")
                    md.append(f"")
                elif itype == "attribution":
                    md.append(f"\n" + "-"*72)
                    md.append(f"*{item['snippet']}*  ")
                    md.append(f"Verification Checkpoint: {item['url']}")
            
            with open(RENDER_MD_FILE, "w", encoding="utf-8") as md_file:
                md_file.write("\n".join(md))
        except Exception as e:
            print(f"[*] Layout Engine Warning: Failed to emit Markdown matrix: {e}")
