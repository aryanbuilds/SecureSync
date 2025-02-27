import asyncio
import json
import logging
from pathlib import Path

class DynamicCrawler:
    def __init__(self, intensity='medium'):
        self.timeout = {'low': 30, 'medium': 60, 'high': 120}[intensity]
        self.depth = {'low': 2, 'medium': 5, 'high': 10}[intensity]
        logging.basicConfig(level=logging.DEBUG)

    async def crawl(self, url, user_agent='Mozilla/5.0'):
        logging.debug(f"Starting crawl for {url} with timeout {self.timeout} and depth {self.depth}")
        cmd = [
            'node', 
            str(Path(__file__).parent / 'dynamic_crawler.js'),
            url,
            str(self.timeout),
            str(self.depth)
        ]
        
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await proc.communicate()
        
        if stderr:
            logging.error(f"Crawler error: {stderr.decode()}")
            raise RuntimeError(f"Crawler error: {stderr.decode()}")
        
        logging.debug(f"Crawl completed for {url}")
        return json.loads(stdout.decode())