#!/usr/bin/python

import peewee
import os
import requests
import sys

from models import ConnectDatabase, Image, ImageCategory, Photographer
from conf import unsplash_key, path_wallpaper

URL = 'https://api.unsplash.com/'


@ConnectDatabase()
def vote_background(vote):
    image_bg = Image.get(Image.current_background == True)
    image_bg.vote = vote
    image_bg.save()


@ConnectDatabase()
def get_image():
    res = requests.get("{url}/photos/random?client_id={key_app}".format(
        url=URL, key_app=unsplash_key)).json()
    user_json = res['user']

    # Setting User
    try: 
        user = Photographer.get(Photographer.id_publisher == user_json['id'])
    except peewee.DoesNotExist:
        user = Photographer(
            name=user_json['name'],
            id_publisher=user_json['id'],
            location=user_json['location'] or '',
        )
        user.save()

    # Setting Image
    path_image = path_wallpaper + '/{}.jpg'.format(res['id'])
    image = Image(
        path=path_image,
        url=res['links']['download'],
        current_background=False,
        likes=res['likes'],
        photographer=user,
        vote=0,
    )
    image.save()

    # Setting ImageCategorie
    for cat in res['categories']:
        categ = ImageCategory(
            image=image,
            name=cat['title'],
            category_id=cat['id'],
        )
        categ.save()

    img_raw = requests.get(image.url)
    with open(path_image, 'w+') as f:
        f.write(img_raw.content)

    return image


@ConnectDatabase()
def set_background(image):
    # os.system('feh --bg-scale {}'.format(image.path))
    os.system('feh --bg-max {}'.format(image.path))
    images_bg = Image.select().where(Image.current_background == True)
    for img in images_bg:
        img.current_background = False
        img.save()
    image.current_background = True
    image.save()


def reload_background():
    with ConnectDatabase():
        image_bg = Image.get(Image.current_background == True)
    set_background(image_bg)


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 2:
        raise ValueError("Need one arguments, the vote !")
    if len(args) == 1:
        # Reloading background
        reload_background()
    else:
        vote = int(args[1])
        vote_background(vote)
        image = get_image()
        set_background(image)
