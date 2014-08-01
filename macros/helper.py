import ROOT, math, lib, copy


def divWithErr(a, ae, b, be):
	central = a/b
	relerr_a = ae/a
	relerr_b = be/b
	relerr_tot = relerr_a + relerr_b
	return central, central*relerr_tot

def getValue(var, sys, evt):
	if   var == 'met':
		if sys == 'nom'  : return evt.met
		if sys == 'jesup': return evt.met_jesup
		if sys == 'jesdn': return evt.met_jesdn
		if sys == 'jer'  : return evt.met_jer
		if sys == 'bup'  : return evt.met_bup
		if sys == 'bdn'  : return evt.met_bdn
	elif var == 'ht':
		if sys == 'nom'  : return evt.ht
		if sys == 'jesup': return evt.ht_jesup
		if sys == 'jesdn': return evt.ht_jesdn
		if sys == 'jer'  : return evt.ht_jer
		if sys == 'bup'  : return evt.ht_bup
		if sys == 'bdn'  : return evt.ht_bdn
	elif var == 'nj':
		if sys == 'nom'  : return evt.nj
		if sys == 'jesup': return evt.nj_jesup
		if sys == 'jesdn': return evt.nj_jesdn
		if sys == 'jer'  : return evt.nj_jer
		if sys == 'bup'  : return evt.nj_bup
		if sys == 'bdn'  : return evt.nj_bdn
	elif var == 'nb':
		if sys == 'nom'  : return evt.nb
		if sys == 'jesup': return evt.nb_jesup
		if sys == 'jesdn': return evt.nb_jesdn
		if sys == 'jer'  : return evt.nb_jer
		if sys == 'bup'  : return evt.nb_bup
		if sys == 'bdn'  : return evt.nb_bdn
	else: 
		print 'trying to get the wrong variable/systematic combination. look into getValue function'
	

def getBinning(var):
	if   var == 'met': return [20,  0., 200.]
	elif var == 'ht' : return [18, 50., 500.]
	elif var == 'nj' : return [ 6,  0 ,   6 ]
	elif var == 'nb' : return [ 6,  0 ,   6 ]
	else:
		print 'look at getBinnning Function, something is wrong'

class cat:
	def __init__(self, sname, rname, name):
		self.name = name
		self.histos = {}
		## kinematic histograms
		for sys in ['nom', 'jesup', 'jesdn', 'jer', 'bup', 'bdn']:
			self.histos[sys] = {}
			for var in ['met', 'ht', 'nj', 'nb']:
				self.histos[sys][var] = {}
				b = getBinning(var)
				self.histos[sys][var]['ll'] = ROOT.TH1F(sname+'_'+rname+'_'+name+'_h_'+var+sys+'_ll', sname+'_'+rname+'_'+name+'_h_'+var+sys+'_ll', b[0], b[1], b[2]); self.histos[sys][var]['ll'].Sumw2()
				self.histos[sys][var]['tl'] = ROOT.TH1F(sname+'_'+rname+'_'+name+'_h_'+var+sys+'_tl', sname+'_'+rname+'_'+name+'_h_'+var+sys+'_tl', b[0], b[1], b[2]); self.histos[sys][var]['tl'].Sumw2()
				self.histos[sys][var]['tt'] = ROOT.TH1F(sname+'_'+rname+'_'+name+'_h_'+var+sys+'_tt', sname+'_'+rname+'_'+name+'_h_'+var+sys+'_tt', b[0], b[1], b[2]); self.histos[sys][var]['tt'].Sumw2()

	nttc , ntlc , nltc , nllc = 0  , 0  , 0  , 0
	ntt  , ntl  , nlt  , nll  = 0. , 0. , 0. , 0.
	npp  , npf  , nfp  , nff  = 0  , 0  , 0  , 0
	ntt2 , ntl2 , nlt2 , nll2 = 0. , 0. , 0. , 0.
	npp2 , npf2 , nfp2 , nff2 = 0  , 0  , 0  , 0

	def __add__(self, other):
		self.nttc = self.nttc + other.nttc ; self.ntlc = self.ntlc + other.ntlc ; self.nltc = self.nltc + other.nltc ; self.nllc = self.nllc + other.nllc
		self.ntt  = self.ntt  + other.ntt  ; self.ntl  = self.ntl  + other.ntl  ; self.nlt  = self.nlt  + other.nlt  ; self.nll  = self.nll  + other.nll 
		self.npp  = self.npp  + other.npp  ; self.npf  = self.npf  + other.npf  ; self.nfp  = self.nfp  + other.nfp  ; self.nff  = self.nff  + other.nff 
		self.ntt2 = self.ntt2 + other.ntt2 ; self.ntl2 = self.ntl2 + other.ntl2 ; self.nlt2 = self.nlt2 + other.nlt2 ; self.nll2 = self.nll2 + other.nll2
		self.npp2 = self.npp2 + other.npp2 ; self.npf2 = self.npf2 + other.npf2 ; self.nfp2 = self.nfp2 + other.nfp2 ; self.nff2 = self.nff2 + other.nff2
		return self
	def __iadd__(self, other):
		self.nttc = self.nttc + other.nttc ; self.ntlc = self.ntlc + other.ntlc ; self.nltc = self.nltc + other.nltc ; self.nllc = self.nllc + other.nllc
		self.ntt  = self.ntt  + other.ntt  ; self.ntl  = self.ntl  + other.ntl  ; self.nlt  = self.nlt  + other.nlt  ; self.nll  = self.nll  + other.nll 
		self.npp  = self.npp  + other.npp  ; self.npf  = self.npf  + other.npf  ; self.nfp  = self.nfp  + other.nfp  ; self.nff  = self.nff  + other.nff 
		self.ntt2 = self.ntt2 + other.ntt2 ; self.ntl2 = self.ntl2 + other.ntl2 ; self.nlt2 = self.nlt2 + other.nlt2 ; self.nll2 = self.nll2 + other.nll2
		self.npp2 = self.npp2 + other.npp2 ; self.npf2 = self.npf2 + other.npf2 ; self.nfp2 = self.nfp2 + other.nfp2 ; self.nff2 = self.nff2 + other.nff2
		return self

class region:
	def __init__(self, sname, name):
		self.name = name
		self.mm = cat(sname, name, 'MUON-MUON')
		self.em = cat(sname, name, 'MUON-ELECTRON')
		self.ee = cat(sname, name, 'ELECTRON-ELECTRON')
		self.cats = [self.mm, self.em, self.ee]
		self.histos = {}
	def __iadd__(self, other):
		self.mm = self.mm + other.mm
		self.em = self.em + other.em
		self.ee = self.ee + other.ee
		return self
	def __add__(self, other):
		self.mm = self.mm + other.mm
		self.em = self.em + other.em
		self.ee = self.ee + other.ee
		return self

class sample:
	def __init__(self, name, file):
		self.name = name
		self.file = ROOT.TFile(file)
		#self.tree = ROOT.TFile(file).Get('closureTree')
		self.tree = self.file.Get('closureTree')
		#self.mm = cat('MUON-MUON')
		#self.em = cat('MUON-ELECTRON')
		#self.ee = cat('ELECTRON-ELECTRON')
		#self.cats = [self.mm, self.em, self.ee]
		#self.histos = {}
		self.regions = []
		self.color = lib.getColor(name)
		self.loaded = False
		if name in ['doublemu', 'doubleel']:
			self.isdata = True
		else:
			self.isdata = False
	def __iadd__(self, other):
		for region in self.regions:
			 region = region + other.regions[self.region.index(region)]
		#self.em = self.em + other.em
		#self.ee = self.ee + other.ee
		return self
	def __add__(self, other):
		for region in self.regions:
			 region = region + other.regions[self.region.index(region)]
		#self.mm = self.mm + other.mm
		#self.em = self.em + other.em
		#self.ee = self.ee + other.ee
		return self

def passRegion(sr, evt):
	passes = True
	if sr  in ['a', 'A']:
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.nj   <   2: passes = False
		if evt.nb  !=   0: passes = False
		if evt.met  < 30.: passes = False
	
	elif sr in ['b', 'B']:
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.type > 2: passes = False
		if evt.nj  <   2: passes = False
		if evt.nb  <   1: passes = False
		if evt.met < 30.: passes = False
	
	elif sr == 3:
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.nj  <   2: passes = False
		if evt.nb  <   2: passes = False
		if evt.met < 30.: passes = False
	
	elif sr == 'wjets':
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.type not in [0,1,2] : passes = False
		if evt.nj  <   0: passes = False
		if evt.nb !=   0: passes = False
		if evt.iso1 < evt.iso2:
			if not 60 < evt.mt1 < 100: passes =False
		else:
			if not 60 < evt.mt2 < 100: passes =False
		#if evt.met < 30.: passes = False
	
	elif sr == 'ttjets':
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.type not in [0,1,2] : passes = False
		if evt.nj <   3: passes = False
		if evt.nb !=  1: passes = False
		#if evt.met < 30.: passes = False

	elif sr == 'ttjets_ht200met100':
		if evt.type not in [0,1,2] : passes = False
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.nj <   3: passes = False
		if evt.nb !=  1: passes = False
		if evt.ht  <  200: passes = False
		if evt.met <  100: passes = False
	
	elif sr == 'ttjets_ht300met100':
		if evt.type not in [0,1,2] : passes = False
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.nj <   3: passes = False
		if evt.nb !=  1: passes = False
		if evt.ht  <  300: passes = False
		if evt.met <  100: passes = False
	
	elif sr == 'ttjets_ht400met120':
		if evt.type not in [0,1,2] : passes = False
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.nj <   3: passes = False
		if evt.nb !=  1: passes = False
		if evt.ht  <  400: passes = False
		if evt.met <  120: passes = False
	
	elif sr == 'ttjets_ht200':
		if evt.type not in [0,1,2] : passes = False
		if evt.pt1 < 20 or evt.pt2 < 20: passes = False
		if evt.nj <   3: passes = False
		if evt.nb !=  1: passes = False
		if evt.ht  <  200: passes = False

	else:
		print 'this signal region doesn\'t exist:', sr
		passes = False
	return passes

def canvasWithRatio(stack, histo, legend):
	c1 = ROOT.TCanvas('canvas', 'canvas', 675, 675)
	pad_plot  = lib.makePad('plot')
	pad_ratio = lib.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

	stackcp = copy.deepcopy(stack)
	stackhisto = copy.deepcopy(stackcp.GetStack().Last())
	hlist = stackcp.GetHists()
	newstack = ROOT.THStack('st', 'st')
	for i in hlist:
		i.Scale(1./stackhisto.Integral())
		newstack.Add(copy.deepcopy(i))
	
	pad_plot.cd()
	stackcp.Draw('hist')
	stackcp.GetYaxis().SetLabelSize(0.05)

	histoerr = copy.deepcopy(stackhisto)
	histoerr.SetFillColor(ROOT.kGray+3)
	histoerr.SetLineColor(ROOT.kGray+3)
	histoerr.SetFillStyle(3004)
	histoerr.Draw('same e2')

	#newstack.Draw('hist')
	histo.SetMarkerStyle(20)
	histo.SetMarkerSize(0.9)
	histo.SetMarkerColor(ROOT.kBlack)
	histo.SetLineColor(ROOT.kBlack)
	histonorm = copy.deepcopy(histo)
	#histonorm.Scale(1./histonorm.Integral())
	histonorm.Draw('same pe')

	stackmax = stackcp.GetMaximum()
	histomax = histo.GetMaximum()
	stackcp.SetMaximum(1.15* max(stackmax, histomax) )

	legend.Draw('same')
	
	pad_ratio.cd()
	#stackhisto.Scale(1./stackhisto.Integral())
	histocp = copy.deepcopy(histo)
	histocp.SetName('ratio')
	histocp.SetStats(0)
	#histocp.Scale(1./histocp.Integral())
	histocp.Divide(stackhisto)
	histocp.GetYaxis().SetRangeUser(0.00, 2.0)
	histocp.Draw('pe')
	histocp.GetYaxis().SetNdivisions(505)
	histocp.GetYaxis().SetLabelSize(0.08)
	histocp.GetXaxis().SetLabelSize(0.12)
	histocp.GetXaxis().SetTitle(histocp.GetName().split('_')[0])
	histocp.GetXaxis().SetTitleOffset(1.15)
	histocp.GetXaxis().SetTitleSize(0.15)
	histocp.SetTitle('')

	fl = ROOT.TF1("fl","[0]*x+[1]",0.,1.)
	histocp.Fit(fl)
	fl.Draw('same')

	line = lib.makeLine(histocp.GetXaxis().GetXmin(), 1., histocp.GetXaxis().GetXmax(), 1.)
	line.Draw('same')
	pad_ratio.Draw()
	pad_ratio.Update()
	c1.Update()
	return c1, stackhisto, histocp, stackcp, newstack, histonorm, line, histoerr


def getLatexVariable(var):
	if var == 'ht' : return 'H_{T}'
	if var == 'met': return 'ME_{T}'
	if var == 'nj' : return 'N_{jets}'
	if var == 'nb' : return 'N_{b-jets}'

def getLatexType(typ):
	if typ == 'tt' : return 'tight-tight'
	if typ == 'tl' : return 'tight-loose'
	if typ == 'lt' : return 'loose-tight'
	if typ == 'll' : return 'loose-loose'

def saveAll(canv, name):
	canv.SaveAs(name+'.pdf')
	canv.SaveAs(name+'.png')
	#canv.SaveAs(name+'.root')
