import requests


class Remot3ItApi(object):
    remot3_api_url = "https://api.remot3.it/apv/v23.5"
    api_login = remot3_api_url + "/user/login"
    api_device_list = remot3_api_url + "/device/list/all"
    api_connect = remot3_api_url + "/device/connect"

    def __init__(self):
        pass

    def get_token(self, login_credentials, login_headers):
        response = requests.post(self.api_login, data=login_credentials, headers=login_headers)
        if response.status_code == 200:
            return response.json()['token']
        else:
            print("Status Code: %s | Response: %s" % (response.status_code, response.text))
            return None

    def get_device_list(self, device_list_headers):
        response = requests.get(self.api_device_list, headers=device_list_headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Status Code: %s | Response: %s" % (response.status_code, response.text))
            return None

    def proxy_connect(self, connect_data, session_headers):

        response = requests.post(self.api_connect, data=connect_data, headers=session_headers)
        if response.status_code == 200:
            result = response.json()
            return result['connection']['status']
        else:
            print("Status Code: %s | Response: %s" % (response.status_code, response.text))
            return None
