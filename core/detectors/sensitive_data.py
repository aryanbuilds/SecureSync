import re
from ..utils.http_utils import send_request

class SensitiveDataExposure:
    def __init__(self):
        self.patterns = {
            'email': re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            'credit_card': re.compile(r'\b(?:\d[ -]*?){13,16}\b'),
            'ssn': re.compile(r'\b\d{3}-\d{2}-\d{4}\b'),
        }

    async def scan(self, base_url, endpoints):
        vulnerabilities = []
        for endpoint in endpoints:
            try:
                response = await send_request(f"{base_url}{endpoint}", method='GET')
                for data_type, pattern in self.patterns.items():
                    if pattern.search(response.text):
                        vulnerabilities.append({
                            'type': 'Sensitive Data Exposure',
                            'url': response.url,
                            'details': f'Exposed {data_type} data',
                            'severity': 'High'
                        })
            except Exception as e:
                continue
        return vulnerabilities