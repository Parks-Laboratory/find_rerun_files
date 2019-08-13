import argparse
import os
try:
	import queue as queue
except:
	import Queue as queue
import re
import sys


def getMissingValues(sequence, begin, end):
	'''
	Return list of all numbers x, s.t. begin <= x <= end, and x is not in sequence
	'''

	value = sequence.get()
	# ignore values
	while value and value < begin and not sequence.empty():
		value = sequence.get()

	missing = []
	curr = begin
	while curr <= end:
		while curr != value and curr <= end:
			missing.append(curr)
			curr += 1

		curr += 1
		if not sequence.empty():
			value = sequence.get()

	return missing


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='''
	Find the missing files in a directory containing sequentially-numbered files.
	The "pattern" argument is used to extract the number from the filename, and the
	"end" argument tells the script the number of the last file to expect.
	''')

	parser.add_argument('end', type=int, help='the highest number in sequence (inclusive)')
	parser.add_argument('-b', '--begin', type=int, default=0, help='the lowest number in sequence (inclusive)')
	parser.add_argument('-p', '--pattern', default='.*[^\d](\d+).*',
		help='e.g. use (in quotes) ".*_(\d+).*"(default) or "(?<=MALE_FAT_MASS_0wks_LOG_)\d+(?=.gwas)" \
		for files like MALE_FAT_MASS_0wks_LOG_8694.gwas')
	parser.add_argument('--path', default='.', help='directory containing files')

	args = parser.parse_args()

	# extract numeric sequence from list of filenames
	sequence = queue.PriorityQueue()
	for file in os.listdir(args.path):
		match = re.search(args.pattern, file)
		# ignore files that don't match the pattern
		if match:
			try:
				sequence.put(int(match.group(1)))
			except ValueError:
				print('Non-numeric value "' + match.group(1) + '" encountered in filenames. Try a different pattern.')
				sys.exit()


	with open('failed.txt', 'w') as f:
		for val in getMissingValues(sequence, args.begin, args.end):
			f.write(str(val) + '\n')