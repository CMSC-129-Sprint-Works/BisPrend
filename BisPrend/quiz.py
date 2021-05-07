import sqlite3

conn = sqlite3.connect('quiz.db')
curs = conn.cursor()

curs.execute("SELECT * FROM balay_quiz")
balay_quiz_items = curs.fetchall()
print(balay_quiz_items)
conn.close()

from kivy.uix.screenmanager import Screen
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivy.graphics import *

class BalayQuiz(Screen):
    score = 0
    level = 0
    mode = ''
    item = ''
    choices = []
    correct_answer = None
    selected_answer = None
    choice_border_color = (0,0,1,1)

    def loadQuiz(self):
        print("Starting Quiz")
        #mult choice
        self.item = balay_quiz_items[self.level][0]
        self.correct_answer = balay_quiz_items[self.level][1]
        self.mode = balay_quiz_items[self.level][2]
        #true or false
        # self.item = balay_quiz_items[1][0]
        # self.correct_answer = balay_quiz_items[1][1]
        # self.mode = balay_quiz_items[1][2]
        #fill in the blanks
        # self.item = "papa.png"
        # self.correct_answer = ['a', 'p']
        # self.mode = "fill in the blank"

        self.ids.img.source = "balay/{}".format(self.item)
        self.ids.choices.clear_widgets()
        if self.mode == "multiple choice":
            self.loadMultipleChoice()
        elif self.mode == "true or false":
            self.ids.img_name.text = "Sala"
            self.loadTrueOrFalse()
            # self.loadTest()
        elif self.mode == "fill in the blank":
            self.entry_text = "_ap_"
            self.entry_text_parsed = []
            self.blanks_count = 0
            for x in self.entry_text:
                if x == '_':
                    self.blanks_count += 1
                    self.entry_text_parsed.append(str("{} "))
                else:
                    self.entry_text_parsed.append(x + " ")    
            self.entry_text_parsed[-1] = str(self.entry_text_parsed[-1]).strip()
            self.loadFillInTheBlank()

    def loadMultipleChoice(self):
        print("Mode: Multiple Choice")
        self.ids.choices.cols = 2
        #create choices buttons
        choice_1 = MDRectangleFlatButton(text = "Kuya", line_color = self.choice_border_color)
        choice_2 = MDRectangleFlatButton(text = "Lola", line_color = self.choice_border_color)
        choice_3 = MDRectangleFlatButton(text = "Ate", line_color = self.choice_border_color)
        choice_4 = MDRectangleFlatButton(text = "Papa", line_color = self.choice_border_color)
        #bind the buttons
        choice_1.bind(on_release = self.highlightToggle)
        choice_2.bind(on_release = self.highlightToggle)
        choice_3.bind(on_release = self.highlightToggle)
        choice_4.bind(on_release = self.highlightToggle)
        #add the choices buttons to the choices layout
        self.ids.choices.add_widget(choice_1)
        self.ids.choices.add_widget(choice_2)
        self.ids.choices.add_widget(choice_3)
        self.ids.choices.add_widget(choice_4)

    def loadTrueOrFalse(self):
        print("Mode: True or False")
        self.ids.choices.cols = 2
        #create choices buttons
        choice_1 = MDRectangleFlatButton(text = "true", line_color = self.choice_border_color)
        choice_2 = MDRectangleFlatButton(text = "false", line_color = self.choice_border_color)
        #bind the buttons
        choice_1.bind(on_release = self.highlightToggle)
        choice_2.bind(on_release = self.highlightToggle)
        #add the choices buttons to the choices layout
        self.ids.choices.add_widget(choice_1)
        self.ids.choices.add_widget(choice_2)

    def loadFillInTheBlank(self):
        print("Mode: Fill in the blanks")
        self.ids.choices.cols = 3
        #create choices buttons
        choice_1 = MDRectangleFlatButton(text = "a", line_color = self.choice_border_color)
        choice_2 = MDRectangleFlatButton(text = "k", line_color = self.choice_border_color)
        choice_3 = MDRectangleFlatButton(text = "l", line_color = self.choice_border_color)
        choice_4 = MDRectangleFlatButton(text = "n", line_color = self.choice_border_color)
        choice_5 = MDRectangleFlatButton(text = "y", line_color = self.choice_border_color)
        choice_6 = MDRectangleFlatButton(text = "p", line_color = self.choice_border_color)
        #bind the buttons
        choice_1.bind(on_release = self.highlightToggleForFITB)
        choice_2.bind(on_release = self.highlightToggleForFITB)
        choice_3.bind(on_release = self.highlightToggleForFITB)
        choice_4.bind(on_release = self.highlightToggleForFITB)
        choice_5.bind(on_release = self.highlightToggleForFITB)
        choice_6.bind(on_release = self.highlightToggleForFITB)
        #add the choices buttons to the choices layout
        self.ids.choices.add_widget(choice_1)
        self.ids.choices.add_widget(choice_2)
        self.ids.choices.add_widget(choice_3)
        self.ids.choices.add_widget(choice_4)
        self.ids.choices.add_widget(choice_5)
        self.ids.choices.add_widget(choice_6)

        #for fitb
        self.ids.img_name.markup = True
        # self.underline_open = "[u]"
        # self.underline_close = "[/u]"
        self.ids.img_name.font_name = "DejaVuSans.ttf"
        self.entry_text = ""
        for x in self.entry_text_parsed:
            if x.startswith("{"):
                self.entry_text += x.format("_")
            else:
                self.entry_text += x
        self.ids.img_name.text = self.entry_text #displays the entry text (with blanks)
        self.selected_answer = {} #contains {index: choice} pair i.e. the selected letters/choices and their filled blank' index

    def highlightToggleForFITB(self, choice):
        '''
        Hightlights the selected letters
        '''
        print(choice.text + " pressed ")

        if choice in self.selected_answer.values():
            # self.selected_answer.remove(choice) #removes the choice from selected answers
            index = 0
            for i in self.selected_answer:
                if self.selected_answer[i] == choice:
                    index = i
                    self.selected_answer.pop(i)
                    break
            self.updateEntry(choice, index)
            # removes the highlight of the deselected choice
            choice.text_color = (0,0,1,1)
            choice.canvas.before.children.pop()
            choice.canvas.before.children.pop()
            choice.canvas.before.children.pop()
        elif len(self.selected_answer) == self.blanks_count:
            print("All blanks filled, deselect a letter to replace with a different one")
        else:
            # self.selected_answer.append(choice) #add the choice to selected answers
            self.selected_answer.update({self.entry_text.find("_"): choice})
            self.updateEntry(choice)
            # adds highlight to the selected choice
            choice.text_color = (1,1,1,1)
            choice.canvas.before.add(Color(0,0,1,1))
            choice.canvas.before.add(Rectangle(size = choice.size, pos = choice.pos))

        choice.bind(size = self.updateHighlight, pos = self.updateHighlight)

    def updateEntry(self, choice, index=0):
        '''
        Updates the blanks in the entry text when a choice has been selected or deselected. It either writes
        the choice to a blank (selected) or removes the choice from its occupied blank (deselected).
        '''
        if choice in self.selected_answer.values():
            #selected (adds letter to the first unoccupied blank)
            temp = self.entry_text
            if len(self.selected_answer) > 1:
                ans_copy = self.selected_answer.copy()
                ans_copy.popitem()
                i = 0
                for x in sorted(ans_copy.keys()):
                    if x != list(sorted(ans_copy.keys()))[0]:
                        i += 7
                    temp = temp[:x+i] + "[u]{}[/u]".format(ans_copy[x].text) + temp[x+i+1:]
            temp = temp.replace("_", "[u]{}[/u]", 1)
            self.ids.img_name.text = temp.format(choice.text) #display the entry text label with filled blanks
            self.entry_text = self.entry_text.replace("_", choice.text, 1)
        else:
            #deselected (removes letter from its occupied blank)
            self.entry_text = self.entry_text[:index] + "_" + self.entry_text[index+1:] #replaces the deselected letter with blank "_"
            temp = self.entry_text
            if self.selected_answer:
                ans_copy = self.selected_answer.copy()
                i = 0
                for x in sorted(ans_copy.keys()):
                    if x != list(sorted(ans_copy.keys()))[0]:
                        i += 7
                    temp = temp[:x+i] + "[u]{}[/u]".format(ans_copy[x].text) + temp[x+i+1:]
            self.ids.img_name.text = temp

    def highlightToggle(self, choice):
        '''
        Hightlights the selected choice
        '''
        print(choice.text + " pressed ")
        button_highlight_color = (0,0,1,1) #Blue
        text_highlight_color = (1,1,1,1) #White
        text_normal_color = (0,0,1,1) #Blue

        if self.selected_answer is None:
            self.selected_answer = choice
            # turn on highlight
            choice.canvas.before.add(Color(rgba = button_highlight_color))
            choice.canvas.before.add(Rectangle(size = choice.size, pos = choice.pos))
            choice.text_color = text_highlight_color #highlight text color
            print("My answer is: " + self.selected_answer.text)
        else:
            if self.selected_answer.text == choice.text:
                self.selected_answer = None
                # toggle off highlight of the answer
                choice.canvas.before.children.pop() #pop the Rectangle
                choice.canvas.before.children.pop() #pop the BindTexture
                choice.canvas.before.children.pop() #pop the Color
                choice.text_color = text_normal_color #change text color to normal
            else:
                # toggle off highlight of previously selected answer/choice
                self.selected_answer.canvas.before.children.pop() #pops the Rectangle
                self.selected_answer.canvas.before.children.pop() #pops the BindTexture
                self.selected_answer.canvas.before.children.pop() #pops the Color
                self.selected_answer.text_color = text_normal_color #change text color to normal
                self.selected_answer = choice #assign the selected choice as the new selected answer
                # turn on highlight for the new selected answer
                choice.canvas.before.add(Color(rgba = button_highlight_color))
                choice.canvas.before.add(Rectangle(size = choice.size, pos = choice.pos))
                choice.text_color = text_highlight_color #highlight the new selected choice text color
                print("My answer is: " + self.selected_answer.text)
        
        choice.bind(size = self.updateHighlight, pos = self.updateHighlight)

    def updateHighlight(self, instance, value):
        '''
        Dynamically change the size and position of the highlight
        when the layout's size/pos changes
        '''
        if len(instance.canvas.before.children) > 3:
            instance.canvas.before.children[-1].size = instance.size
            instance.canvas.before.children[-1].pos = instance.pos

    def clearProgress(self):
        self.score = 0
        self.level = 0
        self.item = ''
        self.mode = ''
        self.choices = []
        self.correct_answer = None
        self.selected_answer = None
        self.ids.img_name.text = ""
        self.ids.choices.canvas.clear()
        