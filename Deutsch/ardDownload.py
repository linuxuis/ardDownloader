#!/bin/python2.7

'''
    Dieses programm kann Videos von der ARD Mediathek herunterladen. 
    Es wurde von tatort-dl inspiriert weil es nicht mehr funksionierte.
    http://gareus.org/wiki/tatort-dl
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


# Farben definieren
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
Dieses function drukt eine kurze hilfe menu.
'''
def usage():
	print('Usage: ardDownloader.py [-i <DokumentID>] [-q <0-3 Qualitaet->3=Hoechste>] [-o <OutputFileName.mp4>] [-p (NurDasURLDruken)]\n\nBitte geben sie das Dokument ID fuer das Video ein und (wenn moeglich) ein namen fuer das video\nz.B: python2.7 ardDownload.py -u 24619450 -q 3 -o video.mp4\n Das Dokument ID ist teil des URL: http://www.ardmediathek.de/tv/Serien-und-Spielfilme/Bornholmer-Stra%C3%9Fe/MDR-Fernsehen/Video?documentId=' + color.BOLD + color.GREEN + '24619450' + color.END+ '&bcastId=19478092')
	sys.exit(2)

'''
Function um das video URL vom JSON zu extrahieren
docID: Das dokument ID vom video URL
quality: Das Qualitaet des Video stream zum herunterladen (0=Niedrig 3= hoechste)
'''
def getVideoURL(docID, quality):
	# Website Inhalt herunterladen
	webPage= urllib2.urlopen('http://www.ardmediathek.de/play/media/'+str(docID)+'?devicetype=pc&features=flash')
	# JSON vom website speichern
	content=webPage.read()
	streamDict=json.loads(content)
	# Video URL vom JSON extrahieren 
	return str(streamDict['_mediaArray'][1]['_mediaStreamArray'][quality]['_stream'])

	
'''
Dieses function beginnt der download vom video URL mit Curl
videoURL: Das URL des Video's dass heruntergeladen werden soll
fileName: Der namen unter dem das Video gespeichert werden soll
'''
def download(videoURL, fileName):
	command='curl -C - ' + str(videoURL) + ' -o ' + str(fileName)
	os.system(command)

'''
Main function
'''
def main(argv):
	# Variables
	outFileName=None
	documentID=None
	quality=None
	printURL=False
	# Die eingaben zum Programm einlesen
	try:
		opts, args = getopt.getopt(argv,"hpi:q:o:",["documentID=","quality=", "outFile="])
	except getopt.GetoptError as err:
		usage()
	for opt, arg in opts:
		if opt == '-h':
			print('python2.7 ardDownload.py -i <Mediathek documentID> -q <qualitaet(0->niedrig - 3->hoch) Freiwillig > -o <OutputFilename_Freiwillig>')
			sys.exit(2)
		elif opt in ("-i", "--documentID"):
			documentID=arg
		elif opt in ("-o", "--outFile"):
			outFileName=arg
		elif opt in ("-q", "--quality"):
			quality=arg
		elif opt in ("-p", "--print"):
			printURL=True
	# Festlegen ob alle noetige eingaben gegeben wurden sind
	if documentID == None:
		usage()
	if outFileName == None:
		outFileName = 'ArdDump_'+datetime.datetime.now().strftime("%Y-%m-%d_%H:%M")+'.mp4'
	if quality == None:
		# Standardwert qualitaet = 3 (hoechste qualitaet)
		quality = 3

	vidURL=getVideoURL(documentID, quality)
	if printURL:
		# Nur das URL des Videos drucken
		print(vidURL + '\nQuality: '+ str(quality))
		sys.exit(0)
	download(vidURL,outFileName)
	sys.exit(0)


                

if __name__ == "__main__":
        main(sys.argv[1:])
