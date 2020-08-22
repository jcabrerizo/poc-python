#!/usr/bin/python3
import datetime as dt
import os
import argparse
import getpass

from picamera import PiCamera #1.13
from time import sleep

where = None
logname = '.photothug.log'
picturesToTake = 3

def setup(args):
    global where, picturesToTake
    
    picturesToTake = args.number
        
    where = args.path
    if not where.endswith("/"): where +="/"
    if not os.path.exists(where):
        os.makedirs(where)

def cleanup():
    global where
    picturesRemoved = 0
    if os.path.exists(where + logname):
        for filename in os.listdir(where):
            if filename.endswith(".jpg") and os.path.isfile(where + filename):
                os.remove(where + filename)
                picturesRemoved +=1
        print(f"Photothug removed {picturesRemoved} old pictures from {where}'")
    else:
        print(f"No {where}{logname} found. Ignoring clean up")

def configArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path",
                        help = "Path to store the pictures",
                        default = ".")
    parser.add_argument("-c", "--cleanup",
                        help = "Remove old pictures",
                        action = "store_true",
                        )
    parser.add_argument("-d", "--delay",
                        help = "Delay between pictures in seconds",
                        default=1,
                        type= int
                        )
    parser.add_argument("-n", "--number",
                        help = "Number of pictures to take",
                        default=4,
                        type= int
                        )
    parser.add_argument("--height",
                        help = "Image height",
                        default=320,
                        type= int
                        )
    parser.add_argument("--width",
                        help = "Image width",
                        default=240,
                        type= int
                        )        
    return parser.parse_args()

args = configArgumentParser()
print("Starting photothug")
with PiCamera(resolution=(args.width, args.height)) as camera:
    setup(args)
    if args.cleanup:
        cleanup()
    
    with open(where + logname, 'a') as log:
        log.write(f"Start capturing at {dt.datetime.now().strftime('%y%m%dT%H%M')} by {getpass.getuser()}\n")
        camera.start_preview(alpha=190)
        for i in range(picturesToTake):
            filename = f"IMG_{dt.datetime.now().strftime('%y%m%dT%H%M%S')}_{i}"
            camera.capture('%s%s.jpg' % (where, filename))
            log.write(f"\tCaptured {filename}.jpg\n")
            sleep(args.delay)
        camera.stop_preview()
    log.close()
    
print(f"Photothug ended after {picturesToTake} 'jobs'")
exit(0)

