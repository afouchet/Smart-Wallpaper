Smart wallpapers
================

This project gets nice images from www.unsplash.com and sets them as you
wallpaper.
You can vote them Up or Down.
In a second time, you'll use machine learning to predict if you'll like an
image, and it will get "only" nice images.

Initialization
--------------

You need to get an API key from www.unsplash.com to request images and their
data (features). Rename the file conf.py.example to conf.py and give the
informations API key, folder to store images.

Then run python init_db.py

Usage
-----

If you like the image:

> python unsplash.py 1

If you don't like it:

> python unsplash.py -1