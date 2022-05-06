from tkinter import ttk
from turtle import width

class BaseComponent():
    def __init__(self, app):
        self.app = app
        self.root = self.app.root
