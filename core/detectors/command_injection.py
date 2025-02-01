import requests
from core.utils.payload_manager import PayloadManager
from core.utils.http_utils import HttpUtils
import logging

class CommandInjector:
    def __init__(self, payload_file='wordlists/command_injection.txt'):
        self.payloads = PayloadManager.load_payloads(payload_file)

    def scan(self, url, crawl_data):
        vulnerabilities = []
        for form in crawl_data.get('forms', []):
            for payload in self.payloads:
                response = HttpUtils.submit_form(url, form, payload)
                if "command" in response.text.lower() or "shell" in response.text.lower():
                    vulnerabilities.append({
                        'type': 'Command Injection',
                        'url': url,
                        'payload': payload,
                        'form': form,
                        'severity': 'Critical'
                    })
                    logging.info(f"Command Injection vulnerability found at {url} with payload {payload}")
        return vulnerabilities
