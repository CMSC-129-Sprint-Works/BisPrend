
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.text import LabelBase

from kivy.config import Config
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from kivy.uix.screenmanager import ScreenManager, Screen


Config.set('graphics', 'resizable', True)

#user dictionary
class User:
    def __init__(self):
        self.__name = ""
        self.__progress = 0

    # create user file after registration (or when the "ok"/"confirm" button is pressed/released)
    #def createUserFile(self):
      #  userFile = open("userfile.txt", "w")
       # userFile.write(self.player.text + "\n0")
        #self.newPlayer.registername(self.player.text)
        #userFile.close()
        #pass

    def registername(self, newname):
        self.__name = newname

    def updateuserprogress(self, newprog:int):
        self.__progress = newprog

    def getName(self):
        return self.__name 
        #im assuming this is for the file saving -kiev

    def getProgress(self):
        return self.__progress

#Screens
class WindowManager(ScreenManager):
    pass

class RegWindow(Screen):
  #  newUser = User()
   # username = any_name.ObjectProperty (None)

    #def reg(self):
     #   if self.username.text != "":
      #      newUser.registername(self.username.text)
       ##self.reset()
    
   # def reset(self):
    #    self.username.text = ""

    def checkProgress(self):
        pass

class WelcomeWindow(Screen):
 #   username = ObjectProperty(None)
    pass

KV = Builder.load_file("bisprend.kv")

class BisprendApp(App):
    def build(self):
        return KV


#Registering Font
LabelBase.register(name="Mont",
    fn_regular= "Mont-HeavyDEMO.otf"
)

if __name__ == '__main__':
    BisprendApp().run()