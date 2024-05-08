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

	def healthy_list(self, specifict_servers):
		"""
		Obtine la lista de health check de servidores desde un archivo csv separado por pipes
		(Posiblemente obsoleto en el futuro). Usará la variable estática.
		"""
		with open(__main__.HEALTHY_FILE, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter='|')
			healts = []
			
			if specifict_servers:

				i = 0

				for row in spamreader:
					if i == 0:
						healts.append(row)
					else:
						for server in specifict_servers.split(","):
							if row[0] == server:
								healts.append(row)

					i = i + 1

				return healts

			return healts
