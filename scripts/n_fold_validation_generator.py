import os
import csv
import shutil
import random
import time
import copy

folds_number = 10
annotations = []

base_path = "D:\\Kimia's Project - HH Experiments Recordings"
labels_path = ".\\labels.csv"
folds_path = os.path.join(base_path, "folds")

full_annotation_path = os.path.join(base_path, "full_annotation.csv")

def write_to_txt(data, fold_number, name):
    base_fold_path = os.path.join(folds_path, str(fold_number))
    fold_path = os.path.join(base_fold_path, name + ".txt")
    if not os.path.exists(base_fold_path): os.mkdir(base_fold_path)
    fold_file = open(fold_path, 'w')
    for row_index in range(len(data) - 1):
        fold_file.write(data[row_index][0] + " " + data[row_index][1])
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

    random.seed(int(time.time() * 1000))
    random.shuffle(annotations)
    
    fold_size = int(len(annotations) / folds_number)
    fold_list = [annotations[i:i + fold_size] for i in range(0, len(annotations), fold_size)]

    if len(fold_list) > folds_number: 
        fold_list[-2] = fold_list[-2] + fold_list[-1]
        fold_list.pop()

    for fold_index in range(len(fold_list)):
        fold_list_copy = copy.deepcopy(fold_list)
        test_fold = fold_list_copy.pop(fold_index)
        val_fold = fold_list_copy.pop(len(fold_list) - fold_index - 2)
        
        train_fold = []
        for fold in fold_list_copy:
            train_fold = train_fold + fold

        write_to_txt(test_fold, fold_index + 1, 'test')
        write_to_txt(val_fold, fold_index + 1, 'val')
        write_to_txt(train_fold, fold_index + 1, 'train')