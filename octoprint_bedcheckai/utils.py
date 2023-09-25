import requests
from base64 import b64encode

ROUTE = 'https://octoprint.printpal.io'
SEGMENT_ENDPOINT = '/api/v2/segment'
CLIENT_TIMEOUT = 30.0


def _get(
    route : str = ROUTE,
    endpoint : str = SEGMENT_ENDPOINT,
    params : dict = None
    ):
    r = requests.get(f'{route}{endpoint}', params=params)
    return r

def _post(
    route : str = ROUTE,
    endpoint : str = SEGMENT_ENDPOINT,
    json : dict = None
    ):
    r = requests.post(f'{route}{endpoint}', json=json)
    return r

def send_infer(fb : bytes, settings, compare : bool) -> dict:
    '''
    settings : octoprint.PluginSettings
    '''
    json = {
        'image' : b64encode(fb).decode('utf-8'),
        'api_key' : settings.get(["api_key"]) if settings.get(["api_key"]) not in [None, ''] else 'octoprint',
        'printer_id' : settings.get(["printer_id"]),
        'compare_baseline' : compare
    }
    r = _post(json=json)
    if r.status_code == 200:
        r = r.json()
        return r
    return r

def update_baseline_(settings, uid_ : str = '') -> dict:
    '''
    settings : octoprint.PluginSettings
    '''
    params_ = {
        'api_key' : settings.get(["api_key"]) if settings.get(["api_key"]) not in [None, ''] else 'octoprint',
        'printer_id' : settings.get(["printer_id"]),
        'unique_id' : uid_
    }
    r = _get(endpoint='/api/v2/segment/set_baseline', params=params_)
    if r.status_code == 200:
        r = r.json()
        return r
    return None

def get_baseline_(settings) -> dict:
    '''
    settings : octoprint.PluginSettings
    '''
    params_ = {
        'api_key' : settings.get(["api_key"]) if settings.get(["api_key"]) not in [None, ''] else 'octoprint',
        'printer_id' : settings.get(["printer_id"])
    }
    r = _get(endpoint='/api/v2/segment/get_baseline', params=params_)
    if r.status_code == 200:
        r = r.json()
        return r
    return None

def snap_sync(url : str) -> bytes:
    r = _get(url)
    return r.content if r.status_code == 200 else False

'''
if __name__ == '__main__':
    params_ = {
        'api_key' : 'fmu_6be6bda1a4724a4ba09299ca78b3c637',
        'printer_id' : 'pid1',
        'unique_id' : '0f5603c5de344313b2c62cff75b5fad1'
    }
    r = _get(route='http://173.230.133.178:8888', endpoint='/api/v2/segment/set_baseline', params=params_)
    if r.status_code == 200:
        r = r.json()
        if r.get("status") == 8000:
            print(r)
'''
