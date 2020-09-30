from clarifai.rest import ClarifaiApp
from telegram import ReplyKeyboardMarkup, KeyboardButton

CLARIFAI_API_KEY = 'dba2a4aba0cc419fa7fde956e4d3f0f8'

def key_board():
    return ReplyKeyboardMarkup(
        [[KeyboardButton('Where am i?', request_location = True)]])
    
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
