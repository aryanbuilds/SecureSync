import requests
import logging

class HeaderChecker:
    def __init__(self):
        self.required_headers = {
            'Content-Security-Policy': 'Defines approved sources of content to prevent XSS attacks.',
            'Strict-Transport-Security': 'Enforces secure (HTTP over SSL/TLS) connections to the server.',
            'X-Content-Type-Options': 'Prevents browsers from MIME-sniffing a response away from the declared content-type.',
            'X-Frame-Options': 'Protects against clickjacking attacks by controlling whether a browser can display a page in a frame or iframe.',
            'X-XSS-Protection': 'Enables cross-site scripting filtering.',
            'Referrer-Policy': 'Controls how much referrer information is included with requests.',
            'Permissions-Policy': 'Allows or denies the use of browser features in its own frame and in iframes that it embeds.'
        }

    def check_headers(self, url):
        try:
            response = requests.get(url, timeout=10)
            response_headers = response.headers

            missing_headers = []
            misconfigured_headers = []

            for header, description in self.required_headers.items():
                if header not in response_headers:
                    missing_headers.append((header, description))
                else:
                    if not self.is_header_configured_properly(header, response_headers[header]):
                        misconfigured_headers.append((header, response_headers[header]))

            return {
                'missing_headers': missing_headers,
                'misconfigured_headers': misconfigured_headers
            }

        except requests.RequestException as e:
            logging.error(f"Error checking headers for {url}: {e}")
            return None

    def is_header_configured_properly(self, header, value):
        # Implement specific checks for each header as needed
        if header == 'Strict-Transport-Security':
            return 'max-age' in value
        elif header == 'X-Content-Type-Options':
            return value.lower() == 'nosniff'
        elif header == 'X-Frame-Options':
            return value.lower() in ['deny', 'sameorigin']
        elif header == 'X-XSS-Protection':
            return value == '1; mode=block'
        elif header == 'Referrer-Policy':
            return value.lower() in [
                'no-referrer', 'no-referrer-when-downgrade', 'same-origin',
                'origin', 'strict-origin', 'origin-when-cross-origin',
                'strict-origin-when-cross-origin', 'unsafe-url'
            ]
        elif header == 'Permissions-Policy':
            # Basic check; implement more detailed checks as needed
            return bool(value)
        elif header == 'Content-Security-Policy':
            # Basic check; implement more detailed checks as needed
            return bool(value)
        return True
