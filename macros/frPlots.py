## frPlots.py

## HEADER

import ROOT, commands, sys, copy
import lib as helper
import lib_FitScale as fit
import lib_FakeRates as FR

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)



class sample:
	def __init__(self, name, infile):
		self.name   = name
		self.file   = ROOT.TFile(infile)
		self.hists  = [self.file.Get(self.name+'/'+i.GetName()) for i in self.file.GetDirectory(self.name).GetListOfKeys() ]
		for h in self.hists: 
			h.SetFillColor(helper.getSampleColor(self))
		self.isdata = (self.name == 'data')
		if self.isdata: 
			for h in self.hists: 
				h.SetMarkerStyle(20)
	color  = helper.getSampleColor
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

leg = helper.makeLegend(0.7, 0.7, 0.85, 0.85)
leg.AddEntry(data  .hists[0], 'Data'    , 'pe')
leg.AddEntry(wjets .hists[0], 'W+Jets'  , 'f' )
leg.AddEntry(dyjets.hists[0], 'DY+Jets' , 'f' )
leg.AddEntry(qcd   .hists[0], 'QCD'     , 'f' )



## LIST OF HISTOGRAMS TO PLOT

plotHists = ['h_Loose_muAwayJetDR', 'h_Loose_muAwayJetPt', 'h_Loose_muClosJetDR', 'h_Loose_muClosJetPt', 'h_Loose_muHT', 'h_Loose_muLepEta', 'h_Loose_muLepIso', 'h_Loose_muLepPt', 'h_Loose_muMET', 'h_Loose_muMETnoMTCut', 'h_Loose_muMT', 'h_Loose_muMTMET30', 'h_Loose_muMaxJPt', 'h_Loose_muNBJets', 'h_Loose_muNJets', 'h_Loose_muNVertices', 'h_Loose_muD0', 'h_Tight_muAwayJetDR', 'h_Tight_muAwayJetPt', 'h_Tight_muClosJetDR', 'h_Tight_muClosJetPt', 'h_Tight_muHT', 'h_Tight_muLepEta', 'h_Tight_muLepIso', 'h_Tight_muLepPt', 'h_Tight_muMET', 'h_Tight_muMETnoMTCut', 'h_Tight_muMT', 'h_Tight_muMTMET30', 'h_Tight_muMaxJPt', 'h_Tight_muNBJets', 'h_Tight_muNJets', 'h_Tight_muNVertices', 'h_Tight_muD0']



# SET SCALING

#qcd.Rescale(fit.getMCScaleFactor(qcd, 'h_Loose_muLepIso', [data], [], 0.2))
#wjets.Rescale(fit.getMCScaleFactor(wjets, 'h_Tight_muMTMET30', [data], [qcd, dyjets], 60, 90))

#scalefactors = fit.doSimScaling(data.hists[37], qcd.hists[37], wjets.hists[37], dyjets.hists[37])
#qcd.Rescale(scalefactors[0])
#wjets.Rescale(scalefactors[1])
#dyjets.Rescale(scalefactors[2])


# Run Over All Samples to Produce Plots

for hist in data.hists:

	i = data.hists.index(hist)
	pad_plot.cd()

	#if hist.GetName() == 'h_muFTight':
	#	FR_data = hist
	#	FR_bg_ns = ROOT.THStack()
	#	for mc in mc_samples:
	#		FR_bg_ns.Add(mc.hists[i])

	#if hist.GetName() == 'h_muFLoose':
	#	FR_data_den = hist
	#	FR_bg_ds = ROOT.THStack()
	#	for mc in mc_samples:
	#		FR_bg_ds.Add(mc.hists[i])

	# Plot Histogram	
	if not hist.GetName() in plotHists: continue

	prepend = ''
	postpend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'

	# Sum BG Contributions in Stack
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
	hist_ratio = hist.Clone()
	hist_ratio.Divide(stack.GetStack().Last())
	hist_ratio.Draw("p e1")
	hist_ratio = helper.setRatioStyle(hist_ratio, hist)
	line = helper.makeLine(hist_ratio.GetXaxis().GetXmin(), 1.00, hist_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()
	helper.saveCanvas(canv, prepend + helper.getSaveName(hist) + postpend)



# compute and plot FR for every variable

FR.PlotFR(data, mc_samples, [qcd])



# compute and plot FR 2d Map (+ Projections)

FR.Plot2dFRMap(data, mc_samples, [qcd], True)






# Computing FakeRate

#setMin = 0.0
#setMax = 0.25

#FR_data_2d  = FR_data
#FR_data_2d.Divide(FR_data_den)

#FR_data_pt  = FR_data.ProjectionX('FR_data_pt')
#FR_data_pt.Divide(FR_data_den.ProjectionX('FR_data_den_pt'))
#
#FR_data_eta = FR_data.ProjectionY('FR_data_eta')
#FR_data_eta.Divide(FR_data_den.ProjectionY('FR_data_den_eta'))

#FR_qcd_2d   = FR_qcd
#FR_qcd_2d.Divide(FR_qcd_den)

#FR_qcd_pt   = FR_qcd.ProjectionX('FR_qcd_pt')
#FR_qcd_pt.Divide(FR_qcd_den.ProjectionX('FR_qcd_den_pt'))
#
#FR_qcd_eta  = FR_qcd.ProjectionY('FR_qcd_eta')
#FR_qcd_eta.Divide(FR_qcd_den.ProjectionY('FR_qcd_den_eta'))

#FR_bg       = FR_bg_ns.GetStack().Last()
#FR_bg_den   = FR_bg_ds.GetStack().Last()

#FR_bg_2d    = FR_bg
#FR_bg_2d.Divide(FR_bg_den)

#FR_bg_pt    = FR_bg.ProjectionX('FR_bg_pt')
#FR_bg_pt.Divide(FR_bg_den.ProjectionX('FR_bg_den_pt'))
#
#FR_bg_eta   = FR_bg.ProjectionY('FR_bg_eta')
#FR_bg_eta.Divide(FR_bg_den.ProjectionY('FR_bg_den_eta'))



# Plotting FR vs Pt

#pad_plot.cd()
#
#FR_data_pt.SetMarkerSize(1.2)
#FR_data_pt.SetMarkerStyle(20)
#FR_data_pt.SetMarkerColor(getColor(data))
#
#FR_bg_pt.SetMarkerSize(1.2)
#FR_bg_pt.SetMarkerStyle(20)
#FR_bg_pt.SetMarkerColor(getColor(wjets))
#
#FR_qcd_pt.SetMarkerSize(1.2)
#FR_qcd_pt.SetMarkerStyle(20)
#FR_qcd_pt.SetMarkerColor(getColor(qcd))
#
#FR_data_pt.Draw("p e1")
#FR_bg_pt.Draw("p e1 same")
#FR_qcd_pt.Draw("p e1 same")
#
#FR_data_pt.SetMinimum(setMin)
#FR_data_pt.SetMaximum(setMax)
#FR_data_pt.GetXaxis().SetTitle(helper.getXTitle(data.hists[12]))
#FR_data_pt.GetYaxis().SetTitle('FR')
#FR_data_pt.SetTitle('muFakeRatio_pt')
#
#l_pt = helper.makeLegend(0.15, 0.65, 0.35, 0.85)
#l_pt.AddEntry(FR_data_pt, 'Data'    , 'pe')
#l_pt.AddEntry(FR_bg_pt,   'QCD + EW', 'pe')
#l_pt.AddEntry(FR_qcd_pt,  'QCD'     , 'pe')
#l_pt.Draw()
#
#pad_ratio.cd()
#data_bg_ratio = FR_data_pt.Clone()
#data_bg_ratio.Divide(FR_bg_pt)
#data_bg_ratio.Draw("p e1")
#data_bg_ratio = helper.setRatioStyle(data_bg_ratio, data.hists[12])
#line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
#line.Draw()
#
##helper.saveCanvas(canv, "muFakeRatio_pt")
#
#
#
## Plotting FR vs Eta
#
#pad_plot.cd()
#
#FR_data_eta.SetMarkerSize(1.2)
#FR_data_eta.SetMarkerStyle(20)
#FR_data_eta.SetMarkerColor(getColor(data))
#
#FR_bg_eta.SetMarkerSize(1.2)
#FR_bg_eta.SetMarkerStyle(20)
#FR_bg_eta.SetMarkerColor(getColor(wjets))
#
#FR_qcd_eta.SetMarkerSize(1.2)
#FR_qcd_eta.SetMarkerStyle(20)
#FR_qcd_eta.SetMarkerColor(getColor(qcd))
#
#FR_data_eta.Draw("p e1")
#FR_bg_eta.Draw("p e1 same")
#FR_qcd_eta.Draw("p e1 same")
#
#FR_data_eta.SetMinimum(setMin)
#FR_data_eta.SetMaximum(setMax)
#FR_data_eta.GetXaxis().SetTitle(helper.getXTitle(data.hists[13]))
#FR_data_eta.GetYaxis().SetTitle('FR')
#FR_data_eta.SetTitle('muFakeRatio_eta')
#
#l_eta = helper.makeLegend(0.15, 0.65, 0.35, 0.85)
#l_eta.AddEntry(FR_data_eta, 'Data'    , 'pe')
#l_eta.AddEntry(FR_bg_eta,   'QCD + EW', 'pe')
#l_eta.AddEntry(FR_qcd_eta,  'QCD'     , 'pe')
#l_eta.Draw()
#
#pad_ratio.cd()
#data_bg_ratio = FR_data_eta.Clone()
#data_bg_ratio.Divide(FR_bg_eta)
#data_bg_ratio.Draw("p e1")
#data_bg_ratio = helper.setRatioStyle(data_bg_ratio, data.hists[13])
#line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
#line.Draw()
#
##helper.saveCanvas(canv, "muFakeRatio_eta")
#


# Plotting 2D FR map

#canv = helper.makeCanvas(900, 675)
#canv.SetRightMargin(0.1)
#
#FR_data_2d.Draw("text colz e")
#FR_data_2d.GetXaxis().SetTitle(helper.getXTitle(data.hists[12]))
#FR_data_2d.GetYaxis().SetTitle(helper.getXTitle(data.hists[13]))
#FR_data_2d.SetMinimum(setMin)
#FR_data_2d.SetMaximum(setMax)
#FR_data_2d.SetTitle('muFakeRatio_data')
#helper.saveCanvas(canv, "muFakeRatio_data")
#
#FR_bg_2d.Draw("text colz e")
#FR_bg_2d.GetXaxis().SetTitle(helper.getXTitle(data.hists[12]))
#FR_bg_2d.GetYaxis().SetTitle(helper.getXTitle(data.hists[13]))
#FR_bg_2d.SetMinimum(setMin)
#FR_bg_2d.SetMaximum(setMax)
#FR_bg_2d.SetTitle('muFakeRatio_bg')
#helper.saveCanvas(canv, "muFakeRatio_bg")





