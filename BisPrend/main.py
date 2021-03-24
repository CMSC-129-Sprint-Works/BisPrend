
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label


Config.set('graphics', 'resizable', True)

class User:
    def __init__(self):
        self.__name = ""
        self.__progress = 0

    def registername(self, newname):
        self.__name = newname

    def updateuserprogress(self, newprog:int):
        self.__progress = newprog

    def getName(self):
        return self.__name 
        #im assuming this is for the file saving -kiev

    def getProgress(self):
        return self.__progress


class BisprendEngine(Widget):
    newPlayer = User()
    def checkProgress(self):
        pass

    # called when the button is pressed/released
    def btn(self):
        self.createUserFile()
        print(f"Name: {self.newPlayer.getName()} \nProgress: {self.newPlayer.getProgress()}")
        popup = BisprendPopup()
        popup.show_popup()

    # create user file after registration (or when the "ok"/"confirm" button is pressed/released)
    def createUserFile(self):
        userFile = open("userfile.txt", "w")
        userFile.write(self.player.text + "\n0")
        self.newPlayer.registername(self.player.text)
        userFile.close()


class BisprendPopup(FloatLayout):
    def show_popup(self):
        show = BisprendPopup()
        popupWindow = Popup(title="", content=show,
                            size_hint=(None, None), size=(200, 100))
        popupWindow.open()


class BisprendApp(App):
    def build(self):
        engine = BisprendEngine()
        return engine


#Registering Font
LabelBase.register(name="Mont",
    fn_regular= "Mont-HeavyDEMO.otf"
)

if __name__ == '__main__':
    BisprendApp().run()