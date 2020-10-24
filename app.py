import requests
from flask import Flask, request, render_template
from translate import Translate
import os

URL = 'http://countryapi.gear.host/v1/Country/getCountries?p'

def convert_lang_to_code(lang, res='code'):
    with open('lang&code.csv', 'r') as lang_code:
        for _ in range(500):
            try:
                code, language = lang_code.readline().split(',')
                language = language.split(' ')[0]
                print(language)
                code = code.split(' ')[0]
                print(code)
            except ValueError:
                return
            if res == 'code':
                if lang in language:
                    return code
            if res == 'language':
                if lang in code:
                    return language

def translate(text, target):
    return Translate(text, target).output


def get_contries(lang_or_name, by_name=False):
    if by_name:
        params = 'Name=' + translate(lang_or_name, 'en')
    else:
        lang = translate(lang_or_name, 'en').split(' ')[0]
        code = convert_lang_to_code(lang)
        try:
            params = 'NativeLanguage=' + code
        except TypeError:
            return 'LangNotFound'
    url = URL + params
    res = requests.get(url).json()
    if by_name:
        try:
            code = res['Response'][0]['NativeLanguage']
        except IndexError:
            return 'סליחה, אבל לא הצלחנו למצוא את המדינה. האם הקלדת נכון את שם המדינה?'
        lang = convert_lang_to_code(code, res='language')
        return translate(lang, 'he')
    contries = []
    for country in res['Response']:
            contries.append(translate(country['Name'], 'he'))
    return contries

app = Flask(__name__)

@app.route('/')
def result():
    return render_template('index.html')
    
@app.route('/find', methods=['POST'])
def find():
    resWhere = ''
    resWhich = ''
    whereTheySpeak = request.form['whereTheySpeak']
    if whereTheySpeak:
        resWhere = get_contries(whereTheySpeak)
    whichLangAt = request.form['whichLangAt']
    if whichLangAt:
        resWhich = get_contries(whichLangAt, by_name=True)
    return render_template('index.html', resWhere=resWhere, resWhich=resWhich)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
