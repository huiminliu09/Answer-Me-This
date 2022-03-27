import speech_recognition as sr
import json
import urllib3
from pynput.keyboard import Key, Controller
from direct import open_chat
from googlesearch import search

keyboard = Controller()
r = sr.Recognizer()
m = sr.Microphone()
r.pause_threshold = .6
keyword = "hey computer"
url = "https://rdc1nf9jza.execute-api.us-east-1.amazonaws.com/api/qna"
api_key = "9HeBB23LR4a8mruNNf3kq17fFuR9b4JP1q5KSMCC"


def get_Eanswer(question: str) -> str:
    http = urllib3.PoolManager()
    res = http.request('GET',
                     url,
                     headers={'x-api-key': api_key},
                     fields={'search_string': question})
    result_json = json.loads(res.data)
    return result_json['longAnswer']

def get_Ganswer(question: str) -> str:
    my_results = []
    for i in search(question,  # The query you want to run
                    lang='en',  # The language
                    num_results=1,  # Number of results per page
                    ):
        my_results.append(i)
    print(my_results)
    return my_results


try:
    print("A moment of silence, please...")

    with m as source:
        r.adjust_for_ambient_noise(source)

    print("Set minimum energy threshold to {}".format(r.energy_threshold))

    while True:
        print("Say something!")

        with m as source:
            audio = r.listen(source)
        print("Got it! Now to recognize it...")

        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            val_str = format(value)

            if keyword in val_str:
                question = val_str[val_str.find(keyword) + len(keyword) + 1:]
                print("Question detected!")
                print("Looking up: " + question)

                try:
                    answer = get_Eanswer(question) + " "
                    print("Answer: " + answer)
                    open_chat()
                    keyboard.type(answer)
                except KeyError:
                    print("No results showing for that question :(")

                try:
                    link = get_Ganswer(question)
                    for i in link:
                        keyboard.type(i)
                    keyboard.press(Key.enter)
                except:
                    print("nothing from google")

            elif str is bytes:  # this version of Python uses bytes for strings (Python 2)
                print(u"You said {}".format(value).encode("utf-8"))

            else:  # this version of Python uses unicode for strings (Python 3+)
                print("You said {}".format(value))

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")

        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))

except KeyboardInterrupt:
    pass



