from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import asyncio
from core.scanner import scan_website
from core.utils.report_generator import ReportGenerator

app = Flask(__name__)
app.secret_key = 'supersecretkey'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    url = request.form['url']
    socketio.start_background_task(target=run_scan, url=url)
    return jsonify({'status': 'started'})

def run_scan(url):
    try:
        results = asyncio.run(scan_website(url, update_status))
        # Generate reports
        report_dir = 'reports'
        md_report = ReportGenerator.generate_markdown_report(results, f"{report_dir}/report.md")
        html_report = ReportGenerator.generate_html_report(results, f"{report_dir}/report.html")
        socketio.emit('scan_complete', {'results': results})
    except Exception as e:
        socketio.emit('scan_error', {'error': str(e)})

def update_status(status):
    socketio.emit('scan_status', {'status': status})

if __name__ == '__main__':
    socketio.run(app, debug=True)