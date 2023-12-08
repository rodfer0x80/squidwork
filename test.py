import whisper
import sounddevice as sd
import numpy as np
import nltk
import pygame
import argparse
import multiprocessing as mp
import os
import re
import sys
import time
from contextlib import contextmanager
from pathlib import Path
import numpy as np
import pyaudio
import yaml
from vits import MODELS as VITS_MODELS
from vits import Y_LENGTH_ESTIMATE_SCALARS, HParams, Synthesizer, TextMapper, get_hparams_from_file, load_model
from whisper import init_whisper, transcribe_waveform
from sentencepiece import SentencePieceProcessor
import tempfile
import os

# https://github.com/tinygrad/tinygrad/blob/master/examples/conversation.py

class Listener:
    RATE = 16000
    CHUNK = 1600

    def __init__(self):
        pass

    @staticmethod
    def chunks(xs, n): 
        for i in range(0, len(xs), n): yield xs[i:i + n]

class Speaker:
    def __init__(self):
        pass
    # def tts(
    # text_to_synthesize: str,
    # synth: Synthesizer,
    # hps: HParams,
    # emotion_embedding: Path,
    # speaker_id: int,
    # model_to_use: str,
    # noise_scale: float,
    # noise_scale_w: float,
    # length_scale: float,
    # estimate_max_y_length: bool,
    # text_mapper: TextMapper,
    # model_has_multiple_speakers: bool,
    # pad_length=600,
    # vits_pad_length=1000
    # ):
    # if model_to_use == "mmts-tts": text_to_synthesize = text_mapper.filter_oov(text_to_synthesize.lower())

    # # Convert the input text to a tensor.
    # stn_tst = text_mapper.get_text(text_to_synthesize, hps.data.add_blank, hps.data.text_cleaners)
    # init_shape = stn_tst.shape
    # assert init_shape[0] < pad_length, "text is too long"
    # x_tst, x_tst_lengths = stn_tst.pad(((0, pad_length - init_shape[0]),), 1).unsqueeze(0), Tensor([init_shape[0]], dtype=dtypes.int64)
    # sid = Tensor([speaker_id], dtype=dtypes.int64) if model_has_multiple_speakers else None

    # # Perform inference.
    # audio_tensor = synth.infer(x_tst, x_tst_lengths, sid, noise_scale, length_scale, noise_scale_w, emotion_embedding=emotion_embedding,
    #                             max_y_length_estimate_scale=Y_LENGTH_ESTIMATE_SCALARS[model_to_use] if estimate_max_y_length else None, pad_length=vits_pad_length)[0, 0]
    # # Save the audio output.
    # audio_data = (np.clip(audio_tensor.numpy(), -1.0, 1.0) * 32767).astype(np.int16)
    # return audio_data

    # def init_vits(
    # model_to_use: str,
    # emotion_path: Path,
    # speaker_id: int,
    # seed: int,
    # ):
    # model_config = VITS_MODELS[model_to_use]

    # # Load the hyperparameters from the config file.
    # hps = get_hparams_from_file(fetch(model_config[0]))

    # # If model has multiple speakers, validate speaker id and retrieve name if available.
    # model_has_multiple_speakers = hps.data.n_speakers > 0
    # if model_has_multiple_speakers:
    #     if speaker_id >= hps.data.n_speakers: raise ValueError(f"Speaker ID {speaker_id} is invalid for this model.")
    #     if hps.__contains__("speakers"): # maps speaker ids to names
    #     speakers = hps.speakers
    #     if isinstance(speakers, list): speakers = {speaker: i for i, speaker in enumerate(speakers)}

    # # Load emotions if any. TODO: find an english model with emotions, this is untested atm.
    # emotion_embedding = None
    # if emotion_path is not None:
    #     if emotion_path.endswith(".npy"): emotion_embedding = Tensor(np.load(emotion_path), dtype=dtypes.int64).unsqueeze(0)
    #     else: raise ValueError("Emotion path must be a .npy file.")

    # # Load symbols, instantiate TextMapper and clean the text.
    # if hps.__contains__("symbols"): symbols = hps.symbols
    # elif model_to_use == "mmts-tts": symbols = [x.replace("\n", "") for x in fetch("https://huggingface.co/facebook/mms-tts/raw/main/full_models/eng/vocab.txt").open(encoding="utf-8").readlines()]
    # else: symbols = ['_'] + list(';:,.!?¡¿—…"«»“” ') + list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') + list("ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ")
    # text_mapper = TextMapper(apply_cleaners=True, symbols=symbols)

    # # Load the model.
    # Tensor.no_grad = True
    # if seed is not None:
    #     Tensor.manual_seed(seed)
    #     np.random.seed(seed)
    # net_g = load_model(text_mapper.symbols, hps, model_config)

    # return net_g, emotion_embedding, text_mapper, hps, model_has_multiple_speakers

    # @contextmanager
    # def output_stream(num_channels: int, sample_rate: int):
    # try:
    #     p = pyaudio.PyAudio()
    #     stream = p.open(format=pyaudio.paInt16, channels=num_channels, rate=sample_rate, output=True)
    #     yield stream
    # except KeyboardInterrupt: pass
    # finally:
    #     stream.stop_stream()
    #     stream.close()
    #     p.terminate()

# def text_to_speech(text, output_path):
#     command = f'tts --text "{text}" --out_path {output_path}'
#     os.system(command)

# def play_audio_and_delete(audio_file):
#     pygame.mixer.init()
#     pygame.mixer.music.load(audio_file)
#     pygame.mixer.music.play()
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)
#     os.remove(audio_file)  # Deletes the temporary audio file

# def capture_audio(duration=5, sr=16000):
#     print("Recording...")
#     audio_data_int = sd.rec(int(duration * sr), samplerate=sr, channels=1, dtype='int16')
#     sd.wait()  # Wait until recording is finished
#     print("Finished recording...")
#     audio_data_float = audio_data_int.flatten().astype(np.float32) / np.iinfo(np.int16).max
#     return audio_data_float

# def main():
#     exit_keywords = ["goodbye!", "bye", "bye!", "goodbye.", "good bye", "goodbye"]
#     nltk.download('punkt')

#     model_size = "tiny"
#     model = whisper.load_model(model_size)
    
#     while True:
#         audio_data = capture_audio()  # Assuming you have a function to capture audio
#         whisper_pred_text = model.transcribe(audio_data)["text"]
#         print(whisper_pred_text)

#         # Tokenize transcribed text into words
#         tokens = nltk.tokenize.word_tokenize(whisper_pred_text.lower())

#         # Check for the presence of exit keywords in the transcribed text
#         if any(keyword in tokens for keyword in exit_keywords):
#             text = "Goodbye Habibi!"
#             with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
#                 text_to_speech(text, temp_audio.name)
#                 play_audio_and_delete(temp_audio.name)
            
#             break  # Exit the loop if goodbye intent is detected

#         with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
#             text_to_speech(whisper_pred_text, temp_audio.name)
#             play_audio_and_delete(temp_audio.name)


def main():
    return 0

if __name__ == '__main__':
    main()
