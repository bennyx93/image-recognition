import requests
from requests.exceptions import HTTPError


class ImaggaAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api.imagga.com/v2"

    def get_tags(self, image_file):
        """
        Get tags from an image
        """
        url = self.base_url + "/tags"
        response = requests.post(
            url,
            auth=(self.api_key, self.api_secret),
            files={"image": image_file},
        )
        response.raise_for_status()
        return response.json()
