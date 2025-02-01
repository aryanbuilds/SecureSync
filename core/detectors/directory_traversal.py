import requests
from core.utils.payload_manager import PayloadManager
from core.utils.http_utils import HttpUtils
import logging

class DirectoryTraversalDetector:
    def __init__(self, payload_file='wordlists/directory_traversal.txt'):
        self.payloads = PayloadManager.load_payloads(payload_file)

    def scan(self, url, crawl_data):
        vulnerabilities = []
        for link in crawl_data.get('links', []):
            for payload in self.payloads:
                test_url = f"{link}/{payload}"
                response = requests.get(test_url)
                if "root:" in response.text or "admin:" in response.text:
                    vulnerabilities.append({
                        'type': 'Directory Traversal',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'High'
                    })
                    logging.info(f"Directory Traversal vulnerability found at {test_url} with payload {payload}")
        return vulnerabilities
