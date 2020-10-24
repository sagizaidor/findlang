import requests
from flask import Flask, request, render_template


URL = 'http://countryapi.gear.host/v1/Country/getCountries?p'

def convert_lang_to_code(lang, res='code'):
    with open('lang&code.csv', 'r') as lang_code:
        while True:
            try:
                code, language = lang_code.readline().split(',')
                language = language.split(' ')[0]
                code = code.split(' ')[0]
            except ValueError:
                return
            if res == 'code':
                if lang in language:
                    return code
            if res == 'language':
                if lang in code:
                    return language

def get_contries(lang_or_name, by_name=False):
    if by_name:
        params = 'Name=' + lang_or_name
    else:
        lang = lang_or_name
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
            return 'אסליחה, אבל לא הצלחנו למצוא את המדינה. האם הקלדת נכון את שם המדינה? או שרשמת באנגלית?'
        lang = convert_lang_to_code(code, res='language')
        return lang
    contries = []
    for country in res['Response']:
            contries.append(country['Name'])

    return contries

app = Flask(__name__)

@app.route('/')
def result():
    return render_template('index.html')
    
@app.route('/find', methods=['POST'])
def find():
    resWhere = ''
    resWhich = ''
    whereTheySpeak = request.form['whereTheySpeak'].capitalize()
    if whereTheySpeak:
        resWhere = get_contries(whereTheySpeak)
    whichLangAt = request.form['whichLangAt'].capitalize()
    if whichLangAt:
        resWhich = get_contries(whichLangAt, by_name=True)
    return render_template('index.html', resWhere=resWhere, resWhich=resWhich)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)