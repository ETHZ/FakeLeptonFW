import ROOT, helper

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
	

data   = sample('data'         , '../outputDir/data_ratios.root')
wjets  = sample('wjets'        , '../outputDir/wjets_ratios.root')
dyjets = sample('dyjets'       , '../outputDir/dyjets_ratios.root')
qcd    = sample('qcdMuEnriched', '../outputDir/qcdMuEnriched_ratios.root')

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

plotHists = ['h_Loose_muAwayJetDR', 'h_Loose_muAwayJetPt', 'h_Loose_muClosJetDR', 'h_Loose_muClosJetPt', 'h_Loose_muHT', 'h_Loose_muLepEta', 'h_Loose_muLepIso', 'h_Loose_muLepPt', 'h_Loose_muMET', 'h_Loose_muMETnoMTCut', 'h_Loose_muMT', 'h_Loose_muMTMET30', 'h_Loose_muMaxJPt', 'h_Loose_muNBJets', 'h_Loose_muNJets', 'h_Loose_muNVertices', 'h_Loose_muD0', 'h_Loose_muF', 'h_Tight_muAwayJetDR', 'h_Tight_muAwayJetPt', 'h_Tight_muClosJetDR', 'h_Tight_muClosJetPt', 'h_Tight_muHT', 'h_Tight_muLepEta', 'h_Tight_muLepIso', 'h_Tight_muLepPt', 'h_Tight_muMET', 'h_Tight_muMETnoMTCut', 'h_Tight_muMT', 'h_Tight_muMTMET30', 'h_Tight_muMaxJPt', 'h_Tight_muNBJets', 'h_Tight_muNJets', 'h_Tight_muNVertices', 'h_Tight_muD0', 'h_Tight_muF']

for hist in data.hists:
	i = data.hists.index(hist)
	if not hist.GetName() in plotHists: continue
	stack = ROOT.THStack()
	stackint = 0.
	for mc in mc_samples:
		stackint += mc.hists[i].Integral()
		stack.Add(mc.hists[i])
	yscale = max(stack.GetMaximum(), hist.GetMaximum())
	stack.Draw('hist')
	stack.SetMaximum(1.2*yscale)
	stack.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.Scale(stackint/hist.Integral())
	hist.Draw('p e1 same')
	leg.Draw()
	prepend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'
	canv.SaveAs(prepend+helper.getSaveName(hist)+'.pdf')
	canv.SaveAs(prepend+helper.getSaveName(hist)+'.png')


