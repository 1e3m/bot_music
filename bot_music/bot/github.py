import requests


class Github:
    def __init__(self, author, repo):
        self.base_url = \
            'https://api.github.com/repos/{0}/{1}/'.format(author, repo)

    def commits(self):
        response = requests.get(self.base_url + 'commits')
        return response.json()
