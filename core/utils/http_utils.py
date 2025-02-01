import requests

def send_request(url, method='GET', data=None, headers=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, data=data, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None