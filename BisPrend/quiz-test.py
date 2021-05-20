from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from quiz import QuizPage, MultipleChoice


Builder.load_file('quiz.kv')
Builder.load_string("""
<Portal>
    name: 'portal'
    BoxLayout:
        Button:
            text: 'Quiz Portal'
            on_release:
                root.manager.current = 'quiz'
                root.manager.transition.direction = 'left'
""")

# Declare screen manager and screens
class ScrnMngr(ScreenManager):
    category_tracker = ['pamilya', 'pamilya-timbaya']

class Portal(Screen):
    pass

class QuizTestApp(MDApp):
    def build(self):
        # Create the screen manager
        sm = ScrnMngr()
        sm.add_widget(Portal())
        sm.add_widget(QuizPage())
        return sm


#Registering Font
LabelBase.register(name="Mont",
    fn_regular= "font/Mont-ExtraLightDemo.otf", 
    fn_bold = "font/Mont-HeavyDEMO.otf"
)

if __name__ == '__main__':
    QuizTestApp().run()