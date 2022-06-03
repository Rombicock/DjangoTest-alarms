from kivy.app import App
from kivy.properties import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
import requests
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.textinput import TextInput


user_id = '0'
token = '0'


class LoginScreen(Screen):

    def __init__(self, **kwargs):
        global user_id, token
        super().__init__(**kwargs)

        my_box1 = BoxLayout(orientation='vertical')
        box_center = BoxLayout()
        box_entry = BoxLayout(orientation='vertical')
        my_label1 = Label(text="Enter your login and password", font_size='24dp')
        login_label = Label(text='login', size_hint=(1, None), width=100, height=30)
        self.login_input = TextInput(size_hint=(None, None), halign='center', pos_hint={'center_x': .5}, width=150, height=30)
        password_label = Label(text='password', size_hint=(1, None), width=100, height=30)
        self.password_input = TextInput(size_hint=(None, None), halign='center', pos_hint={'center_x': .5}, width=150, height=30)
        login_button = Button(text="Login", size_hint=(None, None), pos_hint={'center_x': .5}, width=150, height=30)
        login_button.bind(on_press=self.auth_user)

        self.info_label = Label()

        box_entry.add_widget(login_label)
        box_entry.add_widget(self.login_input)
        box_entry.add_widget(password_label)
        box_entry.add_widget(self.password_input)
        box_entry.add_widget(Label(size_hint=(1, None), width=100, height=15))
        box_entry.add_widget(login_button)

        box_center.add_widget(Label())
        box_center.add_widget(box_entry)
        box_center.add_widget(Label())

        my_box1.add_widget(my_label1)
        my_box1.add_widget(box_center)
        my_box1.add_widget(self.info_label)
        self.add_widget(my_box1)

    def auth_user(self, *args):
        global user_id, token

        def clear_label(*args):
            self.info_label.text = ''

        def switching_function(*args):
            self.info_label.text = 'done!'
            loginScreenManager.switch_to(MainScreens(), direction='up')
            clear_label()

        login = self.login_input.text
        password = self.password_input.text
        try:
            auth = requests.post('http://127.0.0.1:8000/api/auth-token/',
                                 json={'username': login,
                                       'password': password
                                       })
            print(auth)
            if str(auth) == '<Response [200]>':
                token, user_id, _ = auth.json().values()
                Clock.schedule_once(switching_function, 1)
            else:
                raise Exception(str(auth))
        except:
            self.info_label.text = 'try again'
            Clock.schedule_once(clear_label, 2)


class MainScreen(Screen):
    def __init__(self, **kwargs):
        global editable_time, id
        super().__init__(**kwargs)
        self.add_widget(self.load_main_screen())
        editable_time, id = '', ''

    def load_main_screen(self):
        global main_box

        def switching_function(instance, *args):
            global editable_time, id
            id = self.store[self.buttons.index(instance)]['id']
            editable_time = requests.get(f'http://127.0.0.1:8000/api/alarm/edit/{id}/').json()['time'][:-3]
            mainScreenManager.switch_to(EditObjectScreen(), direction='left')
            panel_label.text = 'Alarm'

        self.store = requests.get('http://127.0.0.1:8000/api/alarms/',
                                  headers={'Authorization': f'Token {token}'}
                                  ).json()
        list_data = []
        for item in self.store:
            try:
                list_data.append(item['time'][:-3])
            except:
                pass

        main_box = BoxLayout(orientation='vertical')
        self.buttons = []
        for pos in range(len(list_data)):
            self.buttons.append(Button(text=list_data[pos], size_hint_y=None, height=75))
            self.buttons[pos].bind(on_press=switching_function)
            main_box.add_widget(self.buttons[pos])
        main_box.add_widget(Label())
        return main_box


class CreateObjectScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box_hor = BoxLayout(pos_hint={'center_y': 1}, size_hint_y=None, height=50)
        self.box_vert = BoxLayout(orientation='vertical')

        help_label = Label(text='enter alarm\'s time\nhours:minutes', halign='center', size_hint_y=None, height=50)
        self.hour_input = TextInput(size_hint=(None, None), width=50, height=30)
        self.minute_input = TextInput(size_hint=(None, None), width=50, height=30)
        self.submit_button = Button(text='enter', size_hint=(None, None), pos_hint={'center_x': .5},
                                    width=110, height=30, padding_y=10)
        self.submit_button.bind(on_press=self.create_screen)

        box_hor.add_widget(Label())
        box_hor.add_widget(self.hour_input)
        box_hor.add_widget(Label(text=':', size_hint=(None, None), height=25, width=10))
        box_hor.add_widget(self.minute_input)
        box_hor.add_widget(Label())

        self.box_vert.add_widget(Label(size_hint_y=.5))
        self.box_vert.add_widget(help_label)
        self.box_vert.add_widget(box_hor)
        self.box_vert.add_widget(self.submit_button)

        self.info_label = Label()
        self.box_vert.add_widget(self.info_label)
        self.add_widget(self.box_vert)

    def submit(self):
        post = requests.post('http://127.0.0.1:8000/api/alarm/create/',
                             json={'time': f'{self.hour_input.text}:{self.minute_input.text}:00',
                                   'active': 'True',
                                   'owner': user_id}
                             )
        print(post)
        if str(post) != '<Response [200]>':
            raise Exception(str(post))

    def switching_function(self, *args):
        self.info_label.text = ''
        mainScreenManager.switch_to(MainScreen(), direction='right')
        panel_label.text = 'Main screen'
        mainScreen.clear_widgets()
        mainScreen.add_widget(MainScreen().load_main_screen())

    def create_screen(self, *args):
        def clear_label(*args):
            self.info_label.text = ''

        try:
            if int(self.hour_input.text) < 24 and int(self.minute_input.text) < 60:
                self.submit()
                self.hour_input.text = ''
                self.minute_input.text = ''
                self.info_label.text = 'done!'
                Clock.schedule_once(self.switching_function, 1)
            else:
                self.info_label.text = 'enter correct time'
                Clock.schedule_once(clear_label, 2)
        except:
            self.info_label.text = 'invalid format'
            Clock.schedule_once(clear_label, 2)


class EditObjectScreen(CreateObjectScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hour_input.text = editable_time[:2]
        self.minute_input.text = editable_time[3:]
        del_button = Button(text='del', size_hint=(None, None), pos_hint={'center_x': .5},
                                    width=110, height=30, padding_y=10, color=(1, 0, 0))
        del_button.bind(on_press=self.delete)
        self.box_vert.remove_widget(self.info_label)
        self.box_vert.add_widget(del_button)
        self.box_vert.add_widget(self.info_label)

    def submit(self):
        put = requests.put(f'http://127.0.0.1:8000/api/alarm/edit/{id}/',
                             json={'time': f'{self.hour_input.text}:{self.minute_input.text}:00',
                                   'active': 'True',
                                   'owner': user_id}
                             )
        print(put)
        if str(put) != '<Response [200]>':
            raise Exception(str(put))

    def delete(self, *args):
        delete = requests.delete(f'http://127.0.0.1:8000/api/alarm/edit/{id}/')
        print(delete)
        if str(delete) != '<Response [200]>':
            raise Exception(str(delete))
        mainScreenManager.switch_to(MainScreen(), direction='right')
        panel_label.text = 'Main screen'
        mainScreen.clear_widgets()
        mainScreen.add_widget(MainScreen().load_main_screen())


class TopPanel(RelativeLayout):
    def __init__(self, **kwargs):
        global panel_label

        def switching_on_home_function(*args):
            mainScreenManager.switch_to(MainScreen(), direction='right')
            panel_label.text = 'Main screen'
            mainScreen.clear_widgets()
            mainScreen.add_widget(MainScreen().load_main_screen())

        def switching_on_create_function(*args):
            mainScreenManager.switch_to(CreateObjectScreen(), direction='left')
            panel_label.text = 'Create alarm'

        super().__init__(**kwargs)
        buttons_box = BoxLayout()
        home_button = Button(text='home', size_hint_x=None, width=50)
        home_button.bind(on_press=switching_on_home_function)
        create_alarm_button = Button(text='create alarm', size_hint_x=None, width=100, )
        create_alarm_button.bind(on_press=switching_on_create_function)
        panel_label = Label(text='Main screen')
        buttons_box.add_widget(home_button)
        buttons_box.add_widget(create_alarm_button)
        self.add_widget(panel_label)
        self.add_widget(buttons_box)


class MainScreens(Screen):
    def __init__(self):
        global mainScreenManager, mainScreen
        super().__init__()
        mainScreenManager = ScreenManager()
        main_box = BoxLayout(orientation='vertical')
        panel = TopPanel(size_hint_y=None, height=50)
        mainScreen = MainScreen(name='mainscreen')
        objectScreen = EditObjectScreen(name='objectscreen')
        createObjectScreen = CreateObjectScreen(name='createscreen')

        mainScreenManager.add_widget(mainScreen)
        mainScreenManager.add_widget(objectScreen)
        mainScreenManager.add_widget(createObjectScreen)

        main_box.add_widget(panel)
        main_box.add_widget(mainScreenManager)
        self.add_widget(main_box)



class MainApp(App):
    def build(self):
        global loginScreenManager

        loginScreenManager = ScreenManager()
        loginScreen = LoginScreen()
        mainScreens = MainScreens()



        loginScreenManager.add_widget(loginScreen)
        loginScreenManager.add_widget(mainScreens)

        return loginScreenManager


if __name__ == '__main__':
    myapp = MainApp()
    myapp.run()
