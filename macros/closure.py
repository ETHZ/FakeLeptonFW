import ROOT, math, helper, sys, lib, copy, pickle, os


# definig all the signal regions. here only by name
SRs = [
	'B',
	'wjets',
	'ttjets', 
	'ttjets_ht200',
	'ttjets_ht200met100',
	'ttjets_ht300met100',
	'ttjets_ht400met120'
]

if not 'loaded' in globals():
	print 'loaded is not in globals'
	global loaded
	loaded = False

if not loaded:
	ttjets_sl = helper.sample('ttjets_sl','../closureTest/ttjets_semi_closureOutput_SS.root'  )
	ttjets_fl = helper.sample('ttjets_fl','../closureTest/ttjets_full_closureOutput_SS.root'  )
	ttjets_ha = helper.sample('ttjets_ha','../closureTest/ttjets_hadronic_closureOutput_SS.root'  )
	singletop = helper.sample('singletop','../closureTest/singletop_closureOutput_SS.root'  )
	wjets     = helper.sample('wjets'    ,'../closureTest/wnjets_closureOutput_SS.root'  )
	rares     = helper.sample('rares'    ,'../closureTest/rares_closureOutput_SS.root')
	#qcdmuenr  = helper.sample('qcdmuenr' ,'../closureTest/qcdmuenr_closureOutput_SS.root')
#	dyjets    = helper.sample('dyjets'   ,'../closureTest/dyjets_closureOutput.root'  )
	doublemu  = helper.sample('doublemu' ,'../closureTest/doublemu_closureOutput_SS.root')
	doubleel  = helper.sample('doubleel' ,'../closureTest/doubleel_closureOutput_SS.root')
	samples = [ rares, wjets, ttjets_fl, ttjets_sl, ttjets_ha, singletop, doublemu, doubleel]
	#samples = [ ttjets_sl]
	for sample in samples:
		for sr in SRs:
			sample.regions.append(helper.region(sample.name, sr))

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
			ttjets_ha = (x for x in samples if x.name == 'ttjets_ha').next()
			singletop = (x for x in samples if x.name == 'singletop').next()
			#qcdmuenr  = (x for x in samples if x.name == 'qcdmuenr' ).next()
			rares     = (x for x in samples if x.name == 'rares'    ).next()
			wjets     = (x for x in samples if x.name == 'wjets'    ).next()
			#dyjets    = (x for x in samples if x.name == 'dyjets'   ).next()
	samples = [ rares, wjets, ttjets_fl, ttjets_sl, ttjets_ha, singletop, doublemu, doubleel]
	#samples = [ ttjets_sl]

	trigger = 1
	maxev = 10E20
	
	for sample in samples:
		print '--------------------------------------------'
		print 'AT SAMPLE:', sample.name
		print '--------------------------------------------'
		if sample.loaded == True: continue
		print 'loading sample', sample.name
		for sr in sample.regions: ## initialize all the histograms for all the regions
			i=0
			## muons
			sr.histos['muiso'   ] = ROOT.TH1F('muIso_'   +sr.name+'_'+sample.name, 'muIso_'   +sr.name+'_'+sample.name, 40, 0., 1.0)
			sr.histos['muisoTL' ] = ROOT.TH1F('muIsoTL_' +sr.name+'_'+sample.name, 'muIsoTL_' +sr.name+'_'+sample.name, 40, 0., 1.0)
			sr.histos['muisoT'  ] = ROOT.TH1F('muIsoT_'  +sr.name+'_'+sample.name, 'muIsoT_'  +sr.name+'_'+sample.name, 40, 0., 1.0)
			sr.histos['muisoL'  ] = ROOT.TH1F('muIsoL_'  +sr.name+'_'+sample.name, 'muIsoL_'  +sr.name+'_'+sample.name, 40, 0., 1.0)
			sr.histos['muisoTLT'] = ROOT.TH1F('muIsoTLT_'+sr.name+'_'+sample.name, 'muIsoTLT_'+sr.name+'_'+sample.name, 40, 0., 1.0)
			sr.histos['muisoTLL'] = ROOT.TH1F('muIsoTLL_'+sr.name+'_'+sample.name, 'muIsoTLL_'+sr.name+'_'+sample.name, 40, 0., 1.0)
			sr.histos['muip'    ] = ROOT.TH1F('muIP_'    +sr.name+'_'+sample.name, 'muIP_'    +sr.name+'_'+sample.name, 40, 0., 0.1)
			sr.histos['muipTL'  ] = ROOT.TH1F('muIPTL_'  +sr.name+'_'+sample.name, 'muIPTL_'  +sr.name+'_'+sample.name, 40, 0., 0.1)
			## electrons
			sr.histos['eliso'   ] = ROOT.TH1F('elIso_'   +sr.name+'_'+sample.name, 'elIso_'   +sr.name+'_'+sample.name, 20, 0., 0.6)
			sr.histos['elisoTL' ] = ROOT.TH1F('elIsoTL_' +sr.name+'_'+sample.name, 'elIsoTL_' +sr.name+'_'+sample.name, 20, 0., 0.6)
			sr.histos['elisoT'  ] = ROOT.TH1F('elIsoT_'  +sr.name+'_'+sample.name, 'elIsoT_'  +sr.name+'_'+sample.name, 20, 0., 0.6)
			sr.histos['elisoL'  ] = ROOT.TH1F('elIsoL_'  +sr.name+'_'+sample.name, 'elIsoL_'  +sr.name+'_'+sample.name, 20, 0., 0.6)
			sr.histos['elisoTLT'] = ROOT.TH1F('elIsoTLT_'+sr.name+'_'+sample.name, 'elIsoTLT_'+sr.name+'_'+sample.name, 20, 0., 0.6)
			sr.histos['elisoTLL'] = ROOT.TH1F('elIsoTLL_'+sr.name+'_'+sample.name, 'elIsoTLL_'+sr.name+'_'+sample.name, 20, 0., 0.6)
			sr.histos['elip'    ] = ROOT.TH1F('elIP_'    +sr.name+'_'+sample.name, 'elIP_'    +sr.name+'_'+sample.name, 20, 0., 0.1)
			sr.histos['elipTL'  ] = ROOT.TH1F('elIPTL_'  +sr.name+'_'+sample.name, 'elIPTL_'  +sr.name+'_'+sample.name, 20, 0., 0.1)
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

			if not evt.type in [0, 2]: continue # look only at mumu and elel
		
			for sr in sample.regions:
				if not helper.passRegion(sr.name, evt): continue
		
				## Fill the muons isolation for both muons regardless of tight/loose, but same-sign
				if evt.type in [0]:
					sr.histos['muiso'  ].Fill(evt.iso1, weight*evt.puW)
					sr.histos['muiso'  ].Fill(evt.iso2, weight*evt.puW)
					sr.histos['muisoT' ].Fill(evt.iso1 if evt.iso1 <= evt.iso2 else evt.iso2, weight*evt.puW)
					sr.histos['muisoL' ].Fill(evt.iso2 if evt.iso1 <= evt.iso2 else evt.iso1, weight*evt.puW)
					sr.histos['muip'   ].Fill(evt.ip1 , weight*evt.puW)
					sr.histos['muip'   ].Fill(evt.ip2 , weight*evt.puW)
					if evt.tlcat in [1,2]: 
						sr.histos['muisoTL' ].Fill(evt.iso1, weight*evt.puW)
						sr.histos['muisoTL' ].Fill(evt.iso2, weight*evt.puW)
						sr.histos['muisoTLT'].Fill(evt.iso1 if evt.iso1 <= evt.iso2 else evt.iso2, weight*evt.puW)
						sr.histos['muisoTLL'].Fill(evt.iso2 if evt.iso1 <= evt.iso2 else evt.iso1, weight*evt.puW)
						sr.histos['muipTL'  ].Fill(evt.ip1 , weight*evt.puW)
						sr.histos['muipTL'  ].Fill(evt.ip2 , weight*evt.puW)
				if evt.type in [1]:
					sr.histos['muiso'].Fill(evt.iso1, weight*evt.puW)
					sr.histos['eliso'].Fill(evt.iso2, weight*evt.puW)
				if evt.type in [2]:
					sr.histos['eliso'  ].Fill(evt.iso1, weight*evt.puW)
					sr.histos['eliso'  ].Fill(evt.iso2, weight*evt.puW)
					sr.histos['elisoT' ].Fill(evt.iso1 if evt.iso1 <= evt.iso2 else evt.iso2, weight*evt.puW)
					sr.histos['elisoL' ].Fill(evt.iso2 if evt.iso1 <= evt.iso2 else evt.iso1, weight*evt.puW)
					sr.histos['elip'   ].Fill(evt.ip1 , weight*evt.puW)
					sr.histos['elip'   ].Fill(evt.ip2 , weight*evt.puW)
					if evt.tlcat in [1,2]: 
						sr.histos['elisoTL'].Fill(evt.iso1, weight*evt.puW)
						sr.histos['elisoTL'].Fill(evt.iso2, weight*evt.puW)
						sr.histos['elisoTLT'].Fill(evt.iso1 if evt.iso1 <= evt.iso2 else evt.iso2, weight*evt.puW)
						sr.histos['elisoTLL'].Fill(evt.iso2 if evt.iso1 <= evt.iso2 else evt.iso1, weight*evt.puW)
						sr.histos['elipTL' ].Fill(evt.ip1 , weight*evt.puW)
						sr.histos['elipTL' ].Fill(evt.ip2 , weight*evt.puW)
				
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

				for sys in ['nom', 'jesup', 'jesdn', 'jer', 'bup', 'bdn']:
					for var in ['met', 'ht', 'nj', 'nb']:
						val    = helper.getValue(var, sys, evt)
						maxval = sr.cats[type].histos[sys][var]['tt'].GetXaxis().GetXmax()
						if   evt.tlcat is 0:
							sr.cats[type].histos[sys][var]['tt'].Fill(val if val < maxval else maxval - 0.0001, weight)
		
						elif evt.tlcat is 1:
							sr.cats[type].histos[sys][var]['tl'].Fill(val if val < maxval else maxval - 0.0001, weight)
		
						elif evt.tlcat is 2:
							sr.cats[type].histos[sys][var]['tl'].Fill(val if val < maxval else maxval - 0.0001, weight)
		
						elif evt.tlcat is 3:
							sr.cats[type].histos[sys][var]['ll'].Fill(val if val < maxval else maxval - 0.0001, weight)
	
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

def isoplots(region):
	ROOT.gROOT.SetBatch()
	reg = SRs.index(region)
	for key in samples[0].regions[reg].histos.keys():
		if not key in ['muiso', 'muisoT', 'muisoL', 'muisoTL', 'muisoTLT', 'muisoTLL', 'muip', 'muipTL',  
		               'eliso', 'elisoT', 'elisoL', 'elisoTL', 'elisoTLT', 'elisoTLL', 'elip', 'elipTL' ]: continue
		if 'mu' in key:
			mulegend = lib.makeLegend(0.4, 0.6, 0.6, 0.87)
			mulegend.SetTextSize(0.04)
			mumcstack = ROOT.THStack('mumcstack', 'mumcstack')
			mumcint = 0.
		if 'el' in key:
			ellegend = lib.makeLegend(0.6, 0.6, 0.8, 0.8)
			ellegend.SetTextSize(0.04)
			elmcstack = ROOT.THStack('elmcstack', 'elmcstack')
			elmcint = 0.
		for sample in samples:
			if sample == totals or sample.isdata: continue
			#muons 
			if 'mu' in key:
				sample.regions[reg].histos[key].SetFillColor(sample.color)
				mumcint += sample.regions[reg].histos[key].Integral()
				mumcstack.Add(sample.regions[reg].histos[key])
				mulegend.AddEntry(sample.regions[reg].histos[key], sample.name, 'f')
			#electrons 
			if 'el' in key:
				sample.regions[reg].histos[key].SetFillColor(sample.color)
				elmcint += sample.regions[reg].histos[key].Integral()
				elmcstack.Add(sample.regions[reg].histos[key])
				ellegend.AddEntry(sample.regions[reg].histos[key], sample.name, 'f')
		
		if 'mu' in key:
			mulegend.AddEntry(doublemu.regions[reg].histos[key], doublemu.name, 'pe')
			mufunc = helper.canvasWithRatio(mumcstack, doublemu.regions[reg].histos[key], mulegend)
			cmu = mufunc[0] #don't ask me why this is necessary
			cmu.Update()
			cmu.Draw()
			helper.saveAll(cmu, 'figs/'+key+'_sideband_'+samples[0].regions[reg].name)
	 
		if 'el' in key:
			ellegend.AddEntry(doubleel.regions[reg].histos[key], doubleel.name, 'pe')
			elfunc = helper.canvasWithRatio(elmcstack, doubleel.regions[reg].histos[key], ellegend)
			cel = elfunc[0] #don't ask me why this is necessary
			cel.Update()
			cel.Draw()
			helper.saveAll(cel, 'figs/'+key+'_sideband_'+samples[0].regions[reg].name)
	return

incQCD = False

def kinematicDistributions(region):
	ROOT.gROOT.SetBatch()
	for var in samples[0].regions[0].mm.histos['nom'].keys():
		print 'at variable:', var
		for t in ['tt', 'tl', 'll']:
			print 'at type:', t
			for sys in ['nom', 'jesup', 'jesdn', 'jer', 'bup', 'bdn']:
				print 'at systematic:', sys
				legend = lib.makeLegend(0.6, 0.6, 0.8, 0.87)
				legend.SetTextSize(0.04)
				mcstack = ROOT.THStack('mcstack', 'mcstack')
				mcint = 0.
				for sample in samples:
					if  incQCD == False:
						if 'qcd' in sample.name: continue
					if sample == totals or sample.isdata: continue
					#
					reg = SRs.index(region)
					print sample.name
					sample.regions[reg].mm.histos[sys][var][t].SetFillColor(sample.color)
					mcint += sample.regions[reg].mm.histos[sys][var][t].Integral()
					mcstack.Add(sample.regions[reg].mm.histos[sys][var][t])
					legend.AddEntry(sample.regions[reg].mm.histos[sys][var][t], sample.name, 'f')

				legend.AddEntry(doublemu.regions[reg].mm.histos[sys][var][t], doublemu.name, 'pe')
				func = helper.canvasWithRatio(mcstack, doublemu.regions[reg].mm.histos[sys][var][t], legend)
				c = func[0] #don't ask me why this is necessary
				print c.ls()
				c.Update()
				c.FindObject('ratio').GetXaxis().SetTitle(helper.getLatexVariable(var))
				c.FindObject('mcstack').SetTitle(helper.getLatexType(t))
				c.Draw()
				helper.saveAll(c, 'figs/'+var+'_'+doublemu.regions[reg].name+'_'+sys+'_'+t)
	return
		
	

def printout():
	for sample in samples:
		for region in sample.regions:
			for cat in region.cats:
				cat.fakes = cat.npf+cat.nfp+cat.nff
				cat.obs   = cat.ntt
				cat.ntte , cat.ntle , cat.nlte , cat.nlle  = math.sqrt(cat.ntt2), math.sqrt(cat.ntl2), math.sqrt(cat.nlt2), math.sqrt(cat.nll2)
				cat.nttce, cat.ntlce, cat.nltce, cat.nllce = math.sqrt(cat.nttc), math.sqrt(cat.ntlc), math.sqrt(cat.nltc), math.sqrt(cat.nllc)
				cat.nppe , cat.npfe , cat.nfpe , cat.nffe  = math.sqrt(cat.npp2), math.sqrt(cat.npf2), math.sqrt(cat.nfp2), math.sqrt(cat.nff2)
				cat.fakese = cat.npfe+cat.nfpe+cat.nffe
				cat.obse  = cat.ntte
	
	for r in range(len(SRs)):
		for i in range(3):  ## loop on all the categories
			print i
			print '\n\n\n'
			print '=============================================================================================================='
			print '                                          CATEGORY:', samples[0].regions[r].cats[i].name
			print '=============================================================================================================='
			print '%10s | %10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('SAMPLE', 'NTT','', 'NTL','', 'NLT','', 'NLL','', 'SUM','')
			print '--------------------------------------------------------------------------------------------------------------'
			for sample in samples:
				if sample.name == 'total': continue
				if samples.index(sample) == len(samples) -1:
					print '--------------------------------------------------------------------------------------------------------------'
				print '%10s | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
				      sample.name, sample.regions[r].cats[i].ntt, sample.regions[r].cats[i].ntte, sample.regions[r].cats[i].ntl, sample.regions[r].cats[i].ntle, sample.regions[r].cats[i].nlt, sample.regions[r].cats[i].nlte, sample.regions[r].cats[i].nll, sample.regions[r].cats[i].nlle, sample.regions[r].cats[i].ntt+sample.regions[r].cats[i].ntl+sample.regions[r].cats[i].nlt+sample.regions[r].cats[i].nll, sample.regions[r].cats[i].ntte+sample.regions[r].cats[i].ntle+sample.regions[r].cats[i].nlte+sample.regions[r].cats[i].nlle)
		
			print '--------------------------------------------------------------------------------------------------------------'
			print '--------------------------------------------------------------------------------------------------------------'
			print '%10s | %10s%9s | %10s%9s | %10s%9s | %10s%9s || %10s%9s' %('SAMPLE', 'NPP','', 'NPF','', 'NFP','', 'NFF','', 'SUM','')
			print '--------------------------------------------------------------------------------------------------------------'
			for sample in samples:
				if sample.name == 'total': continue
				if samples.index(sample) == len(samples) -1:
					print '--------------------------------------------------------------------------------------------------------------'
				print '%10s | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f | %10.2f +- %5.2f || %10.2f +- %5.2f' %(
				      sample.name, sample.regions[r].cats[i].npp, sample.regions[r].cats[i].nppe, sample.regions[r].cats[i].npf, sample.regions[r].cats[i].npfe, sample.regions[r].cats[i].nfp, sample.regions[r].cats[i].nfpe, sample.regions[r].cats[i].nff, sample.regions[r].cats[i].nffe, sample.regions[r].cats[i].npp+sample.regions[r].cats[i].npf+sample.regions[r].cats[i].nfp+sample.regions[r].cats[i].nff, sample.regions[r].cats[i].nppe+sample.regions[r].cats[i].npfe+sample.regions[r].cats[i].nfpe+sample.regions[r].cats[i].nffe)
		
			#print '--------------------------------------------------------------------------------------------------------------'
			#print 'OBSERVED     : %.2f +- %.2f' %(totals.regions[r].cats[i].obs  , totals.regions[r].cats[i].ntte)
			#print 'SUM OF FAKES : %.2f +- %.2f' %(totals.regions[r].cats[i].fakes, totals.regions[r].cats[i].npfe+totals.regions[r].cats[i].nfpe+totals.regions[r].cats[i].nffe)
		
			#if totals.cats[i].obs > 0:
			#	res    = helper.divWithErr(totals.regions[r].cats[i].fakes, totals.regions[r].cats[i].fakese, totals.regions[r].cats[i].obs, totals.regions[r].cats[i].obse)	
			#	relres = helper.divWithErr(totals.regions[r].cats[i].fakes - totals.regions[r].cats[i].obs, totals.regions[r].cats[i].fakese - totals.regions[r].cats[i].obse, totals.regions[r].cats[i].fakes, totals.regions[r].cats[i].fakese)	
			#else:
			#	res = [0,0]
			#	relres = [0,0]
			#print '\n------------------------------------------'
			#print '%25s %.3f +- %.3f' %('pred./ obs.:', res[0], res[1])
			#print '\n%25s %.3f +- %.3f' %('(pred. - obs.) / pred.:', relres[0], relres[1])
			#print '------------------------------------------'
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



if __name__ == '__main__':
	print 'in function main'
	#printout()
	#kinematicDistributions()
	#isoplots()
	
