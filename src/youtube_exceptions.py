class BrokenVideoId(Exception):
    """
    Исключение выводится если пользователь
    вводит неверный ID видео
    """
    def __init__(self, *args):
        self.message = args[0] if args else 'BrokenVideoId: Неверный ID видео'

    def __str__(self):
        return self.message
