import ROOT, math, helper, sys, lib, copy, pickle, os


# definig all the signal regions. here only by name
SRs = [
	'wjets',
	'ttjets', 
	'ttjets_ht200',
	'ttjets_ht200met100'
]

if not 'loaded' in globals():
	print 'loaded is not in globals'
	global loaded
	loaded = False

if not loaded:
	ttjets_sl = helper.sample('ttjets_sl','../closureTest/ttjets_semi_closureOutput_SS.root'  )
	ttjets_fl = helper.sample('ttjets_fl','../closureTest/ttjets_full_closureOutput_SS.root'  )
	wjets     = helper.sample('wjets'    ,'../closureTest/wnjets_closureOutput_SS.root'  )
	doublemu  = helper.sample('doublemu' ,'../closureTest/doublemu_closureOutput_SS.root')
	doubleel  = helper.sample('doubleel' ,'../closureTest/doubleel_closureOutput_SS.root')
	rares     = helper.sample('rares'    ,'../closureTest/rares_closureOutput_SS.root')
	#dyjets    = helper.sample('dyjets'   ,'../closureTest/dyjets_closureOutput.root'  )
	samples = [ rares, wjets, ttjets_fl, ttjets_sl, doublemu, doubleel]
	for sample in samples:
		for sr in SRs:
			sample.regions.append(helper.region(sr))

	for i in range(len(samples)):
		f = 'samples/'+samples[i].name+'.pk'
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
		for sr in sample.regions: ## initialize all the histograms for all the regions
			i=0
			sr.histos['muiso'  ] = ROOT.TH1F('muIso_'  +sr.name+'_'+sample.name, 'muIso_'  +sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['muneiso'] = ROOT.TH1F('muNeIso_'+sr.name+'_'+sample.name, 'muNeIso_'+sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['muphiso'] = ROOT.TH1F('muphIso_'+sr.name+'_'+sample.name, 'muphIso_'+sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['muchiso'] = ROOT.TH1F('muchIso_'+sr.name+'_'+sample.name, 'muchIso_'+sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['mupucor'] = ROOT.TH1F('mupucor_'+sr.name+'_'+sample.name, 'mupucor_'+sr.name+'_'+sample.name, 50, 0.,50.)
			sr.histos['eliso'  ] = ROOT.TH1F('elIso_'  +sr.name+'_'+sample.name, 'elIso_'  +sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['elneiso'] = ROOT.TH1F('elNeIso_'+sr.name+'_'+sample.name, 'elNeIso_'+sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['elphiso'] = ROOT.TH1F('elphIso_'+sr.name+'_'+sample.name, 'elphIso_'+sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['elchiso'] = ROOT.TH1F('elchIso_'+sr.name+'_'+sample.name, 'elchIso_'+sr.name+'_'+sample.name, 20, 0., 1.)
			sr.histos['elpucor'] = ROOT.TH1F('elpucor_'+sr.name+'_'+sample.name, 'elpucor_'+sr.name+'_'+sample.name, 20, 0.,50.)

			for key, value in sr.histos.items():
				value.Sumw2()

		## loop over the tree
		for evt in sample.tree:
			i += 1
			if i > maxev:
				continue
		
			if trigger and evt.passTrigger == 0: continue
			weight = evt.lumiW
			type   = evt.type
			if type > 2:
				type -= 3
		
			for sr in sample.regions:
				if not helper.passRegion(sr.name, evt): continue
		
				## Fill the muons isolation for both muons regardless of tight/loose, but same-sign
				if evt.type in [0]:
					sr.histos['muiso'  ].Fill(evt.iso1, weight*evt.puW)
					sr.histos['muiso'  ].Fill(evt.iso2, weight*evt.puW)
					sr.histos['muneiso'].Fill(evt.neiso1/evt.pt1, weight*evt.puW)
					sr.histos['muneiso'].Fill(evt.neiso2/evt.pt2, weight*evt.puW)
					sr.histos['muphiso'].Fill(evt.phiso1/evt.pt1, weight*evt.puW)
					sr.histos['muphiso'].Fill(evt.phiso2/evt.pt2, weight*evt.puW)
					sr.histos['muchiso'].Fill(evt.chiso1/evt.pt1, weight*evt.puW)
					sr.histos['muchiso'].Fill(evt.chiso2/evt.pt2, weight*evt.puW)
					sr.histos['mupucor'].Fill(evt.pucor1, weight*evt.puW)
					sr.histos['mupucor'].Fill(evt.pucor2, weight*evt.puW)
				if evt.type in [1]:
					sr.histos['muiso'].Fill(evt.iso1, weight*evt.puW)
					sr.histos['eliso'].Fill(evt.iso2, weight*evt.puW)
					sr.histos['muneiso'].Fill(evt.neiso1/evt.pt1, weight*evt.puW)
					sr.histos['elneiso'].Fill(evt.neiso2/evt.pt2, weight*evt.puW)
					sr.histos['muphiso'].Fill(evt.phiso1/evt.pt1, weight*evt.puW)
					sr.histos['elphiso'].Fill(evt.phiso2/evt.pt2, weight*evt.puW)
					sr.histos['muchiso'].Fill(evt.chiso1/evt.pt1, weight*evt.puW)
					sr.histos['elchiso'].Fill(evt.chiso2/evt.pt2, weight*evt.puW)
					sr.histos['mupucor'].Fill(evt.pucor1, weight*evt.puW)
					sr.histos['elpucor'].Fill(evt.pucor2, weight*evt.puW)
				if evt.type in [2]:
					sr.histos['eliso'  ].Fill(evt.iso1, weight*evt.puW)
					sr.histos['eliso'  ].Fill(evt.iso2, weight*evt.puW)
					sr.histos['elneiso'].Fill(evt.neiso1/evt.pt1, weight*evt.puW)
					sr.histos['elneiso'].Fill(evt.neiso2/evt.pt2, weight*evt.puW)
					sr.histos['elphiso'].Fill(evt.phiso1/evt.pt1, weight*evt.puW)
					sr.histos['elphiso'].Fill(evt.phiso2/evt.pt2, weight*evt.puW)
					sr.histos['elchiso'].Fill(evt.chiso1/evt.pt1, weight*evt.puW)
					sr.histos['elchiso'].Fill(evt.chiso2/evt.pt2, weight*evt.puW)
					sr.histos['elpucor'].Fill(evt.pucor1, weight*evt.puW)
					sr.histos['elpucor'].Fill(evt.pucor2, weight*evt.puW)
				
				sr.cats[type].npp += evt.npp*weight
				sr.cats[type].npf += evt.npf*weight
				sr.cats[type].nfp += evt.nfp*weight
				sr.cats[type].nff += evt.nff*weight
		
				sr.cats[type].npp2 += evt.npp*evt.npp*weight*weight
				sr.cats[type].npf2 += evt.npf*evt.npf*weight*weight
				sr.cats[type].nfp2 += evt.nfp*evt.nfp*weight*weight
				sr.cats[type].nff2 += evt.nff*evt.nff*weight*weight
	
				if   evt.tlcat is 0:
					sr.cats[type].ntt  +=weight
					sr.cats[type].ntt2 +=weight*weight
					sr.cats[type].nttc +=1
		
				elif evt.tlcat is 1:
					sr.cats[type].ntl  +=weight
					sr.cats[type].ntl2 +=weight*weight
					sr.cats[type].ntlc +=1
		
				elif evt.tlcat is 2:
					sr.cats[type].nlt  +=weight
					sr.cats[type].nlt2 +=weight*weight
					sr.cats[type].nltc +=1
		
				elif evt.tlcat is 3:
					sr.cats[type].nll  +=weight
					sr.cats[type].nll2 +=weight*weight
					sr.cats[type].nllc +=1
	
			sample.loaded = True
	
	for sample in samples:
		if not os.path.isfile('samples/'+sample.name+'.pk'):
			pickle.dump(sample, open('samples/'+sample.name+'.pk','wb'), pickle.HIGHEST_PROTOCOL)
	
	## adding up all the samples
	totals = helper.sample('total','')
	for sample in samples:
		if sample.isdata: continue
		totals += sample
	samples.append(totals)

	loaded = True

#def isoplots():
for i in range(len(samples[0].regions)):
	for key in samples[0].regions[i].histos.keys():
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
				sample.regions[i].histos[key].SetFillColor(sample.color)
				mumcint += sample.regions[i].histos[key].Integral()
				mumcstack.Add(sample.regions[i].histos[key])
				mulegend.AddEntry(sample.regions[i].histos[key], sample.name, 'f')
			#electrons 
			if 'el' in key:
				sample.regions[i].histos[key].SetFillColor(sample.color)
				elmcint += sample.regions[i].histos[key].Integral()
				elmcstack.Add(sample.regions[i].histos[key])
				ellegend.AddEntry(sample.regions[i].histos[key], sample.name, 'f')
		
		
		if 'mu' in key:
			mulegend.AddEntry(doublemu.regions[i].histos[key], doublemu.name, 'pe')
			mufunc = helper.canvasWithRatio(mumcstack, doublemu.regions[i].histos[key], mulegend)
			cmu = mufunc[0] #don't ask me why this is necessary
			cmu.Update()
			cmu.Draw()
			cmu.SaveAs('figs/mu_'+key+'_sideband_'+samples[0].regions[i].name+'.pdf')
			cmu.SaveAs('figs/mu_'+key+'_sideband_'+samples[0].regions[i].name+'.png')
			cmu.SaveAs('figs/mu_'+key+'_sideband_'+samples[0].regions[i].name+'.root')
	
		if 'el' in key:
			ellegend.AddEntry(doubleel.regions[i].histos[key], doubleel.name, 'pe')
			elfunc = helper.canvasWithRatio(elmcstack, doubleel.regions[i].histos[key], ellegend)
			cel = elfunc[0] #don't ask me why this is necessary
			cel.Update()
			cel.Draw()
			cel.SaveAs('figs/el_'+key+'_sideband_'+samples[0].regions[i].name+'.pdf')
			cel.SaveAs('figs/el_'+key+'_sideband_'+samples[0].regions[i].name+'.png')
			cel.SaveAs('figs/el_'+key+'_sideband_'+samples[0].regions[i].name+'.root')



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
