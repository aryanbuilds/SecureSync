import json
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_json_report(results, filename=None):
        report = {
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities': results
        }
        if filename:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=4)
        return json.dumps(report, indent=4)

    @staticmethod
    def generate_html_report(results, filename=None):
        html = """
        <html>
        <head>
            <title>Vulnerability Report</title>
            <style>
                .vuln-high { color: #f44336; }
                .vuln-medium { color: #ff9800; }
                .vuln-low { color: #4caf50; }
            </style>
        </head>
        <body>
            <h1>Vulnerability Report</h1>
            <p>Generated at: {timestamp}</p>
            <table border="1">
                <tr>
                    <th>Type</th>
                    <th>URL</th>
                    <th>Payload</th>
                    <th>Severity</th>
                    <th>Details</th>
                </tr>
                {rows}
            </table>
        </body>
        </html>
        """.format(
            timestamp=datetime.now().isoformat(),
            rows=''.join([
                f'<tr class="vuln-{vuln["severity"].lower()}"><td>{vuln["type"]}</td><td>{vuln["url"]}</td>'
                f'<td>{vuln.get("payload", "N/A")}</td><td>{vuln["severity"]}</td>'
                f'<td>{vuln.get("details", "N/A")}</td></tr>'
                for vuln in results
            ])
        )
        if filename:
            with open(filename, 'w') as f:
                f.write(html)
        return html

    @staticmethod
    def generate_markdown_report(results, filename=None):
        md = f"""# Vulnerability Scan Report
Generated: {datetime.now().isoformat()}

## Summary
Total Vulnerabilities Found: {len(results)}

## Vulnerabilities

| Type | URL | Severity | Details |
|------|-----|----------|---------|
"""
        for vuln in results:
            md += f"| {vuln['type']} | {vuln['url']} | {vuln['severity']} | {vuln.get('details', 'N/A')} |\n"

        md += "\n## Detailed Findings\n\n"
        for i, vuln in enumerate(results, 1):
            md += f"### {i}. {vuln['type']}\n"
            md += f"- **URL:** {vuln['url']}\n"
            md += f"- **Severity:** {vuln['severity']}\n"
            if vuln.get('payload'):
                md += f"- **Payload:** {vuln['payload']}\n"
            if vuln.get('details'):
                md += f"- **Details:** {vuln['details']}\n"
            md += "\n"

        if filename:
            with open(filename, 'w') as f:
                f.write(md)
        return md