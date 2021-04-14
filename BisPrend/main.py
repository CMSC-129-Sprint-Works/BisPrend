
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
import xml.etree.ElementTree as ET

Config.set('graphics', 'resizable', True)

#user dictionary
class User:
    def __init__(self):
        self.__name = ""
        self.__progress = 0
        self.__nouser = True
        self.checkFile()

    def registername(self, newname:str):
        self.__name = newname

    def updateuserprogress(self, newprog:int):
        self.__progress = newprog

    def getName(self):
        return self.__name 

    def getProgress(self):
        return self.__progress

    def hasUser(self):
        return self.__nouser
    
    def checkFile(self):
        try:
            tree = ET.parse("items.xml")
            root = tree.getroot()

            for elem in root:
                subelem = elem.findall("datum")
                self.__name = subelem[0].text
                self.__progress = subelem[1].text

            self.__nouser = False

        except FileNotFoundError:
            self.__nouser = True
        except ET.ParseError:
            self.__nouser = True
    
    def createUserFile(self,name:str):
        self.__name = name
        self.__progress = 0
        self.__nouser = False
        data = ET.Element("data")
        item = ET.SubElement(data,"items")
        log1 = ET.SubElement(item,"datum")
        log2 = ET.SubElement(item,"datum")
        log1.set("name","name")
        log2.set("name","progress")
        log1.text = name
        log2.text = "0"

        toET = ET.ElementTree()
        toET._setroot(data)
        toET.write("items.xml")
        print("wrote in items.xml")

#Screens
class WindowManager(ScreenManager):
    pass

class RegWindow(Screen):
    def checkProgress(self):
        pass

    player = User()
    def registerUser(self):
        self.player.createUserFile(self.username.text)
        print(f"Name: {self.player.getName()} \nProgress: {self.player.getProgress()}")

class WelcomeWindow(Screen):
    pass

class MenuWindow(Screen):
    player_name = RegWindow.player.getName()
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