import os

input_dir = "/Videos/HGV_clips/sets/dataset2/labels"

# Get a sorted list of all files
all_files = sorted(os.listdir(input_dir))

# Iterate over all files
for i, filename in enumerate(all_files):
    # Check if it is a png file
    if filename.endswith('.txt'):
        # Check if it is not a 6th frame
        if i % 6 != 0:
            # Delete it
            os.remove(os.path.join(input_dir, filename))
