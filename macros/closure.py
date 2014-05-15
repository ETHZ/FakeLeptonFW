import ROOT


f = ROOT.TFile('../closureTest/ttjets_closureOutput.root','read')

tree = f.Get('closureTree')


npp, npf, nfp, nff = 0., 0., 0., 0.
ntt, ntl, nlt, nll = 0., 0., 0., 0.

for evt in tree:

	#if evt.nj < 4: continue

	npp += evt.npp
	npf += evt.npf
	nfp += evt.nfp
	nff += evt.nff

	if evt.tlcat is 0: ntt +=1
	if evt.tlcat is 1: nlt +=1
	if evt.tlcat is 2: ntl +=1
	if evt.tlcat is 3: nll +=1

fakes = npf+nfp+nff
print 'npp: %.3f  npf: %.3f  nfp: %.3f  nff: %.3f   sum: %.3f' %(npp, npf, nfp, nff, npp+npf+nfp+nff)
print 'sum of fakes: %.3f' %(fakes)
print 'ntt: %.3f  ntl: %.3f  nlt: %.3f  nll: %.3f   sum: %.3f' %(ntt, ntl, nlt, nll, ntt+ntl+nlt+nll)

print '\n \t (obs. - pred.) / pred.: %.3f' %((ntt - fakes)/fakes)


