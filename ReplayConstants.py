#!/usr/bin/python3
"""
    Replay Toolkit
    Matt Chandler, 2018

    List of Constants:

    - Camera Prefixes
    - Event Dates : dict(namedTuple) i.e.  [Halloween] = startDate, endDate, (cam1, cam2, ..)
    -


"""
import collections


class Constants:

    BaseFolder = '/home/matt/images'
    NoActivityImageFolder = '/home/matt/NoActivityImages'

    SpecialDate = collections.namedtuple('Holiday', 'name startDate endDate camlist')
    Holidays = dict(Halloween = SpecialDate('Halloween', 'YYYY10310700', 'YYYY10311200', '0, 2, 3, 4, 5, 6, 7'))
    ThresholdChannel = 50 #value required to confirm object presence between two compared images
    ThresholdPixelCount = 4  #Numer of pixels required to exceed the threshold
    SkipVelocity = 2 #how many images to skip once object is detected
    DEBUG = True

def main():
    print("Replay Constants")
    exit(0)

def runTest():
    print("running tests...")
    exit(0)

if __name__ == "__main__":
    main()
