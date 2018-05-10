class GenerateHeaders(object):

    def __init__(self, developer_key):
        self.developer_key = developer_key

    def get_login_headers(self):
        return {
            'developerkey': self.developer_key,
            'content-type': "application/json",
            'cache-control': "no-cache"
        }

    def get_session_headers(self, token):
        return {
            'Content-Type': "application/json",
            'developerkey': self.developer_key,
            'token': token,
        }
