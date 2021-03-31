# What I changed:
#       timing for not blocking input -> new problem: program is eating CPU like candy, has to sleep some
#       make output cleaner -> output i like more now <3, colors are default colors from users terminal

#! /usr/bin/env python3

import argparse
import curses
import os
import subprocess
import time

class Timer:

    starttime = None

    def __init__(self, e):

        self.to_elapse = e
    
    def start(self):
        
        self.starttime = time.time()
    
    def ended(self):

        return (time.time() - self.starttime >= self.to_elapse)

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

    global args, step, terminate, timer

    if key == 'KEY_UP':
        args.bpm = min(args.bpm + step, 300) # feEL tHe SpEd

        # reset timer to apply changes
        timer.to_elapse = 60/args.bpm
        timer.start()
        
    elif key == 'KEY_DOWN':
        args.bpm = max(args.bpm - step, 0)

        # reset timer to apply changes
        timer.to_elapse = 60/args.bpm
        timer.start()
        
    elif key == 'KEY_RIGHT':
        step = min(step + 1, 10)
        
    elif key == 'KEY_LEFT':
        step = max(step - 1, 1)
        
    elif key == 'q' or key == 'Q':
        terminate = True

    # clear stdscr or else 10 may become 100
    win.clear()

    # output put on new rows
    win.addstr(0,0,f"BPM: {args.bpm}")
    win.addstr(1,0,f"step: {step}")


def main(win):

    # I wasn't spending time changing my terminal theme to have it taken away by python
    curses.use_default_colors()

    key=None
    cycler = 0
    win.nodelay(True)

    # printing data on startup
    win.addstr(0,0,f"BPM: {args.bpm}")
    win.addstr(1,0,f"step: {step}")
    
    timer.start()

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
    
        if timer.ended():

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

            timer.start()
    
    # limit CPU usage or else the users machine will burn down -> should play with the value, there is still some fire hazard
    time.sleep(0.05)


if __name__ == '__main__':

    args = parser.parse_args()
    step = 1

    # create instance of Timer class to measure the time
    timer = Timer(60/args.bpm)

    terminate = False

    base_path = os.path.dirname(os.path.realpath(__file__))
    audio_files = [
        os.path.join(base_path, "sounds/metronomeup.wav"),
        os.path.join(base_path, "sounds/metronome.wav")
    ]
    curses.wrapper(main)
