import os
import json
import time
import markdown
import logging

class ReportGenerator:
    @staticmethod
    def generate_markdown_report(results, output_path):
        """Generate a Markdown format report from scan results"""
        logging.debug(f"Generating Markdown report at {output_path}")
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        content = f"# Security Scan Report\n\n"
        content += f"**Generated:** {timestamp}\n\n"
        
        content += "## Vulnerabilities Found\n\n"
        
        if not results:
            content += "*No vulnerabilities were found.*\n\n"
        else:
            # Group by severity
            by_severity = {"High": [], "Medium": [], "Low": [], "Info": []}
            for vuln in results:
                severity = vuln.get('severity', 'Info')
                by_severity[severity].append(vuln)
            
            # Generate content for each severity level
            for severity in ["High", "Medium", "Low", "Info"]:
                vulns = by_severity[severity]
                if not vulns:
                    continue
                    
                content += f"### {severity} Severity\n\n"
                
                for i, vuln in enumerate(vulns):
                    content += f"#### {i+1}. {vuln['type']}\n\n"
                    content += f"- **URL:** {vuln['url']}\n"
                    
                    if 'details' in vuln and vuln['details']:
                        content += f"- **Details:** {vuln['details']}\n"
                        
                    if 'payload' in vuln and vuln['payload']:
                        content += f"- **Payload:** `{vuln['payload']}`\n"
                        
                    content += "\n"
                
        # Write to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(content)
        
        logging.debug(f"Markdown report generated at {output_path}")
        return output_path

    @staticmethod
    def generate_html_report(results, output_path):
        """Generate an HTML format report from scan results"""
        logging.debug(f"Generating HTML report at {output_path}")
        # First create the markdown
        md_content = ReportGenerator.generate_markdown_report(results, output_path + ".md.tmp")
        
        # Convert markdown to HTML
        with open(output_path + ".md.tmp", 'r') as f:
            md_text = f.read()
            html = markdown.markdown(md_text, extensions=['tables', 'nl2br'])
        
        # Add CSS styling
        styled_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Security Scan Report</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 40px;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #3498db;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #e74c3c;
                }}
                h3:contains("Medium") {{
                    color: #f39c12;
                }}
                h3:contains("Low") {{
                    color: #27ae60;
                }}
                h4 {{
                    margin-top: 20px;
                    color: #555;
                }}
                ul {{
                    list-style-type: square;
                }}
                code {{
                    background-color: #f8f8f8;
                    padding: 2px 5px;
                    border-radius: 3px;
                    font-family: monospace;
                    font-size: 0.9em;
                }}
            </style>
        </head>
        <body>
            {html}
        </body>
        </html>
        """
        
        # Write HTML to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(styled_html)
        
        # Remove temporary file
        if os.path.exists(output_path + ".md.tmp"):
            os.remove(output_path + ".md.tmp")
        
        logging.debug(f"HTML report generated at {output_path}")
        return output_path