from flask import Flask, render_template, request, jsonify
from core.scanner import AdvancedScanner
import logging

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def start_scan():
    target_url = request.json['url']
    logging.info(f"Starting scan for: {target_url}")
    
    scanner = AdvancedScanner(target_url)
    results = scanner.run_full_scan()
    
    logging.info(f"Scan completed for: {target_url}")
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)