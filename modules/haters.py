# Description:
#   returns a random haters gonna hate image
#
# Commands:
#
#   !haters
#
# Dependencies:
#  random

## Todos:
# filter out non valid images

from botulus.basemodule import BaseModule
import random


class Haters(BaseModule):
    """ Random haters gonna hate image module """

    def default(self):
        haterslist = [
            "http://jesad.com/img/life/haters-gonna-hate/haters-gonna-hate01.jpg",
            "http://i671.photobucket.com/albums/vv78/Sinsei55/HatersGonnaHatePanda.jpg",
            "http://24.media.tumblr.com/tumblr_lltwmdVpoL1qekprfo1_500.gif",
            "http://s3.amazonaws.com/kym-assets/photos/images/newsfeed/000/087/536/1292102239519.gif",
            "http://i391.photobucket.com/albums/oo351/PikaPow3/squirtle.gif",
            "http://c.static.memegenerator.net/cache/instances/500x/13/13355/13676320.jpg",
            "http://icanhasinternets.com/wp-content/uploads/2010/05/haters.gif",
            "http://icanhasinternets.com/wp-content/uploads/2010/05/haters5.jpg",
            "http://media.tumblr.com/tumblr_m2yv2hqw9l1rnvwt1.gif",
            "http://loldailyfun.com/wp-content/uploads/2012/02/Haters-Gonna-hate-Funny.jpg",
            "http://brian.io/slides/incog-intro/img/rollin.jpg",
            "http://static.fjcdn.com/pictures/Haters+Gonna+Hate_0dd058_3113024.jpg"]

        randomimage = random.choice(haterslist)
        msg = 'Haters gonna hate %s' % randomimage
        return msg

__module__ = Haters
