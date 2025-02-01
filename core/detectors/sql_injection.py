class SQLInjector:
    def __init__(self):
        self.payloads = self.load_payloads()
    
    def load_payloads(self):
        with open('wordlists/sql.txt') as f:
            return [line.strip() for line in f]
    
    def scan(self, url, crawl_data):
        vulnerabilities = []
        for form in crawl_data['forms']:
            for payload in self.payloads:
                # Simulate SQL injection
                vulnerabilities.append({
                    'type': 'SQL Injection',
                    'url': url,
                    'payload': payload,
                    'severity': 'Critical'
                })
        return vulnerabilities