import requests
import json
import os.path
import argparse


URL_FIRST_MALE = "http://deron.meranda.us/data/popular-male-first.txt"
URL_FIRST_FEMALE = "http://deron.meranda.us/data/popular-female-first.txt"
URL_LAST = "http://deron.meranda.us/data/popular-last.txt"

parser = argparse.ArgumentParser(
    description='Generate CSV files for bulk uploads')
parser.add_argument('lines', action='store', type=int)
parser.add_argument('perfile', action='store', type=int)
parser.add_argument('--folder', action='store', default="~/Documents/")
args = parser.parse_args()

def get_list(url):
    my_list_response = requests.get(url)
    if my_list_response.status_code == 200:
        my_list_str = my_list_response.text
        my_list = my_list_str.split("\n")
        my_list = [x.lower() for x in my_list if x != ""]
    else:
        raise Exception(
            "{error}: {x.status_code}-{x.reason}".format(
                x=my_list_response,
                error="An error occured while getting list"))
    return my_list

def get_first_names():
    first_names = get_list(URL_FIRST_MALE)
    first_names_female = get_list(URL_FIRST_FEMALE)
    for i in first_names_female:
        if i not in first_names:
            first_names.append(i)
    return first_names

def get_last_names():
    return get_list(URL_LAST)

def get_random_lists():
    from random import shuffle
    first = get_first_names()
    shuffle(first)
    last = get_last_names()
    shuffle(last)
    return first, last

def generate_names(
        first, last, count,
        first_off=0, last_off=0,
        format="{first} {last}"):
    names = []
    for i in range(0, count):
        names.append(format.format(
            first=first[first_off],
            last=last[last_off],
            cnt=i))
        first_off += 1
        if first_off == len(first):
            first_off = 0
            last_off += 1
            if last_off == len(last):
                last_off = 0

    return names, first_off, last_off

def save_csv(file_name, lines, headers):
    my_csv = open(file_name, 'w')
    my_csv.write(headers)
    for line in lines:
        my_csv.write('\n' + line)
    my_csv.close()


def get_file_name(full_base_file_path):
    from string import Formatter
    actual_full_path = os.path.abspath(os.path.expanduser(full_base_file_path))
    if 'num' not in [x[1] for x in Formatter().parse(full_base_file_path)]:
        raise Exception(
            "``num`` not found in path: {path}".format(
                path=full_base_file_path))
    cnt = 0
    while cnt < 1000:
        attempt = actual_full_path.format(num=cnt)
        if not os.path.isfile(attempt):
            return attempt
        else:
            cnt += 1
    raise Exception(
        "There are more than 1000 files with this pattern: {pattern}".format(
            pattern=actual_full_path))

def generate_csvs(
        num_lines,
        lines_per_file,
        base_file_name="data_{num:0>3}.csv",
        base_file_path="~/Documents/"):
    headers = '"FirstName","LastName","Email"'
    f_off = 0
    l_off = 0
    first_names, last_names = get_random_lists()
    print "First({f}) * Last({l}) = {t}".format(f=len(first_names), l=len(last_names), t=len(first_names) * len(last_names))
    lines_remaining = num_lines
    file_num = 0
    my_format = '"{first}","{last}","{first}.{last}@import-%d.fake.com"'
    while lines_remaining > 0:
        if lines_remaining > lines_per_file:
            lines_to_write = lines_per_file
        else:
            lines_to_write = lines_remaining
        my_list, f_off, l_off = generate_names(
            first=first_names,
            last=last_names,
            count=lines_to_write,
            first_off=f_off,
            last_off=l_off,
            format=my_format % (file_num))
        lines_remaining -= lines_per_file
        my_file_path = get_file_name(base_file_path + base_file_name)
        save_csv(
            file_name=my_file_path,
            lines=my_list,
            headers=headers)
        print "Wrote {file} with {num_lines} records, {remaining} lines left to write!".format(
            file=my_file_path, num_lines=lines_to_write, remaining=lines_remaining)
        file_num += 1
        del my_list
    print "DONE!! wrote {num_files} files with total of {num_lines} records.".format(num_files=file_num, num_lines=num_lines)
    
generate_csvs(num_lines=args.lines, lines_per_file=args.perfile, base_file_path=args.folder)
