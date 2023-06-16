import ffmpeg
import os
from os.path import join, exists
import shutil

def lower_framerate(input_path, output_path, fps=5):
    stream = ffmpeg.input(input_path)
    stream = ffmpeg.filter(stream, 'fps', fps=fps)
    stream = ffmpeg.output(stream, output_path)
    ffmpeg.run(stream)

def delete_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"Directory '{directory}' has been deleted successfully.")
    except Exception as e:
        print(f"Failed to delete '{directory}'. Reason: {e}")

def main():
    data_path = "/Videos/HGV_clips"
    unsplit_path = join(data_path, 'unsplit')

    lowered_fps_path = join(data_path, 'unsplit_5fps')
    if exists(lowered_fps_path):
        delete_directory(lowered_fps_path)
    os.mkdir(lowered_fps_path)

    # iterate the video data and create a dataset
    for vid_category in os.listdir(unsplit_path):
        os.mkdir(join(lowered_fps_path, vid_category))
        for vid in os.listdir(join(unsplit_path, vid_category)):
            input_path = join(unsplit_path, vid_category, vid)
            output_path = join(lowered_fps_path, vid_category, vid)
            lower_framerate(input_path, output_path)
            print(f"Completed: {output_path}")

if __name__ == "__main__":
    main()