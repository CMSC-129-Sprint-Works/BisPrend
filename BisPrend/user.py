import xml.etree.ElementTree as ET

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


    # player = User()
    # def registerUser(self):
    #     self.player.createUserFile(self.username.text)
    #     print(f"Name: {self.player.getName()} \nProgress: {self.player.getProgress()}")