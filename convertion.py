import __main__
import csv
import re

class Convertion:
	"""
	Aplicara la conversion necesaria a un documento csv
	"""

	def to_list(self):
		"""
		Conviente un documento csv a una lista de arreglos
		"""

		with open(__main__.CSV_FILE_NAME, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')

			rows = []

			for row in spamreader:
				rows.append(row)
				
				try:
					row[14] = re.sub('(\\d+ \\w+) ', '\\1<br/>', row[14])
					row[15] = re.sub('([^ ]+ MB [^ ]+) ', '\\1<br/>', row[15])
				except IndexError:
					pass


			return rows
