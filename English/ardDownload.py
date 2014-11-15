#!/bin/python2.7

'''
    This script is used for downloading content from ard mediathek.
    Copyright (C) 2013  Frederick Hunter fhunterz@verizon.net

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

import sys
import os
import getopt
import urllib2
import json
import datetime


# Define colors
class color:
        PURPLE = '\033[95m'
        CYAN = '\033[96m'
        DARKCYAN = '\033[36m'
        BLUE = '\033[94m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        RED = '\033[91m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        END = '\033[0m'

'''
This function prints the usage of the script
'''
def usage():
	print('Usage: ardDownloader.py [-i <DokumentID>] [-q <0-3 Quality->3=Highest>] [-o <OutputFileName.mp4>]\n\nPlease enter the document ID the video is on and (optional) provide an output filename \nEX: ardDownload.py -u 24619450 -q 3 -o video.mp4\n The document ID can be found in the url http://www.ardmediathek.de/tv/Serien-und-Spielfilme/Bornholmer-Stra%C3%9Fe/MDR-Fernsehen/Video?documentId=' + color.BOLD + color.GREEN + '24619450' + color.END+ '&bcastId=19478092')
	sys.exit(2)

'''
Function to extract the video URL from json
docID: The document ID from the viceo URL
quality: The quality of the video stream to download (0=lowest 3= highest)
'''
def getVideoURL(docID, quality):
	# download webpage content
	webPage= urllib2.urlopen('http://www.ardmediathek.de/play/media/'+str(docID)+'?devicetype=pc&features=flash')
	# retrieve the json from the webpage
	content=webPage.read()
	streamDict=json.loads(content)
	# extract the url from the json 
	return str(streamDict['_mediaArray'][1]['_mediaStreamArray'][quality]['_stream'])

	
'''
This function will begin the download of the video file using curl
videoURL: The url the video is to be downloaded from
fileName: the filename to store the video under
'''
def download(videoURL, fileName):
	command='curl -C - ' + str(videoURL) + ' -o ' + str(fileName)
	os.system(command)

'''
Main function
'''
def main(argv):
	# Placeholder if we should use a default filename
	outFileName=None
	documentID=None
	quality=None
	printURL=False
	# Get the arguments for the function
	try:
		opts, args = getopt.getopt(argv,"hpi:q:o:",["documentID=","quality=", "outFile="])
	except getopt.GetoptError as err:
		usage()
	for opt, arg in opts:
		if opt == '-h':
			print('python2.7 arDownload.py -i <Mediathek documentID> -q <quality(0->low - 3->high) Optional > -o <OutputFilename_Optional>')
			sys.exit(2)
		elif opt in ("-i", "--documentID"):
			documentID=arg
		elif opt in ("-o", "--outFile"):
			outFileName=arg
		elif opt in ("-q", "--quality"):
			quality=arg
		elif opt in ("-p", "--print"):
			printURL=True
	# Determine if the necessary arguments have been imputted
	if documentID == None:
		usage()
	if outFileName == None:
		outFileName = 'ArdDump_'+datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")+'.mp4'
	if quality == None:
		# Default quality = 3 (highest)
		quality = 3

	vidURL=getVideoURL(documentID, quality)
	if printURL:
		# Just print the url for the video and exit
		print(vidURL + '\nQuality: '+ str(quality))
		sys.exit(0)
	download(vidURL,outFileName)
	#usage()
	sys.exit(0)


                

if __name__ == "__main__":
        main(sys.argv[1:])
