from datetime import datetime
from functools import wraps
import peewee

from conf import database_name

DATABASE = peewee.SqliteDatabase(database_name)

class ConnectDatabase:
    def __enter__(self):
        DATABASE.connect()

    def __exit__(self, type, value, traceback):
        DATABASE.close()

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            with self:
                return func(*args, **kwargs)

        return inner

class BaseModel(peewee.Model):
    class Meta:
        database = DATABASE


class Photographer(BaseModel):
    name = peewee.CharField()
    id_publisher = peewee.CharField()
    location = peewee.CharField()


class Image(BaseModel):
    path = peewee.CharField()
    created_at = peewee.DateTimeField(default=datetime.now)
    url = peewee.CharField()
    current_background = peewee.BooleanField()
    likes = peewee.IntegerField()
    photographer = peewee.ForeignKeyField(Photographer)
    vote = peewee.IntegerField()


class ImageCategory(BaseModel):
    image = peewee.ForeignKeyField(Image)
    name = peewee.CharField()
    category_id = peewee.IntegerField()

    class Meta:
        indexes = (
            (('image', 'category_id'), True),
        )
