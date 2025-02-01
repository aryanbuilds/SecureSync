from flask import Flask, render_template, request, jsonify, send_file
from core.scanner import AdvancedScanner
from core.utils.report_generator import ReportGenerator
import logging
import os
import threading

app = Flask(__name__)
app.config['SCAN_REPORTS'] = 'reports/'

class ScanManager:
    def __init__(self):
        self.active_scans = {}
        self.scan_history = []

    def start_scan(self, scan_id, target_url):
        scanner = AdvancedScanner(target_url)
        self.active_scans[scan_id] = {
            'thread': threading.Thread(target=self.run_scan, args=(scan_id, scanner)),
            'progress': 0,
            'results': None
        }
        self.active_scans[scan_id]['thread'].start()

    def run_scan(self, scan_id, scanner):
        try:
            results = scanner.run_full_scan(progress_callback=lambda p: self.update_progress(scan_id, p))
            self.active_scans[scan_id]['results'] = results
            report_path = ReportGenerator.generate_html_report(results, app.config['SCAN_REPORTS'])
            self.scan_history.append({
                'id': scan_id,
                'report': report_path,
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            logging.error(f"Scan failed: {str(e)}")
        finally:
            self.update_progress(scan_id, 100)

    def update_progress(self, scan_id, progress):
        self.active_scans[scan_id]['progress'] = progress

scan_manager = ScanManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def start_scan():
    scan_id = str(uuid.uuid4())
    target_url = request.json['url']
    scan_manager.start_scan(scan_id, target_url)
    return jsonify({'scan_id': scan_id})

@app.route('/status/<scan_id>')
def scan_status(scan_id):
    if scan_id not in scan_manager.active_scans:
        return jsonify({'error': 'Invalid scan ID'}), 404
    return jsonify({
        'progress': scan_manager.active_scans[scan_id]['progress'],
        'completed': scan_manager.active_scans[scan_id]['results'] is not None
    })

@app.route('/report/<scan_id>')
def get_report(scan_id):
    entry = next((e for e in scan_manager.scan_history if e['id'] == scan_id), None)
    if not entry or not os.path.exists(entry['report']):
        return jsonify({'error': 'Report not found'}), 404
    return send_file(entry['report'])

if __name__ == '__main__':
    os.makedirs(app.config['SCAN_REPORTS'], exist_ok=True)
    app.run(debug=False)