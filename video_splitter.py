import os
import math
import ffmpeg
from os.path import join, exists
from frame_splitter import delete_directory

def main():
    # Supported video file extensions
    video_extensions = ['.mp4', '.avi', '.mkv', '.flv', '.mov']

    # Path definitions
    data_path = "\\Videos\\HGV_clips"
    unsplit_path = join(data_path, 'unsplit_5fps')
    split_path = join(data_path, 'split_5fps')

    if exists(split_path):  delete_directory(split_path)
    os.mkdir(split_path)

    # iterate the video data and create a dataset
    for vid_category in os.listdir(unsplit_path):
        os.mkdir(join(split_path, vid_category))
        for vid in os.listdir(join(unsplit_path, vid_category)):
            video_path = os.path.join(unsplit_path, vid_category, vid)
            print(video_path)

            # Probe the video file for information
            probe = ffmpeg.probe(video_path)
            video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
            duration = float(video_info['duration'])
            
            # Calculate the number of clips
            num_clips = math.ceil(duration / 2)

            # Create clips
            for i in range(num_clips):
                start_time = i * 2

                # Skip if remaining duration is less than 2 seconds
                if (i == num_clips - 1) and (duration - start_time < 2):
                    continue

                output_file = os.path.join(split_path, vid_category, f'{os.path.splitext(vid)[0]}_clip_{i+1}.mp4')
                        
                try:
                    (
                        ffmpeg
                        .input(video_path, ss=start_time, t=2)
                        .output(output_file, c='copy')
                        .run(overwrite_output=True)
                    )
                except ffmpeg.Error as e:
                    print(f'Error occurred: {e.stderr.decode()}')


if __name__ == "__main__":
    main()
