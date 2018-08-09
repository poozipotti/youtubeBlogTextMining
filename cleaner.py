import os, fnmatch, re, string, sys

#the directory of cleaner.py
pattern = "*.*"
#we dont need this yet but python is fun
#print theDir
def scrubTags(dirtyString):
	cleanString = re.sub("<.*>","",dirtyString)
	cleanString = cleanString.translate(None,string.punctuation)
	cleanString = re.sub("\s\s+"," ", cleanString)
	cleanString = cleanString.replace("\n","")
	return cleanString

#this will look for a match in the line so any unique identifier will so
sectionsToSave = ["class=\'post-content\'","class=\'publishdate\'"]	

#filenemaes should be relative to wherever this script is
#we know that the date is in a span so after we get a span write a comma
#this is very brittle so it may have to be changed later
def cleanStandardBlogPost(filename):
	readFile = open(filename,"r")
	writeFile = open("CLEAN_BLOG.csv","a+")
	shouldWrite = False
	innerDivs = 0
	for line in readFile:
		for sectionIdentifier in sectionsToSave:
			if	sectionIdentifier in line:
				shouldWrite = True
		if shouldWrite:
			writeFile.write(scrubTags(line))
			if "<div" in line or "<span" in line:
				innerDivs += 1
			if "</div>" in line or "</span" in line:
				if innerDivs == 0:
					writeFile.write(",")
					shouldWrite = False
				innerDivs -= 1
	writeFile.write("\n")
	readFile.close()
	writeFile.close()

		
			
def addAllFiles(folder):
	try:
		theDir = os.listdir(folder)
		files = (list(map( lambda fileName: folder + "/" + fileName,theDir)))
		directories = (list(filter(lambda directoryEntry: ".html" not in directoryEntry,files)))
		files = (list(filter(lambda directoryEntry: (".html" in directoryEntry) and ("?" not in directoryEntry) and ("index" not in directoryEntry) , files)))
		#print files
		for htmlFile in files:
			cleanStandardBlogPost(htmlFile)
			print "finished parsing " + htmlFile
		for directory in directories:
			addAllFiles(directory) 
	except Exception as e:
		print e

#this is the stuff that actually runs once when the file is called from the command line
if os.path.exists("CLEAN_BLOG.csv"):
	os.remove("CLEAN_BLOG.csv")
addAllFiles(sys.argv[1])
