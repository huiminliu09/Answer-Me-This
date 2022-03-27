from pynput.keyboard import Key, Controller
from python_imagesearch.imagesearch import imagesearch
from focus import cursor
keyboard = Controller()

shortcuts = {
    'open zoom': [Key.ctrl, Key.shift, Key.alt],
    'open chat': [Key.alt, 'h']
}

image_paths = {
    'chat': './answermezoom/chat.png',
    'file': './answermezoom/file.png',
    'typemessage': './answermezoom/typemessage.png'
}


def press_many(keys):
    for key in keys:
        keyboard.press(key)

    for key in keys:
        keyboard.release(key)


def determine_chat() -> bool:
    positions = imagesearch(image_paths['chat']), \
                                          imagesearch(image_paths['file']), \
                                          imagesearch(image_paths['typemessage'])
    for pos in positions:
        for coordinate in pos:
            if coordinate == -1:
                return False

    return True


def open_chat():
    press_many(shortcuts['open zoom'])
    if determine_chat():
        print("chat was open")
        cursor()
    else:
        print('chat was not open')
        press_many(shortcuts['open chat'])