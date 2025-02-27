from .crawler.crawler import DynamicCrawler
from .detectors.header_checker import HeaderChecker
from .detectors.directory_traversal import DirectoryTraversalDetector
from .detectors.command_injection import CommandInjectionDetector
import asyncio
import logging

async def scan_website(url, status_callback=None):
    logging.debug(f"Initializing scan for {url}")
    if status_callback:
        status_callback("Initializing crawlers...")
    
    crawler = DynamicCrawler(intensity='medium')
    header_checker = HeaderChecker()
    dir_traversal = DirectoryTraversalDetector()
    cmd_injection = CommandInjectionDetector()
    
    if status_callback:
        status_callback("Crawling website for endpoints...")
    
    try:
        endpoints = await crawler.crawl(url)
        logging.debug(f"Found {len(endpoints)} endpoints")
    except Exception as e:
        logging.error(f"Error during crawling: {str(e)}")
        if status_callback:
            status_callback(f"Error during crawling: {str(e)}")
        endpoints = ['/']
    
    if status_callback:
        status_callback(f"Found {len(endpoints)} endpoints. Starting security checks...")
    
    header_results = await header_checker.scan(url, endpoints)
    logging.debug(f"Completed header security check, found {len(header_results)} issues")
    if status_callback:
        status_callback(f"Completed header security check, found {len(header_results)} issues")
    
    dir_results = await dir_traversal.scan(url, endpoints)
    logging.debug(f"Completed directory traversal check, found {len(dir_results)} issues")
    if status_callback:
        status_callback(f"Completed directory traversal check, found {len(dir_results)} issues")
    
    cmd_results = await cmd_injection.scan(url, endpoints)
    logging.debug(f"Completed command injection check, found {len(cmd_results)} issues")
    if status_callback:
        status_callback(f"Completed command injection check, found {len(cmd_results)} issues")
    
    all_vulnerabilities = header_results + dir_results + cmd_results
    logging.debug(f"Scan completed. Found {len(all_vulnerabilities)} vulnerabilities")
    
    if status_callback:
        status_callback(f"Scan completed. Found {len(all_vulnerabilities)} vulnerabilities.")
    
    return all_vulnerabilities