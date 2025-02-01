class XSSDetector:
    def __init__(self, http_client, payload_factory):
        self.http_client = http_client
        self.payloads = payload_factory.get_payloads('xss')
        self.context_analyzer = ContextAnalyzer()

    def scan(self, endpoint, rate_limit=1, timeout=5):
        vulnerabilities = []
        
        for form in endpoint['forms']:
            for payload in self.payloads:
                try:
                    # Prepare request based on form method
                    if form['method'] == 'GET':
                        response = self.http_client.get(
                            form['action'],
                            params=self._prepare_parameters(form['inputs'], payload)
                        )
                    else:
                        response = self.http_client.post(
                            form['action'],
                            data=self._prepare_parameters(form['inputs'], payload)
                        )
                    
                    # Advanced context-based analysis
                    injection_context = self.context_analyzer.detect_injection_context(
                        payload, response.text
                    )
                    
                    if injection_context:
                        vulnerabilities.append({
                            'type': 'XSS',
                            'url': form['action'],
                            'payload': payload,
                            'severity': self._determine_severity(injection_context),
                            'context': injection_context,
                            'evidence': response.text[:500]
                        })
                    
                    time.sleep(rate_limit)
                    
                except Exception as e:
                    logging.warning(f"XSS test failed: {str(e)}")
        
        return vulnerabilities

    def _prepare_parameters(self, inputs, payload):
        return {i['name']: payload for i in inputs if i['name']}

    def _determine_severity(self, context):
        severity_map = {
            'html_tag': 'High',
            'html_attribute': 'Medium',
            'javascript': 'Critical',
            'style': 'Low'
        }
        return severity_map.get(context, 'Medium')