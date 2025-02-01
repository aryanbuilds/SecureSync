const puppeteer = require('puppeteer');

(async () => {
    const url = process.argv[2];
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();

    await page.goto(url, { waitUntil: 'networkidle2' });

    const scanData = await page.evaluate(() => {
        const getFormDetails = (form) => {
            const inputs = Array.from(form.elements).map(el => ({
                name: el.name,
                type: el.type,
                value: el.value || '',
                placeholder: el.placeholder || ''
            }));
            return {
                action: form.action,
                method: form.method,
                inputs: inputs
            };
        };

        return {
            links: Array.from(document.querySelectorAll('a[href]')).map(a => a.href),
            forms: Array.from(document.querySelectorAll('form')).map(getFormDetails),
            scripts: Array.from(document.scripts).map(script => script.src)
        };
    });

    await browser.close();
    console.log(JSON.stringify(scanData, null, 2));
})();
