from moviepy.editor import *

def create_short_video(video_path, clips, music_path, output_path):
    video = VideoFileClip(video_path)
    audio = AudioFileClip(music_path)
    final_clips = []
    total_duration = 0

    for start, end in clips:
        clip = video.subclip(start, end)

        # Calculate crop dimensions for 9:16
        width, height = clip.size
        new_width = int(height * (9/16))
        x_center = width / 2
        cropped_clip = clip.crop(x1=x_center - new_width/2, y1=0, x2=x_center + new_width/2, y2=height)

        final_clips.append(cropped_clip)
        total_duration += clip.duration

    final_audio = audio.subclip(0, min(30, total_duration)) #trim audio to clip length or 30 sec

    final_video = concatenate_videoclips(final_clips)
    final_video= final_video.set_audio(final_audio)

    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)


# Example usage
video_path = "longer_video.mp4"  # Replace with your video path
clips = [(5, 9), (15, 20), (35, 40)] # Example clips
music_path = "music.mp3"  # Replace with your music path
output_path = "short_video.mp4"

create_short_video(video_path, clips, music_path, output_path)
