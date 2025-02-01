from ..utils.http_utils import send_request

class HeaderChecker:
    async def scan(self, base_url, endpoints):
        vulnerabilities = []
        for endpoint in endpoints:
            try:
                response = await send_request(f"{base_url}{endpoint}", method='GET')
                headers = response.headers

                if 'X-Frame-Options' not in headers:
                    vulnerabilities.append({
                        'type': 'Missing Security Header',
                        'url': response.url,
                        'details': 'X-Frame-Options header is missing',
                        'severity': 'Medium'
                    })

                if 'Content-Security-Policy' not in headers:
                    vulnerabilities.append({
                        'type': 'Missing Security Header',
                        'url': response.url,
                        'details': 'Content-Security-Policy header is missing',
                        'severity': 'High'
                    })

            except Exception as e:
                continue
        return vulnerabilities