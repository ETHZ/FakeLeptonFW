import ROOT, math, helper, sys, lib, copy, pickle, os


sr = 'ttjets_ht200met100'

if not 'loaded' in globals():
	print 'loaded is not in globals'
	global loaded
	loaded = False

if not loaded:
	ttjets_sl = helper.sample('ttjets_sl','../closureTest/ttjets_semi_closureOutput_SS.root'  )
	ttjets_fl = helper.sample('ttjets_fl','../closureTest/ttjets_full_closureOutput_SS.root'  )
	wjets     = helper.sample('wjets'    ,'../closureTest/wnjets_closureOutput_SS.root'  )
	#dyjets    = helper.sample('dyjets'   ,'../closureTest/dyjets_closureOutput.root'  )
	doublemu  = helper.sample('doublemu' ,'../closureTest/doublemu_closureOutput_SS.root')
	doubleel  = helper.sample('doubleel' ,'../closureTest/doubleel_closureOutput_SS.root')
	rares     = helper.sample('rares'    ,'../closureTest/rares_closureOutput_SS.root')
	samples = [ rares, wjets, ttjets_fl, ttjets_sl, doublemu, doubleel]

	for i in range(len(samples)):
		print 'at sample', samples[i].name
		f = 'samples/'+samples[i].name+'_'+sr+'.pk'
		if os.path.isfile(f):
			f= open(f, 'rb')
			print 'for sample', samples[i].name, 'file exists. loading', f
			samples[i] = pickle.load(f)
			samples[i].loaded = True
			f.close()
			doublemu  = (x for x in samples if x.name == 'doublemu' ).next()
			doubleel  = (x for x in samples if x.name == 'doubleel' ).next()
			ttjets_fl = (x for x in samples if x.name == 'ttjets_fl').next()
			ttjets_sl = (x for x in samples if x.name == 'ttjets_sl').next()
			rares     = (x for x in samples if x.name == 'rares'    ).next()
			wjets     = (x for x in samples if x.name == 'wjets'    ).next()
			#dyjets    = (x for x in samples if x.name == 'dyjets'   ).next()
	samples = [ rares, wjets, ttjets_fl, ttjets_sl, doublemu, doubleel]

	trigger = 1
	maxev = 10E18
	
	for sample in samples:
		if sample.loaded == True: continue
		print 'loading sample', sample.name
		i=0
		sample.histos['muiso'  ] = ROOT.TH1F('muIso_'+sample.name  , 'muIso_'+sample.name  , 20, 0., 1.)
		sample.histos['muneiso'] = ROOT.TH1F('muNeIso_'+sample.name, 'muNeIso_'+sample.name, 20, 0., 1.)
		sample.histos['muphiso'] = ROOT.TH1F('muphIso_'+sample.name, 'muphIso_'+sample.name, 20, 0., 1.)
		sample.histos['muchiso'] = ROOT.TH1F('muchIso_'+sample.name, 'muchIso_'+sample.name, 20, 0., 1.)
		sample.histos['mupucor'] = ROOT.TH1F('mupucor_'+sample.name, 'mupucor_'+sample.name, 50, 0.,50.)
		sample.histos['eliso'  ] = ROOT.TH1F('elIso_'+sample.name  , 'elIso_'+sample.name  , 20, 0., 1.)
		sample.histos['elneiso'] = ROOT.TH1F('elNeIso_'+sample.name, 'elNeIso_'+sample.name, 20, 0., 1.)
		sample.histos['elphiso'] = ROOT.TH1F('elphIso_'+sample.name, 'elphIso_'+sample.name, 20, 0., 1.)
		sample.histos['elchiso'] = ROOT.TH1F('elchIso_'+sample.name, 'elchIso_'+sample.name, 20, 0., 1.)
		sample.histos['elpucor'] = ROOT.TH1F('elpucor_'+sample.name, 'elpucor_'+sample.name, 20, 0.,50.)

		for key, value in sample.histos.items():
			value.Sumw2()

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
				if evt.type not in [0,1,2] : continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj >   0: continue
				if evt.nb !=  0: continue
				if evt.met < 30.: continue
		
			elif sr == 'ttjets':
				if evt.type not in [0,1,2] : continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj <   3: continue
				if evt.nb !=  1: continue
				#if evt.met < 30.: continue
		
			elif sr == 'ttjets_ht200':
				if evt.type not in [0,1,2] : continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj <   3: continue
				if evt.nb !=  1: continue
				if evt.ht  <  200: continue
				if evt.met <  100: continue
				#if evt.met < 30.: continue

			elif sr == 'ttjets_ht200met100':
				if evt.type not in [0,1,2] : continue
				if evt.pt1 < 20 or evt.pt2 < 20: continue
				if evt.nj <   3: continue
				if evt.nb !=  1: continue
				if evt.ht  <  200: continue
				if evt.met <  100: continue
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
				sample.histos['muiso'  ].Fill(evt.iso1, weight*evt.puW)
				sample.histos['muiso'  ].Fill(evt.iso2, weight*evt.puW)
				sample.histos['muneiso'].Fill(evt.neiso1/evt.pt1, weight*evt.puW)
				sample.histos['muneiso'].Fill(evt.neiso2/evt.pt2, weight*evt.puW)
				sample.histos['muphiso'].Fill(evt.phiso1/evt.pt1, weight*evt.puW)
				sample.histos['muphiso'].Fill(evt.phiso2/evt.pt2, weight*evt.puW)
				sample.histos['muchiso'].Fill(evt.chiso1/evt.pt1, weight*evt.puW)
				sample.histos['muchiso'].Fill(evt.chiso2/evt.pt2, weight*evt.puW)
				sample.histos['mupucor'].Fill(evt.pucor1, weight*evt.puW)
				sample.histos['mupucor'].Fill(evt.pucor2, weight*evt.puW)
			if evt.type in [1]:
				sample.histos['muiso'].Fill(evt.iso1, weight*evt.puW)
				sample.histos['eliso'].Fill(evt.iso2, weight*evt.puW)
				sample.histos['muneiso'].Fill(evt.neiso1/evt.pt1, weight*evt.puW)
				sample.histos['elneiso'].Fill(evt.neiso2/evt.pt2, weight*evt.puW)
				sample.histos['muphiso'].Fill(evt.phiso1/evt.pt1, weight*evt.puW)
				sample.histos['elphiso'].Fill(evt.phiso2/evt.pt2, weight*evt.puW)
				sample.histos['muchiso'].Fill(evt.chiso1/evt.pt1, weight*evt.puW)
				sample.histos['elchiso'].Fill(evt.chiso2/evt.pt2, weight*evt.puW)
				sample.histos['mupucor'].Fill(evt.pucor1, weight*evt.puW)
				sample.histos['elpucor'].Fill(evt.pucor2, weight*evt.puW)
			if evt.type in [2]:
				sample.histos['eliso'  ].Fill(evt.iso1, weight*evt.puW)
				sample.histos['eliso'  ].Fill(evt.iso2, weight*evt.puW)
				sample.histos['elneiso'].Fill(evt.neiso1/evt.pt1, weight*evt.puW)
				sample.histos['elneiso'].Fill(evt.neiso2/evt.pt2, weight*evt.puW)
				sample.histos['elphiso'].Fill(evt.phiso1/evt.pt1, weight*evt.puW)
				sample.histos['elphiso'].Fill(evt.phiso2/evt.pt2, weight*evt.puW)
				sample.histos['elchiso'].Fill(evt.chiso1/evt.pt1, weight*evt.puW)
				sample.histos['elchiso'].Fill(evt.chiso2/evt.pt2, weight*evt.puW)
				sample.histos['elpucor'].Fill(evt.pucor1, weight*evt.puW)
				sample.histos['elpucor'].Fill(evt.pucor2, weight*evt.puW)
			
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
	
	for sample in samples:
		if not os.path.isfile('samples/'+sample.name+'_'+sr+'.pk'):
			pickle.dump(sample, open('samples/'+sample.name+'_'+sr+'.pk','wb'), pickle.HIGHEST_PROTOCOL)
	
	## adding up all the samples
	totals = helper.sample('total','')
	for sample in samples:
		if sample.isdata: continue
		totals += sample
	samples.append(totals)

	loaded = True

#def isoplots():
for key in samples[0].histos.keys():
	if 'mu' in key:
		mulegend = lib.makeLegend(0.6, 0.4, 0.8, 0.8)
		mumcstack = ROOT.THStack('mumcstack', 'mumcstack')
		mumcint = 0.
	if 'el' in key:
		ellegend = lib.makeLegend(0.6, 0.4, 0.8, 0.8)
		elmcstack = ROOT.THStack('elmcstack', 'elmcstack')
		elmcint = 0.
	for sample in samples:
		if sample == totals or sample.isdata: continue
		#muons 
		if 'mu' in key:
			sample.histos[key].SetFillColor(sample.color)
			mumcint += sample.histos[key].Integral()
			mumcstack.Add(sample.histos[key])
			mulegend.AddEntry(sample.histos[key], sample.name, 'f')
		#electrons 
		if 'el' in key:
			sample.histos[key].SetFillColor(sample.color)
			elmcint += sample.histos[key].Integral()
			elmcstack.Add(sample.histos[key])
			ellegend.AddEntry(sample.histos[key], sample.name, 'f')
	
	
	if 'mu' in key:
		mulegend.AddEntry(doublemu.histos[key], doublemu.name, 'pe')
		mufunc = helper.canvasWithRatio(mumcstack, doublemu.histos[key], mulegend)
		cmu = mufunc[0] #don't ask me why this is necessary
		cmu.Update()
		cmu.Draw()
		cmu.SaveAs('figs/mu_'+key+'_sideband_'+sr+'.pdf')
		cmu.SaveAs('figs/mu_'+key+'_sideband_'+sr+'.png')
		cmu.SaveAs('figs/mu_'+key+'_sideband_'+sr+'.root')

	if 'el' in key:
		ellegend.AddEntry(doubleel.histos[key], doubleel.name, 'pe')
		elfunc = helper.canvasWithRatio(elmcstack, doubleel.histos[key], ellegend)
		cel = elfunc[0] #don't ask me why this is necessary
		cel.Update()
		cel.Draw()
		cel.SaveAs('figs/el_'+key+'_sideband_'+sr+'.pdf')
		cel.SaveAs('figs/el_'+key+'_sideband_'+sr+'.png')
		cel.SaveAs('figs/el_'+key+'_sideband_'+sr+'.root')



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
