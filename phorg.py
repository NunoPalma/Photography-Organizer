import argparse 
import os
import exifread
from shutil import copy


############# general auxiliary methods #############

"""
Checks if the given file_path leads to a valid file type.

@param String file_path
@return a boolean value	-	True if the file_path is valid
						-	False if it isn't
"""
def validate_file(file_path):
	if os.path.isfile(file_path):
		if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.cr2')): #Figure out if the user should specify the extensions
			return True
	return False


"""
Defines how command-line arguments should be parsed and creates the desired parser.
@return ArgumentParser parser
"""
def create_parser():
	parser = argparse.ArgumentParser()
	sub_parsers = parser.add_subparsers()
	rename_parser = sub_parsers.add_parser('rn')
	rename_parser.set_defaults(which='rn')
	organization_parser = sub_parsers.add_parser('org')
	organization_parser.set_defaults(which='org')
	
	rename_parser.add_argument('-d', metavar='directory', type=str, action='store', default=os.getcwd(),
									help='Desired directory. If no directory is given, the current directory is used.')
	rename_parser.add_argument('-p', metavar='prefix', type=str, action='store', default='',
									help='Desired prefix.')
	rename_parser.add_argument('-v', metavar='value', type=str, action='store', default='0',
									help='The desired starting value.')

	organization_parser.add_argument('-d', metavar='directory', type=str, action='store', default=os.getcwd(), 
											help='Desired directory. If no directory is given, the current directory is used.')
	organization_parser.add_argument('-f', metavar='folder', type=str, action='store', 
											help='Name of the main folder where the organized folders will be stored. \
												If no name is provided then the default name will be \'organized_by<organization method>\'')
	organization_parser.add_argument('organization_method', type=str, action='store', choices=['day', 'month', 'year', 'shutter_speed', 'lens', 'aperture', 'ISO', 'focal_length'], 
											help='Organize the content by one of the following parameters.')

	return parser


"""
Validates the given arguments.
@param ArgumentParser args
"""
def parse_args(args):
	if args.d:
		if not os.path.isdir(args.d):
			print("Invalid directory - " + args.d)
			exit(1)
		if not args.d.lower().endswith('/'):
			args.d += '/'

	if args.p:
		try:
			if '/' in args.p:
				raise Exception('Invalid prefix - ' + args.p + '\nThe prefix can\'t contain the following character: \'/\'')
		except Exception as e:
			print(e)
			exit(1)

#####################################################


############# rn - rename related methods #############

"""
Renames the files in the given directory args.d
@param ArgumentParser args
"""
def rename(args):
	i = args.v
	for file in os.listdir(args.d):
		file_path = args.d + file
		if not validate_file(file_path):
			continue
		extension = os.path.splitext(file)[1] #There might be a better way to do this
		new_file_name = args.d + args.p + i + extension
		i = next_value(i)
		try:
			os.rename(file_path, new_file_name)
		except FileExistsError:
			print('A file with the name ' + new_file_name + ' already exists.')


"""
@param String/int value
@return The correspondent adjacent value to value.
"""
def next_value(value):
	if value[0] >= '0' and value[0] <= '9':
		value = int(value) + 1
		return str(value)
	elif value[0] >= 'A' and value[0] <= 'Z':
		return aux(value, ['A', 'Z'])
	else:
		return aux(value, ['a', 'z'])


"""
Auxiliary method to next_value, if the given value is a String
Returns the correspondent adjacent value to value.
@param String value
@param List<String> limit => [lower_limit, upper_limit]
"""
def aux(value, limit):
	if value == '':
		return limit[0]
	if value[-1] == limit[1]:
		return aux(value[:-1], limit) + limit[0]
	else:
		return value[:-1] + chr(ord(value[-1]) + 1)

#######################################################


###########  org - organize related methods  ##########

"""
Specifies which processing method is used depending on the organization method.
@param ArgumentParser args
"""
def organize_data(args):
	if args.organization_method == 'year':
		organize(args, ['DateTimeOriginal', 'EXIF DateTimeOriginal', 1], process_date_time_data)
	elif args.organization_method == 'month':
		organize(args, ['DateTimeOriginal', 'EXIF DateTimeOriginal', 2], process_date_time_data)
	elif args.organization_method == 'day':
		organize(args, ['DateTimeOriginal', 'EXIF DateTimeOriginal', 3], process_date_time_data)
	elif args.organization_method == 'shutter_speed':
		organize(args, ['ExposureTime', 'EXIF ExposureTime'], process_shutter_speed_data)
	elif args.organization_method == 'lens':
		organize(args, ['LensModel', 'EXIF LensModel'], process_lens_model_data)
	elif args.organization_method == 'aperture':
		organize(args, ['FNumber', 'EXIF FNumber'], process_aperture_data)
	elif args.organization_method == 'ISO':
		organize(args, ['ISOSpeedRatings', 'EXIF ISOSpeedRatings'], process_ISO_data)
	elif args.organization_method == 'focal_length':
		organize(args, ['FocalLength', 'EXIF FocalLength'], process_focal_length_data)


"""
@param ArgumentParser args
@param List data_info
@param method process_data
"""
def organize(args, data_info, process_data):
	if not args.f:
		organization_folder = 'organized_by_' + args.organization_method + '/'
	else:
		if not args.f.endswith('/'):
			organization_folder = args.f + '/'
		else:
			organization_folder = args.f

	try:
		os.mkdir(args.d + organization_folder)
	except FileExistsError:
		print('The given file name ' + args.d + organization_folder + ' already exists.')

	for file in os.listdir(args.d):
		file_path = args.d + file
		if not validate_file(file_path):
			continue

		data = get_image_data(file_path, data_info[0], data_info[1])
		data = process_data(data, data_info)
	
		path = args.d + organization_folder + data
		if not os.path.isdir(path):
			os.mkdir(path)

		copy(file_path, path)	


"""
Processes the image at the given path.
@param String image_path
@param String stop_tag
@param String data_field
@return String Data from the correspondent data_field
"""
def get_image_data(image_path, stop_tag, data_field):
	with open(image_path, 'rb') as image:
		tags = exifread.process_file(image, stop_tag=stop_tag, details=False)
		return str(tags[data_field])


def process_date_time_data(data, data_info):
	return '-'.join(data.replace(' ', ':').split(':')[:data_info[2]])


def process_shutter_speed_data(data, data_info):
	return '-'.join(data.split('/')) + 's'


def process_lens_model_data(data, data_info):
	return '-'.join(data.split('/'))


def process_ISO_data(data, data_info):
	return data


def process_focal_length_data(data, data_info):
	return data + 'mm'


def process_aperture_data(data, data_info):
	data = data.split('/')
	if len(data) == 2:
		return str(float(data[0]) / float(data[1]))
	
	return data[0]


#######################################################

def main():
	parser = create_parser()
	args = parser.parse_args()
	parse_args(args)

	if args.which == 'rn':
		rename(args)
	else:
		organize_data(args)		

if __name__ == "__main__": 
	main()