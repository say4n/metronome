#! /usr/bin/env python3

import argparse
import curses
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


def on_keypress(key, win):
    global args, step, terminate

    if key == 'KEY_UP':
        args.bpm = min(args.bpm + step, 240)
        win.addstr(f"BPM: {args.bpm}")
    elif key == 'KEY_DOWN':
        args.bpm = max(args.bpm - step, 0)
        win.addstr(f"BPM: {args.bpm}")
    elif key == 'KEY_RIGHT':
        step = min(step + 1, 10)
        win.addstr(f"step: {step}")
    elif key == 'KEY_LEFT':
        step = max(step - 1, 1)
        win.addstr(f"step: {step}")
    elif key == 'q' or key == 'Q':
        terminate = True


def main(win):
    cycler = 0
    key = None
    win.nodelay(True)

    while True:
        if terminate:
            curses.endwin()
            break

        try:
            key = win.getkey()
            win.refresh()
            on_keypress(key, win)
        except Exception:
            pass

        if cycler % args.cycles == 0:
            # play beep
            subprocess.Popen(["ffplay", "-nodisp", "-autoexit",
                              audio_files[0]],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.STDOUT)
        else:
            # play bop
            subprocess.Popen(["ffplay", "-nodisp", "-autoexit",
                              audio_files[1]],
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.STDOUT)

        cycler = (cycler + 1) % args.cycles

        pause = 60/args.bpm
        time.sleep(pause)


if __name__ == '__main__':
    args = parser.parse_args()
    step = 1
    terminate = False

    base_path = os.path.dirname(os.path.realpath(__file__))
    audio_files = [
        os.path.join(base_path, "sounds/metronomeup.wav"),
        os.path.join(base_path, "sounds/metronome.wav")
    ]

    curses.wrapper(main)
