import ROOT


f = ROOT.TFile('../closureTest/ttjets_ttbarTruthFR_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_qcdFR_closureOutput.root','read')

tree = f.Get('closureTree')


npp, npf, nfp, nff = 0., 0., 0., 0.
ntt, ntl, nlt, nll = 0., 0., 0., 0.
nttc, ntlc, nltc, nllc = 0., 0., 0., 0.

sr = 3

for evt in tree:

	## print evt.lumiW

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

	npp += evt.npp #*evt.lumiW
	npf += evt.npf #*evt.lumiW
	nfp += evt.nfp #*evt.lumiW
	nff += evt.nff #*evt.lumiW

	if evt.tlcat is 0: ntt +=1 #*evt.lumiW
	if evt.tlcat is 1: nlt +=1 #*evt.lumiW
	if evt.tlcat is 2: ntl +=1 #*evt.lumiW
	if evt.tlcat is 3: nll +=1 #*evt.lumiW

	if evt.tlcat is 0: nttc +=1
	if evt.tlcat is 1: nltc +=1
	if evt.tlcat is 2: ntlc +=1
	if evt.tlcat is 3: nllc +=1

fakes = npf+nfp+nff
print 'npp: %.3f  npf: %.3f  nfp: %.3f  nff: %.3f   sum: %.3f' %(npp, npf, nfp, nff, npp+npf+nfp+nff)
print 'sum of fakes: %.3f' %(fakes)
print 'ntt: %.3f  ntl: %.3f  nlt: %.3f  nll: %.3f   sum: %.3f' %(ntt, ntl, nlt, nll, ntt+ntl+nlt+nll)

print '\n \t pred./ obs.: %.3f' %(fakes/ntt)
print '\n \t (pred. - obs.) / pred.: %.3f' %((fakes - ntt)/fakes)

print 'pure counts:'
print 'ntt: %.3f  ntl: %.3f  nlt: %.3f  nll: %.3f   sum: %.3f' %(nttc, ntlc, nltc, nllc, ntt+ntl+nlt+nllc)

