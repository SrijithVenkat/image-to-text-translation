#Image-To-Text / Language Translation by Srijith V.

import os
import io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
from google.cloud import translate_v2 as translate

whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
language_codes = open('language_codes.txt', 'r')
code_dict = {}
for line in language_codes:
    line = ''.join(filter(whitelist.__contains__, line))
    line = line.split(" ", 1)
    code_dict[line[1].lower()] = line[0]

# # folder_path = input("Where are the images located? (Please enter a folder path)  :  ") - You can change if necessary
image_path = 'download.jpeg'
folder_path = 'Images'
translate_to = code_dict[input("What language do you want to translate to? ").lower()]

def authenticate_google_credentials():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'YOUR-SERVICE-ACCOUNT.JSON'
    return vision_v1.ImageAnnotatorClient(), translate.Client()

def read_image(folder_path, curr_image):
    with io.open(os.path.join(folder_path, image_path),'rb') as image_file:
        content1 = image_file.read()
    image_r = types.Image(content = content1)
    return image_r

vision_client, translate_client = authenticate_google_credentials()

def translate_text_from_images(v_client, t_client, img1, to):
    response = vision_client.text_detection(image = img1)
    texts = response.text_annotations
    initial_txt = ""

    for text in texts:
        initial_txt += text.description + " "

    translated = translate_client.translate(initial_txt, to)

    return translated['translatedText']

translated = translate_text_from_images(v_client=vision_client, t_client=translate_client, img1=read_image(folder_path=folder_path, curr_image=image_path), to=translate_to)
print(translated)