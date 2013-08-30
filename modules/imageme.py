# Description:
#   Image me module
#
# Commands:
#
#   !image me <item> - pull random image from google image search
#
# Dependencies:
#   requests
import requests
import random
from botulus.basemodule import BaseModule


class Imageme(BaseModule):
    def me(self, args=None):
        response = requests.get('http://ajax.googleapis.com/ajax/services/search/images', params=dict(v="1.0", rsz='8', q=args[0], safe='active',))
        if response.status_code == 200:
            data = response.json()
            images = data['responseData']['results']

            if len(images) > 0:
                image = random.choice(images[:5])
                return image['unescapedUrl']

__module__ = Imageme
