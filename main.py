import sys
import os
from optparse import OptionParser

VALID_FILE_EXTENSIONS = (
	'py',
)

IMPORT_KEYWORDS = (
	'from',
	'import',
)


class ImportAnalyzer(object):

	def __init__(self, verbosity=1):
		self.found = {}

		self.verbosity = verbosity


	def run(self, root):
		if not os.path.isdir(root):
			raise Exception("%s doesn't exist." % root)
		self.check_files(root)

	def show_occurance_count(self):
		for k, values in self.found.iteritems():
			print k, len(values)

	def update_found(self, key, filename):
		try:
			self.found[key].append(filename)

		except KeyError:
			self.found[key] = [filename]


	def _log(self, message, verbosity=1):
		if self.verbosity >= verbosity: print message


	def check_file(self, filename):
		self._log("Checking %s" % filename, 2)
		with open(filename, 'r') as f:
			for count, line in enumerate(f.readlines()):
				found = self.check_line(line)
				if found:
					self.update_found(found, filename + "[Line %d]" % count)


	def check_files(self, root):
		for dir_name, _, filenames in os.walk(root):
			for filename in filenames:
				if filename.split('.')[-1] in VALID_FILE_EXTENSIONS:
					self.check_file(dir_name + "/" + filename)


	def check_line(self, line):
		current_pos = 0
		start_consumption = 0
		eating = False
		found = []
		is_comment = False

		while True:
			if current_pos >= len(line):
				break

			if line[current_pos] == '#':
				break

			if eating:
				char = line[current_pos]
				if not char.isalpha():
					break
				found.append(char)

			if not eating:
				for kw in IMPORT_KEYWORDS:
					l = len(kw)
					if line[current_pos:l] == kw:
						eating = True
						current_pos += l

			current_pos += 1

		return ''.join(found)




if __name__ == '__main__':

	parser = OptionParser()
	parser.add_option("-r", "--root", dest="root",
	                  help="Analyze python imports for directory ROOT", metavar="ROOT")

	parser.add_option("-v", "--verbosity", dest="verbosity", default=1,
	                  help="Set vebosity")


	(options, args) = parser.parse_args()

	if not options.root:
		print 'Need to specify a -r/--root.'

	ia = ImportAnalyzer(options.verbosity)
	ia.run(options.root)

	ia.show_occurance_count()

 



