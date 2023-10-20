from pathlib import Path

import pandas as pd
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

PATH_WORDS = Path('Instruments and materials/Data Collection/Words')
SPEECH_RATE = '-35%'

def get_words():
    words_with_data = pd.read_csv(PATH_WORDS / 'Cleaned words/4-words_final.csv')
    words = words_with_data.word.tolist()

    return words

def get_word_recording(word):
    apikey = "2HIxgyPFilvhsS_fH_dl-2-8ubl48VNtEtglhVrCSORU"
    authenticator = IAMAuthenticator(apikey)
    text_to_speech = TextToSpeechV1(authenticator=authenticator)

    url = "https://api.us-south.text-to-speech.watson.cloud.ibm.com/instances/f0cd2d75-e0a9-4e2e-afa0-da9e27749349"
    text_to_speech.set_service_url(url)

    # text_to_speech = setup_speech_synthetizer()
    # the '' in {speech_rate} are necessary for the syntax
    word_final = f"<prosody rate='{SPEECH_RATE}'> {word} </prosody>"
    recording = (
        text_to_speech.synthesize(
            word_final, voice="es-US_SofiaV3Voice", accept="audio/mp3"
        )
        .get_result()
        .content
    )

    return recording

def save_recording(word, recording):
    filename = PATH_WORDS / "Audio" / f"{word}.wav"

    with open(filename, "wb") as audio_file:
        audio_file.write(recording)
        

print('getting words')
words = get_words()
print('creating audio')
for word in words:
    recording = get_word_recording(word)
    save_recording(word, recording)
print('done')