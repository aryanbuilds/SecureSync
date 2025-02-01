const puppeteer = require('puppeteer');

(async () => {
    const url = process.argv[2];
    if (!url) {
        console.error('URL is required');
        process.exit(1);
    }

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url, { waitUntil: 'networkidle2' });

    const data = await page.evaluate(() => {
        const links = Array.from(document.querySelectorAll('a')).map(a => a.href);
        const forms = Array.from(document.querySelectorAll('form')).map(form => {
            const inputs = Array.from(form.elements).map(input => ({
                name: input.name,
                type: input.type
            }));
            return {
                action: form.action,
                method: form.method,
                inputs
            };
        });
        return { links, forms };
    });

    console.log(JSON.stringify(data));
    await browser.close();
})();
