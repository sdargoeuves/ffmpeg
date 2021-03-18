"""
This script allows you to convert MKV to AVI video, using H.264,
likely to be compatibled with TV where H265 is not available.
"""
import os
import sys
import argparse
import time
import re

def video_length(filename):
    """
    This return the length of a video and number of frames
    Not yet in use...
    """
    from cv2 import cv2
    #video = cv2.VideoCapture(filename)
    #duration = video.get(cv2.CAP_PROP_POS_MSEC) ## return ''???
    #frame_count = video.get(cv2.CAP_PROP_FRAME_COUNT)
    #return duration, frame_count
    cap = cv2.VideoCapture(filename)
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps

    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration/60)
    seconds = duration%60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

def select_folder():
    """
    Function to return the path you have selected through the GUI
    Not yet in use...
    """
    from tkinter import Tk
    from tkinter import filedialog
    #from tkinter.filedialog import askdirectory
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory(title='Select Folder')
    #path = askdirectory(title='Select Folder')
    return path


def mkv2avi(path, output_str=None):
    """
    This script allows you to convert MKV to AVI video, using H.264,
    likely to be compatibled with TV where H265 is not available.
    """
    #Create list of MKV files
    list_file = []
    print("here is the list of files to be converted:")
    for filename in os.listdir(path):
        if filename[-4:] == ".mkv":
            file = os.path.join(path,filename)
            list_file.append(file)
            print(filename)
    #Ask for confirmation before converting the video(s)
    try:
        entry_value = str(input("Are you happy to proceed (Y/[N])? "))
    except KeyboardInterrupt:
        sys.exit("\nExit due to user request -- Come back soon")
    if entry_value in ["y","Y","yes","YES"]:
        for file in list_file:
            #if we specified an output format, we search for S00E00
            if output_str is not None:
                try:
                    episode = re.search(r'[sS]\d+[Ee]\d+',file).group(0).upper()
                    output = "".join([path,output_str,episode,".avi"])
                except AttributeError:
                    #If there is no S00E00 in the filename, we will have an error.
                    # we can offer to retry without the option -o
                    try:
                        retry_err = str(input(f'\nERROR - S00E00 cannot be found in the source filename: {file}\
                            \nDo you want to try again without -o option (Y/[N])?'))
                    except KeyboardInterrupt:
                        sys.exit("\nExit due to user request -- Come back soon")

                    if retry_err in ["y","Y","yes","YES"]:
                        output = "".join([file[:-4],".avi"])
                    else:
                        sys.exit("\nExit due to user request -- Retry aborted")
                #output = "".join([path,output_str,episode,".avi"])
            #otherwise we keep the same name but change the extension
            else:
                output = "".join([file[:-4],".avi"])
            command = f'ffmpeg -i "{file}" -c:v libx264 "{output}"'
            print(f'Command exectued:\n{command}')
            exec_time = time.time()
            #time.sleep(2)
            os.system(command)
            print("--- %s minutes ---" % (round((time.time() - exec_time)/60,2)))
    else:
        print('No action requested -- Come back soon')

if __name__ == "__main__":
    start_time = time.time()
    parser = argparse.ArgumentParser(description=
            "Specify the path where the videos are.\
            \nThe output will be in the same folder")
    parser.add_argument("path", help="Path", type=str)
    parser.add_argument("-o", "--output_str", help="Define how you want the \
    output files to be named i.e. \"Reign-\" will become Reign-S02E22.avi", type=str)
    args = parser.parse_args()
    mypath = args.path
    myoutput_str = args.output_str

    if os.path.isdir(mypath):
        mkv2avi(mypath, myoutput_str)
    #Display time to execute
    print("--- TOTAL TIME ---\n--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
    print("-or %s seconds ---" % (round(time.time() - start_time,2)))
