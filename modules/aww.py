# Description:
#   returns an aww image from Reddit's /r/aww frontpage
#
# Commands:
#
#   !aww
#
# Dependencies:
#  requests
#  random

## Todos:
# filter out non valid images

from botulus.basemodule import BaseModule
import requests
import random


class Aww(BaseModule):
    """ Reddit aww pics lookup module """
    def default(self):
        r = requests.get('http://www.reddit.com/r/aww.json')
        if r.status_code == 200:
            data = r.json()
            awwlist = data['data']['children']

            if len(awwlist) > 0:
                randomaww = random.choice(awwlist)
                return randomaww['data']['url']
            else:
                return "No image found"
__module__ = Aww
