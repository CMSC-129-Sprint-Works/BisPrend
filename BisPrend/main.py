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
from kivy.graphics.instructions import Canvas


#kivymd
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.clock import Clock
from user import User
import sqlite3
# import quiz

Config.set('graphics', 'resizable', True)

newPlayer = User() #global scope (for testing)

check = []
for i in range(0,14):
    check.append(0)

class sentenceButton(MDRectangleFlatButton):
    def __init__(self,sampeng:str,sampbis:str):
        super(sentenceButton,self).__init__()
        self.__sampeng = sampeng
        self.__sampbis = sampbis
        self.text = "Sampol nga tudling-pulong\n(sample sentences)"
        self.md_bg_color = [1,0.8,0.4,1]
        self.theme_text_color = 'Custom'
        self.text_color = [0,0,0,1]
        self.font_name = "Mont"
        self.size_hint = (0.3,0.7)
        self.pos_hint = {'y': 0.9, 'x': 0.7}
        
    def on_release(self):
        dialog = MDDialog(
            title = "Sampol nga tudling-pulong\n(sample sentences)",
            text = ("Bisaya : " + self.__sampbis +"\n" + "English: " + self.__sampeng),
            size_hint = (0.4,0.3),
            pos_hint = {"center_x": .5, "center_y": .5}
        )
        dialog.open()
        pass 
        

def CarouselMaker(category:str,subcategory:str):
    conn = sqlite3.connect('Information.db')
    curs = conn.cursor()
    curs.execute("SELECT * FROM Information WHERE Category = \"" + category + "\" AND Subcategory = \"" + subcategory +"\"")
    listofall = curs.fetchall()

    caros = Carousel(direction = "right",size_hint=(1,.91))
    for i in listofall:
        imagesrc = i[3]
        sampbis = i[4]
        sampeng = i[5]
        image = Image(source=imagesrc)
        card = MDCard(size_hint = (.4,.8),
        pos_hint = {"center_x": .5, "center_y": .5}
        )
        floater = FloatLayout(size=(1,1),
            pos_hint = {"center_x":.5,"center_y":.5}
        )
        sentenceButn = sentenceButton(sampeng,sampbis)
        # floater.add_widget(sentenceButn)

        card.add_widget(image)
        card.add_widget(sentenceButn)
        caros.add_widget(card)

    return caros

#Screens
class PageManager(ScreenManager):
    category_tracker = [] #tracks which category-subcategory the user is in
    def updateTracker(self, category):
        '''
        Adds a category to the category tracker if it's not yet added
        '''
        if category not in self.category_tracker:
            self.category_tracker.append(category)
        print("Tracker: " + str(self.category_tracker))

class RegPage(Screen):
    
    def on_enter(self):
        Clock.schedule_once(self.skip)

    def registerUser(self):
        newPlayer.createUserFile(self.username.text)
        print(f"Name: {newPlayer.getName()} \nProgress: {newPlayer.getProgress()}")

    def skip(self,dt):
        if(not newPlayer.hasUser()):
            self.manager.current = 'Selector'

class MenuSelector(Screen):
    def on_enter(self):
        self.manager.category_tracker = [] #reset the tracker to empty
        print("Tracker: " + str(self.manager.category_tracker))

    def playername(self):
        return newPlayer.getName()

#Balay and subcategories
class BalayPage(Screen):
    def on_enter(self):
        self.manager.updateTracker(self.name)

class PamilyaPage(Screen):
    def on_pre_enter(self):
        if check[0] != 1:
            caros = CarouselMaker("Balay","Pamilya")
            self.add_widget(caros)
            check[0] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

    def on_leave(self):
        print("yawa")

class ResibidorPage (Screen):
    def on_pre_enter(self):
        if check[1] != 1:
            caros = CarouselMaker("Balay","Resibidor")
            self.add_widget(caros)
            check[1] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class KomidorPage(Screen):
    def on_pre_enter(self):
        if check[2] != 1:
            caros = CarouselMaker("Balay","Komidor")
            self.add_widget(caros)
            check[2] = 1
    
    def on_enter(self):
        self.manager.updateTracker(self.name)

class Kan_ananPage(Screen):
    def on_pre_enter(self):
        if check[3] != 1:
            caros = CarouselMaker("Balay","Kan-anan")
            self.add_widget(caros)
            check[3] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class KatulgananPage(Screen):
    def on_pre_enter(self):
        if check[4] != 1:
            caros = CarouselMaker("Balay","Katulganan")
            self.add_widget(caros)
            check[4] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class KasilyasPage(Screen):
    def on_pre_enter(self):
        if check[5] != 1:
            caros = CarouselMaker("Balay","Kasilyas")
            self.add_widget(caros)
            check[5] = 1 

    def on_enter(self):
        self.manager.updateTracker(self.name)

#skuylahan and subcategories

class SkuylahanPage(Screen):
    def on_enter(self):
        self.manager.updateTracker(self.name)

class ClassroomPage(Screen):
    def on_pre_enter(self):
        if check[6] != 1:
            caros = CarouselMaker("Skuylahan","Lawak Tunghaan")
            self.add_widget(caros)
            check[6] = 1
    
    def on_enter(self):
        self.manager.updateTracker(self.name)

class NumeroPage(Screen):
    def on_pre_enter(self):
        if check[7] != 1:
            caros = CarouselMaker("Skuylahan","Numero")
            self.add_widget(caros)
            check[7] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class ClinicPage(Screen):
    def on_pre_enter(self):
        if check[8] != 1:
            caros = CarouselMaker("Skuylahan","Tambalan")
            self.add_widget(caros)
            check[8] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class LibPage(Screen):
    def on_pre_enter(self):
        if check[9] != 1:
            caros = CarouselMaker("Skuylahan","Bibliyoteka")
            self.add_widget(caros)
            check[9] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class CanteenPage(Screen):
    def on_pre_enter(self):
        if check[10] != 1:
            caros = CarouselMaker("Skuylahan","Kantin")
            self.add_widget(caros)
            check[10] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

#tindahan and subcategories

class TindahanPage(Screen):
    def on_enter(self):
        self.manager.updateTracker(self.name)

class PagkaonPage(Screen):
    def on_pre_enter(self):
        if check[11] != 1:
            caros = CarouselMaker("Tindahan","Pagkaon")
            self.add_widget(caros)
            check[11] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)

class SaninaPage(Screen):
    def on_pre_enter(self):
        if check[12] != 1:
            caros = CarouselMaker("Tindahan","Sinina")
            self.add_widget(caros)
            check[12]
    
    def on_enter(self):
        self.manager.updateTracker(self.name)

class KwartaPage(Screen):
    def on_pre_enter(self):
        if check[13] != 1:
            caros = CarouselMaker("Tindahan","Kuwarta")
            self.add_widget(caros)
            check[13] = 1

    def on_enter(self):
        self.manager.updateTracker(self.name)



class BisprendApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette= "Blue"
        self.theme_cls.primary_hue= "A700"
        self.theme_cls.accent_palette = "LightGreen"
        self.theme_cls.accent_hue = "A700"
        self.root = Builder.load_file("bisprend.kv")

#Registering Font
LabelBase.register(name="Mont",
    fn_regular= "font/Mont-ExtraLightDemo.otf", 
    fn_bold = "font/Mont-HeavyDEMO.otf"
)

if __name__ == '__main__':
    BisprendApp().run()