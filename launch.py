import argparse
import subprocess
import pipes
import os

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", help="Rout to the file, containing the list of video file names.")
args = vars(ap.parse_args())

with open(args["file"]) as f:
    for name in f:
        name = f"{os.getcwd()}/app/jigsaws/Knot_Tying/video/{name}"
        name1 = f"{os.getcwd()}/app/jigsaws/Knot_Tying/video/{next(f)}"

        finished = False
        while not finished:
            subprocess.run(["python3", "app/main.py", "-vl", pipes.quote(name.strip('\n')), "-vr", pipes.quote(name1.strip('\n'))])
            answer = input("Is the process complete? Y/N")
            if answer == 'Y' or answer =='y':
                finished = True
