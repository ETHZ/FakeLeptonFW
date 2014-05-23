import ROOT, math, helper


f = ROOT.TFile('../closureTest/ttjets_semiLep_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_fullLep_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_massiveb_newEl_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_semilep_elchcons_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_semilep_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_massivebin_trigger_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/wjets_inc_trigger_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_massiveb_elchcons_closureOutput.root','read')

tree = f.Get('closureTree')

class cat:
	def __init__(self, name):
		self.name = name
	nttc, ntlc, nltc, nllc = 0 , 0 , 0 , 0
	ntt, ntl, nlt, nll     = 0., 0., 0., 0.
	npp, npf, nfp, nff     = 0 , 0 , 0 , 0
	ntt2, ntl2, nlt2, nll2     = 0., 0., 0., 0.
	npp2, npf2, nfp2, nff2     = 0 , 0 , 0 , 0


sr = 2

mm = cat('MUON-MUON')
em = cat('ELECTRON-MUON')
ee = cat('ELECTRON-ELECTRON')

cats = [mm, em, ee] ## this order is very important!!!!

trigger = 1

for evt in tree:

	if trigger and evt.passTrigger == 0: continue
	weight = evt.lumiW
	type   = evt.type
	if type > 2:
		type -= 3

	if sr == 1:
		if evt.pt1 < 20 or evt.pt2 < 20: continue
		if evt.nj   <   2: continue
		if evt.nb  !=   0: continue
		if evt.met  < 30.: continue

	if sr == 2:
		if evt.type > 2: continue
		if evt.pt1 < 20 or evt.pt2 < 20: continue
		if evt.nj  <   2: continue
		if evt.nb  <   1: continue
		if evt.met < 30.: continue

	if sr == 3:
		if evt.pt1 < 20 or evt.pt2 < 20: continue
		if evt.nj  <   2: continue
		if evt.nb  <   2: continue
		if evt.met < 30.: continue

	if sr == 0:
		pass

	cats[type].npp += evt.npp*weight
	cats[type].npf += evt.npf*weight
	cats[type].nfp += evt.nfp*weight
	cats[type].nff += evt.nff*weight

	cats[type].npp2 += evt.npp*evt.npp*weight*weight
	cats[type].npf2 += evt.npf*evt.npf*weight*weight
	cats[type].nfp2 += evt.nfp*evt.nfp*weight*weight
	cats[type].nff2 += evt.nff*evt.nff*weight*weight

	if   evt.tlcat is 0:
		cats[type].ntt  +=weight
		cats[type].ntt2 +=weight*weight
		cats[type].nttc +=1

	elif evt.tlcat is 1:
		cats[type].ntl  +=weight
		cats[type].ntl2 +=weight*weight
		cats[type].ntlc +=1

	elif evt.tlcat is 2:
		cats[type].nlt  +=weight
		cats[type].nlt2 +=weight*weight
		cats[type].nltc +=1

	elif evt.tlcat is 3:
		cats[type].nll  +=weight
		cats[type].nll2 +=weight*weight
		cats[type].nllc +=1



for cat in cats:
	cat.fakes = cat.npf+cat.nfp+cat.nff
	cat.obs   = cat.ntt
	cat.ntte , cat.ntle , cat.nlte , cat.nlle  = math.sqrt(cat.ntt2), math.sqrt(cat.ntl2), math.sqrt(cat.nlt2), math.sqrt(cat.nll2)
	cat.nttce, cat.ntlce, cat.nltce, cat.nllce = math.sqrt(cat.nttc), math.sqrt(cat.ntlc), math.sqrt(cat.nltc), math.sqrt(cat.nllc)
	cat.nppe , cat.npfe , cat.nfpe , cat.nffe  = math.sqrt(cat.npp2), math.sqrt(cat.npf2), math.sqrt(cat.nfp2), math.sqrt(cat.nff2)
	cat.fakese = cat.npfe+cat.nfpe+cat.nffe
	cat.obse  = cat.ntte
	
	print '\n\n\n'
	print '=============================================================================================================='
	print '                                          CATEGORY:', cat.name
	print '=============================================================================================================='
	print '%10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('NTT','', 'NTL','', 'NLT','', 'NLL','', 'SUM','')
	print '--------------------------------------------------------------------------------------------------------------'
	print '%10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
	      cat.ntt, cat.ntte, cat.ntl, cat.ntle, cat.nlt, cat.nlte, cat.nll, cat.nlle, cat.ntt+cat.ntl+cat.nlt+cat.nll, cat.ntte+cat.ntle+cat.nlte+cat.nlle)

	print '--------------------------------------------------------------------------------------------------------------'
	print '--------------------------------------------------------------------------------------------------------------'

	print '%10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('NPP','', 'NPF','', 'NFP','', 'NFF','', 'SUM','')
	print '--------------------------------------------------------------------------------------------------------------'
	print '%10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
	      cat.npp, cat.nppe, cat.npf, cat.npfe, cat.nfp, cat.nfpe, cat.nff, cat.nffe, cat.npp+cat.npf+cat.nfp+cat.nff, cat.nppe+cat.npfe+cat.nfpe+cat.nffe)

	print '--------------------------------------------------------------------------------------------------------------'
	print 'OBSERVED     : %.2f +- %.2f' %(cat.obs  , cat.ntte)
	print 'SUM OF FAKES : %.2f +- %.2f' %(cat.fakes, cat.npfe+cat.nfpe+cat.nffe)

	if cat.obs > 0:
		res    = helper.divWithErr(cat.fakes, cat.fakese, cat.obs, cat.obse)	
		relres = helper.divWithErr(cat.fakes - cat.obs, cat.fakese - cat.obse, cat.fakes, cat.fakese)	
	else:
		res = [0,0]
		relres = [0,0]
	print '\n------------------------------------------'
	print '%25s %.3f +- %.3f' %('pred./ obs.:', res[0], res[1])
	print '\n%25s %.3f +- %.3f' %('(pred. - obs.) / pred.:', relres[0], relres[1])
	print '------------------------------------------'
	
	print '\n \nPURE COUNTS:'
	print '%10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('NTT','', 'NTL','', 'NLT','', 'NLL','', 'SUM','')
	print '--------------------------------------------------------------------------------------------------------------'
	print '%10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
	      cat.nttc, cat.nttce, cat.ntlc, cat.ntlce, cat.nltc, cat.nltce, cat.nllc, cat.nllce, cat.nttc+cat.ntlc+cat.nltc+cat.nllc, cat.nttce+cat.ntlce+cat.nltce+cat.nllce)

f.Close()
