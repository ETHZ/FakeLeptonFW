compare = ['test_diff.txt', 'missing.txt']
produce = 'test_diffdiff.txt'

f1 = open(compare[0], 'r')
with = f1.readlines()

for line in with:
	line.rstrip('\n')

f2 = open(compare[1], 'r')
without = f2.readlines()

for line in without:
	line.rstrip('\n')

diff = open(produce, 'w')

for line in without:
	if not line.rstrip('\n') in with:
		diff.write(line)

diff.close()
	
