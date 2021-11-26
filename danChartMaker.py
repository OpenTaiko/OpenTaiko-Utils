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
	def __init__(self, config, songC):
		self.configuration = config
		self.Parts = []
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
	
	def __init__(self, contents):
		self.body = ""
		self.starRating = 0
		self.balloon = ""
	
		# Star rating
		srpattern = re.compile(r"^LEVEL:(\S+)", re.MULTILINE)
		self.starRating = re.findall(srpattern, contents)[0]
		
		# Balloon
		bpattern = re.compile(r"^BALLOON:(\S+)", re.MULTILINE)
		bmatch = re.findall(bpattern, contents)
		self.balloon = ""
		if (len(bmatch) > 0):
			self.balloon = re.findall(bpattern, contents)[0]
		
		# Body
		bdpattern = re.compile(r"^#START((?:.|\n(?!#END))*)", re.MULTILINE)
		self.body = re.findall(bdpattern, contents)[0]
			
class Chart:
	"""Chart general informations"""

	def __init__(self, contents):
		self.raw = contents
		self.difficulties = [None, None, None, None, None]
		self.title = ""
		self.subtitle = ""
		self.demoStart = 0
		self.bpm = 140
		self.wave = ""
		self.offset = 0
		
	def partition(self):
		# General split
		pattern = re.compile(r"(?:^TITLE:|^COURSE:)(?:.|\n(?!COURSE))*", re.MULTILINE)
		matchlist = re.findall(pattern, self.raw)
		
		# Header extraction
		header = matchlist.pop(0)
		
		# Title
		tpattern = re.compile(r"^TITLE:(.*)", re.MULTILINE)
		self.title = re.findall(tpattern, header)[0]
		
		# Demo start
		dspattern = re.compile(r"^DEMOSTART:(\S+)", re.MULTILINE)
		self.demoStart = re.findall(dspattern, header)[0]
		
		# Bpm
		bpattern = re.compile(r"^BPM:(\S+)", re.MULTILINE)
		self.bpm = re.findall(bpattern, header)[0]
		
		# Wave
		wpattern = re.compile(r"^WAVE:(\S+)", re.MULTILINE)
		self.wave = re.findall(wpattern, header)[0]
		
		# Offset
		opattern = re.compile(r"^OFFSET:(\S+)", re.MULTILINE)
		self.offset = float(re.findall(opattern, header)[0]) * -1;
		
		# Subtitle
		stpattern = re.compile(r"^SUBTITLE:--(.*)", re.MULTILINE)
		self.subtitle = re.findall(stpattern, header)[0]
		
		# Extract difficulties
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
	
	# Dan header
	eprint("// Enter the dan chart name : ")
	chartName = input()
	
	# Global exams
	nonGlobalIndexes = []
	globalIndexes = []
	for i in range(examCount):
		if (exams[i].configuration == 1):
			if (i == 0):
				eprint("// Enter the Gauge exam red condition [0-100] : ")
				exams[i].Parts[0].redPass = clamp(0, int(input()), 100)
				eprint(f"// Enter the Gauge exam gold condition [{exams[i].Parts[0].redPass}-100] : ")
				exams[i].Parts[0].goldPass = clamp(exams[i].Parts[0].redPass, int(input()), 100)
			else:
				eprint(f"// Enter the exam {i + 1} type : ")
				eprint("// 1 : Perfect count")
				eprint("// 2 : Good count")
				eprint("// 3 : Bad count")
				eprint("// 4 : Score")
				eprint("// 5 : Rolls")
				eprint("// 6 : Hit notes")
				eprint("// 7 : Combo")
				eprint("// 8 : Accuracy")
				tmp = clamp(1, int(input()), 8)
				exams[i].Parts[0].examType = ExamTypesDict[tmp]
				eprint(f"// Enter the exam {i + 1} range : ")
				eprint("// 1 : More")
				eprint("// 2 : Less")
				tmp = clamp(1, int(input()), 2)
				exams[i].Parts[0].examRange = ExamRangeDict[tmp]
				eprint(f"// Enter the exam {i + 1} red condition [0-[ : ")
				exams[i].Parts[0].redPass = clamp(0, int(input()), 999999)
				if (exams[i].Parts[0].examRange == "m"):
					eprint(f"// Enter the exam {i + 1} gold condition [{exams[i].Parts[0].redPass}-[ : ")
					exams[i].Parts[0].goldPass = clamp(exams[i].Parts[0].redPass, int(input()), 999999)
				else:
					eprint(f"// Enter the exam {i + 1} gold condition [0-{exams[i].Parts[0].redPass}] : ")
					exams[i].Parts[0].goldPass = clamp(0, exams[i].Parts[0].redPass, int(input()))
			globalIndexes.append(i)
		else:
			nonGlobalIndexes.append(i)
	
	# Choose difficulties
	difficulties = []
	for i in range(songCount):
		eprint(f"// Enter the Selected difficulty for the song {charts[i].title} : ")
		for j in range(5):
			if (charts[i].difficulties[j] is not None):
				eprint(f"// {j} - {charts[i].difficulties[j].starRating} stars")
		difficulties.append(clamp(1, int(input()), 5))
		
	# Individual Exams
	for i in nonGlobalIndexes:
		eprint(f"// Enter the exam {i + 1} type : ")
		eprint("// 1 : Perfect count")
		eprint("// 2 : Good count")
		eprint("// 3 : Bad count")
		eprint("// 4 : Score")
		eprint("// 5 : Rolls")
		eprint("// 6 : Hit notes")
		eprint("// 7 : Combo")
		eprint("// 8 : Accuracy")
		tmp = clamp(1, int(input()), 8)
		exams[i].Parts[0].examType = ExamTypesDict[tmp]
		eprint(f"// Enter the exam {i + 1} range : ")
		eprint("// 1 : More")
		eprint("// 2 : Less")
		tmp = clamp(1, int(input()), 2)
		exams[i].Parts[0].examRange = ExamRangeDict[tmp]
		for j in range(songCount):
			eprint(f"// [Song {j} individual] Enter the exam {i + 1} red condition [0-[ : ")
			exams[i].Parts[j].redPass = clamp(0, int(input()), 999999)
			if (exams[i].Parts[0].examRange == "m"):
				eprint(f"// [Song {j} individual] Enter the exam {i + 1} gold condition [{exams[i].Parts[j].redPass}-[ : ")
				exams[i].Parts[j].goldPass = clamp(exams[i].Parts[j].redPass, int(input()), 999999)
			else:
				eprint(f"// [Song {j} individual] Enter the exam {i + 1} gold condition [0-{exams[i].Parts[j].redPass}] : ")
				exams[i].Parts[j].goldPass = clamp(0, exams[i].Parts[j].redPass, int(input()))
	
	# Dan ticks
	eprint("// Enter the DANTICK value [0-5] : ")
	danTick = clamp(0, int(input()), 5)
	eprint("// Enter the DANTICKCOLOR string following the hex rgb format (Default : #ffffff) : ")
	danColor = input()
	if (danColor == ""):
		danColor = "#ffffff"
	
	# Display Header
	balloons = "BALLOON:"
	balloonsContent = ""
	print(f"TITLE:{chartName}")
	print(f"BPM:{charts[0].bpm}")
	print(f"WAVE:{charts[0].wave}")
	print(f"DEMOSTART:{charts[0].demoStart}")
	print(f"SCOREMODE:2")
	print(f"COURSE:Dan")
	print(f"LEVEL:10")
	print(f"BPM:{charts[0].bpm}")
	for i in range(songCount):
		if (balloonsContent != "" and charts[i].difficulties[difficulties[i]].balloon != ""):
			balloonsContent += "," + charts[i].difficulties[difficulties[i]].balloon
		else:
			balloonsContent += charts[i].difficulties[difficulties[i]].balloon
	print(balloons + balloonsContent)
	for gid in globalIndexes:
		print(f"EXAM{gid + 1}:{exams[gid].Parts[0].examType},{exams[gid].Parts[0].redPass},{exams[gid].Parts[0].goldPass},{exams[gid].Parts[0].examRange}")
	print(f"DANTICK:{danTick}")
	print(f"DANTICKCOLOR:{danColor}")
	
	# Process charts
	print("#START")
	
	for i in range(songCount):
		print(f"#NEXTSONG {charts[i].title},{charts[i].subtitle},,{charts[i].wave},350,80,{charts[i].difficulties[difficulties[i]].starRating},{difficulties[i]}")
		print(f"#BPMCHANGE {charts[i].bpm}")
		print(f"#MEASURE 4/4")
		print(f"#SCROLL 1.0")
		print(f"#DELAY {charts[i].offset}")
		# Individual exams
		for ngid in nonGlobalIndexes:
			print(f"EXAM{ngid + 1}:{exams[ngid].Parts[0].examType},{exams[ngid].Parts[i].redPass},{exams[ngid].Parts[i].goldPass},{exams[ngid].Parts[0].examRange}")
		print(charts[i].difficulties[difficulties[i]].body)
	
	print("#END")
	