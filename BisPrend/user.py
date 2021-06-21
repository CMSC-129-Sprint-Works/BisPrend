import xml.etree.ElementTree as ET
import re

#user dictionary
class User:
    def __init__(self):
        self.__name = ""
        self.__progress = [0,0,0]
        self.__nouser = True
        self.checkFile()

    def registername(self, newname:str):
        self.__name = newname
        self.updateUserFile()

    def updateUserProgress(self, cat:str):
        if cat == 'balay':
            self.__progress[0] += 1
        elif cat == 'skuylahan':
            self.__progress[1] += 1
        elif cat == 'tindahan':
            self.__progress[2] += 1
        self.updateUserFile()

    def getName(self):
        return self.__name

    def getProgress(self):
        return self.__progress

    def hasNoUser(self):
        return self.__nouser
    
    def checkFile(self):
        try:
            tree = ET.parse("users.xml")
            root = tree.getroot()

            for elem in root:
                subelem = elem.findall("datum")
                self.__name = subelem[0].text
                temp = subelem[1].text
                temp = temp.split(',')
                for i in range(0,len(temp)):
                    temp[i] = int(temp[i])
                self.__progress = temp

            self.__nouser = False

        except FileNotFoundError:
            self.__nouser = True
        except ET.ParseError:
            self.__nouser = True
    
    def updateUserFile(self):
        newprog = re.sub("\[|\s|\]", "", str(self.__progress))

        try:
            tree = ET.parse("users.xml")
            root = tree.getroot()

            for elem in root:
                subelem = elem.findall("datum")
                subelem[0].text = self.__name
                subelem[1].text = str(newprog)
            
            tree.write("users.xml")
            self.__nouser = False
            print("updated user file")
            
        except FileNotFoundError:
            self.__nouser = True
        except ET.ParseError:
            self.__nouser = True

    def createUserFile(self,name:str):
        self.__name = name
        self.__progress = [0,0,0]
        self.__nouser = False
        data = ET.Element("data")
        item = ET.SubElement(data,"items")
        log1 = ET.SubElement(item,"datum")
        log2 = ET.SubElement(item,"datum")
        log1.set("name","name")
        log2.set("name","progress")
        log1.text = name
        log2.text = "0,0,0"

        toET = ET.ElementTree()
        toET._setroot(data)
        toET.write("users.xml")
        print("wrote in users.xml")


    # player = User()
    # def registerUser(self):
    #     self.player.createUserFile(self.username.text)
    #     print(f"Name: {self.player.getName()} \nProgress: {self.player.getProgress()}")