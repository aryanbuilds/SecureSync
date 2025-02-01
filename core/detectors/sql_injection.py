import logging
from core.utils.payload_manager import PayloadManager
from core.utils.http_utils import HTTPClient

class SQLInjector:
    def __init__(self, http_client: HTTPClient, payload_factory: PayloadManager):
        self.http_client = http_client
        self.payloads = payload_factory.get_payloads('sql')

    def scan(self, endpoint, rate_limit, timeout):
        vulnerabilities = []
        for form in endpoint.get('forms', []):
            for payload in self.payloads:
                response = self.http_client.post(endpoint['url'], data={form['field']: payload}, timeout=timeout)
                if "error" in response['text'].lower() or "sql" in response['text'].lower():
                    vulnerabilities.append({
                        'type': 'SQL Injection',
                        'url': endpoint['url'],
                        'payload': payload,
                        'form': form,
                        'severity': 'Critical'
                    })
                    logging.info(f"SQL Injection vulnerability found at {endpoint['url']} with payload {payload}")
        return vulnerabilities