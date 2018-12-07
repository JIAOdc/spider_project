import requests
from lxml import etree


class Login(object):
    def __init__(self):
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'Host': 'github.com'
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()
    
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        selector = etree.HTML(response.text)
        token = selector.xpath('//div//input[2]/@value')
        return token
    
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token()[0],
            'login': email,
            'password': password
        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        # print(response.text)

        if response.status_code == 200:
            self.dynamics(response.text)
    
    def dynamics(self, html):
        selector = etree.HTML(html)
        dynamics = selector.xpath('//a[contains(@class, "user-profile-link")]//strong[contains(@class, "css-truncate-target")]//text()')[0]
        print(dynamics)


if __name__ == "__main__":
    login = Login()
    login.login(email='carmackxiao', password='Vff635241')
