import requests


class Translate:
    def __init__(self, text, target):
        if target == 'he':
            src = 'en'
        else:
            src = 'he'
        url = f'https://api.mymemory.translated.net/get?q={text}&langpair={src}|{target}'
        translate = requests.get(url).json()
        self.output = translate['responseData']['translatedText']