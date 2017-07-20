from models import DATABASE, Image, ImageCategory, Photographer, ConnectDatabase


def create_tables():
    with ConnectDatabase():
        DATABASE.create_tables([Photographer, Image, ImageCategory])

def drop_tables():
    with ConnectDatabase():
        DATABASE.drop_tables([Photographer, Image, ImageCategory])
