## frPlots.py

## HEADER

import ROOT, helper, commands, sys

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

def getColor(self):
	mycolor = ROOT.TColor()
	if   self.name == 'wjets'        : return mycolor.GetColor(102, 0, 0)
	elif self.name == 'dyjets'       : return mycolor.GetColor(255, 204, 0)
	elif self.name == 'qcdMuEnriched': return mycolor.GetColor(51, 102, 153)
	elif self.name == 'data'         : return ROOT.kBlack


def getScaleFactor(dataset, histforscale, datasetforscale, minforint = 0, maxforint = 0):
	scalefactor = 1.0

	for hist in datasetforscale.hists:
		i = datasetforscale.hists.index(hist)
		if hist.GetName() == histforscale:
			if minforint == 0: minbin = 1
			else: minbin = hist.FindBin(minforint)
			if maxforint == 0: maxbin = hist.GetNbinsX()
			else: maxbin = hist.FindBin(maxforint)

			scalefactor = hist.Integral(minbin, maxbin) / dataset.hists[i].Integral(minbin, maxbin) 

	return scalefactor


class sample:
	def __init__(self, name, infile):
		self.name   = name
		self.file   = ROOT.TFile(infile)
		self.hists  = [self.file.Get(self.name+'/'+i.GetName()) for i in self.file.GetDirectory(self.name).GetListOfKeys() ]
		for h in self.hists: 
			h.SetFillColor(getColor(self))
		self.isdata = (self.name == 'data')
		if self.isdata: 
			for h in self.hists: 
				h.SetMarkerStyle(20)
	color  = getColor
	scale  = 1.0

	def Rescale(self, newscale):
		self.scale = newscale
		for h in self.hists: h.Scale(newscale)
	

args = sys.argv
directory = args[1]

data   = sample('data'         , directory + 'data_ratios.root')
wjets  = sample('wjets'        , directory + 'wjets_ratios.root')
dyjets = sample('dyjets'       , directory + 'dyjets_ratios.root')
qcd    = sample('qcdMuEnriched', directory + 'qcdMuEnriched_ratios.root')



## INITIALIZING SAMPLES, CANVAS, LEGEND

mc_samples = []
mc_samples.append(qcd   )
mc_samples.append(wjets )
mc_samples.append(dyjets)

canv = helper.makeCanvas(900, 675)
pad_plot = helper.makePad('plot')
pad_ratio = helper.makePad('ratio')
pad_plot.cd()

leg = helper.makeLegend(0.70, 0.65, 0.95, 0.90)
leg.AddEntry(data  .hists[0], 'Data'    , 'pe')
leg.AddEntry(wjets .hists[0], 'W+Jets'  , 'f' )
leg.AddEntry(dyjets.hists[0], 'DY+Jets' , 'f' )
leg.AddEntry(qcd   .hists[0], 'QCD'     , 'f' )


## LIST OF HISTOGRAMS TO PLOT

plotHists = ['h_Loose_muAwayJetDR', 'h_Loose_muAwayJetPt', 'h_Loose_muClosJetDR', 'h_Loose_muClosJetPt', 'h_Loose_muHT', 'h_Loose_muLepEta', 'h_Loose_muLepIso', 'h_Loose_muLepPt', 'h_Loose_muMET', 'h_Loose_muMETnoMTCut', 'h_Loose_muMT', 'h_Loose_muMTMET30', 'h_Loose_muMaxJPt', 'h_Loose_muNBJets', 'h_Loose_muNJets', 'h_Loose_muNVertices', 'h_Loose_muD0', 'h_Tight_muAwayJetDR', 'h_Tight_muAwayJetPt', 'h_Tight_muClosJetDR', 'h_Tight_muClosJetPt', 'h_Tight_muHT', 'h_Tight_muLepEta', 'h_Tight_muLepIso', 'h_Tight_muLepPt', 'h_Tight_muMET', 'h_Tight_muMETnoMTCut', 'h_Tight_muMT', 'h_Tight_muMTMET30', 'h_Tight_muMaxJPt', 'h_Tight_muNBJets', 'h_Tight_muNJets', 'h_Tight_muNVertices', 'h_Tight_muD0']


# Set Scaling Factors

qcd.Rescale(getScaleFactor(qcd, 'h_Loose_muLepIso', data, 0.2))
wjets.Rescale(getScaleFactor(wjets, 'h_Tight_muMTMET30', data, 60, 90))


# Get Numerator and Denominator from QCD Sample Alone

for hist in qcd.hists:
	if hist.GetName() == 'h_muFLoose':
		FR_qcd_den = hist
		FR_qcd_den.SetName("FR_qcd_den")
	if hist.GetName() == 'h_muFTight':
		FR_qcd = hist
		FR_qcd.SetName("FR_qcd")


# Run Over All Samples to Produce Plots

for hist in data.hists:

	i = data.hists.index(hist)
	pad_plot.cd()

	# Get Numerator Plots
	if hist.GetName() == 'h_muFTight':
		FR_data = hist
		FR_bg_ns = ROOT.THStack()
		for mc in mc_samples:
			FR_bg_ns.Add(mc.hists[i])

	# Get Denominator Histograms
	if hist.GetName() == 'h_muFLoose':
		FR_data_den = hist
		FR_bg_ds = ROOT.THStack()
		for mc in mc_samples:
			FR_bg_ds.Add(mc.hists[i])
	
	# Plot Histogram	
	if not hist.GetName() in plotHists: continue

	prepend = ''
	postpend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'

	# Sum Contributions in Stack
	stack = ROOT.THStack()
	stackint = 0.
	for j,mc in enumerate(mc_samples):
		stackint += mc.hists[i].Integral()
		stack.Add(mc.hists[i])
	yscale = max(stack.GetMaximum(), hist.GetMaximum())
	
	stack.Draw('hist')
	stack.SetMaximum(1.2*yscale)
	stack.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.Draw('p e1 same')
	leg.Draw()

	pad_ratio.cd()


	helper.saveCanvas(canv, prepend + helper.getSaveName(hist) + postpend)



# Computing FakeRate

pad_plot.cd()

FR_data_pt  = FR_data.ProjectionX('FR_data_pt')
FR_data_pt.Divide(FR_data_den.ProjectionX('FR_data_den_pt'))

FR_data_eta = FR_data.ProjectionY('FR_data_eta')
FR_data_eta.Divide(FR_data_den.ProjectionY('FR_data_den_eta'))

FR_qcd_pt   = FR_qcd.ProjectionX('FR_qcd_pt')
FR_qcd_pt.Divide(FR_qcd_den.ProjectionX('FR_qcd_den_pt'))

FR_qcd_eta  = FR_qcd.ProjectionY('FR_qcd_eta')
FR_qcd_eta.Divide(FR_qcd_den.ProjectionY('FR_qcd_den_eta'))

FR_bg       = FR_bg_ns.GetStack().Last()
FR_bg_den   = FR_bg_ds.GetStack().Last()

FR_bg_pt    = FR_bg.ProjectionX('FR_bg_pt')
FR_bg_pt.Divide(FR_bg_den.ProjectionX('FR_bg_den_pt'))

FR_bg_eta   = FR_bg.ProjectionY('FR_bg_eta')
FR_bg_eta.Divide(FR_bg_den.ProjectionY('FR_bg_den_eta'))



# Plotting FR vs Pt

FR_data_pt.SetMarkerSize(1.2)
FR_data_pt.SetMarkerStyle(20)
FR_data_pt.SetMarkerColor(getColor(data))

FR_bg_pt.SetMarkerSize(1.2)
FR_bg_pt.SetMarkerStyle(20)
FR_bg_pt.SetMarkerColor(getColor(wjets))

FR_qcd_pt.SetMarkerSize(1.2)
FR_qcd_pt.SetMarkerStyle(20)
FR_qcd_pt.SetMarkerColor(getColor(qcd))

FR_data_pt.Draw("p e1")
FR_bg_pt.Draw("p e1 same")
FR_qcd_pt.Draw("p e1 same")

FR_data_pt.SetMaximum(0.3)
FR_data_pt.GetXaxis().SetTitle(helper.getXTitle(data.hists[12]))
FR_data_pt.GetYaxis().SetTitle('FR')
FR_data_pt.SetTitle('muFakeRatio_pt')

l_pt = helper.makeLegend(0.15, 0.65, 0.4, 0.90)
l_pt.AddEntry(FR_data_pt, 'Data'    , 'pe')
l_pt.AddEntry(FR_bg_pt,   'QCD + EW', 'pe')
l_pt.AddEntry(FR_qcd_pt,  'QCD'     , 'pe')
l_pt.Draw()

helper.saveCanvas(canv, "muFakeRatio_pt")



# Plotting FR vs Eta

FR_data_eta.SetMarkerSize(1.2)
FR_data_eta.SetMarkerStyle(20)
FR_data_eta.SetMarkerColor(getColor(data))

FR_bg_eta.SetMarkerSize(1.2)
FR_bg_eta.SetMarkerStyle(20)
FR_bg_eta.SetMarkerColor(getColor(wjets))

FR_qcd_eta.SetMarkerSize(1.2)
FR_qcd_eta.SetMarkerStyle(20)
FR_qcd_eta.SetMarkerColor(getColor(qcd))

FR_data_eta.Draw("p e1")
FR_bg_eta.Draw("p e1 same")
FR_qcd_eta.Draw("p e1 same")

FR_data_eta.SetMaximum(0.3)
FR_data_eta.GetXaxis().SetTitle(helper.getXTitle(data.hists[13]))
FR_data_eta.GetYaxis().SetTitle('FR')
FR_data_eta.SetTitle('muFakeRatio_eta')

l_eta = helper.makeLegend(0.15, 0.65, 0.4, 0.90)
l_eta.AddEntry(FR_data_eta, 'Data'    , 'pe')
l_eta.AddEntry(FR_bg_eta,   'QCD + EW', 'pe')
l_eta.AddEntry(FR_qcd_eta,  'QCD'     , 'pe')
l_eta.Draw()

helper.saveCanvas(canv, "muFakeRatio_eta")


