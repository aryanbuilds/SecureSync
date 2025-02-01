import subprocess
import json
import logging
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from ..utils.http_utils import HTTPClient

class AdvancedCrawler:
    def __init__(self):
        self.http_client = HTTPClient()
        self.visited_urls = set()
        self.crawl_data = {'endpoints': []}

    def crawl(self, base_url, depth=3, exclude=None):
        self._crawl_recursive(base_url, depth, exclude or [])
        return self.crawl_data

    def _crawl_recursive(self, url, depth, exclude):
        if depth <= 0 or url in self.visited_urls:
            return
        
        try:
            # Static crawling
            static_data = self._static_crawl(url)
            self.crawl_data['endpoints'].append(static_data)
            self.visited_urls.add(url)
            
            # Dynamic crawling
            dynamic_data = self._dynamic_crawl(url)
            self._merge_crawl_data(dynamic_data)
            
            # Recursive crawling
            for link in static_data['links'] + dynamic_data['links']:
                if not any(pattern in link for pattern in exclude):
                    self._crawl_recursive(link, depth-1, exclude)
                    
        except Exception as e:
            logging.error(f"Crawling error at {url}: {str(e)}")

    def _static_crawl(self, url):
        response = self.http_client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return {
            'url': url,
            'links': [urljoin(url, a['href']) for a in soup.find_all('a', href=True)],
            'forms': self._parse_forms(soup, url),
            'scripts': [script['src'] for script in soup.find_all('script', src=True)],
            'comments': self._find_hidden_comments(soup)
        }

    def _dynamic_crawl(self, url):
        try:
            result = subprocess.run(
                ['node', 'core/crawler/dynamic_crawler.js', url],
                capture_output=True, text=True, timeout=30
            )
            return json.loads(result.stdout)
        except Exception as e:
            logging.error(f"Dynamic crawl failed: {str(e)}")
            return {'links': [], 'forms': []}

    def _parse_forms(self, soup, base_url):
        forms = []
        for form in soup.find_all('form'):
            form_data = {
                'action': urljoin(base_url, form.get('action',