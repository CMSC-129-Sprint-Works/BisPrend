from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.config import Config
from kivy.graphics import *
from kivy.uix.carousel import Carousel
from kivy.uix.image import Image

#kivy uix
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.stacklayout import StackLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout

#kivymd
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.dialog import MDDialog

from kivy.clock import Clock
from user import User
from quiz import QuizPage
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
        global newPlayer
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
        global newPlayer
        return newPlayer.getName()

    def on_balay_btn_pressed(self):
        self.manager.updateTracker("balay")
        self.manager.transition.direction = "left"
        self.manager.current = "Category"

    def on_skuylahan_btn_pressed(self):
        self.manager.updateTracker("skuylahan")
        self.manager.transition.direction = "left"
        self.manager.current = "Category"

    def on_tindahan_btn_pressed(self):
        self.manager.updateTracker("tindahan")
        self.manager.transition.direction = "left"
        self.manager.current = "Category"


class CategoryPage(Screen):
    categories = {}
    def __init__(self, **kw):
        global newPlayer
        prog = newPlayer.getProgress()
        super().__init__(**kw)
        self.bind(size = self.on_size_change)
        self.progress = {'balay': prog[0], 'skuylahan': prog[1], 'tindahan': prog[2]} #change the numbers to the values in user.xml
    
    def initSubcatButtons(self):
        for subcat in self.subcategories_list:
            btn_img_loc = "{}/buttons/{}.jpg".format(self.cat_location, subcat)
            # if unlocked
            if self.subcategories_list.index(subcat) <= self.categories[self.cat_name]['progress']:
                self.categories[self.cat_name]['buttons'].add_widget(
                    SubcategoryButton(
                        subcat_name = subcat, locked = False,
                        icon = btn_img_loc, on_release = self.on_subcat_btn_pressed
                    )
                )
            # else if locked
            else:
                self.categories[self.cat_name]['buttons'].add_widget(
                    SubcategoryButton(subcat_name = subcat, locked = True, icon = btn_img_loc)
                )
        print("Subcategory buttons initialized")
    
    def unlockSubcatButton(self, cat, curr_subcat):
        for i in range(len(self.categories[cat]['buttons'].children)-1):
            subcat = self.categories[cat]['buttons'].children[i+1]
            if subcat.subcat_name == curr_subcat:
                btn_to_unlock = self.categories[cat]['buttons'].children[i]
                break
        if btn_to_unlock.locked:
            btn_to_unlock.unlock()
            btn_to_unlock.bind(on_release = self.on_subcat_btn_pressed)

    def updatePadding(self):
        num_btns = math.floor(self.width/210)
        if num_btns:
            rem_space = self.width - (num_btns*210)
            for cat in self.categories.keys():
                self.categories[cat]['buttons'].padding = rem_space/2, "10dp"

    def on_pre_enter(self, *args):
        if not self.ids.subcat_btns_scrollview.children:
            self.cat_name = self.manager.category_tracker[0]
            self.cat_location = os.getcwd() + "/" + self.cat_name
            self.subcategories_list = [f.name for f in os.scandir(self.cat_location) if f.is_dir()]
            self.subcategories_list.remove("buttons")
            self.subcategories_list.sort()
            
            if self.cat_name not in self.categories.keys():
                self.categories[self.cat_name] = {}
                self.categories[self.cat_name]['progress'] = self.progress[self.cat_name]
                self.categories[self.cat_name]['buttons'] = SubcategoryButtonsContainer()
                self.updatePadding()
                self.initSubcatButtons()
            
            # add buttons
            self.ids.subcat_btns_scrollview.add_widget(self.categories[self.cat_name]['buttons'])
            # set background
            self.ids.subcat_btns_scrollview.bg = "{}/{}-bg.jpg".format(self.cat_name, self.cat_name)

    def on_size_change(self, *args):
        self.updatePadding()

    def on_subcat_btn_pressed(self, subcat_btn_instance):
        self.manager.updateTracker(subcat_btn_instance.subcat_name)
        self.manager.transition.direction = "left"
        self.manager.current = "Subcategory"

    def on_back_pressed(self):
        # clear subcategory buttons
        self.ids.subcat_btns_scrollview.clear_widgets()


class SubcategoryPage(Screen):
    subcategories = {}
    def on_pre_enter(self):
        if not self.ids.carousel_container.children:
            self.cat = self.manager.category_tracker[0]
            self.subcat = self.manager.category_tracker[1]
            self.quiz_name = self.subcat + "-quiz"
            if self.subcat not in self.subcategories.keys():
                self.subcategories[self.subcat] = {}
                self.subcategories[self.subcat]['carousel'] = self.CarouselMaker(self.cat, self.subcat)
                self.subcategories[self.subcat]['quiz'] = QuizPage(cat=self.cat, subcat=self.subcat, name=self.quiz_name)
                self.manager.add_widget(self.subcategories[self.subcat]['quiz'])

            self.ids.carousel_container.add_widget(self.subcategories[self.subcat]['carousel'])
            self.ids.carousel_container.bg = "{}/{}-bg.jpg".format(self.cat, self.cat)

    def on_back_pressed(self):
        self.manager.category_tracker.pop()
        self.ids.carousel_container.clear_widgets()

    def on_quiz_btn_pressed(self, *args):
        print("Take Quiz")
        self.manager.transition.direction = "left"
        self.manager.current = self.quiz_name

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
        
        quiz_portal = QuizPortal()
        quiz_portal.btn.bind(on_release = self.on_quiz_btn_pressed)
        caros.add_widget(quiz_portal)
        return caros


class SubcategoryButtonsContainer(StackLayout):
    pass


class SubcategoryButton(MDIconButton):
    def __init__(self, subcat_name: str, locked: bool, **kwargs):
        super().__init__(**kwargs)
        self.subcat_name = subcat_name
        self.user_font_size = "180dp"
        self.locked = locked
        self.lock_icon = None
        if self.locked:
            self.lock()

    def unlock(self):
        self.remove_widget(self.lock_icon)
        self.locked = False
        self.lock_icon = None

    def lock(self):
        self.lock_icon = MDIconButton(
            icon = 'lock', user_font_size = "100sp", theme_text_color = "Custom", text_color = (1,1,1,.4)
        )
        with self.lock_icon.canvas.before:
            Color(0,0,0,.6)
            self.rect = Rectangle(size = self.size, pos = self.pos)
        self.bind(size = self.updateRect, pos = self.updateRect)
        self.add_widget(self.lock_icon)

    def updateRect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos


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


class QuizPortal(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation = "vertical", size_hint = (.8, .3), pos_hint = {"center_x": .5, "center_y": .6})
        lbl = Label(text = "Well Done!", color = (0,0,0,1), font_name = "Mont", font_size = "30dp")
        self.btn = Button(text = "take quiz", size_hint = (.5, 1/3), pos_hint = {"center_x": .5})
        box.add_widget(lbl)
        box.add_widget(self.btn)
        self.add_widget(box)



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