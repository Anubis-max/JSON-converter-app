import tkinter as tk
from tkinter import filedialog

import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line

import json

class DrawingWidget(Widget):
    def __init__(self, **kwargs):
        super(DrawingWidget, self).__init__(**kwargs)
        self.is_drawing = False 
        self.rect_start = None
        self.current_rect = None

    def enable_drawing(self):
        self.is_drawing = True 
        self.rect_start = None
        self.current_rect = None

    def disable_drawing(self):
        self.is_drawing = False

    def on_touch_down(self, touch):
        if self.is_drawing:
            self.rect_start = (touch.x, touch.y)
        return super().on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.is_drawing and self.rect_start:
            if self.current_rect:
                self.canvas.remove(self.current_rect)
            x1, y1 = self.rect_start
            x2, y2 = touch.x, touch.y
            with self.canvas:
                Color(1, 1, 0, 0.5)
                self.current_rect = Line(rectangle=(x1, y1, x2 - x1, y2 - y1), width=1.5)
        return super().on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self.is_drawing and self.rect_start:
            x1, y1 = self.rect_start
            x2, y2 = touch.x, touch.y

            global Point1
            global Point2
            Point1 = (int(x1), int(y1))
            Point2 = (int(x2), int(y2))

            with self.canvas:
                Color(1, 1, 0, 1)
                Line(rectangle=(x1, y1, x2 - x1, y2 - y1), width=1.5)
            self.rect_start = None
            self.current_rect = None
        return super().on_touch_up(touch)

    def convert(self):
        global Point1
        global Point2
        data = {}
        data = {
            "Rectangle-start: ": Point1,
            "Rectangle-end": Point2
        }

        print(json.dumps(data))

class MyGrid(FloatLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.drawing_widget = DrawingWidget()
        self.add_widget(self.drawing_widget)

    def get_path(self):
        root = tk.Tk()
        root.withdraw()
        Path = filedialog.askopenfilename()
        image_widget = Image(source=Path, size=(Window.width, Window.height - (Window.height * 0.1)), allow_stretch=True, keep_ratio=False, size_hint=(None, None), pos=(self.x, self.y + Window.height * 0.1))
        self.add_widget(image_widget)
        self.remove_widget(self.drawing_widget)
        self.add_widget(self.drawing_widget)


class MyApp(App):
    def build(self):
        self.title = "JSON Converter"
        self.icon = "img/icon.png"
        Window.clearcolor = (0.733, 0.749, 0.737, 1)
        Window.size = (600, 600)
        Config.set('graphics', 'resizable', False)
        Config.write()

        return MyGrid()


if __name__ == "__main__":
    MyApp().run()
