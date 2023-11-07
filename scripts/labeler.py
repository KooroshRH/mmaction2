import os
import csv

label_key = "Label"
label_id_key = "LabelId"
path_key = "Path"
subject_key = "Subject"

base_path = "D:\\Kimia's Project - HH Experiments Recordings"
labels_path = ".\\labels.csv"

full_annotation_path = os.path.join(base_path, "full_annotation.csv")
compact_annotation_path = os.path.join(base_path, "compact_annotation.csv")

if __name__ == "__main__":
    video_path_list = []

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".MP4") or file.endswith(".mp4"):
                video_path_list.append(os.path.join(root, file))

    print("Working on", len(video_path_list), "videos")

    labels_file = open(labels_path)
    labels_reader = csv.reader(labels_file, delimiter=',')
    labels = {}
    for row in labels_reader:
        labels[row[0]] = row[1]

    full_annotation_file = open(full_annotation_path)
    full_annotation_reader = csv.reader(full_annotation_file, delimiter=',')
    previous_paths = []
    for row in full_annotation_reader:
        previous_paths.append(row[0])
    full_annotation_file.close()

    full_annotation_file = open(full_annotation_path, 'a', newline='')
    compact_annotation_file = open(compact_annotation_path, 'a', newline='')
    full_writer = csv.writer(full_annotation_file)
    compact_writer = csv.writer(compact_annotation_file)

    print(video_path_list[0])
    main_dir = ''.join(video_path_list[0].split('\\')[:-1])
    subject = input("Who is the subject for this directory? ")
    os.system('cls')
    for video_path in video_path_list:
        relative_path = video_path.replace(base_path, ".")
        current_main_dir = ''.join(video_path.split('\\')[:-1])
        
        if relative_path in previous_paths: 
            print("Skipping video")
            continue
        if main_dir != current_main_dir:
            print(video_path)
            subject = input("Who is the subject for this directory? ")
            main_dir = current_main_dir
            os.system('cls')
        elif subject == '-':
            print("Subject video passed")
            continue

        print(video_path)
        label = input("What is the activity label for this video? ")
        if label == "-":
            os.system('cls')
            continue

        full_writer.writerow([relative_path, label, labels[label], subject])
        compact_writer.writerow([relative_path, label])
        os.system('cls')
    
    full_annotation_file.close()
    compact_annotation_file.close()