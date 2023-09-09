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

        TEMP_AUDIO_PATH = "./temp_audio/"

        clip_list = []
        index = 0
        for post in post_sentence_list:
            for sentence in post:
                if sentence != '':
                    temp_filename = TEMP_AUDIO_PATH + f"tts_temp{index}.mp3"

                    TTS_audio = gTTS(text=sentence, lang='en', slow=False)
                    TTS_audio.save(temp_filename)

                    audio_clip = AudioFileClip(temp_filename)
                    audio_clip = audio_clip.set_duration(audio_clip.duration - 0.3)
                    audio_clip.write_audiofile(temp_filename, verbose=False, logger=None)
                    audio_clip.close()

                    clip_list.append(audio_clip)

                    index += 1
        return clip_list

    def delete_temp_audio(self, directory):
        """
        Deletes all audio clips in a directory
        :param directory: name of directory to delete clips from
        """

        for audio_file in os.listdir(directory):
            if audio_file.endswith(".mp3"):
                clip = AudioFileClip(directory + audio_file)
                clip.close()
                os.remove(directory + audio_file)

    def create_final_audio(self, clip_list):
        """
        Combines audio clips from a clip list to create a final audio clip
        :param clip_list: list of audio clips
        """

        TEMP_AUDIO_PATH = "./temp_audio/"
        FINAL_AUDIO_PATH = "./final_video/"

        final_audio = concatenate_audioclips(clip_list)
        final_audio.write_audiofile(FINAL_AUDIO_PATH + "tts_final_audio.mp3", verbose=False, logger=None)

        #self.delete_temp_audio(TEMP_AUDIO_PATH)


"""
Video editor

- Convert script to audio file DONE
- combine audio files to make final single file ACTIVE
- manage files and delete unused ones DONE
- create captions for video NOT STARTED
"""

if __name__ == "__main__":
    VE = VideoEditor()

    happy = VE.get_sentences("temp_text.txt")
    sad = VE.convert_file_temp_audio(happy)
    VE.create_final_audio(sad)
    os.system("start ./final_video/tts_final_audio.mp3")
