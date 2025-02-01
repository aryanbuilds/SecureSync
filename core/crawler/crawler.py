import subprocess
import json
import logging

class AdvancedCrawler:
    def crawl(self, url):
        try:
            result = subprocess.run(
                ['node', 'core/crawler/dynamic_crawler.js', url],
                capture_output=True, text=True
            )
            return json.loads(result.stdout)
        except Exception as e:
            logging.error(f"Error during crawling: {e}")
            return {'links': [], 'forms': []}