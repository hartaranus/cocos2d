import math
import cPickle

import cocos
from cocos.director import director
from cocos.sprite import Sprite

import pyglet
from pyglet.gl import *
from pyglet.window import key

import ui
import animator
from skeleton import Bone, Skeleton, Skin, Animation, Animate

class Player(cocos.layer.Layer):
    """ Skeletal animation player example

    we take a skeleton and a list of animations and let the player
    choose what animation to play and how
    """
    is_event_handler = True

    def __init__(self, sk, skin, *anims):
        super(Player, self).__init__()
        self.skeleton = sk
        self.anims = [ cPickle.load(open(a)) for a in anims ]

        # we create a skin. Skins are what are rendered.
        # skins also are cocos nodes, so we add it to ourselves
        self.skin = animator.BitmapSkin(self.skeleton, skin)
        self.add( self.skin )

        x, y = director.get_window_size()
        self.skin.position = x/2, y/2
        self.translate = False
        self.flipped = False

    def on_key_press(self, k, mod):
        numbers = [key._1, key._2, key._3, key._4, key._5,
                   key._6, key._7, key._8, key._9, key._0 ]
        if k == key.T:
            # track if the user wants to translate origin to the current
            # skeleton position
            # if you run two walk left animations without translation
            # you will see a player move left, go to the origin and move
            # left again.
            # if you use translation, the player will just move left twice
            # as far
            self.translate = not self.translate
        if k == key.F:
            # track if the user wants to run the animation normal or flipped
            # if the animation is a guy walking left, when flipped it will
            # walk right
            self.flipped = not self.flipped
            self.skin.flip()

        if k in numbers:
            # find which animation the user wants to run
            n = numbers.index(k)
            if n < len(self.anims):
                # kill current animations
                self.skin.stop()
                anim = self.anims[n]
                # if we want to run the animation flipped, we create
                # the flipped version
                if self.flipped:
                    anim = anim.flipped()
                # we run the animation on the skin using the Animate action.
                # remember that Animate is a cocos action, so you can do
                # any action stuff you want with them.
                # you just have to say which animation you want to use
                # and what kind of translation
                self.skin.do( Animate( anim , recenter_x=self.translate ) )



if __name__ == "__main__":
    import sys, imp, os
    p = os.path.abspath(os.path.normpath(
            os.path.join(os.path.dirname(__file__).replace("\\", "/"), "../data")
            ))
    pyglet.resource.path.append(p)
    pyglet.resource.reindex()
    director.init()

    def usage():
        return "USAGE:\n"+\
               "python animator.py skeleton animation.anim+ \n" +\
               "   skeleton is a python file with a skeleton variable inside \n"+\
               "       which has the skeleton you will want to animate\n"+\
               "   animation.anim+ means a list of animation file names \n"+\
               "       each of this files will be asigned to a number 1-0"

    if len(sys.argv)<3:
        print usage()
        sys.exit()

    skin_data = imp.load_source("skin", sys.argv[2]).skin
    sk_file = imp.load_source("skeleton", sys.argv[1])
    player = Player(sk_file.skeleton, skin_data, *sys.argv[3:])
    director.run(cocos.scene.Scene(player))
