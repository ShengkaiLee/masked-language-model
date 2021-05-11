import os
import numpy as np
import random
import json


def removeDuplicateSpace(theStr):
    spaceFlag = 0
    result = ''
    for i in theStr:
        if i == ' ':
            if (not spaceFlag):
                result += i
                spaceFlag = 1
        elif i == '\n':
            if (not spaceFlag):
                result += ' '
                spaceFlag = 1
        elif i != ' ':
            result += i
            spaceFlag = 0
    return result


if __name__ == "__main__":

    np.random.seed(8)
    random.seed(8)

    train_frac = 0.8
    valid_frac = 0.1

    DIR = "assembly-source"

    os.system("rm -rf {}".format(DIR))
    os.system("mkdir {}".format(DIR))

    all_data = list()
    for build in os.listdir('data/assembly_src_match'):
        build_path = os.path.join('data/assembly_src_match', build)
        if os.path.isdir(build_path):
            for package in os.listdir(build_path):
                package_path = os.path.join(build_path, package)
                if os.path.isdir(package_path):
                    for json_file in os.listdir(package_path):
                        json_path = os.path.join(package_path, json_file)
                        if os.path.isfile(json_path) and json_path.endswith(".json"):
                            
                            with open(json_path, "r") as fin:
                                data = json.load(fin)
                            
                            for key, val in data.items():

                                if len(val["source"]) > 0:

                                    src = val["source"].strip()
                                    assembly = val["assembly"].strip()

                                    src = removeDuplicateSpace(src)
                                    if "{" in src:
                                        src = src[src.index("{"):]

                                    all_data.append(assembly + " " + src)
    

    train_num = int(len(all_data) * train_frac)
    valid_num = int(len(all_data) * valid_frac)
    test_num = len(all_data) - train_num - valid_num

    arr = np.arange(len(all_data))
    np.random.shuffle(arr)

    train_idx = arr[0:train_num]
    valid_idx = arr[train_num:train_num + valid_num]
    test_idx = arr[train_num + valid_num:]

    for name, idx in zip(['train', 'valid', 'test'], [train_idx, valid_idx, test_idx]):

        with open(os.path.join(DIR, "assembly-source.{}.tokens").format(name), "w") as fout:
            
            for index in idx:
                fout.write(all_data[index])
                fout.write("\n")
    
    print("training data size: {}".format(train_num))
    print("valid data size: {}".format(valid_num))
    print("test data size: {}".format(test_num))
