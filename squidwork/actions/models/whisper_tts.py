import whisper
import sounddevice as sd
import numpy as np
import nltk
import pygame

import tempfile
import os

# https://github.com/tinygrad/tinygrad/blob/master/examples/conversation.py

def text_to_speech(text, output_path):
    command = f'tts --text "{text}" --out_path {output_path}'
    os.system(command)

def play_audio_and_delete(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    os.remove(audio_file)  # Deletes the temporary audio file

def capture_audio(duration=5, sr=16000):
    print("Recording...")
    audio_data_int = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    print("Finished recording...")
    audio_data_float = audio_data_int.flatten().astype(np.float32) / np.iinfo(np.int16).max
    return audio_data_float

def main():
    exit_keywords = ["goodbye!", "bye", "bye!", "goodbye.", "good bye", "goodbye"]
    nltk.download('punkt')

    model_size = "tiny"
    model = whisper.load_model(model_size)
    
    while True:
        audio_data = capture_audio()  # Assuming you have a function to capture audio
        whisper_pred_text = model.transcribe(audio_data)["text"]
        print(whisper_pred_text)

        # Tokenize transcribed text into words
        tokens = nltk.tokenize.word_tokenize(whisper_pred_text.lower())

        # Check for the presence of exit keywords in the transcribed text
        if any(keyword in tokens for keyword in exit_keywords):
            text = "Goodbye Habibi!"
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                text_to_speech(text, temp_audio.name)
                play_audio_and_delete(temp_audio.name)
            
            break  # Exit the loop if goodbye intent is detected

        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
            text_to_speech(whisper_pred_text, temp_audio.name)
            play_audio_and_delete(temp_audio.name)


if __name__ == '__main__':
    main()
