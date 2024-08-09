from openai import OpenAI
from pathlib import Path
import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound

client = OpenAI()

def record_audio():
    # 비트레이트
    fs = 44100
    seconds = 3

    record = sd.rec(int(seconds*fs), samplerate=fs, channels=2)
    sd.wait()

    audio_input_path = "audio_input.wav"
    write(audio_input_path, fs, record)
    return audio_input_path

def conn_whisper(audio_input_path):
    audio_file= open(audio_input_path, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    print(transcription.text)
    text_input = transcription.text
    return text_input


def conn_chatgpt(text_input):
    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": text_input}
    ]
    )
    print(completion.choices[0].message.content)
    text_output = completion.choices[0].message.content
    return text_output


def conn_tts(text_output):
    speech_file_path = Path(__file__).parent / "audio_output.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text_output
    )
    response.stream_to_file(speech_file_path)
    audio_output_path = str(speech_file_path)

    return audio_ouput_path


def main():
    # 마이크 input => audio_input_path
    audio_input_path = record_audio()
    text_input = conn_whisper()
    text_output = conn_chatgpt(text_input)
    audio_output_path = conn_tts(text_output)
    playsound(audio_output_path)
    # audio_output_path의 mp3를 play

    return


main()