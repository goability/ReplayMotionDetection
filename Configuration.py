#!/usr/bin/python

from ReplayConstants import Constants
"""
    Load configuration

    rev1 - from constants class
    rev2 - from mongo document


"""
class ImageNaming:
    ImageFileNameDateTimeLength = 16 #YYYY MMDD HHMM SSmm
    ImageFileExtension = ".jpg"
    ImageFolderPrefixesByCamera = {1 : 'IMPORT', 2 : 'ImportCam2', 3 : 'ImportCam3', 4 : 'IMPORTCam4', 5 : 'ImportCam5', 6 : 'ImportCam6', 7 : 'ImportCam7'}
    ImageFileNamePrefixesByCamera = {1 : 'camKitchen', 2 : 'camera1', 3 : 'cam3', 4 : 'cam4', 5 : 'cam5', 6 : 'cam6', 7 : 'cam7'}

class Configuration:

    imageNaming = ImageNaming
    DEBUG = True #Turns on logging and debug messages
    BaseFolder = Constants.BaseFolder
    NoActivityImageFolder = Constants.NoActivityImageFolder
    SpecialDate = Constants.SpecialDate
    Holidays = Constants.Holidays
    #value required to confirm object presence between two compared images
    ThresholdChannel = Constants.ThresholdChannel
    #Numer of pixels required to exceed the threshold
    ThresholdPixelCount = Constants.ThresholdPixelCount
    #how many images to skip once object is detected
    SkipVelocity = Constants.SkipVelocity


if __name__ == "__main__":
    main()
