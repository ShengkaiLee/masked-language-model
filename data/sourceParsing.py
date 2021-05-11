import os
import os.path
import pickle
import re
import sys
import csv
import itertools
import shutil

type_list = ['int', 'char', 'float', 'double', 'bool', 'void', 'short', 'long', 'signed', 'struct']


def pickle_dump(root_path, data, file_name):
    os.chdir(root_path)
    fp = open(file_name, "w")
    pickle.dump(data, fp)
    fp.close()

def pickle_load(root_path, file_name):
    os.chdir(root_path)
    fp_case = open(file_name, "r")
    dict_case = pickle.load(fp_case)
    fp_case.close()
    return dict_case


def is_valid_name(name):
    if re.match("[a-zA-Z_][a-zA-Z0-9_]*", name) == None:
        return False
    return True

def is_func(line):
    line = line.strip()
    if len(line) < 2:
        return None

    if '(' not in line: 
        return None

    if line[0] == '#' or line[0] == '/':
        return None


    line = re.sub('\*', ' ', line)
    line = re.sub('\&', ' ', line)

    line = re.sub('\(', ' \( ', line)
    line_split = line.split()

    if len(line_split) < 2:
        return None

    bracket_num = 0
    for ch in line:
        if ch == '(':
            bracket_num += 1

    has_type = False
    for type_a in type_list:
        if type_a in line_split[0]:
            has_type = True

    if bracket_num == 1:
        for index in range(len(line_split)):
            if '(' in line_split[index]:
                return line_split[index - 1]
    else:
        line = re.sub('\(', ' ', line)
        line = re.sub('\)', ' ', line)
        line_split = line.split()
        index = 0
        for one in line_split:
            if is_valid_name(one):
                index += 1
                if index == 2:
                    return one
        return None

def get_line_type(line):
    line = line.strip()
    if line.startswith("/*"):
        return "comment_paragraph"
    elif line.startswith("//"):
        return "comment_line"
    elif line.startswith("#"):
        return "macro"
    return "other"

def is_comment_end(line):
    line = line.strip()
    if line.endswith('*/'):
        return True
    return False

def is_func_end(line, left_brack_num):
    line = line.strip()
    left_brack_num += line.count("{")
    if "}" in line:
        left_brack_num -= line.count("}")
        if left_brack_num == 0:
            return True
    return False

def func_name_extract(file_path):

    if not os.path.isfile(file_path):
        return


    file_list = []
    with open(file_path, "r") as fp:
        for line in fp.readlines():
            file_list.append(line)

    func_list = []

    i = -1
    while i < len(file_list) - 1:
        i += 1
        line = file_list[i]
        line_type = get_line_type(line)
        if line_type == "comment_line" or line_type == "macro":
            continue
        elif line_type == "comment_paragraph":
            while not is_comment_end(file_list[i]):
                i += 1
        else:
            func_name = is_func(line)
            if func_name != None:
                start_line = i
                left_brack_num = 0
                while True:
                    if i >= len(file_list):
                        break
                    line = (file_list[i]).strip()
                    left_brack_num += line.count('{')
                    if "}" in line:
                        left_brack_num -= line.count("}")
                        if left_brack_num < 1:
                            break
                    i += 1
                end_line = i
                func_list.append([func_name, start_line + 1, end_line + 1])
    return func_list

def write_to_file(func_list, output_file):

    with open(output_file, "w") as out_file:
        csv_write = csv.writer(out_file, delimiter = ",")
        for one in func_list:
            csv_write.writerow(one)

def sourceParsing_main(file_path):
    try:
        func_list = func_name_extract(file_path)
        ret = dict()
        to_remove = set()
        if func_list != None:
            for func_imfo in func_list:
                func_name = func_imfo[0]
                func_start = func_imfo[1]
                func_end  = func_imfo[2]
                func_str = ""
                with open(file_path) as text_file:
                    for line in itertools.islice(text_file, func_start, func_end):
                        func_str += str(line)
                if ret.get(func_name, None) is not None:
                    to_remove.add(func_name)
                ret[func_name] = func_str
        for key in to_remove:
            ret.pop(key, None)
        return ret
    except:
        return None

if __name__ == '__main__':

    if len(sys.argv) != 3:
        print ('Usage: python func_name_extract.py <file_path> <output_path>\n')
        exit(-1)
    # print(func_list)
    shutil.rmtree(sys.argv[2])
    os.mkdir(sys.argv[2])
    func_list = func_name_extract(sys.argv[1])
    if func_list != None:
        for func_imfo in func_list:
            func_name = func_imfo[0]
            func_start = func_imfo[1]
            func_end  = func_imfo[2]
            with open(sys.argv[1]) as text_file:
                fp = open(sys.argv[2]+ "/" + func_name, "w")
                for line in itertools.islice(text_file, func_start, func_end):
                    fp.write(line)
                
