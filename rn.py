import argparse 
import os 
parser = argparse.ArgumentParser()
directory = os.getcwd() 

def rename(directory=directory): 
	i = 0
	for file in os.listdir(directory):
		file_path = directory + file

		if not validateFile(file_path):
			continue

		extension = os.path.splitext(file)[1] #There might be a better way to do this
		new_file_name = directory + str(i) + extension
		i += 1
		os.rename(file_path, new_file_name)

def validateFile(file_path):
	if os.path.isfile(file_path):
		if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')): #Figure out if the user should specify the extensions
			return True
	return False

def addArgs(): 
	parser.add_argument('-d', action='store')

def parseArgs(args):
	if args.d:
		if not os.path.isdir(args.d):
			print("Invalid directory - " + args.d)
			exit(1)
			
if __name__ == "__main__": 
	addArgs()
	args = parser.parse_args()
	parseArgs(args)
	rename(args.d)
	#rename()