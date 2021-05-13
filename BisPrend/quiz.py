import sqlite3
import random
import time

from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton
# from kivymd.uix.dialog import MDDialog
from kivy.graphics import *

class QuizPage(Screen):
    score = 0
    entry = ''
    entry_name = ''
    correct_answer = ''
    choices = []
    selected_answer = None

    cat = ''
    subcat = ''
    quiz_items = {}

    pause_btn = None
    check_btn = None

    def on_pre_enter(self):
        self.pause_btn = PauseBtn()
        self.check_btn = CheckAnswerBtn()
        self.ids.quiz_sm.current = "options"
        self.loadDatabase()
        self.setBackground()

    def loadDatabase(self):
        # category and subcategory
        # self.cat =  self.manager.category_tracker[0].lower() #converted to lower case to match
        # self.subcat = self.manager.category_tracker[1].lower()
        self.cat = "balay" #for testing purpose
        self.subcat = "pamilya-timbaya" #for testing purpose
        # fetch quiz data from the quiz database (quiz.db)
        conn = sqlite3.connect('quiz.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM multiple_choice WHERE subcategory = :cat", {'cat': self.subcat})
        mtc = curs.fetchall()
        # curs.execute("SELECT * FROM true_or_false WHERE subcategory = :cat", {'cat': self.subcat})
        # tof = curs.fetchall()
        tof = []
        # curs.execute("SELECT * FROM fill_in_the_blank WHERE subcategory = :cat", {'cat': self.subcat})
        # fitb = curs.fetchall()
        fitb = []
        conn.close()
        # add the fetched items into the quiz items and types
        if mtc:
            self.quiz_items['mtc'] = mtc
        if tof:
            self.quiz_items['tof'] = tof
        if fitb:
            self.quiz_items['fitb'] = fitb
        print("\nItems: " + str(self.quiz_items))

    def loadQuiz(self):
        if self.quiz_items:
            #shuffle the quiz types and items
            temp_items = list(self.quiz_items.items())
            random.shuffle(temp_items)
            self.quiz_items = dict(temp_items)
            q_type = list(self.quiz_items.keys())[0] #first quiz type
            random.shuffle(self.quiz_items[q_type]) #shuffle the items in the q_type
            q_item = self.quiz_items[q_type].pop(0) #return and remove first quiz item of q_type

            if not self.quiz_items[q_type]:
                self.quiz_items.pop(q_type) #remove the q_type if it's now empty
            
            if q_type == "mtc":
                # self.manager.current = "multiple-choice"
                self.ids.quiz_sm.current = "multiple-choice"
                self.ids.quiz_sm.current_screen.item = q_item
                self.loadMTC()
            elif q_type == "tof":
                pass
            elif q_type == "fitb":
                pass
            self.ids.quiz_sm.transition.direction = "left"

            # pause button during quiz
            if self.pause_btn not in self.children:
                self.add_widget(self.pause_btn)
        else:
            self.ids.quiz_sm.current = "final-result"

    def loadMTC(self):
        self.ids.quiz_sm.get_screen("multiple-choice").loadEntry()
        self.ids.quiz_sm.get_screen("multiple-choice").loadChoices()

    def setBackground(self):
        if self.cat == "skuylahan":
            self.ids.content.bg = "skuylahan/school-bg.jpg"
        else:
            self.ids.content.bg = "{}/{}-bg.jpg".format(self.cat, self.cat)

    def on_leave(self):
        self.score = 0
        self.cat = ''
        self.subcat = ''
        self.quiz_items = {}
        self.pause_btn = None
        self.check_btn = None

class MultipleChoice(Screen):
    item = None
    entry = ''
    choices = []
    correct_answer = ''
    selected_answer = None

    def on_enter(self):
        print("Mode: Multiple Choice")

    def loadEntry(self):
        self.entry = self.item[0]
        self.correct_answer = self.item[2]
        self.choices = self.item[1].split(",")
        self.choices.append(self.correct_answer)
        random.shuffle(self.choices)

        cat = self.manager.parent.parent.cat
        subcat = self.manager.parent.parent.subcat

        self.ids.img_entry.source = "{}/{}/{}".format(cat, subcat, self.entry)

    def loadChoices(self):
        self.choice_1 = ChoiceToggleButton(text=self.choices[0].strip())
        self.choice_2 = ChoiceToggleButton(text=self.choices[1].strip())
        self.choice_3 = ChoiceToggleButton(text=self.choices[2].strip())
        self.choice_4 = ChoiceToggleButton(text=self.choices[3].strip())
        self.ids.choices.add_widget(self.choice_1)
        self.ids.choices.add_widget(self.choice_2)
        self.ids.choices.add_widget(self.choice_3)
        self.ids.choices.add_widget(self.choice_4)

    def checkAnswer(self):
        if self.selected_answer.text == self.correct_answer:
            self.manager.parent.parent.score += 1
            return 'Correct'
        else:
            return 'Incorrect'

    def addCheckBtn(self):
        self.add_widget(self.manager.parent.parent.check_btn)
        print("check button added")

    def removeCheckBtn(self):
        if self.manager.parent.parent.check_btn in self.children:
            self.remove_widget(self.manager.parent.parent.check_btn)
            print("check button removed")

    def resetEntry(self):
        self.item = None
        self.entry = ''
        self.choices = []
        self.correct_answer = ''
        self.selected_answer = None

    def on_pre_leave(self):
        print("leaving multiple choice")
        self.ids.choices.remove_widget(self.choice_1)
        self.ids.choices.remove_widget(self.choice_2)
        self.ids.choices.remove_widget(self.choice_3)
        self.ids.choices.remove_widget(self.choice_4)
        self.removeCheckBtn()
        self.resetEntry()

class TrueOrFalse(Screen):
    def on_enter(self):
        print("Mode: True or False")

class Options(Screen):
    def on_enter(self):
        print("Options")
        #removes the pause button
        if self.manager.parent.parent.pause_btn in self.manager.parent.parent.children:
            self.manager.parent.parent.remove_widget(self.manager.parent.parent.pause_btn)

class CheckResult(Screen):
    def on_enter(self):
        t1 = time.clock()
        t2 = t1 + 1
        while t1 <= t2:
            t1 = time.clock()
        self.manager.parent.parent.loadQuiz()

class FinalResult(Screen):
    pass

class PauseBtn(FloatLayout):
    pass

class CheckAnswerBtn(FloatLayout):
    def showResult(self):
        '''
        Displays the result in check result Screen
        '''
        # remove pause button while result is showed
        if self.parent.manager.parent.parent.pause_btn in self.parent.manager.parent.parent.children:
            self.parent.manager.parent.parent.remove_widget(self.parent.manager.parent.parent.pause_btn)
        # checks result and update score
        res = self.parent.checkAnswer()
        score = self.parent.manager.parent.parent.score
        self.parent.manager.get_screen("check-result").ids.result.text = res
        self.parent.manager.get_screen("check-result").ids.score.text = "Score: " + str(score)
        self.parent.manager.current = "check-result"

class ChoiceToggleButton(MDRectangleFlatButton):
    def on_release(self):
        print("Pressed: " + self.text)
        button_highlight_color = self.canvas.before.children[0].rgba #Blue
        text_highlight_color = (1,1,1,1) #White
        text_normal_color = self.canvas.before.children[0].rgba #Blue
        if self.parent.parent.parent.selected_answer is None:
            self.parent.parent.parent.selected_answer = self
            # turn on highlight
            self.canvas.before.add(Color(rgba = button_highlight_color))
            self.canvas.before.add(Rectangle(size = self.size, pos = self.pos))
            self.text_color = text_highlight_color #highlight text color
            print("My answer is: " + self.text)
            # add check button
            self.parent.parent.parent.addCheckBtn()
        else:
            if self.parent.parent.parent.selected_answer == self:
                self.parent.parent.parent.selected_answer = None
                # toggle off highlight
                self.canvas.before.children.pop() #pop the Rectangle
                self.canvas.before.children.pop() #pop the BindTexture
                self.canvas.before.children.pop() #pop the Color
                self.text_color = text_normal_color #change text color to normal
                # remove check button
                self.parent.parent.parent.removeCheckBtn()
            else:
                # toggle off highlight of previously selected answer/choice
                self.parent.parent.parent.selected_answer.canvas.before.children.pop()
                self.parent.parent.parent.selected_answer.canvas.before.children.pop()
                self.parent.parent.parent.selected_answer.canvas.before.children.pop()
                self.parent.parent.parent.selected_answer.text_color = text_normal_color
                self.parent.parent.parent.selected_answer = self
                # turn on highlight for the new selected answer
                self.canvas.before.add(Color(rgba = button_highlight_color))
                self.canvas.before.add(Rectangle(size = self.size, pos = self.pos))
                self.text_color = text_highlight_color #highlight the new selected choice text color
                print("My answer is: " + self.text)

        self.bind(size = self.updateHighlight, pos = self.updateHighlight)

    def updateHighlight(self, instance, value):
        '''
        Dynamically change the size and position of the highlight
        when the layout's size/pos changes
        '''
        if len(instance.canvas.before.children) > 3:
            instance.canvas.before.children[-1].size = instance.size
            instance.canvas.before.children[-1].pos = instance.pos



# class QuizPage(Screen):
#     score = 0
#     entry = ''
#     entry_name = ''
#     correct_answer = ''
#     choices = []
#     selected_answer = None
#     choice_border_color = (0,0,1,1) #color of the choices buttons' border

#     def on_enter(self):
#         self.loadDatabase()
#         self.loadQuiz()

#     def loadDatabase(self):
#         # category and subcategory
#         # self.cat =  self.manager.category_tracker[0].lower() #converted to lower case to match
#         # self.subcat = self.manager.category_tracker[1].lower()
#         self.cat = "balay"
#         self.subcat = "pamilya-timbaya"
#         # fetch quiz data from the quiz database (quiz.db)
#         conn = sqlite3.connect('quiz.db')
#         curs = conn.cursor()
#         curs.execute("SELECT * FROM multiple_choice WHERE subcategory = :cat", {'cat': self.subcat})
#         mtc = curs.fetchall()
#         # curs.execute("SELECT * FROM true_or_false WHERE subcategory = :cat", {'cat': self.subcat})
#         # tof = curs.fetchall()
#         tof = []
#         # curs.execute("SELECT * FROM fill_in_the_blank WHERE subcategory = :cat", {'cat': self.subcat})
#         # fitb = curs.fetchall()
#         fitb = []
#         conn.close()
#         # add the fetched items into the quiz items dictionary
#         self.quiz_types = ["mtc", "tof", "fitb"] #contain the quiz types
#         self.quiz_items = {'mtc': mtc, 'tof': tof, 'fitb': fitb} #contain the fetched quiz items
#         print("Items: " + str(self.quiz_items))

#     def loadQuiz(self):
#         print("Starting Quiz")
#         #set background image of the quiz
#         bg = self.cat + "-bg.jpg"
#         if self.cat == "skuylahan":
#             bg = "school-bg.jpg"
#         self.ids.content.bg = "{}/{}".format(self.cat, bg)
        
#         while(self.quiz_items):
#             random.shuffle(self.quiz_types) #shuffles the quiz types
#             q_type = self.quiz_types[0]
#             if not self.quiz_items[q_type]:
#                 # remove the first quiz type (also from the dictionary) if it's empty
#                 self.quiz_items.pop(q_type)
#                 self.quiz_types.remove(q_type)
#                 continue
            
#             random.shuffle(self.quiz_items[q_type]) #shuffles the items of the first quiz type
#             q_item = self.quiz_items[q_type].pop(0) #return and remove first quiz item
            
#             proceed = False
#             if q_type == "mtc": #if multiple choice
#                 self.loadMultipleChoice(q_item)
#             elif q_type == "tof": #if true or False
#                 pass
#             elif q_type == "fitb": #if Fill in the Blank
#                 pass

#         # if self.mode == "multiple choice":
#         #     self.loadMultipleChoice()
#         # elif self.mode == "true or false":
#         #     self.ids.img_name.text = "Sala"
#         #     self.loadTrueOrFalse()
#         #     # self.loadTest()
#         # elif self.mode == "fill in the blank":
#         #     self.entry_text = "_ap_"
#         #     self.entry_text_parsed = []
#         #     self.blanks_count = 0
#         #     for x in self.entry_text:
#         #         if x == '_':
#         #             self.blanks_count += 1
#         #             self.entry_text_parsed.append(str("{} "))
#         #         else:
#         #             self.entry_text_parsed.append(x + " ")    
#         #     self.entry_text_parsed[-1] = str(self.entry_text_parsed[-1]).strip()
#         #     self.loadFillInTheBlank()

#     def loadMultipleChoice(self, item):
#         print("Mode: Multiple Choice")
#         self.entry = item[0]
#         self.correct_answer = item[2]
#         self.choices = item[1].split(",")
#         self.choices.append(self.correct_answer)
#         random.shuffle(self.choices)
#         # set img_entry
#         self.ids.img_entry.source = "{}/{}/{}".format(self.cat, self.subcat, self.entry)
#         # set 1 column for the choices
#         self.ids.choices.cols = 1
#         #create choices buttons
#         choice_1 = MDRectangleFlatButton(text = self.choices[0], line_color = self.choice_border_color)
#         choice_2 = MDRectangleFlatButton(text = self.choices[1], line_color = self.choice_border_color)
#         choice_3 = MDRectangleFlatButton(text = self.choices[2], line_color = self.choice_border_color)
#         choice_4 = MDRectangleFlatButton(text = self.choices[3], line_color = self.choice_border_color)
#         #bind the buttons
#         choice_1.bind(on_release = self.highlightToggle)
#         choice_2.bind(on_release = self.highlightToggle)
#         choice_3.bind(on_release = self.highlightToggle)
#         choice_4.bind(on_release = self.highlightToggle)
#         #add the choices buttons to the choices layout
#         self.ids.choices.add_widget(choice_1)
#         self.ids.choices.add_widget(choice_2)
#         self.ids.choices.add_widget(choice_3)
#         self.ids.choices.add_widget(choice_4)

#         #check answer button
#         check_btn = MDTextButton(text="Check Answer")
#         check_btn.pos_hint = {'center_x': .5, 'y': .1}
#         # check_btn.bind(on_release = self.checkAnswer)

#     def loadTrueOrFalse(self):
#         print("Mode: True or False")
#         self.ids.choices.cols = 2
#         #create choices buttons
#         choice_1 = MDRectangleFlatButton(text = "true", line_color = self.choice_border_color)
#         choice_2 = MDRectangleFlatButton(text = "false", line_color = self.choice_border_color)
#         #bind the buttons
#         choice_1.bind(on_release = self.highlightToggle)
#         choice_2.bind(on_release = self.highlightToggle)
#         #add the choices buttons to the choices layout
#         self.ids.choices.add_widget(choice_1)
#         self.ids.choices.add_widget(choice_2)

#     def loadFillInTheBlank(self):
#         print("Mode: Fill in the blanks")
#         self.ids.choices.cols = 3
#         #create choices buttons
#         choice_1 = MDRectangleFlatButton(text = "a", line_color = self.choice_border_color)
#         choice_2 = MDRectangleFlatButton(text = "k", line_color = self.choice_border_color)
#         choice_3 = MDRectangleFlatButton(text = "l", line_color = self.choice_border_color)
#         choice_4 = MDRectangleFlatButton(text = "n", line_color = self.choice_border_color)
#         choice_5 = MDRectangleFlatButton(text = "y", line_color = self.choice_border_color)
#         choice_6 = MDRectangleFlatButton(text = "p", line_color = self.choice_border_color)
#         #bind the buttons
#         choice_1.bind(on_release = self.highlightToggleForFITB)
#         choice_2.bind(on_release = self.highlightToggleForFITB)
#         choice_3.bind(on_release = self.highlightToggleForFITB)
#         choice_4.bind(on_release = self.highlightToggleForFITB)
#         choice_5.bind(on_release = self.highlightToggleForFITB)
#         choice_6.bind(on_release = self.highlightToggleForFITB)
#         #add the choices buttons to the choices layout
#         self.ids.choices.add_widget(choice_1)
#         self.ids.choices.add_widget(choice_2)
#         self.ids.choices.add_widget(choice_3)
#         self.ids.choices.add_widget(choice_4)
#         self.ids.choices.add_widget(choice_5)
#         self.ids.choices.add_widget(choice_6)

#         #for fitb
#         self.ids.img_name.markup = True
#         # self.underline_open = "[u]"
#         # self.underline_close = "[/u]"
#         self.ids.img_name.font_name = "DejaVuSans.ttf"
#         self.entry_text = ""
#         for x in self.entry_text_parsed:
#             if x.startswith("{"):
#                 self.entry_text += x.format("_")
#             else:
#                 self.entry_text += x
#         self.ids.img_name.text = self.entry_text #displays the entry text (with blanks)
#         self.selected_answer = {} #contains {index: choice} pair i.e. the selected letters/choices and their filled blank' index

#     def highlightToggleForFITB(self, choice):
#         '''
#         Hightlights the selected letters
#         '''
#         print(choice.text + " pressed ")

#         if choice in self.selected_answer.values():
#             # self.selected_answer.remove(choice) #removes the choice from selected answers
#             index = 0
#             for i in self.selected_answer:
#                 if self.selected_answer[i] == choice:
#                     index = i
#                     self.selected_answer.pop(i)
#                     break
#             self.updateEntry(choice, index)
#             # removes the highlight of the deselected choice
#             choice.text_color = (0,0,1,1)
#             choice.canvas.before.children.pop()
#             choice.canvas.before.children.pop()
#             choice.canvas.before.children.pop()
#         elif len(self.selected_answer) == self.blanks_count:
#             print("All blanks filled, deselect a letter to replace with a different one")
#         else:
#             # self.selected_answer.append(choice) #add the choice to selected answers
#             self.selected_answer.update({self.entry_text.find("_"): choice})
#             self.updateEntry(choice)
#             # adds highlight to the selected choice
#             choice.text_color = (1,1,1,1)
#             choice.canvas.before.add(Color(0,0,1,1))
#             choice.canvas.before.add(Rectangle(size = choice.size, pos = choice.pos))

#         choice.bind(size = self.updateHighlight, pos = self.updateHighlight)

#     def updateEntry(self, choice, index=0):
#         '''
#         Updates the blanks in the entry text when a choice has been selected or deselected. It either writes
#         the choice to a blank (selected) or removes the choice from its occupied blank (deselected).
#         '''
#         if choice in self.selected_answer.values():
#             #selected (adds letter to the first unoccupied blank)
#             temp = self.entry_text
#             if len(self.selected_answer) > 1:
#                 ans_copy = self.selected_answer.copy()
#                 ans_copy.popitem()
#                 i = 0
#                 for x in sorted(ans_copy.keys()):
#                     if x != list(sorted(ans_copy.keys()))[0]:
#                         i += 7
#                     temp = temp[:x+i] + "[u]{}[/u]".format(ans_copy[x].text) + temp[x+i+1:]
#             temp = temp.replace("_", "[u]{}[/u]", 1)
#             self.ids.img_name.text = temp.format(choice.text) #display the entry text label with filled blanks
#             self.entry_text = self.entry_text.replace("_", choice.text, 1)
#         else:
#             #deselected (removes letter from its occupied blank)
#             self.entry_text = self.entry_text[:index] + "_" + self.entry_text[index+1:] #replaces the deselected letter with blank "_"
#             temp = self.entry_text
#             if self.selected_answer:
#                 ans_copy = self.selected_answer.copy()
#                 i = 0
#                 for x in sorted(ans_copy.keys()):
#                     if x != list(sorted(ans_copy.keys()))[0]:
#                         i += 7
#                     temp = temp[:x+i] + "[u]{}[/u]".format(ans_copy[x].text) + temp[x+i+1:]
#             self.ids.img_name.text = temp

#     def highlightToggle(self, choice):
#         '''
#         Hightlights the selected choice
#         '''
#         print(choice.text + " pressed ")
#         button_highlight_color = (0,0,1,1) #Blue
#         text_highlight_color = (1,1,1,1) #White
#         text_normal_color = (0,0,1,1) #Blue

#         if self.selected_answer is None:
#             self.selected_answer = choice
#             # turn on highlight
#             choice.canvas.before.add(Color(rgba = button_highlight_color))
#             choice.canvas.before.add(Rectangle(size = choice.size, pos = choice.pos))
#             choice.text_color = text_highlight_color #highlight text color
#             print("My answer is: " + self.selected_answer.text)
#         else:
#             if self.selected_answer.text == choice.text:
#                 self.selected_answer = None
#                 # toggle off highlight of the answer
#                 choice.canvas.before.children.pop() #pop the Rectangle
#                 choice.canvas.before.children.pop() #pop the BindTexture
#                 choice.canvas.before.children.pop() #pop the Color
#                 choice.text_color = text_normal_color #change text color to normal
#             else:
#                 # toggle off highlight of previously selected answer/choice
#                 self.selected_answer.canvas.before.children.pop() #pops the Rectangle
#                 self.selected_answer.canvas.before.children.pop() #pops the BindTexture
#                 self.selected_answer.canvas.before.children.pop() #pops the Color
#                 self.selected_answer.text_color = text_normal_color #change text color to normal
#                 self.selected_answer = choice #assign the selected choice as the new selected answer
#                 # turn on highlight for the new selected answer
#                 choice.canvas.before.add(Color(rgba = button_highlight_color))
#                 choice.canvas.before.add(Rectangle(size = choice.size, pos = choice.pos))
#                 choice.text_color = text_highlight_color #highlight the new selected choice text color
#                 print("My answer is: " + self.selected_answer.text)
        
#         choice.bind(size = self.updateHighlight, pos = self.updateHighlight)

#     def updateHighlight(self, instance, value):
#         '''
#         Dynamically change the size and position of the highlight
#         when the layout's size/pos changes
#         '''
#         if len(instance.canvas.before.children) > 3:
#             instance.canvas.before.children[-1].size = instance.size
#             instance.canvas.before.children[-1].pos = instance.pos

#     def clearProgress(self):
#         self.score = 0
#         self.entry = ''
#         self.entry_name = ''
#         self.correct_answer = ''
#         self.choices = []
#         self.selected_answer = None
#         self.ids.entry_name.text = ""
#         self.ids.choices.canvas.clear()
#         self.ids.choices.clear_widgets()
