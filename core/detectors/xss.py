from ..utils.payload_manager import get_payloads
from ..utils.http_utils import send_request

class XSSDetector:
    def __init__(self):
        self.payloads = get_payloads('xss')

    async def scan(self, base_url, endpoints):
        vulnerabilities = []
        for endpoint in endpoints:
            for payload in self.payloads:
                try:
                    response = await send_request(f"{base_url}{endpoint}", params={'q': payload})
                    if self._check_reflection(response.text, payload):
                        vulnerabilities.append({
                            'type': 'XSS',
                            'url': f"{base_url}{endpoint}",
                            'payload': payload,
                            'severity': 'High'
                        })
                except Exception as e:
                    continue
        return vulnerabilities

    def _check_reflection(self, response, payload):
        return payload in response