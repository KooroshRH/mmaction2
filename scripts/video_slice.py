import cv2 as cv
import os
import shutil
import csv

start_time_key = "StartTime"
end_time_key = "EndTime"
label_key = "Label"
window_name_key = "WindowName"

base_path = "D:\\Kimia's Project - HH Experiments Recordings"

def slice_video(video_path):
    label_path = video_path.replace(".MP4", "-label.csv")

    file_name = os.path.splitext(os.path.basename(video_path))[0]
    folder_path = '\\'.join(video_path.split('\\')[0:-1])
    video = cv.VideoCapture(video_path)
    fps = int(video.get(cv.CAP_PROP_FPS))
    length = int(video.get(cv.CAP_PROP_FRAME_COUNT))

    labels = []
    if not os.path.exists(label_path): return
    with open(label_path) as label_csv:
        csv_reader = csv.reader(label_csv, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            else:
                label = {start_time_key: int(row[0]), end_time_key: int(row[1]), label_key: row[2]}
                labels.append(label)
                line_count += 1

    new_folder_path = os.path.join(folder_path, file_name)
    annotation_path = os.path.join(new_folder_path, file_name + "_annotation" + ".csv")

    if os.path.exists(new_folder_path):
        shutil.rmtree(new_folder_path)

    os.mkdir(new_folder_path)
    annotation_file = open(annotation_path, 'w', newline='')
    annotation_writer = csv.writer(annotation_file)
    annotation_writer.writerow([window_name_key, label_key])

    window_size = 3 * fps
    number_to_ignore = 0

    frame_number = 0
    window_number = 0
    window = []
    while True:
        ret, frame = video.read()
        if not frame is None:
            frame_number = frame_number + 1
            if frame_number % (number_to_ignore + 1) == 0:
                window.append(frame)
            if frame_number % window_size == 0:
                window_number = window_number + 1
                start_time = (frame_number - len(window)) / fps
                end_time = frame_number / fps
                is_valid = False
                for label_dict in labels:
                    if label_dict[start_time_key] <= start_time and label_dict[end_time_key] >= start_time and label_dict[start_time_key] <= end_time and label_dict[end_time_key] >= end_time:
                        is_valid = True
                        final_label = label_dict[label_key]
                        break
                
                if not is_valid:
                    window = []
                    continue
                
                window_file_name = file_name + "-" + "{:05d}".format(window_number)
                file_path = os.path.join(new_folder_path, window_file_name + '.mp4')
                annotation_writer.writerow([window_file_name, final_label])
                out = cv.VideoWriter(file_path, cv.VideoWriter_fourcc(*'DIVX'), fps, (frame.shape[1], frame.shape[0]))
                for sub_frame_index in range(len(window)):
                    out.write(window[sub_frame_index])
                window = []
                out.release()
        elif frame_number >= length:
            break

    annotation_file.close()

if __name__ == "__main__":
    video_path_list = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".MP4"):
                video_path_list.append(os.path.join(root, file))
    print("Working on", len(video_path_list), "videos")
    for video_path in video_path_list:
        print("Slicing", video_path)
        slice_video(video_path)