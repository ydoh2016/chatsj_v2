import requests
from key.kakao_client import CLIENT_ID, REDIRECT_URI


class Oauth:

    def __init__(self):
        self.auth_server = "https://kauth.kakao.com%s"
        self.api_server = "https://kapi.kakao.com%s"
        self.default_header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Cache-Control": "no-cache",
        }

    def auth(self, code):
        # print("로그인중")
        # print(res)
        # code = "Bearer " + res['access_token']
        return requests.post(
            url=self.auth_server % "/oauth/token",
            headers=self.default_header,
            data={
                "grant_type": "authorization_code",
                "client_id": CLIENT_ID,
                "redirect_uri": REDIRECT_URI,
                "code": code,
            },
        ).json()
    
    def userinfo(self, bearer_token):
        return requests.post(
            url=self.api_server % "/v2/user/me",
            headers={
                **self.default_header,
                **{"Authorization": bearer_token}
            },
            # "property_keys":'["kakao_account.profile_image_url"]'
            data={}
        ).json()

    def send(self, bearer_token, message):
        return requests.get(
            url = "https://kapi.kakao.com/v1/api/talk/friends",
            headers = {"Authorization": bearer_token}
        ).json()