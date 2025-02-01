import asyncio
from core.crawler.crawler import DynamicCrawler
from core.detectors.xss import XSSDetector
from core.detectors.sql_injection import SQLiDetector
from core.detectors.command_injection import CommandInjectionDetector
from core.detectors.sensitive_data import SensitiveDataExposure
from core.detectors.directory_traversal import DirectoryTraversalDetector
from core.detectors.header_checker import HeaderChecker

class Scanner:
    def __init__(self, target_url, checks=None, update_status=None):
        self.target_url = target_url
        self.checks = checks or ['xss', 'sqli', 'ci', 'sde', 'dt', 'headers']
        self.crawler = DynamicCrawler()
        self.detectors = self._initialize_detectors()
        self.update_status = update_status

    def _initialize_detectors(self):
        detectors = []
        if 'xss' in self.checks:
            detectors.append(XSSDetector())
        if 'sqli' in self.checks:
            detectors.append(SQLiDetector())
        if 'ci' in self.checks:
            detectors.append(CommandInjectionDetector())
        if 'sde' in self.checks:
            detectors.append(SensitiveDataExposure())
        if 'dt' in self.checks:
            detectors.append(DirectoryTraversalDetector())
        if 'headers' in self.checks:
            detectors.append(HeaderChecker())
        return detectors

    async def run_scan(self):
        endpoints = await self.crawler.crawl(self.target_url)
        results = []
        tasks = []
        for detector in self.detectors:
            if self.update_status:
                self.update_status(f"Running {detector.__class__.__name__} scan")
            tasks.append(detector.scan(self.target_url, endpoints))
        
        results = await asyncio.gather(*tasks)
        return self._process_results(results)

    def _process_results(self, raw_results):
        processed = []
        for vuln_list in raw_results:
            processed.extend(vuln_list)
        return sorted(processed, key=lambda x: x['severity'], reverse=True)

async def scan_website(url, update_status=None):
    scanner = Scanner(target_url=url, update_status=update_status)
    results = await scanner.run_scan()
    return results