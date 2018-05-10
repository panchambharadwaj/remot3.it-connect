import json
import os

from generate.data import GenerateData
from generate.headers import GenerateHeaders
from remot3_it_api import Remot3ItApi


class Initialize(object):

    def __init__(self):
        pass

    @staticmethod
    def get_config():
        from crypt import AESCipher

        config_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(config_path, 'config.json')
        with open(config_file, 'r') as f:
            config = json.load(f)

        crypt = AESCipher(config['CRYPT_KEY'])

        config_developer_key = crypt.decrypt(config['DEVELOPER_KEY'])
        config_login_user_name = crypt.decrypt(config['REMOT3_USER_NAME'])
        config_login_password = crypt.decrypt(config['REMOT3_PASSWORD'])

        return config_developer_key, config_login_user_name, config_login_password


class Remot3ItConnect(object):
    ssh_pattern = "ssh -l pi %s -p %s"

    def __init__(self):
        pass

    @staticmethod
    def find_between(value, a, b):
        pos_a = value.find(a)
        if pos_a == -1: return ""
        pos_b = value.rfind(b)
        if pos_b == -1: return ""
        adjusted_pos_a = pos_a + len(a)
        if adjusted_pos_a >= pos_b: return ""
        return value[adjusted_pos_a:pos_b]

    @staticmethod
    def find_after(value, a):
        pos_a = value.rfind(a)
        if pos_a == -1: return ""
        adjusted_pos_a = pos_a + len(a)
        if adjusted_pos_a >= len(value): return ""
        return value[adjusted_pos_a:]

    def main(self):
        generate_data = GenerateData()
        generate_headers = GenerateHeaders(developer_key)
        remot3_it_api = Remot3ItApi()

        login_credentials = generate_data.get_login_data(login_user_name, login_password)
        login_headers = generate_headers.get_login_headers()
        token = remot3_it_api.get_token(login_credentials, login_headers)

        session_headers = generate_headers.get_session_headers(token)
        device_list = remot3_it_api.get_device_list(session_headers)

        available_devices = {}
        device_count = 1
        for devices in device_list['devices']:
            available_devices[device_count] = {'device_name': devices['devicealias'],
                                               'device_address': devices['deviceaddress'],
                                               'host_ip': devices['devicelastip']}
            device_count += 1

        for device_name in available_devices.iteritems():
            print("%s. %s" % (device_name[0], device_name[1]['device_name']))

        device_chosen = int(raw_input("\nSelect device to connect to: "))
        device_address = available_devices[device_chosen]['device_address']
        host_ip = available_devices[device_chosen]['host_ip']

        connect_data = generate_data.get_connect_data(device_address, host_ip)
        status = remot3_it_api.proxy_connect(connect_data, session_headers)

        is_ssh = raw_input("\nNeed for SSH? [Y/N]: ")
        if is_ssh.lower() == "y":
            status = self.ssh_pattern % (self.find_between(status, "http://", ":"), (self.find_after(status, ":")))

        print("\n" + status)


if __name__ == '__main__':
    initialize_bot = Initialize()
    developer_key, login_user_name, login_password = initialize_bot.get_config()
    remot3_it_connect = Remot3ItConnect()
    remot3_it_connect.main()
