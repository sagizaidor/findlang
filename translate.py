import os
from google.cloud import translate_v2 as translate


class Translate:
    def __init__(self, text, target):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\Users\sagiz\Desktop\PythonCourse\week 12\googlekey.json"
        trns_client = translate.Client()
        output = trns_client.translate(text, target_language=target)
        self.output = output['translatedText']