import ROOT, math, helper, sys, lib, copy


if not 'loaded' in globals():
	print 'loaded is not in globals'
	global loaded
	loaded = False

if not loaded:
	ttjets_sl = helper.sample('ttjets_sl','../closureTest/ttjets_semi_closureOutput.root'  )
	ttjets_fl = helper.sample('ttjets_fl','../closureTest/ttjets_full_closureOutput.root'  )
	wjets     = helper.sample('wjets'    ,'../closureTest/wnjets_closureOutput.root'  )
	#dyjets    = helper.sample('dyjets'   ,'../closureTest/dyjets_closureOutput.root'  )
	doublemu  = helper.sample('doublemu' ,'../closureTest/doublemu_closureOutput.root')
	doubleel  = helper.sample('doubleel' ,'../closureTest/doubleel_closureOutput.root')
	rares     = helper.sample('rares'    ,'../closureTest/rares_closureOutput.root')
	samples = [rares, wjets, ttjets_fl, ttjets_sl, doublemu, doubleel]

	sr = 'wjets'
	
	trigger = 1
	maxev = 10E18
	
	totals = helper.sample('total','')
	
	
	for sample in samples:
		#if sample.loaded == True: continue
		i=0
		sample.muiso = ROOT.TH1F('muIso_'+sample.name, 'muIso_'+sample.name, 20, 0., 1.)
		sample.muiso.Sumw2()
		sample.eliso = ROOT.TH1F('elIso_'+sample.name, 'elIso_'+sample.name, 20, 0., 1.)
		sample.eliso.Sumw2()
		for evt in sample.tree:
			i += 1
			if i > maxev:
				continue
		
			if trigger and evt.passTrigger == 0: continue
			weight = evt.lumiW
			type   = evt.type
			if type > 2:
				type -= 3
		
			if sr  in ['a', 'A']:
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj   <   2: continue
				if evt.nb  !=   0: continue
				if evt.met  < 30.: continue
		
			elif sr in ['b', 'B']:
				if evt.type > 2: continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj  <   2: continue
				if evt.nb  <   1: continue
				if evt.met < 30.: continue
		
			elif sr == 3:
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj  <   2: continue
				if evt.nb  <   2: continue
				if evt.met < 30.: continue
		
			elif sr == 'wjets':
				if evt.type not in [0,1,3] : continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj >   0: continue
				if evt.nb !=  0: continue
				if evt.met < 30.: continue
		
			elif sr == 'ttjets':
				if evt.type not in [0,1,3] : continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj <   3: continue
				if evt.nb !=  1: continue
				#if evt.met < 30.: continue
		
			elif sr == 0:
				pass
		
			sample.cats[type].npp += evt.npp*weight
			sample.cats[type].npf += evt.npf*weight
			sample.cats[type].nfp += evt.nfp*weight
			sample.cats[type].nff += evt.nff*weight
		
			sample.cats[type].npp2 += evt.npp*evt.npp*weight*weight
			sample.cats[type].npf2 += evt.npf*evt.npf*weight*weight
			sample.cats[type].nfp2 += evt.nfp*evt.nfp*weight*weight
			sample.cats[type].nff2 += evt.nff*evt.nff*weight*weight
	
			## Fill the muons isolation for both muons regardless of tight/loose, but same-sign
			if evt.type in [0]:
				sample.muiso.Fill(evt.iso1, weight*evt.puW)
				sample.muiso.Fill(evt.iso2, weight*evt.puW)
			if evt.type in [1]:
				sample.muiso.Fill(evt.iso1, weight*evt.puW)
				sample.eliso.Fill(evt.iso2, weight*evt.puW)
			if evt.type in [2]:
				sample.eliso.Fill(evt.iso1, weight*evt.puW)
				sample.eliso.Fill(evt.iso2, weight*evt.puW)
			
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
	
		sample.loaded = True
	
	## adding up all the samples
	totals = helper.sample('total','')
	for sample in samples:
		if sample.isdata: continue
		totals += sample
	samples.append(totals)
	
	loaded = True

#def isoplots():
mulegend = lib.makeLegend(0.6, 0.4, 0.8, 0.8)
mumcstack = ROOT.THStack('mumcstack', 'mumcstack')
mumcint = 0.
ellegend = lib.makeLegend(0.6, 0.4, 0.8, 0.8)
elmcstack = ROOT.THStack('elmcstack', 'elmcstack')
elmcint = 0.
for sample in samples:
	if sample == totals or sample.isdata: continue
	#muons 
	sample.muiso.SetFillColor(sample.color)
	mumcint += sample.muiso.Integral()
	mumcstack.Add(sample.muiso)
	mulegend.AddEntry(sample.muiso, sample.name, 'f')
	#muons 
	sample.eliso.SetFillColor(sample.color)
	elmcint += sample.eliso.Integral()
	elmcstack.Add(sample.eliso)
	ellegend.AddEntry(sample.eliso, sample.name, 'f')

mulegend.AddEntry(doublemu.muiso, doublemu.name, 'pe')
ellegend.AddEntry(doubleel.eliso, doubleel.name, 'pe')


mufunc = helper.canvasWithRatio(mumcstack, doublemu.muiso, mulegend)
cmu = mufunc[0] #don't ask me why this is necessary
cmu.Update()
cmu.Draw()
cmu.SaveAs('mu_iso_sideband_'+sr+'.pdf')

elfunc = helper.canvasWithRatio(elmcstack, doubleel.eliso, ellegend)
cel = elfunc[0] #don't ask me why this is necessary
cel.Update()
cel.Draw()
cel.SaveAs('el_iso_sideband_'+sr+'.pdf')



def printout():
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
