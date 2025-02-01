import concurrent.futures
from .crawler.crawler import AdvancedCrawler
from .detectors import (
    XSSDetector, SQLInjector, 
    CommandInjector, DirectoryTraversalDetector,
    SensitiveDataDetector, HeaderChecker
)
from .utils.report_generator import ReportGenerator
import logging

class AdvancedScanner:
    def __init__(self, target_url):
        self.target_url = target_url
        self.crawler = AdvancedCrawler()
        self.detectors = [
            XSSDetector(),
            SQLInjector(),
            CommandInjector(),
            DirectoryTraversalDetector(),
            SensitiveDataDetector(),
            HeaderChecker()
        ]
    
    def run_full_scan(self):
        logging.info(f"Crawling website: {self.target_url}")
        crawl_data = self.crawler.crawl(self.target_url)
        
        vulnerabilities = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(detector.scan, self.target_url, crawl_data)
                for detector in self.detectors
            ]
            
            for future in concurrent.futures.as_completed(futures):
                vulnerabilities.extend(future.result())
        
        logging.info(f"Generating report for: {self.target_url}")
        report = ReportGenerator.generate(vulnerabilities)
        
        return {
            'status': 'completed',
            'vulnerabilities': vulnerabilities,
            'report': report
        }