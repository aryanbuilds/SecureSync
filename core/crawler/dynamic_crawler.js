const puppeteer = require('puppeteer');

(async () => {
    const [url, timeout, depth] = process.argv.slice(2);
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    await page.setUserAgent('SecureSyncCrawler/1.0');
    const visited = new Set();
    const endpoints = [];

    const crawl = async (currentUrl, currentDepth) => {
        if (currentDepth > parseInt(depth) || visited.has(currentUrl)) return;
        visited.add(currentUrl);

        try {
            console.log(`Crawling ${currentUrl} at depth ${currentDepth}`);
            await page.goto(currentUrl, { waitUntil: 'networkidle2', timeout: parseInt(timeout) * 1000 });
            const links = await page.evaluate(() => 
                Array.from(document.querySelectorAll('a')).map(a => a.href)
            );

            endpoints.push(currentUrl);

            for (const link of links) {
                if (link.startsWith(url)) {
                    await crawl(link, currentDepth + 1);
                }
            }
        } catch (error) {
            console.error(`Error crawling ${currentUrl}:`, error);
        }
    };

    await crawl(url, 0);
    await browser.close();
    console.log(JSON.stringify(endpoints));
})();