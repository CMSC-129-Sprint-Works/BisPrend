from kivymd.app import MDApp

from kivy.lang import Builder
from kivy.core.text import LabelBase
#from kivy.properties import ObjectProperty
from kivy.config import Config

#kivy uix
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

#kivymd
from kivymd.uix.label import MDLabel
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.card import MDCard

from kivy.clock import Clock
from user import User
import quiz


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

# class BalayPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class PamilyaPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class ResibidorPage (Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class KomidorPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class Kan_ananPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class KatulgananPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class KasilyasPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)

# class SkuylahanPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class ClassroomPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class NumeroPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class ClinicPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class LibPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)
# class CanteenPage(Screen):
#     def on_enter(self):
#         self.manager.updateTracker(self.name)

class TindahanPage(Screen):
    def on_enter(self):
        self.manager.updateTracker(self.name)
class PagkaonPage(Screen):
    def on_enter(self):
        self.manager.updateTracker(self.name)
class SaninaPage(Screen):
    def on_enter(self):
        self.manager.updateTracker(self.name)
class KwartaPage(Screen):
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