def get_payloads(detector_type):
    payload_file = f'wordlists/{detector_type}.txt'
    with open(payload_file, 'r', encoding='utf-8') as f:
        payloads = f.read().splitlines()
    return payloads