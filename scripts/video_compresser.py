import os
import subprocess

base_path = "D:\\Kimia'sProject-HHExperimentsRecordings"

video_path_list = []

for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith(".MP4") or file.endswith(".mp4"):
            if not file.split('\\')[-1].startswith("._"):
                video_path_list.append(os.path.join(root, file.replace("MP4", "mp4")))

for file in video_path_list:
    new_path = file.replace(base_path, base_path + "_compressed")
    new_directory = "\\".join(new_path.split("\\")[:-1])
    if not os.path.isdir(new_directory):
        os.makedirs(new_directory)
    # print(file, new_path)
    # break
    subprocess.run('ffmpeg -i {} -vf "scale=854:480" -b:v 2M -an -c:a aac -strict experimental {}'.format(file, new_path))
