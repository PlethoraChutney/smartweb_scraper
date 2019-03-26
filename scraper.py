import csv
import os
import sys
import argparse
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

# Save the html files with the format '***_$of#.html', where *** is some string
# of any length that identifies which job title you searched, # is the total
# number of pages you downloaded, and $ is whatever the current page is
# For instance, 'RA_1of10.html'
#
# If you want to change this format it's used in get_content() and you'll have
# to update the argument parsing as well.


# name_id is what identifies the `name` field in the O2 directory. Unless OHSU
# changes the way smartweb is formatted, this shouldn't change
name_id = 'Click to view more details on this directory record'

# I'm assuming you've structured your directory like this, with union_shit being
# whatever your parent directory is:
# .../union_shit/scraper.py
# .../union_shit/lists/*.html
# Lists made with this script would, in this case, end up in .../union_shit
path = os.getcwd()


# Names are the grandchildren of the total entry; department is another grandchild
# This pulls both and returns them in a list
# I basically lucked out that the department is the only other <a> tag
# For some reason checking against a dep_id didn't work

def find_dep(name):
	parent = name.parent.parent
	for link in parent.find_all('a'):
		if link.string is not name.string:
			dep = link.string
	return [name.string, dep]

def get_content(type, max, quiet):
	content_list = []
	num = []

	if max > 1:
		num = range(1,max+1)
	else:
		num = [1]

	for i in num:
		content_list.append(os.path.join(path,'lists',"%s_%iof%i.html" % (type, i, max)))

	soups = []
	for content in content_list:
		soups.append(bs4.BeautifulSoup(open(content), "html.parser"))

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
		print(f'Found {len(list_of_names)} employees in {max} lists of {type} workers.')

	with open("%s_names_deps.csv" % (type), 'w', newline = '') as file:
			wr = csv.writer(file, quoting=csv.QUOTE_ALL)
			for i in range(0, len(list_of_names)):
				wr.writerow([list_of_names[i], list_of_deps[i]])

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description = 'A simple script to analyze SmartWeb htmls saved as ###_{i}of{n}.html')
	parser.add_argument('prefix', help = 'Prefix added to html files to be scraped')
	parser.add_argument('number', help = 'Number of html files to scrape', type = int)
	parser.add_argument('-q', '--quiet', help = 'Don\'t print number of employees found', action = 'store_true')

	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(0)

	args = parser.parse_args()
	get_content(args.prefix, args.number, args.quiet)
