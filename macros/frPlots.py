import ROOT, helper

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

def getColor(self):
	mycolor = ROOT.TColor()
	if   self.name == 'wjets'        : return mycolor.GetColor(102, 0, 0)
	elif self.name == 'dyjets'       : return mycolor.GetColor(255, 204, 0)
	elif self.name == 'qcdMuEnriched': return mycolor.GetColor(51, 102, 153)
	elif self.name == 'data'         : return ROOT.kBlack
	

class sample:
	def __init__(self, name, infile):
		self.name   = name
		self.file   = ROOT.TFile(infile)
		self.hists  = [self.file.Get(self.name+'/'+i.GetName()) for i in self.file.GetDirectory(self.name).GetListOfKeys() ]
		for i in self.hists:
			i.SetFillColor(getColor(self))
		self.isdata = (self.name == 'data')
		if self.isdata: 
			for i in self.hists: i.SetMarkerStyle(20)
	color  = getColor
	

data   = sample('data'         , '../fakeHistos/data_ratios.root')
wjets  = sample('wjets'        , '../fakeHistos/wjets_ratios.root')
dyjets = sample('dyjets'       , '../fakeHistos/dyjets_ratios.root')
qcd    = sample('qcdMuEnriched', '../fakeHistos/qcdMuEnriched_ratios.root')

mc_samples = []
mc_samples.append(qcd   )
mc_samples.append(wjets )
mc_samples.append(dyjets)


canv = helper.makeCanvas(900, 675)
canv.cd()

leg = helper.makeLegend(0.70, 0.65, 0.95, 0.90)

leg.AddEntry(data  .hists[0], 'Data'    , 'pe')
leg.AddEntry(wjets .hists[0], 'W+Jets'  , 'f' )
leg.AddEntry(dyjets.hists[0], 'DY+Jets' , 'f' )
leg.AddEntry(qcd   .hists[0], 'QCD'     , 'f' )

plotHists = ['h_Loose_muAwayJetDR', 'h_Loose_muAwayJetPt', 'h_Loose_muClosJetDR', 'h_Loose_muClosJetPt', 'h_Loose_muHT', 'h_Loose_muLepEta', 'h_Loose_muLepIso', 'h_Loose_muLepPt', 'h_Loose_muMET', 'h_Loose_muMETnoMTCut', 'h_Loose_muMT', 'h_Loose_muMTMET30', 'h_Loose_muMaxJPt', 'h_Loose_muNBJets', 'h_Loose_muNJets', 'h_Loose_muNVertices', 'h_Loose_muD0', 'h_Tight_muAwayJetDR', 'h_Tight_muAwayJetPt', 'h_Tight_muClosJetDR', 'h_Tight_muClosJetPt', 'h_Tight_muHT', 'h_Tight_muLepEta', 'h_Tight_muLepIso', 'h_Tight_muLepPt', 'h_Tight_muMET', 'h_Tight_muMETnoMTCut', 'h_Tight_muMT', 'h_Tight_muMTMET30', 'h_Tight_muMaxJPt', 'h_Tight_muNBJets', 'h_Tight_muNJets', 'h_Tight_muNVertices', 'h_Tight_muD0']

plotSingle = []


for hist in qcd.hists:
	if hist.GetName() == 'h_muFLoose':
		FR_qcd_den = hist.ProjectionX()
		FR_qcd_den.SetName("FR_qcd_den")
	if hist.GetName() == 'h_muFTight':
		FR_qcd = hist.ProjectionX()
		FR_qcd.SetName("FR_qcd")


for hist in data.hists:

	i = data.hists.index(hist)
	if hist.GetName() == 'h_muFLoose':
		FR_data_den = hist.ProjectionX()
		FR_data_den.SetName("FR_data_den")
		FR_bg_den = FR_data_den.Clone()
		FR_bg_den.SetName("FR_bg_den")
		FR_bg_den.Reset()

		for mc in mc_samples:
			FR_bg_den.Add(mc.hists[i].ProjectionX())
		
	if hist.GetName() == 'h_muFTight':
		FR_data = hist.ProjectionX()
		FR_data.SetName("FR_data")
		FR_bg = FR_data.Clone()
		FR_bg.SetName("FR_bg")
		FR_bg.Reset()

		for mc in mc_samples:
			FR_bg.Add(mc.hists[i].ProjectionX())

	if not hist.GetName() in plotHists: continue

	prepend = ''
	postpend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'
	
	if hist.GetName() in plotSingle:
		hist.Draw("text colz e")
		postpend = '_data'
		helper.saveCanvas(canv, prepend + helper.getSaveName(hist) + postpend)

		for mc in mc_samples:
			mc.hists[i].Draw("text colz e")
			postpend = '_' + mc.name
			helper.saveCanvas(canv, prepend + helper.getSaveName(mc.hists[i]) + postpend)

	else:
		stack = ROOT.THStack()
		stackint = 0.
		for mc in mc_samples:
			stackint += mc.hists[i].Integral()
			stack.Add(mc.hists[i])
		yscale = max(stack.GetMaximum(), hist.GetMaximum())
		stack.Draw('hist')
		stack.SetMaximum(1.2*yscale)
		stack.GetXaxis().SetTitle(helper.getXTitle(hist))
		## hist.Scale(stackint/hist.Integral())
		if not hist.GetName() in plotSingle: # with this step, we plot only total mc (stack) without data as data already is plotted solely before
			hist.Draw('p e1 same')
			leg.Draw()
		helper.saveCanvas(canv, prepend + helper.getSaveName(hist) + postpend)



FR_data.Divide(FR_data_den)
FR_data.SetFillColor(ROOT.kBlack)
FR_bg.Divide(FR_bg_den)
FR_bg.SetFillColor(ROOT.kRed)
FR_qcd.Divide(FR_qcd_den)
FR_qcd.SetFillColor(ROOT.kBlue)

FR_bg.Draw("hist")
FR_qcd.Draw("hist same")
FR_data.Draw("e same")

leg = helper.makeLegend(0.15, 0.35, 0.4, 0.60)
leg.AddEntry(FR_data, 'Data'  , 'pe')
leg.AddEntry(FR_bg, 'QCD + EW', 'f' )
leg.AddEntry(FR_qcd, 'QCD'    , 'f' )
leg.Draw()

helper.saveCanvas(canv, "muFakeRatio")






