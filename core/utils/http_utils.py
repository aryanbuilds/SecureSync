import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HTTPClient:
    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) WebVulnScanner/1.0'
        })

    def get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self._request('POST', url, data=data, **kwargs)

    def _request(self, method, url, **kwargs):
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return self._analyze_response(response)
        except requests.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")

    def _analyze_response(self, response):
        # Add security headers analysis
        security_headers = {
            'CSP': response.headers.get('Content-Security-Policy'),
            'HSTS': response.headers.get('Strict-Transport-Security'),
            'X-Content-Type': response.headers.get('X-Content-Type-Options')
        }
        
        return {
            'status': response.status_code,
            'headers': dict(response.headers),
            'security_headers': security_headers,
            'text': response.text,
            'timing': response.elapsed.total_seconds()
        }