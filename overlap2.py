#! /usr/bin/python
import commands, sys, math


def fillSet(f):
	tmpFile = open(f,'r')
	tmpSet = set()
	for line in tmpFile.readlines():
		## tmp = event()
		run = line.split()[0]
		ls  = line.split()[1]
		evn = line.split()[2]# .lstrip('-')
		all = run+':'+ls+':'+evn
		#tmp = int(all)
		#tmpSet.add(tmp)
		if all in tmpSet:
			print 'this one is already here:', all
		tmpSet.add(all)
	return tmpSet
	

def getCorrelations2(s1, s2, verbose=False):
	n1, n2 = len(s1), len(s2)
	inboth = s1.intersection(s2)
	print '--------------------------'
	print 'I have two sets here with lengths:', n1, '(set 1), and', n2, '(set 2)'
	print 'there are %d events in both sets' %( len(inboth) )
	print 'the overlap in set 1 is: %.2f +- %.2f' %( len(inboth)/float(n1), math.sqrt(len(inboth))/float(n1) )
	print 'the overlap in set 2 is: %.2f +- %.2f' %( len(inboth)/float(n2), math.sqrt(len(inboth))/float(n2) )
	print '------> the correlation factor is then: %.3f' %(len(inboth)/math.sqrt(n1*n2))
	if verbose:
		print 'in set 1 but not set 2', s1.difference(s2)
		print 'in set 2 but not set 1', s2.difference(s1)
	


def getCorrelations3(s1, s2, s3):
	n1, n2, n3 = len(s1), len(s2), len(s3)
	inall = s1.intersection(s2, s3)
	in12 = s1.intersection(s2)
	in13 = s1.intersection(s3)
	in23 = s2.intersection(s3)
	print '--------------------------'
	print 'I have three sets here with lengths: %d (set 1), %d (set 2) and %d (set 3)' %(n1, n2, n3)
	print 'there are %d events in all three sets' %( len(inall) )
	print 'the total overlap of set 1 is %.2f +- %.2f' %( len(inall)/float(n1), math.sqrt(len(inall))/float(n1) )
	print 'the total overlap of set 2 is %.2f +- %.2f' %( len(inall)/float(n2), math.sqrt(len(inall))/float(n2) )
	print 'the total overlap of set 3 is %.2f +- %.2f' %( len(inall)/float(n3), math.sqrt(len(inall))/float(n3) )
	print 'the overlap of set 1 and 2 is %.2f and %.2f respectively' %( len(in12)/float(n1), len(in12)/float(n2) )
	print 'the overlap of set 1 and 3 is %.2f and %.2f respectively' %( len(in13)/float(n1), len(in13)/float(n3) )
	print 'the overlap of set 2 and 3 is %.2f and %.2f respectively' %( len(in23)/float(n2), len(in23)/float(n3) )


args = sys.argv
print args
set1 = fillSet(args[1])
set2 = fillSet(args[2])
if '-v' in args:
	verbose = True
else:
	verbose = False
 
 
getCorrelations2(set1, set2, verbose)
print '\n'
