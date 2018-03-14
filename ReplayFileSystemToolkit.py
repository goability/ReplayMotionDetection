#!/user/bin/python3

from Configuration import Configuration
from ReplayConstants import Constants

import os

class FileToolkit:

    @staticmethod
    def MoveInactiveFiles(cameraID, cameraDateTimeSubfolder, imageDatesWithMotion):
    """
        Iterate entire cameraDateTimeSubfolder, skipping files in imageDatesWithMotion

    """
        if Constants.DEBUG:
            print("Moving " + len(fileList) + " inactive files to folder: " + Configuration.NoActivityImageFolder)
#        for f in fileList:
#            os.rename(old, new)



def main():
    print("Replay file system helperConfigurations")

if __name__ == "__main__":
    main()
