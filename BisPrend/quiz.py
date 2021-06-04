import random
import sqlite3
import time
import math

from kivy.clock import Clock
from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivymd.uix.button import MDRectangleFlatButton, MDTextButton
from kivymd.uix.dialog import MDDialog


class QuizPage(Screen):
    score = 0
    cat = ''
    subcat = ''
    quiz_items = {}
    num_of_items = 0
    item_num = 0
    perfect_score = 0
    passing_score = 0

    def __init__(self, cat: str, subcat: str, **kwargs):
        super().__init__(**kwargs)
        self.cat = cat.lower()
        self.subcat = subcat.lower()
        self.quiz_items = {}
        self.item_num = 0
        self.loadDatabase()
        self.setBackground()
        self.score_board = ScoreBoard()
        self.num_of_items = self.countItems(self.quiz_items)
        self.perfect_score = self.countHighestPossibleScore(self.quiz_items)
        self.passing_score = math.floor(self.perfect_score*.75)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        if self.countItems(self.quiz_items) < self.num_of_items:
            self.loadDatabase()
        self.ids.quiz_manager.transition.direction = "left"
        self.ids.quiz_manager.current = "menu"

    def countItems(self, q_items):
        count = 0
        for key in q_items.keys():
            count += len(q_items[key])
        return count
    
    def countHighestPossibleScore(self, q_items):
        count = 0
        for key in q_items:
            if key == "mat":
                count += (len(q_items[key]) * 5)
            else:
                count += len(q_items[key])
        return count

    def setBackground(self):
        self.ids.background.bg = "{}/{}-bg.jpg".format(self.cat, self.cat)

    def loadDatabase(self):
        # fetch quiz data from the quiz database (quiz.db)
        conn = sqlite3.connect('quiz.db')
        curs = conn.cursor()
        curs.execute("SELECT * FROM multiple_choice WHERE subcategory = :cat", {'cat': self.subcat})
        mtc = curs.fetchall()
        curs.execute("SELECT * FROM true_or_false WHERE subcategory = :cat", {'cat': self.subcat})
        tof = curs.fetchall()
        curs.execute("SELECT * FROM fill_in_the_blank WHERE subcategory = :cat", {'cat': self.subcat})
        fitb = curs.fetchall()
        curs.execute("SELECT * FROM matching_type WHERE subcategory = :cat", {'cat': self.subcat})
        mat = curs.fetchall()
        conn.close()
        # add the fetched items into the quiz items and types
        if mtc:
            self.quiz_items['mtc'] = mtc
        if tof:
            self.quiz_items['tof'] = tof
        if fitb:
            self.quiz_items['fitb'] = fitb
        if mat:
            self.quiz_items['mat'] = mat
        print("Items: " + str(self.quiz_items))

    def loadQuizItems(self):
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
                self.loadMTC(q_item)
            elif q_type == "tof":
                self.loadTOF(q_item)
            elif q_type == "fitb":
                self.loadFITB(q_item)
            elif q_type == "mat":
                self.loadMAT(q_item)
            self.showScoreBoard()
        else:
            # final result
            self.removeScoreBoard()
            self.ids.quiz_manager.transition.direction = "left"
            self.ids.quiz_manager.current = "final-result"

    def loadMTC(self, item):
        print("\nMode: Multiple Choice")
        self.ids.quiz_manager.get_screen("multiple-choice").loadData(item)
        self.ids.quiz_manager.get_screen("multiple-choice").loadWidgets()
        self.ids.quiz_manager.transition.direction = "left"
        self.ids.quiz_manager.current = "multiple-choice"

    def loadTOF(self, item):
        print("\nMode: True or False")
        self.ids.quiz_manager.get_screen("true-or-false").loadData(item)
        self.ids.quiz_manager.get_screen("true-or-false").loadWidgets()
        self.ids.quiz_manager.transition.direction = "left"
        self.ids.quiz_manager.current = "true-or-false"

    def loadFITB(self, item):
        print("\nMode: Fill in the Blanks")
        self.ids.quiz_manager.get_screen("fill-in-the-blank").loadData(item)
        self.ids.quiz_manager.get_screen("fill-in-the-blank").loadWidgets()
        self.ids.quiz_manager.transition.direction = "left"
        self.ids.quiz_manager.current = "fill-in-the-blank"

    def loadMAT(self, item):
        print("\nMode: Matching Type")
        self.ids.quiz_manager.get_screen("matching-type").loadData(item)
        self.ids.quiz_manager.get_screen("matching-type").loadWidgets()
        self.ids.quiz_manager.transition.direction = "left"
        self.ids.quiz_manager.current = "matching-type"

    def showScoreBoard(self):
        if not self.ids.score_board.children:
            self.ids.score_board.add_widget(self.score_board)
            # print(self.ids.score_board.children)
    def removeScoreBoard(self):
        self.ids.score_board.remove_widget(self.score_board)
    def updateScoreBoard(self):
        print("Update ScoreBoard")
        self.item_num += 1
        self.score_board.ids.question_num.text = "{}/{}".format(self.item_num, self.num_of_items)
        self.score_board.ids.score.text = str(self.score)
    def resetScoreBoardData(self):
        self.score = 0
        self.item_num = -1
        self.updateScoreBoard()

    def showPauseDialog(self):
        self.pause_dialog = QuizPauseDialog()
        self.pause_dialog.ids.exit_btn.bind(on_release = self.on_exit_quiz)
        self.pause_dialog.open()
    
    def updateScore(self, points):
        self.score += points

    def on_exit_quiz(self, exit_btn_instance):
        print("Exit Quiz")
        self.removeScoreBoard()
        self.ids.quiz_manager.transition.direction = "right"
        self.ids.quiz_manager.current = "menu"
        self.resetScoreBoardData()
        self.loadDatabase() #reload the database so it will reset to beginning after exiting

    def on_leave(self):
        self.resetScoreBoardData()


class MultipleChoice(Screen):
    source = "quiz/"
    entry = ""
    correct_answer = ""
    selected_answer = ""
    choices = []

    check_btn = None
    instruction_lbl = None

    def on_enter(self):
        self.manager.parent.parent.updateScoreBoard()

    def loadData(self, item):
        # self.source = "{}/{}/".format(item[3], item[4])
        self.entry = item[0].strip()
        self.correct_answer = item[2].strip()
        self.choices = item[1].split(",")
        self.choices.append(self.correct_answer)
        random.shuffle(self.choices)

    def loadWidgets(self):
        self.ids.entry.source = self.source + self.entry
        self.ids.choice_1.text = self.choices[0].strip()
        self.ids.choice_2.text = self.choices[1].strip()
        self.ids.choice_3.text = self.choices[2].strip()
        self.ids.choice_4.text = self.choices[3].strip()
        self.check_btn = CheckBtn()
        self.check_btn.bind(on_release = self.on_check_release)
        self.instruction_lbl = Instruction(text="[b]DAGHANG KAPILIAN[/b]. Pilia ang pulong nga maghulagway sa imahe.\n[b]MULTIPLE CHOICE[/b]. Choose the word that best describes the image.")
        self.ids.check_btn.add_widget(self.instruction_lbl)

    def resetWidgets(self):
        self.ids.entry.source = ""
        self.ids.choice_1.state = 'normal'
        self.ids.choice_2.state = 'normal'
        self.ids.choice_3.state = 'normal'
        self.ids.choice_4.state = 'normal'
        if self.ids.check_btn.children:
            self.ids.check_btn.clear_widgets()

    def on_choice_toggle(self, choice_btn):
        '''
        Updates the selected answer.
        Adds a check button if a choice is selected (down).
        Removes check button if no choice is selected (choices are in normal state).
        '''
        if choice_btn.state == "down":
            self.selected_answer = choice_btn.text
            self.ids.check_btn.remove_widget(self.instruction_lbl)
            self.ids.check_btn.add_widget(self.check_btn)
        else:
            self.selected_answer = ""
            self.ids.check_btn.remove_widget(self.check_btn)
        print("My answer is: " + self.selected_answer)

    def on_check_release(self, check_btn_instance):
        result = self.checkAnswer()
        if result == "Correct":
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#00FF00]SAKTO[/color][/b]"
            check_btn_instance.result_dialog.ids.description.text = "+1 puntos"
        else:
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#FF0000]SAYOP[/color][/b]"
            check_btn_instance.result_dialog.ids.description.text = "Ang sakto nga tubag\nkay [i]{}[/i].".format(self.correct_answer)
        
        check_btn_instance.result_dialog.copyCurrentScreen(self)
        check_btn_instance.result_dialog.open()

    def checkAnswer(self):
        if self.selected_answer == self.correct_answer:
            self.manager.parent.parent.updateScore(1)
            return "Correct"
        else:
            return "Incorrect"

    def goToNextItem(self):
        self.resetWidgets()
        self.manager.parent.parent.loadQuizItems()

    def on_leave(self):
        self.resetWidgets()


class TrueOrFalse(Screen):
    source = "quiz/"
    entry = ""
    entry_name = ""
    correct_answer = ""
    selected_answer = ""

    check_btn = None
    instruction_lbl = None

    def on_enter(self):
        self.manager.parent.parent.updateScoreBoard()

    def loadData(self, item):
        # self.source = "{}/{}/".format(item[3], item[4])
        self.entry = item[0].strip()
        self.entry_name = item[1].strip()
        self.correct_answer = item[2].strip()

    def loadWidgets(self):
        self.ids.entry.source = self.source + self.entry
        self.ids.entry_name.text = self.entry_name
        self.check_btn = CheckBtn()
        self.check_btn.bind(on_release = self.on_check_release)
        self.instruction_lbl = Instruction(text="[b]SAKTO O SAYOP[/b]. Pilia ang [i]Sakto[/i] kung ang pulong kay naghulagway sa imahe, [i]Sayop[/i] kung dili .\n[b]TRUE OR FALSE[/b]. Choose [i]Sakto[/i] if the word describes the image, otherwise, [i]Sayop[/i].")
        self.ids.check_btn.add_widget(self.instruction_lbl)

    def resetWidgets(self):
        self.ids.entry.source = ""
        self.ids.entry_name.text = ""
        self.ids.choice_1.state = 'normal'
        self.ids.choice_2.state = 'normal'
        if self.ids.check_btn.children:
            self.ids.check_btn.clear_widgets()

    def on_check_release(self, check_btn_instance):
        result = self.checkAnswer()
        if result == "Correct":
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#00FF00]SAKTO[/color][/b]"
            check_btn_instance.result_dialog.ids.description.text = "+1 puntos"
        else:
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#FF0000]SAYOP[/color][/b]"
            check_btn_instance.result_dialog.ids.description.text = "Ang sakto nga tubag\nkay [i]{}[/i].".format(self.correct_answer)
        check_btn_instance.result_dialog.copyCurrentScreen(self)
        check_btn_instance.result_dialog.open()

    def on_choice_toggle(self, choice_btn):
        '''
        Updates the selected answer.
        Adds a check button if a choice is selected (down).
        Removes check button if no choice is selected (choices are in normal state).
        '''
        if choice_btn.state == "down":
            self.selected_answer = choice_btn.text
            self.ids.check_btn.remove_widget(self.instruction_lbl)
            self.ids.check_btn.add_widget(self.check_btn)
        else:
            self.selected_answer = ""
            self.ids.check_btn.remove_widget(self.check_btn)
        print("My answer is: " + self.selected_answer)

    def checkAnswer(self):
        if self.selected_answer == self.correct_answer:
            self.manager.parent.parent.updateScore(1)
            return "Correct"
        else:
            return "Incorrect"

    def goToNextItem(self):
        self.resetWidgets()
        self.manager.parent.parent.loadQuizItems()

    def on_leave(self):
        self.resetWidgets()


class FillInTheBlank(Screen):
    source = "quiz/"
    entry = ""
    entry_name = ""
    correct_answer = ""
    selected_answer = ""
    choices = []
    entry_chars = {}

    check_btn = None
    instruction_lbl = None

    def on_enter(self):
        self.manager.parent.parent.updateScoreBoard()

    def initEntryChars(self):
        self.entry_chars = {}
        for i in range(len(self.entry_name)):
            self.entry_chars[i] = self.entry_name[i]

    def loadData(self, item):
        # self.source = "{}/{}/".format(item[4], item[5])
        self.entry = item[0].strip()
        self.entry_name = item[1].strip()
        self.selected_answer = self.entry_name #the selected answer is initially the entry_name which has blanks (_)
        self.correct_answer = item[3].strip()
        self.choices = item[2].split(",")
        random.shuffle(self.choices)
        self.initEntryChars()

    def loadEntryNameDisplay(self):
        entry_text = ""
        for char in self.entry_chars.values():
            entry_text += char + " "
        self.ids.entry_name.text = entry_text.strip()

    def loadWidgets(self):
        self.ids.entry.source = self.source + self.entry
        self.ids.choice_1.text = self.choices[0].strip()
        self.ids.choice_2.text = self.choices[1].strip()
        self.ids.choice_3.text = self.choices[2].strip()
        self.ids.choice_4.text = self.choices[3].strip()
        self.ids.choice_5.text = self.choices[4].strip()
        self.ids.choice_6.text = self.choices[5].strip()
        self.check_btn = CheckBtn()
        self.check_btn.bind(on_release = self.on_check_release)
        self.instruction_lbl = Instruction(text="[b]SUDLI ANG BLANGKO[/b]. Pilia ang mga letra nga mokompleto sa pulong nga naghulagway sa imahe.\n[b]FILL IN THE BLANKS[/b]. Select letters to complete the word that describes the image.")
        self.ids.check_btn.add_widget(self.instruction_lbl)
        self.loadEntryNameDisplay()

    def resetWidgets(self):
        self.ids.entry.source = ""
        self.ids.entry_name.text = ""
        self.ids.choice_1.state = 'normal'
        self.ids.choice_2.state = 'normal'
        self.ids.choice_3.state = 'normal'
        self.ids.choice_4.state = 'normal'
        self.ids.choice_5.state = 'normal'
        self.ids.choice_6.state = 'normal'
        if self.ids.check_btn.children:
            self.ids.check_btn.clear_widgets()

    def on_choice_toggle(self, choice_btn):
        '''
        Updates the selected answer.
        Adds a check button if a choice is selected (down).
        Removes check button if no choice is selected (choices are in normal state).
        '''
        if choice_btn.state == "down":
            if self.answerIsComplete():
                choice_btn.state = "normal"
            else:
                self.addToEntryName(choice_btn)
                self.addToEntryChars(choice_btn)
        else:
            self.removeFromEntryChars(choice_btn)
            self.removeFromEntryName(choice_btn)
        
        if self.answerIsComplete() and self.check_btn not in self.ids.check_btn.children:
            self.ids.check_btn.remove_widget(self.instruction_lbl)
            self.ids.check_btn.add_widget(self.check_btn)
        elif not self.answerIsComplete() and self.check_btn in self.ids.check_btn.children:
            self.ids.check_btn.remove_widget(self.check_btn)
        print("My answer is: " + self.selected_answer)

    def on_check_release(self, check_btn_instance):
        result = self.checkAnswer()
        if result == "Correct":
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#00FF00]SAKTO[/color][/b]"
            check_btn_instance.result_dialog.ids.description.text = "+1 puntos"
        else:
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#FF0000]SAYOP[/color][/b]"
            check_btn_instance.result_dialog.ids.description.text = "Ang sakto nga tubag\nkay [i]{}[/i].".format(self.correct_answer)
        
        check_btn_instance.result_dialog.copyCurrentScreen(self)
        check_btn_instance.result_dialog.open()

    def addToEntryName(self, letter_btn):
        '''
        Add letter to entry_name's blank and automatically updates selected_answer
        '''
        letter_btn.index = self.entry_name.find("_")
        self.entry_name = self.entry_name.replace("_", letter_btn.text, 1)
        self.selected_answer = self.entry_name
    
    def removeFromEntryName(self, letter_btn):
        '''
        Remove letter from its occupied blank and automatically updates selected_answer
        '''
        if letter_btn.index >= 0:
            self.entry_name = self.entry_name[:letter_btn.index] + "_" + self.entry_name[letter_btn.index+1:]
            self.selected_answer = self.entry_name
            letter_btn.index = -1
    
    def addToEntryChars(self, letter_btn):
        self.entry_chars[letter_btn.index] = "[u]{}[/u]".format(letter_btn.text)
        self.loadEntryNameDisplay() #updates the display on screen
    
    def removeFromEntryChars(self, letter_btn):
        if letter_btn.index >= 0:
            self.entry_chars[letter_btn.index] = "_"
            self.loadEntryNameDisplay() #updates the display on screen

    def answerIsComplete(self):
        if "_" in self.selected_answer:
            return False
        else:
            return True

    def checkAnswer(self):
        if self.selected_answer == self.correct_answer:
            self.manager.parent.parent.updateScore(1)
            return "Correct"
        else:
            return "Incorrect"

    def goToNextItem(self):
        self.resetWidgets()
        self.manager.parent.parent.loadQuizItems()

    def on_leave(self):
        self.resetWidgets()


class MatchingType(Screen):
    source = "quiz/" #source of the image
    entries = {}
    entry_names = []
    entry_images = []
    selected_answer = {}

    check_btn = None
    instruction_lbl = None

    def on_enter(self):
        self.manager.parent.parent.updateScoreBoard()

    def initEntries(self, db_entries):
        # reset entries
        self.entries = {}
        self.entry_names = []
        self.entry_images = []
        self.selected_answer = {}
        # load entries
        temp_entries = db_entries.split(";")
        for entry in temp_entries:
            temp_entry = entry.split(",")
            self.entries[temp_entry[0].strip()] = temp_entry[1].strip()
            self.entry_names.append(temp_entry[0].strip())
            self.entry_images.append(temp_entry[1].strip())
        print("Entries:", str(self.entries))
        print("Entry Names:", str(self.entry_names))
        print("Entry Images:", str(self.entry_images))

    def loadData(self, item):
        # self.source = "{}/{}/".format(item[1], item[2])
        self.initEntries(item[0])
        random.shuffle(self.entry_names)
        random.shuffle(self.entry_images)

    def loadWidgets(self):
        self.ids.entry_name_1.text = self.entry_names[0]
        self.ids.entry_name_2.text = self.entry_names[1]
        self.ids.entry_name_3.text = self.entry_names[2]
        self.ids.entry_name_4.text = self.entry_names[3]
        self.ids.entry_name_5.text = self.entry_names[4]
        self.ids.entry_img_1.source = self.source + self.entry_images[0]
        self.ids.entry_img_2.source = self.source + self.entry_images[1]
        self.ids.entry_img_3.source = self.source + self.entry_images[2]
        self.ids.entry_img_4.source = self.source + self.entry_images[3]
        self.ids.entry_img_5.source = self.source + self.entry_images[4]
        self.check_btn = CheckBtn()
        self.check_btn.bind(on_release = self.on_check_release)
        self.instruction_lbl = Instruction(text="[b]PAGTUKMA[/b]. Pagdibuho ug linya para masumpay ang pulong sa iyang sakto nga imahe.\n[b]MATCHING TYPE[/b]. Draw a line to connect each word with their corresponding image.")
        self.ids.check_btn.add_widget(self.instruction_lbl)

    def resetWidgets(self):
        self.ids.entry_name_1.text = ""
        self.ids.entry_name_2.text = ""
        self.ids.entry_name_3.text = ""
        self.ids.entry_name_4.text = ""
        self.ids.entry_name_5.text = ""
        self.ids.entry_img_1.source = ""
        self.ids.entry_img_2.source = ""
        self.ids.entry_img_3.source = ""
        self.ids.entry_img_4.source = ""
        self.ids.entry_img_5.source = ""
        if self.ids.check_btn.children:
            self.ids.check_btn.clear_widgets()
        for child in self.ids.mat_canvas.children:
            if type(child) is MATBtnNumber or type(child) is MATBtnLetter:
                child.reset()

    def addToSelectedAnswer(self, name, image):
        self.selected_answer[name] = image
        if len(self.selected_answer) == len(self.entries):
            self.ids.check_btn.remove_widget(self.instruction_lbl)
            self.ids.check_btn.add_widget(self.check_btn)
        print("Answer: ", str(self.selected_answer))
    
    def removeFromSelectedAnswer(self, name):
        self.selected_answer.pop(name)
        if self.check_btn in self.ids.check_btn.children:
            self.ids.check_btn.remove_widget(self.check_btn)
        print("Answer: ", str(self.selected_answer))

    def on_check_release(self, check_btn_instance):
        points = self.checkAnswer()
        if points:
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#00FF00]{} SAKTO[/color][/b]".format(points)
        else:
            check_btn_instance.result_dialog.ids.result.text = "[b][color=#FF0000]0 SAYOP[/color][/b]"
        check_btn_instance.result_dialog.ids.description.text = "+{} puntos(s)".format(points)
        
        check_btn_instance.result_dialog.copyCurrentScreen(self)
        check_btn_instance.result_dialog.open()

    def checkAnswer(self):
        points = 0
        for entry_name in self.selected_answer.keys():
            if self.selected_answer[entry_name] == self.entries[entry_name]:
                points += 1
        self.manager.parent.parent.updateScore(points)
        return points

    def goToNextItem(self):
        self.resetWidgets()
        self.manager.parent.parent.loadQuizItems()

    def on_leave(self):
        self.resetWidgets()


class Menu(Screen):
    def on_exit_pressed(self):
        self.manager.parent.parent.manager.get_screen("Subcategory").on_back_pressed()
        self.manager.parent.parent.manager.transition.direction = "right"
        self.manager.parent.parent.manager.current = "Category"

class BlankScreen(Screen):
    pass

class FinalResult(Screen):
    def on_pre_enter(self, *args):
        if self.manager.parent.parent.score >= self.manager.parent.parent.passing_score:
            self.ids.result.text = "Nakapasar ka sa pasulit. Pwede na ka mopadayun sa sunod nga kategoriya.\nYou passed the quiz. You can now proceed to the next category."
            cat = self.manager.parent.parent.cat
            subcat = self.manager.parent.parent.subcat
            self.manager.parent.parent.manager.get_screen("Category").unlockSubcatButton(cat, subcat)
        else:
            score_needed = self.manager.parent.parent.passing_score
            self.ids.result.text = """Nakahuman ka sa pasulit. Kailangan ka ug {} puntos para makasulod sa sunod nga kategoriya.\nYou completed the quiz. You need at least {} point(s) to unlock a new category.
            """.format(score_needed,score_needed)
    
    def on_back_pressed(self):
        self.manager.parent.parent.manager.get_screen("Subcategory").on_back_pressed()
        self.manager.parent.parent.manager.transition.direction = "right"
        self.manager.parent.parent.manager.current = "Category"
        self.manager.current = 'menu' #reset to menu screen


# LAYOUTS
class ScoreBoard(RelativeLayout):
    pass

class MATcanvas(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_point = None

    def updateStartPoint(self, point):
        self.start_point = point

    def resetStartPoint(self):
        self.start_point = None


# POPUP/DIALOG
class QuizPauseDialog(MDDialog):
    pass

class CheckResultDialog(MDDialog):
    def on_open(self):
        self.delay()
        self.dismiss()

    def delay(self):
        t1 = time.time()
        t2 = t1 + 1.5
        while t1 <= t2:
            t1 = time.time()

    def copyCurrentScreen(self, current_screen):
        self.current_screen = current_screen

    def on_dismiss(self):
        self.current_screen.manager.current = "blank-screen"
        self.current_screen.goToNextItem()


# LABEL
class Instruction(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.markup = True
        self.color = 0,0,0,1
        self.text_size = self.size
        self.halign = 'center'
        self.bind(
            size = lambda *x: self.setter('text_size')(self, (self.width, None)),
            # texture_size=lambda *x: self.setter('height')(self, self.texture_size[1])
        )


# BUTTONS
class ChoiceToggleBtn(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.group = "choices"
        self.size_hint = (.8,.2)
        self.pos_hint = {"center_x": .5}

class FITBbutton(ToggleButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.index = -1

class CheckBtn(MDTextButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markup = True
        self.text = "[b][u]SUMITER ANG TUBAG[/u][/b]"
        self.pos_hint = {"center_x": .5, "center_y": .5}
        self.result_dialog = CheckResultDialog()

class MATBtnNumber(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = "20dp", "20dp"
        self.type = "number"
        self.paired = False
        self.pair = None
        self.line = None

    def setLine(self, line):
        self.line = line

    def getLinePoints(self, line_points):
        self.line_points = line_points

    def on_touch_down(self, touch):
        self.x1, self.y1 = self.pos
        self.x2, self.y2 = self.pos[0]+self.size[0], self.pos[1]+self.size[1]
        if self.x1 < touch.x < self.x2 and self.y1 < touch.y < self.y2:
            if self.paired:
                self.clearHighlight()
                self.line = None
                self.pair.clearHighlight()
                self.pair.line = None
                self.unpair()
            self.line_x1, self.line_y1 = (self.x1+self.x2)/2, (self.y1+self.y2)/2
            with self.canvas.after:
                Color(0, 0, 1)
                self.point = Rectangle(pos=self.pos, size=self.size)
                touch.ud['line'] = Line(points=(self.line_x1, self.line_y1, self.line_x1, self.line_y1), width=2)
            self.bind(size = self.updatePoint, pos = self.updatePoint)
            self.parent.updateStartPoint(self)

    def on_touch_up(self, touch):
        if self.parent.start_point and self.x1 < touch.x < self.x2 and self.y1 < touch.y < self.y2:
            if self.parent.start_point.type != self.type:
                if self.paired:
                    if self.pair != self.parent.start_point:
                        self.pair.clearHighlight()
                        self.pair.line = None
                    self.clearHighlight()
                    self.line = None
                    self.unpair()
                self.pair = self.parent.start_point
                self.paired = True
                self.pair.pair = self
                self.pair.paired = True
                self.getLinePoints(self.pair.line_points)
                with self.canvas.after:
                    Color(0, 0, 1)
                    self.point = Rectangle(pos=self.pos, size=self.size)
                    self.line = Line(points = self.line_points, width = 2)
                self.bind(size = self.updatePoint, pos = self.updatePoint)
                self.pair.canvas.after.children.pop()
                self.pair.canvas.after.children.pop()
                print("valid in", self.text)
                if self.type == "number":
                    ans_name = self.answer.strip()
                    ans_img = str(self.pair.answer).split("/")[-1]
                    self.parent.parent.parent.addToSelectedAnswer(ans_name, ans_img)
                else:
                    ans_name = self.pair.answer.strip()
                    ans_img = str(self.answer).split("/")[-1]
                    self.parent.parent.parent.addToSelectedAnswer(ans_name, ans_img)
            else:
                print("Invalid in", self.text)
                self.parent.start_point.clearHighlight()
            # print(self.type, self.parent.start_point.type)
            self.parent.resetStartPoint()

    def updatePoint(self, *args):
        self.point.size = self.size
        self.point.pos = self.pos
        # for the line
        if self.line and self.paired:
            self.x1, self.y1 = self.pair.pos
            self.x2, self.y2 = self.pair.pos[0]+self.pair.size[0], self.pair.pos[1]+self.pair.size[1]
            self.line_x1, self.line_y1 = (self.x1+self.x2)/2, (self.y1+self.y2)/2
            self.x1, self.y1 = self.pos
            self.x2, self.y2 = self.pos[0]+self.size[0], self.pos[1]+self.size[1]
            self.line_x2, self.line_y2 = (self.x1+self.x2)/2, (self.y1+self.y2)/2
            self.line.points = self.line_x1, self.line_y1, self.line_x2, self.line_y2

    def on_touch_move(self, touch):
        if self.parent.start_point:
            x1, y1 = self.parent.start_point.pos
            x2, y2 = x1+self.parent.start_point.size[0], y1+self.parent.start_point.size[1]
            self.parent.start_point.line_x1, self.parent.start_point.line_y1 = (x1+x2)/2, (y1+y2)/2
            line_x1, line_y1 = self.parent.start_point.line_x1, self.parent.start_point.line_y1
            self.line_x2, self.line_y2 = touch.x, touch.y
            touch.ud['line'].points = [line_x1, line_y1, self.line_x2, self.line_y2]
            self.getLinePoints(touch.ud['line'].points)

    def clearHighlight(self):
        self.canvas.after.clear()
        print("Cleared", self.text)

    def unpair(self):
        if self.type == "number":
            self.parent.parent.parent.removeFromSelectedAnswer(self.answer.strip())
        else:
            self.parent.parent.parent.removeFromSelectedAnswer(self.pair.answer.strip())
        self.pair.pair = None
        self.pair.paired = False
        self.pair = None
        self.paired = False

    def reset(self):
        self.canvas.after.clear()
        self.pair = None
        self.paired = False

class MATBtnLetter(MATBtnNumber):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = None, None
        self.size = "20dp", "20dp"
        self.type = "letter"
        self.paired = False
        self.pair = None
        self.line = None

class MATLastTouch(Label):
    def on_touch_up(self, touch):
        if self.parent.start_point:
            self.parent.start_point.clearHighlight()
            self.parent.resetStartPoint()
