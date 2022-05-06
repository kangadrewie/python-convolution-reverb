class BaseComponent():
    def __init__(self, app):
        self.app = app
        self.root = self.app.root

    def style(self, type):
        if type == 'button':
            return ('Helvetica', '16')
