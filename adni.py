#!/usr/bin/env python
# NOTES FOR HARVARD MEDICAL SCHOOL COURSE (April, 2015)

import math

def avg (x):
	return sum(x) / float(len(x))

def stdev(s):
	av = avg (s)
	variance = map (lambda x: (x - av)**2, s)
	average = avg (variance)
	return math.sqrt (average)

class Measures:
	def __init__ (self,filename):
		self.tbl = [i.rstrip().split() for i in open(filename).readlines()]
		self.header = self.tbl[0]
		self.index = i[0][0]

	def hdrprint (self):
		for i in xrange(len(self.header)):
			print i,self.header[i]
			
	def DataById (self,id):
		for i in self.tbl[1:]:
			if i[0] == id:
				return [float(j) for j in i[1:]]



class Patients:
	def __init__ (self,filename):
		self.tbl = [i.rstrip().split() for i in open(filename).readlines()]
		self.patients = self.tbl[1:]

	def setMeasures (self,measure):
		self.measure = measure

	def diag2Code (self,diag):
		if (diag =="AD"):
			return 1
		if (diag == "OC"):
			return -1
		if (diag == "MCI"):
			return 0
		return -1000

	def gender2code(self,gender):
		if (gender=="M"):
			return -1
		if (gender=="F"):
			return 1
		return 0

	def exportSVM (self):
		self.lines  = []
		for i in self.patients:
			line = [self.diag2Code(i[3])]
			line.append (i[2])
			line.append (self.gender2code(i[1]))
			line += self.measure.DataById(i[0])
			self.lines.append(line)

	def exportMean (self, tipo):
		codes = [i[0] for i in self.patients if i[3]==tipo]
		selmesures = map (self.measure.DataById,codes)
		hippo = [((i[13]+i[30]) / i[50]) for i in selmesures]
		grmat = [((i[1]+i[21]) / i[50]) for i in selmesures]
		wmatt = [((i[0]+i[20]) / i[50]) for i in selmesures]
		ventl = [((i[2]+i[22]) / i[50]) for i in selmesures]
		clvet = [((i[3]+i[23]) / i[50]) for i in selmesures]
		amygd = [((i[14]+i[31]) / i[50]) for i in selmesures]
		print "Gray Matter  %.2f %.3f"%(100*avg(grmat),100*stdev(grmat))
		print "White Matter %.2f %.3f"%(100*avg(wmatt),100*stdev(wmatt))
		print "Lat-Vent     %.2f %.3f"%(100*avg(ventl),100*stdev(ventl))
		print "Lat-Inf Vent %.2f %.3f"%(100*avg(clvet),100*stdev(clvet))
		print "Hippocampus  %.2f %.3f"%(100*avg(hippo),100*stdev(hippo))
		print "Amygdala     %.2f %.3f"%(100*avg(amygd),100*stdev(amygd))
		
	# Print data to train Support Vector Machine
	def printSVM (self):
		for i in self.lines:
			for j in xrange(len(i)):
				if (j>0):
					print ("%d:%s"%(j,i[j])),
				else:
					print i[0],
			print ""

m1 = Measures("adni814.aseg.stats")
p = Patients("qdec.adni814.dat")
p.setMeasures(m1)
p.exportMean("OC")
