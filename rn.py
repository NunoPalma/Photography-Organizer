import argparse

parser = argparse.ArgumentParser(
	description='Testing')

def addArgs():
	parser.add_argument('-a', action='store_true', default=False)

def parseArgs():
	print(parser.parse_args(['-a']))

if __name__ == "__main__":
	addArgs()
	parseArgs()