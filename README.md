## Screenshot Engine (screenshot_engine.py)
This script was made to automate taking screenshots of videos and specifically movies. I wanted to save the most cool and impressive scenes from.
It was initially meant to work in collaboration with my filmobot project but feel free to use it for other things.

## Requirements
- ffmpeg (script has been tested with ffmpeg version n4.4-15-ge87e006121 on Windows 10 but should work for any version)
- python (script has been tested with Python 3.9.1 on Windows 10 but should work for any Python 3.X version)


## Guide
### Pre-requisites (reminder)
Execute this program using a terminal.
As specified before you need Python and ffmpeg installed for this to work


### Arguments
Multiple parameters exists and some can work in combination.

#### Change file names (can be important)
- -chnames : allows you to change the names of video files replacing spaces by . so everything is working properly 
for -chnames to work you need to specify -p which is the path of the folder you want to modify the video files name from.


#### Take screenshots
- -a or --all : take screenshots of all the video files in the current folder (the folder where this script is contained), that way you can move the script and execute it from wherever you want easily.
- -s or --select : take screenshots of all the video files in the specified folder, that way you can put the script somewhere and have it work on a folder elsewhere.
- -o or --one : take one screenshot from one specified videofile at the specified time.


#### Paths, filenames and timedelays

- -f or --filename : specify the filename you want to take screenshots from (for -o)
- -p or --path : specify the path where your video files are, every video file contained in the root of the specified folder will get screenshots taken from (for -chnames and -s)
- -t or --timedelay : specify the time betewen each screenshot (for -o, -a and -s)


### Examples

- I want to take a screenshot every 3 seconds for the videos contained in the specified folder
```
python .\screenshot_engine.py -chnames -p C:\Users\Thomas\Art\Videos
python .\screenshot_engine.py -s -p C:\Users\Thomas\Art\Videos -t 3
```

- I want to take one screenshot at the specified time (1000 secondes) from one video
```
python .\screenshot_engine.py -o -f C:\Users\Thomas\Art\my.video.mp4 -t 1000
```

- I want to take a screenshot every 5 seconds from videos in the working folder (folder where this script is)
```
python .\screenshot_engine.py -a -t 5
```