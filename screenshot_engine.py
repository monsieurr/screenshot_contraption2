# start a loop
    # open a new movie file
    # get all the screenshots from that movie
        # we want to get a screen every X seconds
        # put all screenshots inside a specific folder for that movie and screening session
        # name all screen with the movie name and specific timecode
    # close the movie file
# all movies have been screened
# loop ends

## TODO : 
## 1. fix timer, allow to start at 00:00:00 and increment X seconds at each iteration [DONE]
## 2. create function def take_multiple_screenshots() based on take_three_screenshots() [DONE]
## 3. create function def take_all_screenshots() that analyzes the root folder and take screenshots for all the movies in it [DONE]
##      1. put all screens of a specific movie inside a folder with the name of that movie [DONE]
##      2. each screen has the current datetime + name of movie in it [DONE]
##      X. must manage different type of video file [DONE]
##      X. may be able to escape and continue to next movie if there's an error
## 3. add arguments for proper python script execution, allowing to change movie/folder name and give interval [DONE]


import os
import subprocess
import argparse
from datetime import datetime, timedelta, time
import random
from pathlib import Path

# get filenames inside the folder
def get_filenames(path="."):
    filenames = []
    for file in os.listdir(path):
        if file.endswith((".mp4", ".avi", ".mkv")):
            print(os.path.join(".", file))
            filenames.append(file)
    return filenames

# remove spaces from movie files (this is a workaround to allow working on the files)
def change_filenames(path):
    for file in os.listdir(path):
        print("FILE : ", file)
        if file.endswith((".mp4",".avi",".mkv")):
            filename_nospaces = file.replace(" ", ".")
            Path(f"{path}"+"/"+f"{file}").rename(f"{path}" +"/"+f"{filename_nospaces}")


def get_filenames_inside_folders(dirName="."):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if entry.endswith((".mp4", ".avi", ".mkv")):
            if os.path.isdir(fullPath):
                allFiles = allFiles + get_filenames_inside_folders(fullPath)
            else:
                allFiles.append(fullPath)
    return allFiles

# get length of the video
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)

# get the current time
def get_current_time():
    current_time = datetime.now()
    current_time = current_time.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    current_time = current_time.replace("/", "_")
    current_time = current_time.replace(":", "_")
    current_time = current_time.replace(" ", "-")

    #name_screen = topic + "-" + dt_string + ".jpg"

    return current_time

## not sure I need those functions as I am probably just using the system to open and close the files
def open_file(filename):
    f = open(filename, "r")
    print(f.read())


def close_file(filename):
    f = open(filename, "r")
    print(f.readline())
    f.close()

def create_folder(filename='default'):
    path = os.getcwd()
    print("The current working directory is %s" % path)

    # define the name of the directory to be created
    path = os.path.splitext(filename)[0].title()

    try:
        os.mkdir(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
    return path

# Take one screenshot given one input file and a start time
def take_one_screenshot(input_file, time_delay=3, output_file="output.jpg"):
    print("time : ", time_delay)
    print("input file : ", input_file)

    ## Initialise start_time à 00:00:00
    start_time = datetime.min
    print("0. START TIME EST DE TYPE : ", type(
        start_time))  # datetime.datetime

    ## Keep only the time part (remove the Y/M/D part from datetime)
    start_time = start_time + timedelta(0, time_delay)

    start_time_str = start_time.strftime("%H:%M:%S")

    os.system(
        f"ffmpeg -ss {start_time_str} -i {input_file} -vframes 1 -q:v 2 output.jpg")

# Take all the screenshots (given time_delay) of the input_file
def take_screenshots(input_file, time_delay=3, movie_length=1000, path="."):
    print("time : ", time_delay)
    print("input : ", input_file)
    i = 0
    #start_time = datetime.strptime(start_time, "%H:%M:%S")
    print("DELAY START TIME : : : : : ", time_delay)

    ## Initialise start_time à 00:00:00
    start_time = datetime.min
    print("0. START TIME EST DE TYPE : ", type(start_time)) # datetime.datetime

    ## Keep only the time part (remove the Y/M/D part from datetime)
    start_time = start_time + timedelta(0, time_delay)
    print("1. START TIME EST DE TYPE : ", type(start_time)) # datetime.datetime


    print(start_time)
    print("--- END TESTING ZONE ---")
    ## END TESTING ZONE
    print("TAILLE DU FILM : ", movie_length)

    # removing the file extension and capitalizing first letter
    movie_title = os.path.splitext(input_file)[0].title()
    
    #formatted_input_file = "'" + input_file + "'"
    #print("LE TITRE FORMATTED ", formatted_input_file)

    while(i < movie_length / time_delay):
        #time.sleep(3)
        start_time_str = start_time.strftime("%H:%M:%S")
        print("2. START TIME EST DE TYPE : ", type(start_time_str))  # str


        current_movie_time = start_time_str.replace(":", "_")

        # movieTitle - currentComputerTime - movieTimeOfScreenshot
        random_name = movie_title + '-' + get_current_time() + '-' + current_movie_time


        path_file = path + "/" + input_file
        print("INPUT FILE", path_file)
        os.system(f"ffmpeg -ss {start_time_str} -i {path_file} -vframes 1 -q:v 2 {random_name}.jpg -y")
        #os.system(f"ffmpeg -ss {start_time_str} -i "f"{input_file}"" -vframes 1 -q:v 2 "f"{random_name}.jpg -y")



        ## Add time_delay seconds to start_time
        #start_time = datetime.strptime(start_time, '%H:%M:%S').time() 
        print("3. START TIME EST DE TYPE : ", type(start_time)) # <class 'datetime.time'>
        start_time = start_time + timedelta(0, time_delay)
        print("4. START TIME EST DE TYPE : ", type(start_time))

        i += 1




if __name__ == "__main__":
    # ARGUMENTS TO DEFINE
    # -i interval between each picture
    # -n name of the movie to analyze (optionnal, if not given, takes the name of the file without special characters)
    parser = argparse.ArgumentParser(
        description='List the content of a folder')
    parser.add_argument("-o", "--one", action='store_true', help="take one movie's screenshots")
    parser.add_argument("-a", "--all", action='store_true', help="take all screenshots in working directory")
    parser.add_argument("-s", "--select", action='store_true', help="take all screenshots for the selected input file")
    parser.add_argument("-chnames", "--changenames", action='store_true',
                        help="remove all whitespaces from movie files and replace them with dots in specified folder")

    parser.add_argument("-file", "--filename", help="specify the filename (needed for -o method)")
    parser.add_argument("-p", "--path", help="specify the path (needed for -a method and changing names)")
    parser.add_argument("-t", "--timedelay", help="specify the time between each screenshot (default 3)", type=int)
    args = parser.parse_args()


    if(args.one):
        # If we want to take one screenshot
        filename_nospaces = args.filename.replace(" ", "")
        take_one_screenshot(filename_nospaces, args.timedelay)

    elif(args.all):
        # If we want to take all the screenshots of all the movies contained in working directory
        # (might change to selected directory and working if no argument)
        get_current_time()
        filenames = get_filenames()
        # Print the current working directory
        print("Current working directory: {0}".format(os.getcwd()))

        for filename in filenames:
            print("Fichier : ", filename)
            folder = create_folder(filename)

            filename_nospaces = filename.replace(" ", ".")
            Path(f"./{filename}").rename(f"{folder}" + "/" + f"{filename_nospaces}")


            # Change the current working directory
            os.chdir(f'{folder}')
            cwd = os.getcwd()
            print("CURRENT WORKING DIRECTORY", cwd)
            # Get the current working directory

            length_of_video = get_length(filename_nospaces)
            if(args.timedelay):
                take_screenshots(filename_nospaces, args.timedelay, length_of_video)
            else:
                take_screenshots(filename_nospaces, movie_length=length_of_video)
            # Change the current working directory
            os.chdir('../')
    ## STEPS FOR THE ADVANCED METHOD
    # select a path where you want to analyze for movies
    # loop while movies to analyze
        # get the movie file inside the directory
        # create a specific screenshot folder inside the working directory
        # print and move the screenshots inside the specific movie folder in the working directory
    # end loop
    elif(args.select):
        print("ADVANCED METHOD")
        #filenames = get_filenames("I:\Films\FILMS[ANGLAIS]")
        filenames = get_filenames(args.path)
        print(filenames)


        for filename in filenames:
            print("Fichier : ", filename)
            filename_nospaces = filename.replace(" ", ".")
            folder = create_folder("screenshots_" + filename)
            # Change the current working directory
            os.chdir(f'{folder}')
            cwd = os.getcwd()
            print("CURRENT WORKING DIRECTORY", cwd)

            #length_of_video = get_length(f"I:\Films\FILMS[ANGLAIS]\{filename}")
            print(f"{args.path}")
            print(f"{filename}")
            print(f"{args.path}\{filename}")
            length_of_video = get_length(f"{args.path}\{filename}")
            print(f"{length_of_video}")

            #take_screenshots(filename_nospaces, args.timedelay, length_of_video, path="I:\Films\FILMS[ANGLAIS]")

            take_screenshots(filename_nospaces, args.timedelay, length_of_video, path=f"{args.path}")

            #filename_nospaces = filename.replace(" ", "")
            #*Path(f"./{filename}").rename(f"{folder}" + "/" + f"{filename_nospaces}")

            # Print the current working directory
            print("Current working directory: {0}".format(os.getcwd()))
            os.chdir('../')
    elif(args.changenames):
        print("CHANGING NAMES IN FOLDER", args.path)
        change_filenames(args.path)
    else:
        print("NO METHOD SELECTED, PLEASE ADD -a for -all, -s for select or -o for one")

    print("END OF SCRIPT")

