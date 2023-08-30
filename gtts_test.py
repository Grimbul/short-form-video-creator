from gtts import gTTS
from moviepy.editor import *
import os

language = 'en'

test_text = "The mr fortnite"
test_list = test_text.split()


def create_audio_list(word_list):
    x = 0
    clip_list = []
    for word in word_list:
        filename = f"input{x}.mp3"
        word_sound = gTTS(text=word, lang=language, slow=False)
        word_sound.save(filename)

        audio_var = AudioFileClip(filename)
        clip_list.append(audio_var)
        x += 1
    return clip_list


final_audio = concatenate_audioclips(create_audio_list(test_list))
final_audio.write_audiofile("output.mp3")

os.system("start output.mp3")