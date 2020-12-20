import requests


class BlizzardTools():
    """ Class of tools to facilitate authenticating and fetching basic information
        from Blizzard Entertainment WoW Profile API"""

    def __init__(self, auth_data):
        self.description = 'Consumes Blizzard WoW Profile API'
        self.domain = "api.blizzard.com"
        self.auth_domain = "battle.net"
        self.region = auth_data.get('region', "eu")
        self.base_url = f"https://{self.region}.{self.domain}"
        self.auth_url = f"https://{self.region}.{self.auth_domain}"
        self.client_id = auth_data['client_id']
        self.client_secret = auth_data['client_secret']
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.jar = requests.cookies.RequestsCookieJar()
        self.session = requests.Session()
        self.auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        self.client_token = None

    def _get(self, url=None, parameters=None, auth=None, response="json"):
        r = self.session.get(url=url, params=parameters, auth=auth, headers=self.headers,
                             cookies=self.jar)
        if response == "text":
            return r.text
        elif response == "json":
            return r.json()

    def _post(self, url=None, parameters=None, payload=None, response="json"):
        if parameters is None:
            r = self.session.post(url=url, headers=self.headers, cookies=self.jar,
                                  data=payload)
        else:
            r = self.session.post(url=url, headers=self.headers,
                                  cookies=self.jar, params=parameters,
                                  data=payload)
        if response == "text":
            return r.text
        elif response == "json":
            return r.json()

    def get_auth_token(self):
        url = f"{self.auth_url}/oauth/token"
        parameters = {"grant_type": "client_credentials"}
        self.client_token = self._get(url, auth=self.auth, parameters=parameters)
        self.headers['Authorization'] = f'Bearer {self.client_token["access_token"]}'
        return self.client_token

    def get_character_profile(self, realm, char_name):
        url = f"{self.base_url}/profile/wow/character/{realm}/{char_name}"
        if self.client_token is None:
            self.get_auth_token()
        parameters = {"namespace": f"profile-{self.region}",
                      "locale": "en_US",
                      "access_token": self.client_token["access_token"]}
        profile = self._get(url, parameters=parameters)
        return profile

    def get_guild_roster(self, realm, guild_name):
        url = f"{self.base_url}/data/wow/guild/{realm}/{guild_name}/roster"
        if self.client_token is None:
            self.get_auth_token()
        parameters = {"namespace": f"profile-{self.region}",
                      "locale": "en_US",
                      "access_token": self.client_token["access_token"]}
        roster = self._get(url, parameters=parameters)
        return roster
