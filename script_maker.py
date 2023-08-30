from gtts import gTTS
from moviepy.editor import *

class VideoEditor:

    def get_sentences(self, text_file):
        """
        Creates lists sentences from the provided text file
        Each post is separated by an empty list value,
            the title is the first value after an empty value,
            and the body is the element after the title.
        :param text_file: a text file with posts
        :return: list of sentences from all posts
        """
        post_list = []
        sentence_list = []

        with open(text_file, 'r', encoding="utf-8") as reader:
            current_line = reader.readline()
            while current_line:
                if current_line != "\n":
                    unformatted_line = current_line.strip()
                    formatted_line = unformatted_line.split('. ')
                    sentence_list += formatted_line
                else:
                    post_list.append(sentence_list)
                    sentence_list = []
                current_line = reader.readline()
        return post_list


    def convert_file_temp_audio(self, post_sentence_list):
        """
        Converts text from a text file to GTTS audio clips
        :param post_sentence_list: list of sentences from a post
        :return: list of audio clips
        """

        index = 0
        clip_list = []
        for post in post_sentence_list:
            for sentence in post:
                if sentence != '':
                    temp_filename = f"temp{index}.mp3"

                    TTS_audio = gTTS(text=sentence, lang='en', slow=False)
                    TTS_audio.save("./temp_audio/" + temp_filename)

                    audio_clip = AudioFileClip("./temp_audio/" + temp_filename)
                    clip_list.append(audio_clip)
                    index += 1


        # final_audio = concatenate_audioclips(create_audio_list(test_list))
        # final_audio.write_audiofile("output.mp3")

        return clip_list




"""
Video editor

- Convert script to audio file
- combine audio files to make final single file
- manage files and delete unused ones
- create captions for video
"""

if __name__ == "__main__":
    VE = VideoEditor()

    happy = VE.get_sentences("temp_text.txt")
    VE.convert_file_temp_audio(happy)