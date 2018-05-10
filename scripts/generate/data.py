import json


class GenerateData(object):

    def __init__(self):
        pass

    @staticmethod
    def get_login_data(login_user_name, login_password):
        return json.dumps({
            "username": login_user_name,
            "password": login_password
        })

    @staticmethod
    def get_connect_data(device_address, host_ip):
        return json.dumps({
            'deviceaddress': device_address,
            'hostip': host_ip,
            'wait': True
        })
