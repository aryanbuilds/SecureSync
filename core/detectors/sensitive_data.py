import logging
import re
from core.utils.http_utils import HTTPClient

class SensitiveDataDetector:
    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.patterns = {
            'Credit Card': r'\b(?:\d[ -]*?){13,16}\b',
            'Social Security Number': r'\b\d{3}-\d{2}-\d{4}\b',
            'API Key': r'\b[A-Za-z0-9]{32,}\b'
        }

    def scan(self, endpoint, rate_limit, timeout):
        vulnerabilities = []
        response = self.http_client.get(endpoint['url'], timeout=timeout)
        for data_type, pattern in self.patterns.items():
            if re.search(pattern, response['text']):
                vulnerabilities.append({
                    'type': 'Sensitive Data Exposure',
                    'url': endpoint['url'],
                    'data_type': data_type,
                    'severity': 'Medium'
                })
                logging.info(f"Sensitive data ({data_type}) found at {endpoint['url']}")
        return vulnerabilities