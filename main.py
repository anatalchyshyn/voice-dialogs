from pypdf import PdfReader
import pytesseract
import shutil
import os
import random
from PIL import Image
from IPython.display import clear_output, display
import ipywidgets as widgets
from google.colab import files
from openai import OpenAI
import json
import glob
from pydub import AudioSegment
import re
from extraction import TextExtraction 

client = OpenAI(api_key='your_api_key')

PDF_FILE = "/content/1.pdf"
IMAGE_FOLDER = "/content/pages"

voices = {
    'US male': 1138,  # US male
    'US female': 2271,  # US female
    'CAN male': 3403,  # Canadian male
    'IND male': 4535,  # Indian male
    'US male2': 5667,  # US male
    'US female2': 6799   # US female
}


extractor = TextExtrator(PDF_PATH, IMAGE_FOLDER)
non_image_dialogs = extractor.pdf_to_images()
text_model = TextProcessing(client)
speech_model = SpeechModel()
speech_model.upload_model()

voice_folder = "/content/voice"

if os.path.exists(voice_folder):
    shutil.rmtree(voice_folder)
os.mkdir(voice_folder)

def extract_number(filename):
    match = re.search(r'\d+', filename)
    if match:
        return int(match.group())
    else:
        return float('inf')


if non_image_dialogs:
    
    dialogs = list(non_image_dialogs.keys())
    
    for j, dialog in enumerate(dialogs):
        
        updated_dialog = text_model.text_gpt_update(dialog)
        speakers = text_model.get_unique_speakers(updated_dialog)
        speakers_dict = dict(zip(speakers, ['US male', 'US female']))
        
        for key in updated_dialog.keys():
             for i, line in enumerate(updated_dialog[key]):
                
                line_keys = list(line.keys())
                prompt = line[line_keys[1]]
                filename =  voice_folder + "/line" + str(i) + '.mp3'
                
                voice = voices[speakers_dict[line[line_keys[0]]]]

                speech_model.save_text_to_speech(prompt, filename, voice)
             
        mp3_files = sorted(os.listdir(voice_folder), key=extract_number)
        
        speech_model.combine_replics(mp3_files, voice_folder, "dialog_" + str(j) + ".mp3")
        
else:
    image_files = sorted(glob.glob(IMAGE_FOLDER + "/*.jpg"))
    
    for j, image_file in enumerate(image_files):
        
        dialog = extractor.extract_text_from_image(image_file)
        updated_dialog = text_model.text_gpt_update(dialog)
        speakers = text_model.get_unique_speakers(updated_dialog)
        speakers_dict = dict(zip(speakers, ['US male', 'US female']))
        
        for key in updated_dialog.keys():
             for i, line in enumerate(updated_dialog[key]):
                
                line_keys = list(line.keys())
                prompt = line[line_keys[1]]
                filename =  voice_folder + "/line" + str(i) + '.mp3'
                
                voice = voices[speakers_dict[line[line_keys[0]]]]

                speech_model.save_text_to_speech(prompt, filename, voice)
             
        mp3_files = sorted(os.listdir(voice_folder), key=extract_number)
        
        speech_model.combine_replics(mp3_files, voice_folder, "dialog_" + str(j) + ".mp3")

    
   