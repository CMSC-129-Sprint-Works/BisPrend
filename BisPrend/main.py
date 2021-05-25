from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.text import LabelBase
#from kivy.properties import ObjectProperty
from kivy.config import Config
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image

#kivy uix
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout

#kivymd
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog

from kivy.clock import Clock
from user import User
# import quiz
import os
import math
import sqlite3


Config.set('graphics', 'resizable', True)

newPlayer = User() #global scope (for testing)


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


class CategoryPage(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(size = self.on_size_change)
    
    def on_size_change(self, *args):
        num_btns = math.floor(self.width/210)
        if num_btns:
            rem_space = self.width - (num_btns*210)
            self.ids.subcat_btns_container.padding = rem_space/2, "10dp"

    def on_pre_enter(self, *args):
        self.cat_name = self.manager.category_tracker[0]
        self.cat_location = os.getcwd() + "/" + self.cat_name
        self.subcategories_list = [f.name for f in os.scandir(self.cat_location) if f.is_dir()]
        self.subcategories_list.remove("buttons")
        # set background
        self.ids.subcat_btns_scrollview.bg = "{}/{}-bg.jpg".format(self.cat_name, self.cat_name)

    def on_enter(self):
        # load subcategory buttons
        if not self.ids.subcat_btns_container.children:
            for subcat in self.subcategories_list:
                btn_img_loc = "{}/buttons/{}.jpg".format(self.cat_location, subcat)
                self.ids.subcat_btns_container.add_widget(SubcategoryButton(subcat_name = subcat, icon = btn_img_loc, on_release = self.on_subcat_btn_pressed))

    def on_subcat_btn_pressed(self, subcat_btn_instance):
        self.manager.updateTracker(subcat_btn_instance.subcat_name)
        self.manager.transition.direction = "left"
        self.manager.current = "Subcategory"

    def on_back_pressed(self):
        # clear subcategory buttons
        self.ids.subcat_btns_container.clear_widgets()

    def on_leave(self):
        # clear subcategory buttons
        # self.ids.subcat_btns_container.clear_widgets()
        pass


class SubcategoryPage(Screen):
    subcategories = {}
    def on_pre_enter(self):
        self.cat = self.manager.category_tracker[0]
        self.subcat = self.manager.category_tracker[1].capitalize()
        if self.subcat not in self.subcategories.keys():
            self.subcategories[self.subcat] = self.CarouselMaker(self.cat, self.subcat)

        self.ids.carousel_container.add_widget(self.subcategories[self.subcat])
        self.ids.carousel_container.bg = "{}/{}-bg.jpg".format(self.cat, self.cat)

    def on_back_pressed(self):
        self.manager.category_tracker.pop()
        self.ids.carousel_container.clear_widgets()

    def CarouselMaker(self, category:str,subcategory:str):
        conn = sqlite3.connect('Information.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM Information WHERE Category = \"" + category + "\" AND Subcategory = \"" + subcategory +"\"")
        listofall = curs.fetchall()
        conn.close()

        caros = Carousel(direction = "right")
        for i in listofall:
            imagesrc = i[3]
            sampbis = i[4]
            sampeng = i[5]
            container = RelativeLayout(orientation = "vertical", size_hint = (.8, .8),
            pos_hint = {'center_x': .5, 'center_y': .5})
            image = Image(source=imagesrc)
            sentenceBtn = sentenceButton(sampeng, sampbis)

            container.add_widget(image)
            container.add_widget(sentenceBtn)
            caros.add_widget(container)

        return caros


class SubcategoryButton(MDIconButton):
    def __init__(self, subcat_name, **kwargs):
        super().__init__(**kwargs)
        self.subcat_name = subcat_name
        self.user_font_size = "180dp"


class sentenceButton(Button):
    def __init__(self,sampeng:str,sampbis:str, **kwargs):
        super().__init__(**kwargs)
        self.__sampeng = sampeng
        self.__sampbis = sampbis
        # self.text = "Sampol nga tudling-pulong\n(sample sentences)"
        self.text = ""
        self.background_normal = ''
        self.background_color = 0, 0, 0, 0
        self.font_name = "Mont"
        
    def on_release(self):
        dialog = MDDialog(
            title = "Sampol nga tudling-pulong\n(sample sentences)",
            text = ("Bisaya : " + self.__sampbis +"\n" + "English: " + self.__sampeng),
            size_hint = (0.8, None),
            pos_hint = {"center_x": .5, "center_y": .5}
        )
        dialog.open()



class BisprendApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette= "Blue"
        self.theme_cls.primary_hue= "A700"
        self.theme_cls.accent_palette = "LightGreen"
        self.theme_cls.accent_hue = "A700"
        # self.root = Builder.load_file("bisprend.kv")

#Registering Font
LabelBase.register(name="Mont",
    fn_regular= "font/Mont-ExtraLightDemo.otf", 
    fn_bold = "font/Mont-HeavyDEMO.otf"
)

if __name__ == '__main__':
    BisprendApp().run()