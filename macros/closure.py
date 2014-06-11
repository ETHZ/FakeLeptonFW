import ROOT, math, helper, sys


#f = ROOT.TFile('../closureTest/ttjets_semiLep_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_fullLep_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_massiveb_newEl_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_semilep_elchcons_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_semilep_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_massivebin_trigger_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/wjets_inc_trigger_closureOutput.root','read')
#f = ROOT.TFile('../closureTest/ttjets_massiveb_elchcons_closureOutput.root','read')

ttjets = helper.sample('ttjets','../closureTest/ttjets_semiLep_closureOutput.root')
wjets  = helper.sample('wjets' ,'../closureTest/ttjets_semiLep_closureOutput.root')



sr = 2

## mm = helper.cat('MUON-MUON')
## em = helper.cat('ELECTRON-MUON')
## ee = helper.cat('ELECTRON-ELECTRON')

##cats = [mm, em, ee] ## this order is very important!!!!
samples = [ttjets, wjets]

trigger = 1
maxev = 10E4

totals = helper.sample('total','')


for sample in samples:
	i=0
	for evt in sample.tree:
		i += 1
		if i > maxev:
			continue
	
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
	
		sample.cats[type].npp += evt.npp*weight
		sample.cats[type].npf += evt.npf*weight
		sample.cats[type].nfp += evt.nfp*weight
		sample.cats[type].nff += evt.nff*weight
	
		sample.cats[type].npp2 += evt.npp*evt.npp*weight*weight
		sample.cats[type].npf2 += evt.npf*evt.npf*weight*weight
		sample.cats[type].nfp2 += evt.nfp*evt.nfp*weight*weight
		sample.cats[type].nff2 += evt.nff*evt.nff*weight*weight
	
		if   evt.tlcat is 0:
			sample.cats[type].ntt  +=weight
			sample.cats[type].ntt2 +=weight*weight
			sample.cats[type].nttc +=1
	
		elif evt.tlcat is 1:
			sample.cats[type].ntl  +=weight
			sample.cats[type].ntl2 +=weight*weight
			sample.cats[type].ntlc +=1
	
		elif evt.tlcat is 2:
			sample.cats[type].nlt  +=weight
			sample.cats[type].nlt2 +=weight*weight
			sample.cats[type].nltc +=1
	
		elif evt.tlcat is 3:
			sample.cats[type].nll  +=weight
			sample.cats[type].nll2 +=weight*weight
			sample.cats[type].nllc +=1


## adding up all the samples
totals = helper.sample('total','')
for sample in samples:
	totals += sample
samples.append(totals)


for sample in samples:
	for cat in sample.cats:
		cat.fakes = cat.npf+cat.nfp+cat.nff
		cat.obs   = cat.ntt
		cat.ntte , cat.ntle , cat.nlte , cat.nlle  = math.sqrt(cat.ntt2), math.sqrt(cat.ntl2), math.sqrt(cat.nlt2), math.sqrt(cat.nll2)
		cat.nttce, cat.ntlce, cat.nltce, cat.nllce = math.sqrt(cat.nttc), math.sqrt(cat.ntlc), math.sqrt(cat.nltc), math.sqrt(cat.nllc)
		cat.nppe , cat.npfe , cat.nfpe , cat.nffe  = math.sqrt(cat.npp2), math.sqrt(cat.npf2), math.sqrt(cat.nfp2), math.sqrt(cat.nff2)
		cat.fakese = cat.npfe+cat.nfpe+cat.nffe
		cat.obse  = cat.ntte

for i in range(0, 3):  ## loop on all the categories
	print '\n\n\n'
	print '=============================================================================================================='
	print '                                          CATEGORY:', samples[0].cats[i].name
	print '=============================================================================================================='
	print '%10s | %10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('SAMPLE', 'NTT','', 'NTL','', 'NLT','', 'NLL','', 'SUM','')
	print '--------------------------------------------------------------------------------------------------------------'
	for sample in samples:
		if samples.index(sample) == len(samples) -1:
			print '--------------------------------------------------------------------------------------------------------------'
		print '%10s | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
		      sample.name, sample.cats[i].ntt, sample.cats[i].ntte, sample.cats[i].ntl, sample.cats[i].ntle, sample.cats[i].nlt, sample.cats[i].nlte, sample.cats[i].nll, sample.cats[i].nlle, sample.cats[i].ntt+sample.cats[i].ntl+sample.cats[i].nlt+sample.cats[i].nll, sample.cats[i].ntte+sample.cats[i].ntle+sample.cats[i].nlte+sample.cats[i].nlle)

	print '--------------------------------------------------------------------------------------------------------------'
	print '--------------------------------------------------------------------------------------------------------------'
	print '%10s | %10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('SAMPLE', 'NPP','', 'NPF','', 'NFP','', 'NFF','', 'SUM','')
	print '--------------------------------------------------------------------------------------------------------------'
	for sample in samples:
		if samples.index(sample) == len(samples) -1:
			print '--------------------------------------------------------------------------------------------------------------'
		print '%10s | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
		      sample.name, sample.cats[i].npp, sample.cats[i].nppe, sample.cats[i].npf, sample.cats[i].npfe, sample.cats[i].nfp, sample.cats[i].nfpe, sample.cats[i].nff, sample.cats[i].nffe, sample.cats[i].npp+sample.cats[i].npf+sample.cats[i].nfp+sample.cats[i].nff, sample.cats[i].nppe+sample.cats[i].npfe+sample.cats[i].nfpe+sample.cats[i].nffe)

	print '--------------------------------------------------------------------------------------------------------------'
	print 'OBSERVED     : %.2f +- %.2f' %(totals.cats[i].obs  , totals.cats[i].ntte)
	print 'SUM OF FAKES : %.2f +- %.2f' %(totals.cats[i].fakes, totals.cats[i].npfe+totals.cats[i].nfpe+totals.cats[i].nffe)

	if totals.cats[i].obs > 0:
		res    = helper.divWithErr(totals.cats[i].fakes, totals.cats[i].fakese, totals.cats[i].obs, totals.cats[i].obse)	
		relres = helper.divWithErr(totals.cats[i].fakes - totals.cats[i].obs, totals.cats[i].fakese - totals.cats[i].obse, totals.cats[i].fakes, totals.cats[i].fakese)	
	else:
		res = [0,0]
		relres = [0,0]
	print '\n------------------------------------------'
	print '%25s %.3f +- %.3f' %('pred./ obs.:', res[0], res[1])
	print '\n%25s %.3f +- %.3f' %('(pred. - obs.) / pred.:', relres[0], relres[1])
	print '------------------------------------------'
#		
#		print '\n \nPURE COUNTS:'
#		print '%10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('NTT','', 'NTL','', 'NLT','', 'NLL','', 'SUM','')
#		print '--------------------------------------------------------------------------------------------------------------'
#		if samples.index(sample) == len(samples) -1:
#			print '--------------------------------------------------------------------------------------------------------------'
#		print '%10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
#		      sample.cats[i].nttc, sample.cats[i].nttce, sample.cats[i].ntlc, sample.cats[i].ntlce, sample.cats[i].nltc, sample.cats[i].nltce, sample.cats[i].nllc, sample.cats[i].nllce, sample.cats[i].nttc+sample.cats[i].ntlc+sample.cats[i].nltc+sample.cats[i].nllc, sample.cats[i].nttce+sample.cats[i].ntlce+sample.cats[i].nltce+sample.cats[i].nllce)
#
	sample.file.Close()
