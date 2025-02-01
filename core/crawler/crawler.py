import asyncio
import json
from pathlib import Path

class DynamicCrawler:
    def __init__(self, intensity='medium'):
        self.timeout = {'low': 30, 'medium': 60, 'high': 120}[intensity]
        self.depth = {'low': 2, 'medium': 5, 'high': 10}[intensity]

    async def crawl(self, url):
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
            raise RuntimeError(f"Crawler error: {stderr.decode()}")
            
        return json.loads(stdout.decode())