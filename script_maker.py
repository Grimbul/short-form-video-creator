from gtts import gTTS
from moviepy.editor import *
from pydub import *

from text_parser import Parser


class VideoEditor:

    def create_audio_file(self, post, audio_directory):
        """
        Uses GTTS to turn a post into a mp3 audio file. Saves file to specified directory
        :param post: the post to be "read" out
        :param audio_directory: the directory where the created audio will be saved
        """

        AUDIO_FILENAME = f"post_audio.mp3"
        audio_path = f"/{audio_directory}/"

        TTS_audio = gTTS(text=post, lang='en', slow=False)
        TTS_audio.save(audio_path.join(AUDIO_FILENAME))

"""
Video editor

- Convert script to audio file DONE
- create captions for video NOT STARTED
"""

if __name__ == "__main__":
    parser = Parser()
    VE = VideoEditor()

    post = parser.read_post("temp_text.txt", 0)
    VE.create_audio_file(post, "audio_files")

    os.system("start ./audio_files/post_audio.mp3")
