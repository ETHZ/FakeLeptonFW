import ROOT, math, lib, copy


def divWithErr(a, ae, b, be):
	central = a/b
	relerr_a = ae/a
	relerr_b = be/b
	relerr_tot = relerr_a + relerr_b
	return central, central*relerr_tot

class cat:
	def __init__(self, name):
		self.name = name
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

class sample:
	def __init__(self, name, file):
		self.name = name
		self.file = ROOT.TFile(file)
		#self.tree = ROOT.TFile(file).Get('closureTree')
		self.tree = self.file.Get('closureTree')
		self.mm = cat('MUON-MUON')
		self.em = cat('MUON-ELECTRON')
		self.ee = cat('ELECTRON-ELECTRON')
		self.cats = [self.mm, self.em, self.ee]
		self.number = 0
		self.color = lib.getColor(name)
		if name in ['doublemu', 'doubleel']:
			self.isdata = True
		else:
			self.isdata = False
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

def canvasWithRatio(stack, histo, legend):
	c1 = ROOT.TCanvas('canvas', 'canvas', 900, 675)
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
	histocp.SetStats(0)
	#histocp.Scale(1./histocp.Integral())
	histocp.Divide(stackhisto)
	histocp.GetYaxis().SetRangeUser(0.00, 1.60)
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

	line = lib.makeLine(0., 1., 1., 1.)
	line.Draw('same')
	pad_ratio.Draw()
	c1.Update()
	return c1, stackhisto, histocp, stackcp, newstack, histonorm, line


