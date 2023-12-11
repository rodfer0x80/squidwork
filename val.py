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

from tinygrad.helpers import Timing, dtypes, fetch
from tinygrad.tensor import Tensor


# https://github.com/tinygrad/tinygrad/blob/master/examples/conversation.py

class Listener:
    RATE = 16000
    CHUNK = 1600

    def __init__(self, whisper_model_name="tiny.en"):
        nltk.download("punkt")
        Tensor.no_grad = True
        self.model, self.enc = init_whisper(whisper_model_name)
        self.is_listening_event = None
        pass

    @staticmethod
    def chunks(xs, n): 
        for i in range(0, len(xs), n): yield xs[i:i + n]

    def listen(self):
        q = mp.Queue()
        self.is_listening_event = mp.Event()
        p = mp.Process(target=self.listener, args=(q, is_listening_event,))
        p.daemon = True
        p.start()
    
    @staticmethod
    def listener(self, q: mp.Queue, event: mp.Event):
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNCK)
            did_print = False
            while True:
                data = stream.read(self.CHUNK) # read data to avoid overflow
                if event.is_set():
                    if not did_print:
                        print("listening...")
                        did_print = True
                    q.put(((np.frombuffer(data, np.int16)/32768).astype(np.float32)*3))
                else:
                    did_print = False
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
    

class Speaker:
    # TODO: put this in a config file, only speak should be arg void
    def __init__(self):
        self.vits_model_to_use = "vctk"
        self.vits_emotion_path = None
        self.vits_speaker_id = 6
        self.vits_seed = 1337
        self.synth, self.emotion_embedding, self.text_mapper, self.hps, self.model_has_multiple_speakers = self.init_vits(self.vits_model_to_use, self.vits_emotion_path, self.vits_speaker_id, self.vits_seed)
        self.vits_num_channels = 1
        self.vits_noise_scale =0.8
        self.vits_estimate_max_y_length = False
        self.vits_noise_scale_w = None
        self.out_counter = None

    @contextmanager
    def output_stream(self, num_channels: int, sample_rate: int):
        try:
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16, channels=num_channels, rate=sample_rate, output=True)
            yield stream
        except KeyboardInterrupt: pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    @staticmethod
    def mp_output_stream(self, q: mp.Queue, counter: mp.Value, num_channels: int, sample_rate: int):
        with self.output_stream(num_channels, sample_rate) as stream:
            while True:
                try:
                    stream.write(q.get())
                    counter.value += 1
                except KeyboardInterrupt:
                    break
    
    def speak(self):
        out_q = mp.Queue()
        self.out_counter = mp.Value("i", 0)
        out_p = mp.Process(target=self.mp_output_stream, args=(out_q, self.out_counter, self.vits_num_channels,self. self.hps.data.sampling_rate,))
        out_p.daemon = True
        out_p.start()
        for i in ["Hello, I'm a chat bot", "I am capable of doing a lot of things"]:
            self.tts(
                i, self.synth, self.hps, self.emotion_embedding,
                self.vits_speaker_id, self.vits_model_to_use, self.vits_noise_scale,
                self.vits_noise_scale_w, self.vits_length_scale,
                self.vits_estimate_max_y_length, self.text_mapper, self.model_has_multiple_speakers
            )

    def tts( 
        self,
        text_to_synthesize: str,
        synth: Synthesizer,
        hps: HParams,
        emotion_embedding: Path,
        speaker_id: int,
        model_to_use: str,
        noise_scale: float,
        noise_scale_w: float,
        length_scale: float,
        estimate_max_y_length: bool,
        text_mapper: TextMapper,
        model_has_multiple_speakers: bool,
        pad_length=600,
        vits_pad_length=1000
    ):
        if model_to_use == "mmts-tts": text_to_synthesize = text_mapper.filter_oov(text_to_synthesize.lower())

        # Convert the input text to a tensor.
        stn_tst = text_mapper.get_text(text_to_synthesize, hps.data.add_blank, hps.data.text_cleaners)
        init_shape = stn_tst.shape
        assert init_shape[0] < pad_length, "text is too long"
        x_tst, x_tst_lengths = stn_tst.pad(((0, pad_length - init_shape[0]),), 1).unsqueeze(0), Tensor([init_shape[0]], dtype=dtypes.int64)
        sid = Tensor([speaker_id], dtype=dtypes.int64) if model_has_multiple_speakers else None

        # Perform inference.
        audio_tensor = synth.infer(x_tst, x_tst_lengths, sid, noise_scale, length_scale, noise_scale_w, emotion_embedding=emotion_embedding,
                                    max_y_length_estimate_scale=Y_LENGTH_ESTIMATE_SCALARS[model_to_use] if estimate_max_y_length else None, pad_length=vits_pad_length)[0, 0]
        # Save the audio output.
        audio_data = (np.clip(audio_tensor.numpy(), -1.0, 1.0) * 32767).astype(np.int16)
        return audio_data

    def init_vits(
        self,
        model_to_use: str,
        emotion_path: Path,
        speaker_id: int,
        seed: int,
    ):
        model_config = VITS_MODELS[model_to_use]

        # Load the hyperparameters from the config file.
        hps = get_hparams_from_file(fetch(model_config[0]))

        # If model has multiple speakers, validate speaker id and retrieve name if available.
        model_has_multiple_speakers = hps.data.n_speakers > 0
        if model_has_multiple_speakers:
            if speaker_id >= hps.data.n_speakers: raise ValueError(f"Speaker ID {speaker_id} is invalid for this model.")
            if hps.__contains__("speakers"): # maps speaker ids to names
                speakers = hps.speakers
                if isinstance(speakers, list): speakers = {speaker: i for i, speaker in enumerate(speakers)}

        # Load emotions if any. TODO: find an english model with emotions, this is untested atm.
        emotion_embedding = None
        if emotion_path is not None:
            if emotion_path.endswith(".npy"): emotion_embedding = Tensor(np.load(emotion_path), dtype=dtypes.int64).unsqueeze(0)
            else: raise ValueError("Emotion path must be a .npy file.")

        # Load symbols, instantiate TextMapper and clean the text.
        if hps.__contains__("symbols"): symbols = hps.symbols
        elif model_to_use == "mmts-tts": symbols = [x.replace("\n", "") for x in fetch("https://huggingface.co/facebook/mms-tts/raw/main/full_models/eng/vocab.txt").open(encoding="utf-8").readlines()]
        else: symbols = ['_'] + list(';:,.!?¡¿—…"«»“” ') + list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz') + list("ɑɐɒæɓʙβɔɕçɗɖðʤəɘɚɛɜɝɞɟʄɡɠɢʛɦɧħɥʜɨɪʝɭɬɫɮʟɱɯɰŋɳɲɴøɵɸθœɶʘɹɺɾɻʀʁɽʂʃʈʧʉʊʋⱱʌɣɤʍχʎʏʑʐʒʔʡʕʢǀǁǂǃˈˌːˑʼʴʰʱʲʷˠˤ˞↓↑→↗↘'̩'ᵻ")
        text_mapper = TextMapper(apply_cleaners=True, symbols=symbols)

        # Load the model.
        Tensor.no_grad = True
        if seed is not None:
            Tensor.manual_seed(seed)
            np.random.seed(seed)
        net_g = load_model(text_mapper.symbols, hps, model_config)

        return net_g, emotion_embedding, text_mapper, hps, model_has_multiple_speakers


class Agent:
    def __init__(self):
        self.speaker = Speaker()
        self.listener = Listener()

    # TODO: put this in logger class
    @contextmanager
    def log_writer(self):
        try:
            logs = []
            yield logs
        finally:
            sep = "="*os.get_terminal_size()[1]
            print(f"{sep[:-1]}\nCHAT LOG")
            print(*logs, sep="\n")
            print(sep)
    
    def chat(self):
        with self.log_writer() as log:
            while True:
                tokens = [self.listener.enc._special_tokens["<|startoftranscript|>"], self.listener.enc._special_tokens["<|notimestamps|>"]]
                total = np.array([])
                self.speaker.out_counter.value = 0

                s = time.perf_counter()
                self.listener.is_listening_event.set()
                prev_text = None
        while True:
            for _ in range(RATE // CHUNK): total = np.concatenate([total, q.get()])
            txt = transcribe_waveform(model, enc, [total], truncate=True)
            print(txt, end="\r")
            if txt == "[BLANK_AUDIO]" or re.match(r"^\([\w+ ]+\)$", txt.strip()): continue
            if prev_text is not None and prev_text == txt:
            is_listening_event.clear()
            break
            prev_text = txtsxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        print() # to avoid llama printing on the same line
        log.append(f"{user_delim.capitalize()}: {txt}")

        # Generate with llama
        with Timing("llama generation: "):
            outputted, start_pos, response = llama_generate(
            llama, toks, outputted, txt, start_pos,
            user_delim=user_delim, resp_delim=resp_delim, temperature=args.llama_temperature,
            max_tokens=args.llama_count
            )
            log.append(f"{resp_delim.capitalize()}: {response}")

        # Convert to voice
        with Timing("tts: "):
            sentences = nltk.sent_tokenize(response.replace('"', ""))
            for i in sentences:
            total = np.array([], dtype=np.int16)
            for j in chunks(i.split(), args.max_sentence_length):
                audio_data = tts(
                " ".join(j), synth, hps, emotion_embedding,
                args.vits_speaker_id, args.vits_model_to_use, args.vits_noise_scale,
                args.vits_noise_scale_w, args.vits_length_scale,
                args.vits_estimate_max_y_length, text_mapper, model_has_multiple_speakers
                )
                total = np.concatenate([total, audio_data])
            out_q.put(total.tobytes())
        while out_counter.value < len(sentences): continue
        log.append(f"Total: {time.perf_counter() - s}")

    def parrot(self, data:str) -> str:
        return data

    def predict(self, data:str) -> str:
        return self.parrot(data)

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
