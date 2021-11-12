#!/usr/bin/python3
"""Данная программа осуществялет копирование файлов в соответствии с конфигурационным файлом.
Конфигурационный файл должен иметь формат xml. Для каждого файла в конфигурационном файле должно быть указано его имя,
исходный путь и путь, по которому файл требуется скопировать.
Также в реализована проверка существования по пути назначения файла с таким же именем и запрашивается подтверждение на
перезапись.
Вид вызова команды: сopy_files.py  scratch.xml"""

# ---------------------------------------------------------------
# Program by Olga N.
#
# Version     Date      Info
# 4.0       11/12/21    Lesson
#
# ---------------------------------------------------------------

import xml.etree.ElementTree as ET      # for parsing of xml file
import os                               # for to connect paths and check if a file exists
import sys                              # for CLI Arguments
import shutil                           # for copy file

# main function
def copy(source_path, destination_path, file_name):
    file_source_path = os.path.join(source_path, file_name)  # get full source path of the file
    if (os.path.isfile(file_source_path) == True) and (os.path.exists(destination_path) == True):  # checking if full source and destination path of the file exist
        if os.path.isfile(os.path.join(destination_path, file_name)) == True:  # checking if a file exists in the destination path
            if input(f"the file {file_name} already exists in {destination_path}.replace file? [y/n] ") in ['y', '']:
                shutil.copy(file_source_path, destination_path)  # copy file
                print(f'File {file_name} from {source_path} copied to {destination_path}')
            else:
                print("file not copied")
        else:
            shutil.copy(file_source_path, destination_path)  # copy file
            print(f'File {file_name} from {source_path} copied to {destination_path}')
    else:
        print(f'COPY FAILED: Paths {file_source_path} or {destination_path} are not found')

# Checking of command:
if len(sys.argv) < 2:
    print("Missing arguments: Usage is 'script.py file.xml'")
    exit(1)

file = sys.argv[1]                      # get file's name
tree = ET.parse(file)                   # get tree of xml-file
root = tree.getroot()                   # get root of xml-file

for i, child in enumerate(root):
    print(f'copy file #{i+1}')
    dict_attrib = child.attrib                                                  # get dictionary of attributes of child
    source_path = dict_attrib.get("source_path", "path not found")              # get source path
    destination_path = dict_attrib.get("destination_path", "path not found")    # get destination path
    file_name = dict_attrib.get("file_name", "file's name not found")           # get file's name

    # check of source path, destination path and file's name:
    flage = True
    if source_path == "path not found":
        print(f"Path 'source_path' not found in file {file}")
        flage = False
    if destination_path == "path not found":
        print(f"Path 'destination_path' not found in file {file}")
        flage = False
    if file_name == "file's name not found":
        print(f"File's name not found in file {file}")
        flage = False

    # main function call
    if flage == True:
        copy(source_path, destination_path, file_name)
    else:
        print(f'COPY FAILED: to check paths in {file}')