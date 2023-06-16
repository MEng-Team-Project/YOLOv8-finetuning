import os 
from os.path import join

def main():
    data_path = "/Videos/HGV_clips"
    annotations_path = join(data_path, 'annotations')
    annotation_files = [f'{"_".join(f.split("_")[0:2])}' for f in os.listdir(join(data_path, 'annotations'))]

    while True:
        filename = input("\nEnter file_name: ").strip()
        filename = "_".join(filename.split("_")[0:2])
        
        if filename in annotation_files:
            print(f'{filename} already annotated')
        else:
            print(f'{filename} not annotated')

if __name__ == '__main__':
    main()