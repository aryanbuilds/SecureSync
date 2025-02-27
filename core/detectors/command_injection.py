import re
from ..utils.payload_manager import get_payloads
from ..utils.http_utils import send_request

class CommandInjectionDetector:
    def __init__(self):
        self.payloads = get_payloads('command_injection')
        self.error_patterns = [
            re.compile(r'bash: .*: command not found', re.IGNORECASE),
            re.compile(r'sh: .*: not found', re.IGNORECASE),
            re.compile(r'cmd: .*: not recognized', re.IGNORECASE),
            re.compile(r'command not found', re.IGNORECASE),
        ]

    async def scan(self, base_url, endpoints):
        vulnerabilities = []
        for endpoint in endpoints:
            for payload in self.payloads:
                try:
                    response = await send_request(f"{base_url}{endpoint}", params={'q': payload})
                    if self._is_vulnerable(response.text):
                        vulnerabilities.append({
                            'type': 'Command Injection',
                            'url': f"{base_url}{endpoint}",
                            'payload': payload,
                            'severity': 'High'
                        })
                except Exception as e:
                    continue
        return vulnerabilities

    def _is_vulnerable(self, response_text):
        return any(pattern.search(response_text) for pattern in self.error_patterns)