#!/usr/bin/python3

import cv2
import numpy
import sys
from os import listdir
from os.path import isfile, join, exists
from ReplayConstants import Constants
from Configuration import Configuration
from Configuration import ImageNaming
from ReplayToolkit import Toolkit
from ReplayFileSystemToolkit import FileToolkit

"""
    CLASS OBJECTIVE:  Given a set of static images, identify ones that have presence
    INPUTS:  CameraID, SubfolderDate (YYYYMMDDHH)
    DEPENDS:  Toolkit, FileSystemToolkit, Constants, Configuration

    DESIGN:
        Scan all images in a folder, comparing current image with the next using image subtraction

        Iterate the returned collection and insert record into noSQL document:  Camera, dateTime
        Output statistics:  DateTime ranges for images found with presence.  When large amounts of activity, show time range

        REV 1:  -- Display Only, show stats, make sure script works
        --- Example script output for logging -----
             August 3, 2017:  7,300 out of 16, 784 images detected with motion.  8:03, 8:12, 10:45, 12:00-12:20
        REV 2: -- JSON Output
        {
            "CameraName" : "1",
            "Images" : [
            {
                "RelativePath" : "20170906/1400",

            }
            ]
        }
        REV 3: -- Insert into MONGO

"""
class MotionDetection:

    _cameraDateTimeSubfolder = ""
    _cameraID = 0
    _dirName = ""
    _debugMode = Configuration.DEBUG


    #Public Properties
    AllImages = []
    IndexesWithObjects = []


    def __init__(self, cameraID, cameraDateTimeSubfolder):

        self._cameraDateTimeSubfolder = cameraDateTimeSubfolder
        self._cameraID = cameraID
        self._dirName = join(Configuration.BaseFolder, ImageNaming.ImageFolderPrefixesByCamera[int(cameraID)], cameraDateTimeSubfolder[:-4], cameraDateTimeSubfolder[-4::])

        if self._validateInput() == False:
            print("Directory " + self._dirName + " does not exist.  Check configuration for camera, and ensure to use YYMMDDHHmm where mm = 00 or 30 for the minutes")
            exit(0)

    def _validateInput(self):
        if not exists(self._dirName):
            print(self._dirName + " does not exist")
            return False
        else:
            return True


    #  FUNCTION:  GetMotionDatesByCamera
    #  Search all images, return all paths and a list of indexes where motion was found
    #   : Uses OpenCV to compare two images and if the second one has changed, add it to the list
    #   : Use a threshold value because even a shadow will cause a change
    def GetMotionDatesByCamera(self):

        print('Scanning for image changes in directory: ' +  self._dirName + "\n for Camera" + self._cameraID)

        for f in listdir(self._dirName):
            fullPath = join(self._dirName,f)
            if isfile(fullPath):
                self.AllImages.append(fullPath)

        numImages = len(self.AllImages)

        self.AllImages.sort()
        countDiffs = 0

        """
            Search Algorithm:
                Scan every image, start skipping a range of images if no activity seen
        """
        sequentialNoDifferencesCount = 0
        sequentialMotionDetectedCount = 0
        skipRate = 0
        for f in range(numImages-1):

            if self._debugMode:
                print("image: " + str(f))
            if f%5:#Every five images, increase velocity if deadspace
                if sequentialNoDifferencesCount>5 : #If number of sequential images with no activity
                    if (skipRate<20):#Never skip over 20 images at a time
                        skipRate = skipRate + 2
                        if self._debugMode:
                            print("No activity found after " + str(f) + " images. Increasing skiprate to " + str(skipRate))
            if not skipRate==0 and f%skipRate:
                print("SkipRate is " + str(skipRate) + ".  Continuing")
                continue


            if f > 0 and foundDiff == False: # this is from previous image
                sequentialNoDifferencesCount = sequentialNoDifferencesCount + 1

            img1 = self.AllImages[f]
            img2 = self.AllImages[f + 1]
            # --- Compare this image with the next one
            if self._debugMode:
                #print("Comparing image: (" + str(f) + ") "+ img1  + "\n with image " + img2)
                #print("\n Size: " + str(cols) + " x " + str(rows) + " x " + str(channels))
                print  ("Scanning Image ( " + str(f) + "): " + img2)


            foundDiff = self.compareTwoImages(img1, img2)


            if (foundDiff):
                self.IndexesWithObjects.append(f) #capture the index for this image
                skipRate = 0 #skipRate - 2 #Found an image, slow the skipping down
                sequentialNoDifferencesCount = 0

                if self._debugMode:
                    print("Object detected : ")
                    #sys.stdout.write("{}".format(pixels))
                    #sys.stdout.write(" - image ")
                    imgDate = Toolkit.GetDateTimeFromFileName(img2)
                    sys.stdout.write(imgDate)
                    print(" Resetting skiprate back to zero (slowing down ...)")
                    print(" Resetting number of sequentialNoDifferenceCount back to zero")

    # Compare two images, return true if difference
    def compareTwoImages(self, fpath1, fpath2):

        foundDiff = False
        img1 = fpath1
        img2 = fpath2
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)
        diff = cv2.subtract(image2, image1)

        rows, cols, channels = diff.shape

        totalPixelDifferencesForThisImage = 0

        for row in range(rows):
            if foundDiff==True: #Difference found in this image, just stop scanning
                if self._debugMode:
                    print("Difference found for this image, going to next one...")
                break #stop iterating rows, end analysis of this image
            for col in range(cols):
                pixels = diff[row][col]
                #Look at one pixel (RGB) and see if the differences are outside the +- threshold
                if any(x>Configuration.ThresholdChannel for x in pixels):
                    totalPixelDifferencesForThisImage = totalPixelDifferencesForThisImage + 1
                    #TODO:  Consider not doing diff for whole image, but instead for a region
                    if (totalPixelDifferencesForThisImage > Configuration.ThresholdPixelCount):
                        foundDiff = True
                    break #Found some difference on this row, end analysif of this row

        return foundDiff

def main():

    if  len(sys.argv) < 3:
        print ("Usage:  program CameraID YYYYMMDDHHMM\n where CameraId= (1, 2, 3, 4, 5, 6, 7) and minute = 00 or 30")
        exit()

    cameraID = sys.argv[1]
    cameraDateTimeSubfolder = sys.argv[2]

    motionDetection = MotionDetection(cameraID, cameraDateTimeSubfolder)
    motionDetection.GetMotionDatesByCamera()

    numImages = len(motionDetection.AllImages)
    if Configuration.DEBUG == True:
        for idx, val in enumerate(motionDetection.IndexesWithObjects):
            print(Toolkit.GetDateTimeFromFileName(motionDetection.AllImages[idx])[-8::])
        print("Found " + str(len(motionDetection.IndexesWithObjects)) + " imagesWithObjects out of " + str(numImages))

    #FileToolkit.MoveInactiveFiles(cameraID, motionDatesByCamera)

if __name__ == "__main__":
    main()
