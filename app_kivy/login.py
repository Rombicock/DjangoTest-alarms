from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput


class LoginScreen(Screen):

    def __init__ (self,**kwargs):
        super().__init__(**kwargs)

        my_box1 = BoxLayout(orientation='vertical')
        box_center = BoxLayout()
        box_entry = BoxLayout(orientation='vertical')
        my_label1 = Label(text="Enter your login and password", font_size='24dp')
        login_label = Label(text='login', size_hint=(1, None), width=100, height=30)
        login_input = TextInput(size_hint=(None, None), halign='center', pos_hint={'center_x': .5}, width=150, height=30)
        password_label = Label(text='password', size_hint=(1, None), width=100, height=30)
        password_input = TextInput(size_hint=(None, None), halign='center', pos_hint={'center_x': .5}, width=150, height=30)
        login_button = Button(text="Login", size_hint=(None, None), pos_hint={'center_x': .5}, width=150, height=30)
        login_button.bind(on_press=self.changer)

        box_entry.add_widget(login_label)
        box_entry.add_widget(login_input)
        box_entry.add_widget(password_label)
        box_entry.add_widget(password_input)
        box_entry.add_widget(Label(size_hint=(1, None), width=100, height=15))
        box_entry.add_widget(login_button)

        box_center.add_widget(Label())
        box_center.add_widget(box_entry)
        box_center.add_widget(Label())

        my_box1.add_widget(my_label1)
        my_box1.add_widget(box_center)
        my_box1.add_widget(Label())
        self.add_widget(my_box1)

    def changer(self,*args):
        self.manager.current = 'screen2'

class ScreenTwo(Screen):

    def __init__(self,**kwargs):
        super (ScreenTwo,self).__init__(**kwargs)

        my_box1 = BoxLayout(orientation='vertical')
        my_label1 = Label(text="BlaBlaBla on screen 2",font_size='24dp')
        my_button1 = Button(text="Go to screen 1",size_hint_y=None)
        my_button1.bind(on_press=self.changer)
        my_box1.add_widget(my_label1)
        my_box1.add_widget(my_button1)
        self.add_widget(my_box1)

    def changer(self,*args):
        self.manager.current = 'screen1'

class TestApp(App):

        def build(self):
            my_screenmanager = ScreenManager()
            screen1 = LoginScreen(name='screen1')
            screen2 = ScreenTwo(name='screen2')
            my_screenmanager.add_widget(screen1)
            my_screenmanager.add_widget(screen2)
            return my_screenmanager

if __name__ == '__main__':
    TestApp().run()
