import csv
import os
import sys
import argparse
import re
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
#
# The html files need a unique identifier at the beginning



# name_id is what identifies the `name` field in the O2 directory. Unless OHSU
# changes the way smartweb is formatted, this shouldn't change
name_id = 'Click to view more details on this directory record'

# Names are the grandchildren of the total entry; department is another grandchild
# This pulls both and returns them in a list
# I basically lucked out that the department is the only other <a> tag
# For some reason checking against a dep_id didn't work
def get_files(dir, indicator = '.html'):
	list_of_files = []
	regex = re.compile('^' + indicator)

	for file in os.listdir(dir):
		if file.endswith('.html') & (re.match(regex, file) is not None):
			list_of_files.append(os.path.join(dir, file))
	return list_of_files

def find_dep(name):
	parent = name.parent.parent
	for link in parent.find_all('a'):
		if link.string is not name.string:
			dep = link.string
	return [name.string, dep]

def get_content(type, directory, quiet):
	files = get_files(directory, type)

	soups = []
	for file in files:
		if not quiet:
			print(f'Reading {os.path.basename(file)}')

		soups.append(bs4.BeautifulSoup(open(file), "html.parser"))

	list_of_names = []
	list_of_deps = []
	name_column = []

	for soup in soups:
		name_column = soup.find_all('a',{'title':name_id})
		for name in name_column:
			if name.string is not None:
				list_of_names.append(find_dep(name)[0])
				list_of_deps.append(find_dep(name)[1])

	if not quiet:
		print(f'Found {len(list_of_names)} employees in {len(files)} lists of {type} workers.')

	with open("%s_names_deps.csv" % (type), 'w', newline = '') as file:
			wr = csv.writer(file, quoting=csv.QUOTE_ALL)
			for i in range(0, len(list_of_names)):
				wr.writerow([list_of_names[i], list_of_deps[i]])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'A simple script to analyze SmartWeb htmls saved as ###_{i}of{n}.html')
	parser.add_argument('prefix', help = 'Prefix added to html files to be scraped')
	parser.add_argument('directory', help = 'Directory to look for lists in')
	parser.add_argument('-q', '--quiet', help = 'Don\'t print number of employees found', action = 'store_true')
	args = parser.parse_args()

	if len(sys.argv) == 1:
		sys.exit(0)
	get_content(args.prefix, args.directory, args.quiet)
