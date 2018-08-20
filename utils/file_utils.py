import os
import json

def file_read(path, spliter="\n", ftype='r', start=0, end=None, delimiter=None):
    with open(path, ftype) as f:
        lines = f.read().split(spliter)[start: end]
        if delimiter:
            lines = [l.strip().split(delimiter) for l in lines]
        return lines


def file_read_json(path, ftype='r'):
    with open(path, ftype) as f:
        lines = f.read()
        return json.loads(lines)


def dir_read(dir_path, spliter="\n", ftype='r', start=0, end=None, filter_name_lst=None):
    files = os.listdir(dir_path)
    res = dict()
    for fn in files:
        with open(os.path.json(dir_path, fn), ftype) as f:
            lines = f.read().split(spliter)[start:end]
            res[fn] = lines
    return res
