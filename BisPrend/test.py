# from user import User

# userInst = User()

# userInst.createUserFile("John Doe")

# print(userInst.getName())
# print(userInst.getProgress())
# print(userInst.hasUser())

# userInst.registername("Mark")
# userInst.updateuserprogress(5)

# userInst2 = User()

# print(userInst.getName())
# print(userInst.getProgress())
# print(userInst.hasUser())
from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.text import LabelBase
#from kivy.properties import ObjectProperty
from kivy.config import Config

#kivy uix
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image

#kivymd
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard

import sqlite3



category = "Balay"
subcategory = "Pamilya"

def main():
    conn = sqlite3.connect('Information.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM Information WHERE Category = \"" + category + "\" AND Subcategory = \"" + subcategory +"\"")
    listofall = curs.fetchall()

    caros = Carousel(direction = "right")
    for i in listofall:
        imagesrc = i[3]
        sampbis = i[4]
        sampeng = i[5]
        image = Image(source=imagesrc)
        card = MDCard(size_hint = (.4,.8),pos_hint = {"center_x": .5, "center_y": .5},)
        card.add_widget(image)
        caros.add_widget(card)

    return caros




main()