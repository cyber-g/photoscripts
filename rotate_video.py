#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   rotate_video.py

    A (simple) library to rotate movies.

"""

#     cmd = """
#     ORIGINAL_IFS=$IFS
#     IFS=$'\n'
#     ffmpeg  -i %s -v 0  -vf "transpose=%s"  -qscale 0 -y tmp.mov && mv tmp.mov %s
#     IFS=$ORIGINAL_IFS
#     """ % (PATH, str(int(CCW)), PATH)
#

import sys, os, glob
import argparse

def rotate(PATH, CW=False):
    """
    0 = 90CounterCLockwise and Vertical Flip (default)
    1 = 90Clockwise
    2 = 90CounterClockwise
    3 = 90Clockwise and Vertical Flip
    """
    EXT = PATH.split('.')[-1]
#     print 'DEBUG: # of transpose = ', str(1+int(CW))
    cmd = 'ffmpeg  -i "%s" -v 0  -vf "transpose=%s" -qscale 0 -map_metadata 0  -codec:a copy -y "%s-tmp.%s" && mv "%s-tmp.%s" "%s"' % (PATH, str(1 + int(CW)), PATH, EXT, PATH, EXT, PATH)
    print ('DEBUG: cmd = ', cmd)
    try:
        os.system(cmd)
    except Exception as e:
        print ('Command ', cmd, ' failed, error is: ', e)

if __name__=="__main__":

    parser = argparse.ArgumentParser(
        prog="rotate_video.py",
        description='A (simple) tool to rotate movies by 90 degrees.',
        usage="python %(prog)s [-c] 'pattern'")
    
    parser.add_argument("-c", 
        help="turn video counter-clockwise --- the default is clockwise",
        action="store_true")

    parser.add_argument('file', type=argparse.FileType('r'), nargs='+')

    args = parser.parse_args()

    PATHS = args.file

    for PATH in PATHS:
        for filename in glob.glob(PATH.name):
            print ('Processing file ', filename)
            rotate(filename, args.c)
