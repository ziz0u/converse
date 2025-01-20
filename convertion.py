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
					row[23] = re.sub(r'(\d{2}:\d{2}:\d{2} - [.0-9]+) ', r'\1<br/>', row[23])   #I/O Wait Peaks
					row[32] = re.sub('(\\d{2}:\\d{2}:\\d{2} -> [.0-9]+) ', '\\1<br/>', row[32])  #Number of tasks currently blocked
					row[33] = re.sub('(\\d+ \\w+) ', '\\1<br/>', row[33])			#IPC facilities (MQueues-SMemory-SArrays)
					row[34] = re.sub('(\\d+ \\w+) ', '\\1<br/>', row[34])			#Process by User
					row[35] = re.sub(r'(\S+: \S+) ', r'\1<br/>', row[35])      #Network
					row[36] = re.sub('([^ ]+ MB [^ ]+) ', '\\1<br/>', row[36])      #Procs w/higher MEM consumption
				except IndexError:
					pass


			return rows

	def healthy_list(self, specifict_servers, all_data = False):
		"""
		Obtine la lista de health check de servidores desde un archivo csv separado por pipes
		(Posiblemente obsoleto en el futuro). Usará la variable estática __main__.HEALTHY_FILE.
		"""
		with open(__main__.HEALTHY_FILE, newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter='|')
			healts = []
			
			if not specifict_servers:
				return healts

			for i, row in enumerate(spamreader):
				if i == 0:
					healts.append(row)
				else:
					for server in specifict_servers.split(","):
						if row[0] == server:
							healts.append(row)

			if len(healts) <= 1 or all_data:
			    return healts

			for healt in healts:
				for index in range(1, len(healt)):
					if not index in [14, 15, 35, 36, 38, 39, 40, 41, 42,
							44, 45, 46, 48, 49, 51, 52, 53, 54,
							55, 56, 70, 71, 72, 76, 77, 80, 83,
							84, 87, 88, 91, 101,102,103,104,105,
							106,107,108,109,110,112,113,115,116,
							119,120,127,130,131,134,135,136,
							137,142,144,150,151,153,154,158,159]:
						healt[index] = "#####"

			return healts
