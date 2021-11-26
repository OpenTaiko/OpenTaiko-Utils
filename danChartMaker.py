# -*- coding: shift-jis -*-
import sys
import optparse
import copy
import codecs
from enum import Enum
import sys
import os
import re

def eprint(*args, **kwargs): print(*args, file=sys.stderr, **kwargs)

def clamp(minval, value, maxval): return sorted((minval, value, maxval))[1]

class ExamConfiguration(Enum):
	GLOBAL = 1
	INDIVIDUAL = 2

ExamTypesDict = {
	1:'jp',
	2:'jg',
	3:'jb',
	4:'s',
	5:'r',
	6:'h',
	7:'c',
	8:'a'
}

ExamRangeDict = {
	1:'m',
	2:'l'
}

class ExamPart:
	"""Dan exam partial informations"""
	def __init__(self):
		self.examType = 'g'
		self.redPass = 0
		self.goldPass = 0
		self.examRange = 'm'
	

class Exam:
	"""Dan exam informations"""
	Parts = []
	
	def __init__(self, config, songC):
		self.configuration = config
		for i in range(songC):
			self.Parts.append(ExamPart())
			
DifficultyDict = {
	"oni":3,
	"edit":4,
	"ura":4,
	"hard":2,
	"normal":1,
	"easy":0,
	"kantan":0,
	"futsuu":1,
	"muzukashii":2,
	"extreme":3,
	"0":0,
	"1":1,
	"2":2,
	"3":3,
	"4":4
}

class Difficulty:
	"""Chart difficulty informations"""
	body = ""
	starRating = 0
	balloon = ""
	
	def __init__(self, contents):
		# Star rating
		srpattern = re.compile(r"^LEVEL:(\S+)", re.MULTILINE)
		self.starRating = re.findall(srpattern, contents)[0]
		
		# Balloon
		bpattern = re.compile(r"^BALLOON:(\S+)", re.MULTILINE)
		self.balloon = re.findall(bpattern, contents)[0]
		
		# Body
		bdpattern = re.compile(r"^#START((?:.|\n(?!#END))*)", re.MULTILINE)
		self.body = re.findall(bdpattern, contents)[0]
			
class Chart:
	"""Chart general informations"""
	difficulties = [None, None, None, None, None]
	title = ""
	subtitle = ""
	demoStart = 0
	bpm = 140
	wave = ""
	
	def __init__(self, contents):
		self.raw = contents
		
	def partition(self):
		pattern = re.compile(r"(?:^TITLE:|^COURSE:)(?:.|\n(?!COURSE))*", re.MULTILINE)
		matchlist = re.findall(pattern, self.raw)
		
		header = matchlist.pop(0)
		
		for e in matchlist:
			diffpattern = re.compile(r"^COURSE:(\S+)", re.MULTILINE)
			diff = DifficultyDict[re.findall(diffpattern, e)[0].lower()]
			self.difficulties[diff] = Difficulty(e)


if __name__ == "__main__":
	
	sys.stdout = codecs.getwriter("shift-jis")(sys.stdout.detach())

	# Header
	print("// ===== Made using 0AuBSQ's Dan Chart Maker =====\n")

	# Enumerables
	eprint("// Enter the dan song count [1-9] : ")
	songCount = clamp(1, int(input()), 9)
	eprint("// Enter the dan exam count [1-7] : ")
	examCount = clamp(1, int(input()), 7)
	
	# Chart files loading
	charts = []
	for i in range(songCount):
		eprint(f'// Enter the chart {i + 1} file name : ')
		fileName = input()
		with open(os.path.join(sys.path[0], fileName), "r", encoding="shift-jis") as f:
			charts.append(Chart(f.read()))
			
	# Chart preprocessing
	for c in charts:
		c.partition()
	
	# Exam general informations
	exams = []
	for i in range(examCount):
		if (i > 0):
			eprint(f'// Enter the dan exam {i + 1} configuration type : ')
			eprint("// 1 : Global")
			eprint("// 2 : Individual")
			examConf = clamp(1, int(input()), 2)
			exams.append(Exam(examConf, songCount))
		else:
			exams.append(Exam(1, songCount))
	
	
	#print(charts[0].raw)
	