from config import SAMPLE_INPUTS, SAMPLE_OUTPUTS
from moviepy.editor import *
from moviepy.audio.fx.all import volumex
from PIL import Image

source_video_path = os.path.join(SAMPLE_INPUTS, "video.mp4")
source_audio_path = os.path.join(SAMPLE_INPUTS, "audio.mp3")
final_video_path = os.path.join(SAMPLE_INPUTS, "final.mp4")

video_clip = VideoFileClip(source_video_path)
new_audio_clip = AudioFileClip(source_audio_path)
new_audio_clip = new_audio_clip.subclip(0, video_clip.duration)

final_clip = video_clip.set_audio(new_audio_clip)
final_clip.write_videofile(final_video_path, codec="libx264", audio_codec="aac")