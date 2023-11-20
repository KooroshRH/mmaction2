import os
import csv
import shutil
import random
import time
import copy

output_num = 3
annotations = []

base_path = "/cluster/home/t125959uhn/Data/Kimia'sProject-HHExperimentsRecordings_compressed"
labels_path = "labels.csv"
folds_path = os.path.join(base_path, "30_70")

full_annotation_path = os.path.join(base_path, "full_annotation.csv")

def write_to_txt(data, fold_number, name):
    base_fold_path = os.path.join(folds_path, str(fold_number))
    fold_path = os.path.join(base_fold_path, name + ".txt")
    if not os.path.exists(base_fold_path): os.mkdir(base_fold_path)
    fold_file = open(fold_path, 'w')
    for row_index in range(len(data) - 1):
        fold_file.write(data[row_index][0].replace("\\", "/").replace("./", "").replace("MP4", "mp4") + " " + data[row_index][1])
        if row_index != len(data) - 1: fold_file.write('\n')
    fold_file.close()


if __name__ == "__main__":
    full_annotation_file = open(full_annotation_path)
    full_annotation_reader = csv.reader(full_annotation_file, delimiter=',')

    for row in full_annotation_reader:
        annotations.append((row[0], row[1]))
    full_annotation_file.close()
    
    if os.path.exists(folds_path):
        shutil.rmtree(folds_path)

    os.mkdir(folds_path)

    for index in range(output_num):
        random.seed(int(time.time() * 1000))

        random.shuffle(annotations)
        
        train_list = annotations[:int(len(annotations) * 0.7)]
        test_list = annotations[int(len(annotations) * 0.7):]

        write_to_txt(test_list, index + 1, 'test')
        write_to_txt(train_list, index + 1, 'train')