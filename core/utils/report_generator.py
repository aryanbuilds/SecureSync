from jinja2 import Environment, FileSystemLoader
import pdfkit
import os
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate_html_report(scan_results, output_dir):
        env = Environment(loader=FileSystemLoader('templates'))
        template = env.get_template('report_template.html')
        
        report_html = template.render(
            scan=scan_results,
            vulnerabilities=scan_results['vulnerabilities'],
            scan_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        os.makedirs(output_dir, exist_ok=True)
        report_path = os.path.join(output_dir, f"report_{scan_results['target'].replace('://', '_').replace('/', '_')}.html")
        
        with open(report_path, 'w') as f:
            f.write(report_html)
            
        # Generate PDF version
        pdf_path = report_path.replace('.html', '.pdf')
        pdfkit.from_file(report_path, pdf_path)
        
        return pdf_path

    @staticmethod
    def generate_console_report(scan_results):
        print(f"\nScan Report for {scan_results['target']}")
        print(f"Vulnerabilities Found: {len(scan_results['vulnerabilities'])}")
        for vuln in scan_results['vulnerabilities']:
            print(f"- {vuln['type']} at {vuln['url']} (Severity: {vuln['severity']})")