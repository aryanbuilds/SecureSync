import concurrent.futures
import time
from typing import Callable
from core.crawler.crawler import AdvancedCrawler
from core.detectors import ALL_DETECTORS
from core.utils.report_generator import ReportGenerator
from core.utils.http_utils import HTTPClient
from core.utils.payload_manager import PayloadFactory
from core.utils.logging_utils import ScannerLogger
import yaml

class AdvancedScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.crawler = AdvancedCrawler()
        self.http_client = HTTPClient()
        self.config = self.load_config()
        self.logger = ScannerLogger(__name__)
        self.payload_factory = PayloadFactory()

    def load_config(self):
        with open('config/settings.yaml') as f:
            return yaml.safe_load(f)

    def run_full_scan(self, progress_callback: Callable[[int], None] = None):
        try:
            self.logger.info(f"Initializing scan for {self.target_url}")
            
            # Phase 1: Crawling
            progress_callback(5)
            crawl_data = self.crawler.crawl(
                self.target_url,
                depth=self.config['crawling']['max_depth'],
                exclude=self.config['crawling']['exclude_patterns']
            )
            
            # Phase 2: Vulnerability Scanning
            progress_callback(20)
            vulnerabilities = []
            total_tests = len(crawl_data['endpoints']) * len(ALL_DETECTORS)
            completed_tests = 0
            
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=self.config['scanning']['max_threads']
            ) as executor:
                futures = []
                for endpoint in crawl_data['endpoints']:
                    for detector_cls in ALL_DETECTORS:
                        detector = detector_cls(self.http_client, self.payload_factory)
                        futures.append(
                            executor.submit(
                                self.execute_detection,
                                detector,
                                endpoint,
                                self.config['scanning']
                            )
                        )
                
                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result:
                        vulnerabilities.extend(result)
                    completed_tests += 1
                    progress = 20 + int(70 * (completed_tests / total_tests))
                    progress_callback(min(progress, 95))
            
            # Phase 3: Post-scan analysis
            progress_callback(95)
            final_vulns = self.analyze_results(vulnerabilities)
            
            progress_callback(100)
            return {
                'target': self.target_url,
                'vulnerabilities': final_vulns,
                'scan_metrics': {
                    'pages_crawled': len(crawl_data['endpoints']),
                    'tests_performed': total_tests,
                    'vulnerabilities_found': len(final_vulns)
                }
            }
            
        except Exception as e:
            self.logger.error(f"Scan failed: {str(e)}")
            raise

    def execute_detection(self, detector, endpoint, config):
        try:
            return detector.scan(
                endpoint,
                rate_limit=config['rate_limit'],
                timeout=config['request_timeout']
            )
        except Exception as e:
            self.logger.warning(f"Detection failed for {endpoint['url']}: {str(e)}")
            return []

    def analyze_results(self, vulnerabilities):
        # Implement false positive filtering and severity adjustment
        return [vuln for vuln in vulnerabilities if self.is_valid_vulnerability(vuln)]

    def is_valid_vulnerability(self, vulnerability):
        # Add validation logic based on response analysis
        return True