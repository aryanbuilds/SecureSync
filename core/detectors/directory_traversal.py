from ..utils.payload_manager import get_payloads
from ..utils.http_utils import send_request

class DirectoryTraversalDetector:
    def __init__(self):
        self.payloads = get_payloads('directory_traversal')

    async def scan(self, base_url, endpoints):
        vulnerabilities = []
        for endpoint in endpoints:
            for payload in self.payloads:
                try:
                    response = await send_request(f"{base_url}{endpoint}", params={'q': payload})
                    if self._is_vulnerable(response.text):
                        vulnerabilities.append({
                            'type': 'Directory Traversal',
                            'url': f"{base_url}{endpoint}",
                            'payload': payload,
                            'severity': 'High'
                        })
                except Exception as e:
                    continue
        return vulnerabilities

    def _is_vulnerable(self, response_text):
        return "root:x" in response_text or "windows" in response_text.lower()