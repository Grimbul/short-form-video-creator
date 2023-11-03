from gtts import gTTS
from moviepy.editor import *
from pydub import *


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

        TEMP_AUDIO_PATH = "./temp_audio/"

        for post_num, post in enumerate(post_sentence_list):
            os.mkdir(f"{TEMP_AUDIO_PATH}post{post_num}")
            for sentence_num, sentence in enumerate(post):
                if post != '':
                    temp_filename = f"{TEMP_AUDIO_PATH}tts_temp{sentence_num}.mp3"

                    TTS_audio = gTTS(text=sentence, lang='en', slow=False)
                    TTS_audio.save(temp_filename)

    def delete_temp_audio(self, directory):
        """
        Deletes all temporary directories
        :param directory: name of directory to delete temp directories from
        """

        for dir in os.listdir(directory):
            if directory.startswith("post"):
                os.remove(dir)

    def create_final_audio(self, clip_directory):
        """
        Combines audio clips from a clip directory to create a final audio clip
        :param clip_directory: list of audio clips
        """

        TEMP_AUDIO_PATH = "./temp_audio/"
        FINAL_AUDIO_PATH = "./final_video/"

        combined = AudioSegment.empty()
        for audio_clip in os.listdir(TEMP_AUDIO_PATH + clip_directory):
            audio_clip = AudioSegment.from_mp3(audio_clip)
            combined += audio_clip

        combined.export(FINAL_AUDIO_PATH + clip_directory, format="mp3")

        self.delete_temp_audio(TEMP_AUDIO_PATH)


"""
Video editor

- Convert script to audio file DONE
- combine audio files to make final single file ACTIVE
- manage files and delete unused ones DONE
- create captions for video NOT STARTED
"""

if __name__ == "__main__":
    VE = VideoEditor()

    post_list = VE.get_sentences("temp_text.txt")
    VE.convert_file_temp_audio(post_list)
    VE.create_final_audio("post0")
    os.system("start ./final_video/post0.mp3")
