from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO
import asyncio
import yaml
import os
import logging
from pathlib import Path
from core.scanner import scan_website
from core.utils.report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app, async_mode='threading')

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Load settings
try:
    with open('config/settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)
except FileNotFoundError:
    with open(Path(__file__).parent.parent / 'config/settings.yaml', 'r') as f:
        settings = yaml.safe_load(f)

# Ensure report directory exists
report_dir = settings['report']['output_dir']
os.makedirs(report_dir, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    socketio.start_background_task(target=run_scan, url=url)
    return jsonify({'status': 'started'})

@app.route('/reports/<path:filename>')
def get_report(filename):
    return send_from_directory(report_dir, filename)

def run_scan(url):
    try:
        update_status(f"Starting scan for {url}")
        logging.debug(f"Starting scan for {url}")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        results = loop.run_until_complete(scan_website(url, update_status))
        loop.close()
        
        # Generate reports
        md_report = ReportGenerator.generate_markdown_report(results, f"{report_dir}/report.md")
        html_report = ReportGenerator.generate_html_report(results, f"{report_dir}/report.html")
        
        socketio.emit('scan_complete', {
            'results': results, 
            'reports': {
                'markdown': '/reports/report.md',
                'html': '/reports/report.html'
            }
        })
        logging.debug(f"Scan completed for {url}")
    except Exception as e:
        logging.error(f"Scan error for {url}: {str(e)}")
        socketio.emit('scan_error', {'error': str(e)})

def update_status(status):
    logging.debug(f"Status update: {status}")
    socketio.emit('scan_status', {'status': status})

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)