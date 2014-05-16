import ROOT


#f = ROOT.TFile('../closureTest/ttjets_ttbarTruthFR_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_qcdFR_closureOutput.root','read')
f = ROOT.TFile('../closureTest/ttjets_closureOutput.root','read')

tree = f.Get('closureTree')

class cat:
	def __init__(self, name):
		self.name = name
	ntt, ntl, nlt, nll     = 0., 0., 0., 0.
	nttc, ntlc, nltc, nllc = 0 , 0 , 0 , 0
	npp, npf, nfp, nff     = 0 , 0 , 0 , 0


sr = 2

mm = cat('mu-mu')
em = cat('el-mu')
ee = cat('el-el')

cats = [mm, em, ee] ## this order is very important!!!!

for evt in tree:

	if sr == 1:
		if evt.nj   <  2: continue
		if evt.nb  !=  0: continue
		if evt.met  < 30.: continue

	if sr == 2:
		if evt.nj  <   2: continue
		if evt.nb  <   1: continue
		if evt.met < 30.: continue

	if sr == 3:
		if evt.nj  <   2: continue
		if evt.nb  <   2: continue
		if evt.met < 30.: continue

	if sr == 0:
		pass

	cats[evt.type].npp += evt.npp*evt.lumiW
	cats[evt.type].npf += evt.npf*evt.lumiW
	cats[evt.type].nfp += evt.nfp*evt.lumiW
	cats[evt.type].nff += evt.nff*evt.lumiW

	if evt.tlcat is 0: cats[evt.type].ntt +=1*evt.lumiW
	if evt.tlcat is 1: cats[evt.type].nlt +=1*evt.lumiW
	if evt.tlcat is 2: cats[evt.type].ntl +=1*evt.lumiW
	if evt.tlcat is 3: cats[evt.type].nll +=1*evt.lumiW

	if evt.tlcat is 0: cats[evt.type].nttc +=1
	if evt.tlcat is 1: cats[evt.type].nltc +=1
	if evt.tlcat is 2: cats[evt.type].ntlc +=1
	if evt.tlcat is 3: cats[evt.type].nllc +=1



for cat in cats:
	cat.fakes = cat.npf+cat.nfp+cat.nff
	cat.obs   = cat.ntt
	
	print '\n\n\nCATEGORY:', cat.name
	print '=================================================================='
	print '=================================================================='
	## print 'ntt: %.3f  ntl: %.3f  nlt: %.3f  nll: %.3f   sum: %.3f' %(cat.ntt, cat.ntl, cat.nlt, cat.nll, cat.ntt+cat.ntl+cat.nlt+cat.nll)
	print '%10s \t| %10s \t| %10s \t| %10s \t|| %10s' %('NTT', 'NTL', 'NLT', 'NLL', 'SUM')
	print '-------------------------------------------------------------------------------------'
	print '%10.2f \t| %10.2f \t| %10.2f \t| %10.2f \t|| %10.2f' %(cat.ntt, cat.ntl, cat.nlt, cat.nll, cat.ntt+cat.ntl+cat.nlt+cat.nll)

	print '-------------------------------------------------------------------------------------'
	print '-------------------------------------------------------------------------------------'

	print '%10s \t| %10s \t| %10s \t| %10s \t|| %10s' %('NPP', 'NPF', 'NFP', 'NFF', 'SUM')
	print '-------------------------------------------------------------------------------------'
	print '%10.2f \t| %10.2f \t| %10.2f \t| %10.2f \t|| %10.2f' %(cat.npp, cat.npf, cat.nfp, cat.nff, cat.npp+cat.npf+cat.nfp+cat.nff)

	print '-------------------------------------------------------------------------------------'
	print 'SUM OF FAKES: %.3f' %(cat.fakes)
	print 'OBSERVED    : %.3f' %(cat.obs)

	
	print '\n %25s %.3f' %('pred./ obs.:', cat.fakes/cat.obs)
	print '\n %25s %.3f' %('(pred. - obs.) / pred.:', (cat.fakes - cat.obs)/cat.fakes)
	
	print '\n \nPURE COUNTS:'
	print '%10s \t| %10s \t| %10s \t| %10s \t|| %10s' %('NTT', 'NTL', 'NLT', 'NLL', 'SUM')
	print '-------------------------------------------------------------------------------------'
	print '%10.2f \t| %10.2f \t| %10.2f \t| %10.2f \t|| %10.2f' %(cat.nttc, cat.ntlc, cat.nltc, cat.nllc, cat.nttc+cat.ntlc+cat.nltc+cat.nllc)

