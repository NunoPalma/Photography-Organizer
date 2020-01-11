import argparse 
import os 
parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers()
rename_parser = sub_parsers.add_parser('rn')
order_parser = sub_parsers.add_parser('order')

directory = os.getcwd() 

def rename(args):
	i = args.v
	for file in os.listdir(args.d):
		file_path = args.d + file
		if not validate_file(file_path):
			continue
		extension = os.path.splitext(file)[1] #There might be a better way to do this
		new_file_name = args.d + args.p + i + extension
		i = next_value(i)
		os.rename(file_path, new_file_name)


def next_value(value):
	if value[0] >= '0' and value[0] <= '9':
		value = int(value) + 1
		return str(value)
	elif value[0] >= 'A' and value[0] <= 'Z':
		return aux(value, ['A', 'Z'])
	else:
		return aux(value, ['a', 'z'])


def aux(value, limit):
	if value == '':
		return limit[0]
	if value[-1] == limit[1]:
		return aux(value[:-1], limit) + limit[0]
	else:
		return value[:-1] + chr(ord(value[-1]) + 1)


def validate_file(file_path):
	if os.path.isfile(file_path):
		if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')): #Figure out if the user should specify the extensions
			return True
	return False


def add_args():
	rename_parser.add_argument('-d', type=str, action='store', default=directory, help='Desired directory. If no directory is given, the current directory is used.')
	rename_parser.add_argument('-p', type=str, action='store', default='', help='Desired prefix.')
	rename_parser.add_argument('-v', type=str, action='store', default='0', help='The desired starting value.')


def parse_args(args):
	if args.d:
		if not os.path.isdir(args.d):
			print("Invalid directory - " + args.d)
			exit(1)
		if not args.d.lower().endswith('/'):
			args.d += '/'


def main():
	add_args()
	args = parser.parse_args()
	parse_args(args)
	rename(args)


if __name__ == "__main__": 
	main()