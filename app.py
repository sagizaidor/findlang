import json
from flask import Flask, request, render_template


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
    lang_or_name = lang_or_name.capitalize()
    with open('countries.json', encoding='utf-8') as contries:
        data = json.load(contries)
    countries = data['Response']
    if by_name:
        for country in countries:
            if country['Name'] == lang_or_name:
                return convert_lang_to_code(country['NativeLanguage'], res='language')
        return 'סליחה, אבל לא הצלחנו למצוא את המדינה. האם הקלדת נכון את שם המדינה? או שרשמת באנגלית?'
    else:
        code = convert_lang_to_code(lang_or_name, res='code')
        res = []
        for country in countries:
            if country['NativeLanguage'] == code:
                res.append(country['Name'])
        return res


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