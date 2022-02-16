import os
import sys
import argparse
import glob
try:
	import bs4
except:
	print('You don\'t have beautifulsoup4 installed.\nTry `python -m pip install beautifulsoup4` to get it')
	sys.exit(0)

# If you can't run this script (ImportError or ModuleNotFoundError) you need to
# install BeautifulSoup. Try `python -m pip install beautifulsoup4` to install it
#
# You have to manually pull SmartWeb records from here:
# http://smartweb.ohsu.edu/smartweb/
# You'll need to be on OHSU campus---not sure if you need a login or not.
#
# When you're searching for job titles, try a few different things, because
# whatever search they're doing sucks

# Names are the grandchildren of the total entry; department is another grandchild
# This pulls both and returns them in a list
# I basically lucked out that the department is the only other <a> tag
# For some reason checking against a dep_id didn't work

def find_dep(name):
	parent = name.parent.parent
	for link in parent.find_all('a'):
		if link.string is not name.string:
			dep = link.string
	
	role = parent.find_all('td')[16].string

	return [name.string, dep, role]

def get_content(file_glob):
	# name_id is what identifies the `name` field in the O2 directory. Unless OHSU
	# changes the way smartweb is formatted, this shouldn't change
	name_id = 'Click to view more details on this directory record'

	files = glob.glob(file_glob)

	soups = []
	for file in files:
		print(f'Reading {os.path.basename(file)}')

		soups.append(bs4.BeautifulSoup(open(file), "html.parser"))

	names = []

	for soup in soups:
		name_column = soup.find_all('a',{'title':name_id})
		for name_a in name_column:
			if name_a.string is not None:
				names.append(find_dep(name_a))

	with open(f'names.csv', 'w') as f:
		f.write('First,Last,Department,Role\n')
		for name in names:
			f.write(f'{name[0]},{name[1]},{name[2]}\n')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = 'A simple script to analyze SmartWeb html files'
		)
	parser.add_argument(
		'files', help = 'Glob for files (e.g., *.htm)'
		)
	args = parser.parse_args()

	get_content(args.files)
