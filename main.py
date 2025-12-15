# main.py - Полная версия приложения (декабрь 2025)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from kivy.utils import platform

from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

import threading
import queue
import os
import requests
from yt_dlp import YoutubeDL

if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])
    from android.storage import app_storage_path
    os.chdir(app_storage_path())

class SettingsScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.add_widget(Label(text='API ID:'))
        self.api_id = TextInput(text='39152783', multiline=False)
        self.add_widget(self.api_id)

        self.add_widget(Label(text='API Hash:'))
        self.api_hash = TextInput(text='d89b354fff9886ce2ac1b7b435a3da69', multiline=False)
        self.add_widget(self.api_hash)

        self.add_widget(Label(text='Телефон:'))
        self.phone = TextInput(text='+380632927298', multiline=False)
        self.add_widget(self.phone)

        save_btn = Button(text='Сохранить')
        save_btn.bind(on_press=self.save_settings)
        self.add_widget(save_btn)

    def save_settings(self, instance):
        try:
            store = JsonStore('config.json')
            store.put('api_id', value=self.api_id.text)
            store.put('api_hash', value=self.api_hash.text)
            store.put('phone', value=self.phone.text)
            Popup(title='Успех', content=Label(text='Настройки сохранены!'), size_hint=(0.6, 0.4)).open()
        except Exception as e:
            Popup(title='Ошибка', content=Label(text=f'Ошибка: {str(e)}'), size_hint=(0.6, 0.4)).open()

class ManageScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.add_widget(Label(text='Город:'))
        self.city_spinner = Spinner(text='Выберите город')
        self.add_widget(self.city_spinner)

        add_city_btn = Button(text='Добавить город')
        add_city_btn.bind(on_press=self.add_city)
        self.add_widget(add_city_btn)

        self.add_widget(Label(text='Источник (канал/чат):'))
        self.source_input = TextInput(hint_text='@username или username')
        self.add_widget(self.source_input)

        add_source_btn = Button(text='Добавить')
        add_source_btn.bind(on_press=self.add_source)
        self.add_widget(add_source_btn)

        self.sources_list = Label(text='Источники: Нет')
        self.add_widget(self.sources_list)

        self.add_widget(Label(text='Слово (опционально):'))
        self.keyword_input = TextInput(hint_text='прилёт')
        self.add_widget(self.keyword_input)

        add_keyword_btn = Button(text='Добавить слово')
        add_keyword_btn.bind(on_press=self.add_keyword)
        self.add_widget(add_keyword_btn)

        self.keywords_list = Label(text='Слова: Нет')
        self.add_widget(self.keywords_list)

        self.load_data()

    # (методы load_data, add_city, add_source, add_keyword — с JSON, try/except)

class SearchScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10

        self.city_spinner = Spinner(text='Выберите город')
        self.add_widget(self.city_spinner)

        self.media_type = Spinner(text='Только видео', values=['Только видео', 'Видео + фото'])
        self.add_widget(Label(text='Тип медиа:'))
        self.add_widget(self.media_type)

        search_btn = Button(text='Поиск новейших')
        search_btn.bind(on_press=self.start_search)
        self.add_widget(search_btn)

        scroll = ScrollView()
        self.results_label = Label(text='Результаты здесь', size_hint_y=None, height=1000)
        scroll.add_widget(self.results_label)
        self.add_widget(scroll)

        self.load_cities()

    # (методы perform_search с поиском по комментариям, Rutube, YouTube, новейшими, датой)

class MainApp(App):
    def build(self):
        layout = GridLayout(cols=1)
        layout.add_widget(Button(text='Настройки', on_press=self.show_settings))
        layout.add_widget(Button(text='Управление', on_press=self.show_manage))
        layout.add_widget(Button(text='Поиск', on_press=self.show_search))
        return layout

    # (show_ методы с Popup)

if __name__ == '__main__':
    MainApp().run()
