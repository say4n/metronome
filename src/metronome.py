#! /usr/bin/env python3

import argparse
import os
import subprocess
import time


parser = argparse.ArgumentParser(description="a cli metronome utility")
parser.add_argument("-b",
                    "--bpm",
                    help="beats per minute",
                    type=int,
                    default=60)
parser.add_argument("-c",
                    "--cycles",
                    help="beats per cycle",
                    type=int,
                    default=4)

args = parser.parse_args()

pause = 60/args.bpm
cycler = 0

base_path = os.path.dirname(os.path.realpath(__file__))
audio_files = [
    os.path.join(base_path, "sounds/metronomeup.wav"),
    os.path.join(base_path, "sounds/metronome.wav")
]


while True:
    if cycler % args.cycles == 0:
        # play beep
        subprocess.Popen(["ffplay", "-nodisp", "-autoexit", audio_files[0]],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    else:
        # play bop
        subprocess.Popen(["ffplay", "-nodisp", "-autoexit", audio_files[1]],
                         stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    cycler = (cycler + 1) % args.cycles

    time.sleep(pause)
