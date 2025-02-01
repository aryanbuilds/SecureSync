from ..utils.payload_manager import get_payloads
from ..utils.http_utils import send_request

class SQLiDetector:
    def __init__(self):
        self.payloads = get_payloads('sqli')

    async def scan(self, base_url, endpoints):
        vulnerabilities = []
        for endpoint in endpoints:
            for payload in self.payloads:
                try:
                    response = await send_request(f"{base_url}{endpoint}", params={'q': payload})
                    if self._check_injection(response.text):
                        vulnerabilities.append({
                            'type': 'SQL Injection',
                            'url': f"{base_url}{endpoint}",
                            'payload': payload,
                            'severity': 'High'
                        })
                except Exception as e:
                    continue
        return vulnerabilities

    def _check_injection(self, response):
        return "syntax error" in response.lower()