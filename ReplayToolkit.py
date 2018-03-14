#!/usr/bin/python3
"""
    Replay Toolkit
    Matt Chandler, 2018

    This toolkit contains helper functions for:
        - Identifying images by human known times
        - Provide dynamic skip rates for image scans to assist speeding up searching for presence
        - DateTime functions for parsing camera and image file names

    Get times of day
    : Most likely activity  --
    : Most likely NOT activity

    Get known occasions
    : Breakfast
    : Lunch
    : Dinner
    : Kitchen
    : Halloween
    : Thanksgiving
    : Christmas
    : AfterSchool
    : SpecialGuests
    : Easter
    : Birthdays
    : First day of school
    : LeaveForSchool
    : HomeFromSchool


"""
from collections import namedtuple
from datetime import date
from ReplayConstants import Constants

class Toolkit:

    @staticmethod
    def GetDateTimeFromFileName(filename):
        #Given a filename YYYYMMDDHHMMSSmm.jpg, return YYYYMMDDHHMM

        parsedFilename = ""
        fileLength = len(filename)
        if fileLength>=20:
            parsedFilename = filename[fileLength-20: fileLength-4]

        return parsedFilename

    @staticmethod
    def GetFriendlyDateTimeName(filename):
        dt = GetDateTimeFromFileName(filename)

def main():
    print("Replay Toolkit")
    exit(0)

if __name__ == "__main__":
    main()
