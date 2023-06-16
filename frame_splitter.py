import os
import shutil
import ffmpeg
import zipfile
from os.path import join, exists, splitext, isfile

def delete_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"Directory '{directory}' has been deleted successfully.")
    except Exception as e:
        print(f"Failed to delete '{directory}'. Reason: {e}")

def main():
    data_path = "/Videos/HGV_clips"
    unsplit_path = join(data_path, 'unsplit_5fps')
    split_path = join(data_path, 'split_5fps')

    annotation_files = [f.strip("_pred_mask.zip") for f in os.listdir(join(data_path, 'annotations_5fps'))]

    dataset_path = join(data_path, 'sets', 'dataset3')
    if exists(dataset_path):
        delete_directory(dataset_path)
    os.mkdir(dataset_path)

    dataset_label_path = join(dataset_path, "labels")
    dataset_data_path =  join(dataset_path, "data")
    os.mkdir(dataset_label_path)
    os.mkdir(dataset_data_path)

    # iterate the video data and create a dataset
    for vid_category in os.listdir(split_path):
        for vid in os.listdir(join(split_path, vid_category)):
            # check annotation exists in category file
            vid = vid.strip(".mp4")
            if vid in annotation_files:
                # split clip into frames
                path = join(split_path, vid_category,  vid + '.mp4')
                ffmpeg.input(path).output(f'{dataset_data_path}/{vid}_%05d.png').run()

                # unzip annotations 
                path = join(data_path, 'annotations_5fps', vid + '_pred_mask.zip')
                with zipfile.ZipFile(path, 'r') as zip_ref:
                    zip_ref.extractall(dataset_label_path)

    # Replace name numbers because ffmpeg naming convention is annoying af
    frame_names = [f for f in os.listdir(dataset_data_path)]
    new_frame_names = []
    for name in frame_names:
        num = int(name[-9:-4]) - 1
        new_frame_names.append(name[:-9] + str(num).zfill(5) + '.png')

    # rename all data files
    for name, new_name in zip(frame_names, new_frame_names):
        os.rename(join(dataset_data_path, name), join(dataset_data_path, new_name))

    # Remove frames with missing annotations (usually the last frame somehow)
    data_files = set(splitext(f)[0] for f in os.listdir(dataset_data_path) if isfile(join(dataset_data_path, f)))
    label_files = set(splitext(f)[0] for f in os.listdir(dataset_label_path) if isfile(join(dataset_label_path, f)))

    missing_labels = data_files - label_files

    for file in missing_labels:
        os.remove(join(dataset_data_path, file + '.png'))

if __name__ == "__main__":
    main()
