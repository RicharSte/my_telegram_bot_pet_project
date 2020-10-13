from clarifai.rest import ClarifaiApp
from telegram import ReplyKeyboardMarkup, KeyboardButton

CLARIFAI_API_KEY = 'Token'

def key_board():
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Where am i?', request_location = True),
          'Заполнить анкету']])
    
def is_cat(file_name):
    app = ClarifaiApp(api_key=CLARIFAI_API_KEY)
    model = app.public_models.general_model
    response = model.predict_by_filename(file_name, max_concepts=5)
    if response['status']['code'] == 10000:
        for concept in response['outputs'][0]['data']['concepts']:
            if concept['name'] == 'cat':
                return True
    return False

if __name__ == '__main__':
    print(is_cat('photos\cat1.jpg'))
    print(is_cat('photos\cat2.jpg'))
