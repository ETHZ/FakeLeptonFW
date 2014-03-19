## frPlots.py

## HEADER

import ROOT, commands, sys, copy, os
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
			h.SetMarkerColor(helper.getSampleColor(self))
			h.SetLineColor(helper.getSampleColor(self))
			h.SetFillColor(helper.getSampleColor(self))
		self.isdata = (self.name == 'data')
		if self.isdata: 
			for h in self.hists: 
				h.SetMarkerStyle(20)
	color  = helper.getSampleColor
	scale  = 1.0

	def GetName(self):
		return self.name

	def GetScale(self):
		return self.scale

	def Rescale(self, newscale):
		self.scale = newscale
		for h in self.hists: h.Scale(newscale)
	

args = sys.argv
inputDir = args[1]
outputDir = args[2]
scaling = args[3]

data   = sample('data'         , inputDir + 'data_ratios.root')
wjets  = sample('wjets'        , inputDir + 'wjets_ratios.root')
dyjets = sample('dyjets'       , inputDir + 'dyjets_ratios.root')
qcd    = sample('qcdMuEnriched', inputDir + 'qcdMuEnriched_ratios.root')

if not os.path.exists(outputDir): os.mkdir(outputDir)



## INITIALIZING SAMPLES, CANVAS, LEGEND

mc_samples = []
mc_samples.append(qcd   )
mc_samples.append(wjets )
mc_samples.append(dyjets)

canv = helper.makeCanvas(900, 675)

leg = helper.makeLegend(0.7, 0.6, 0.85, 0.85)
leg.AddEntry(data  .hists[0], helper.getLegendName(data.GetName())  , 'pe')
leg.AddEntry(wjets .hists[0], helper.getLegendName(wjets.GetName()) , 'f' )
leg.AddEntry(dyjets.hists[0], helper.getLegendName(dyjets.GetName()), 'f' )
leg.AddEntry(qcd   .hists[0], helper.getLegendName(qcd.GetName())   , 'f' )



## LIST OF HISTOGRAMS TO PLOT

plot1dHists = ['h_Loose_muAwayJetDR', 'h_Loose_muAwayJetPt', 'h_Loose_muClosJetDR', 'h_Loose_muClosJetPt', 'h_Loose_muHT', 'h_Loose_muLepEta', 'h_Loose_muLepIso', 'h_Loose_muLepPt', 'h_Loose_muMET', 'h_Loose_muMETnoMTCut', 'h_Loose_muMT', 'h_Loose_muMTMET30', 'h_Loose_muMaxJPt', 'h_Loose_muAllJCPt', 'h_Loose_muAllJRPt', 'h_Loose_muAllJEta', 'h_Loose_muNBJets', 'h_Loose_muNJets', 'h_Loose_muNVertices', 'h_Loose_muD0', 'h_Tight_muAwayJetDR', 'h_Tight_muAwayJetPt', 'h_Tight_muClosJetDR', 'h_Tight_muClosJetPt', 'h_Tight_muHT', 'h_Tight_muLepEta', 'h_Tight_muLepIso', 'h_Tight_muLepPt', 'h_Tight_muMET', 'h_Tight_muMETnoMTCut', 'h_Tight_muMT', 'h_Tight_muMTMET30', 'h_Tight_muMaxJPt', 'h_Tight_muAllJCPt', 'h_Tight_muAllJRPt', 'h_Tight_muAllJEta', 'h_Tight_muNBJets', 'h_Tight_muNJets', 'h_Tight_muNVertices', 'h_Tight_muD0']

plot2dHists = ['h_Loose_muDJPtJEta', 'h_Loose_muFJPtJEta', 'h_Loose_muDJPtJPt', 'h_Loose_muFJPtJPt', 'h_Tight_muDJPtJEta', 'h_Tight_muFJPtJEta', 'h_Tight_muDJPtJPt', 'h_Tight_muFJPtJPt'] 


# SET SCALING

if 'qcd' in scaling:
	qcd.Rescale(fit.getMCScaleFactor(qcd, 'h_Loose_muLepIso', [data], [], 0.2))

if 'wjets' in scaling:
	wjets.Rescale(fit.getMCScaleFactor(wjets, 'h_Tight_muMTMET30', [data], [qcd, dyjets], 60, 90))

if 'fit' in scaling:
	scind = 0
	for i, hist in enumerate(data.hists): 
		if hist.GetName() == 'h_Tight_muMTMET30': 
			scind = i
	scalefactors = fit.doSimScaling(data.hists[scind], qcd.hists[scind], wjets.hists[scind], dyjets.hists[scind])
	qcd.Rescale(scalefactors[0])
	wjets.Rescale(scalefactors[1])
	dyjets.Rescale(scalefactors[2])

helper.PrintScale(canv, outputDir, [qcd,wjets,dyjets])
print "scale of qcd = " + str(qcd.GetScale())
print "scale of wjets = " + str(wjets.GetScale())
print "scale of dyjets = " + str(dyjets.GetScale())


# Run Over All Samples to Produce 1d Plots

pad_plot = helper.makePad('plot')
pad_ratio = helper.makePad('ratio')
pad_ratio.cd()

for hist in data.hists:

	i = data.hists.index(hist)
	pad_plot.cd()


	# Plot Histogram	
	if not hist.GetName() in plot1dHists: continue

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

	yscale = 1.5*max(hist.GetMaximum(), stack.GetMaximum())
	stack.Draw('hist')
	stack.SetMaximum(yscale)
	stack.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.Draw('p e1 same')
	hist.SetMaximum(yscale)
	leg.Draw()

	pad_ratio.cd()
	hist_ratio = hist.Clone()
	hist_ratio.Divide(stack.GetStack().Last())
	hist_ratio.Draw("p e1")
	hist_ratio = helper.setRatioStyle(hist_ratio, hist)
	line = helper.makeLine(hist_ratio.GetXaxis().GetXmin(), 1.00, hist_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()
	helper.saveCanvas(canv, pad_plot, outputDir, prepend + helper.getSaveName(hist) + postpend)


for hist in wjets.hists:

	i = wjets.hists.index(hist)
	pad_plot.cd()


	# Plot Histogram	
	if not "AllJ" in hist.GetName(): continue

	prepend = ''
	postpend = '_closer'
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'

	hist.Draw()
	hist.Scale(1.0/hist.Integral())
	dyjets.hists[i].Draw("same")
	dyjets.hists[i].Scale(1.0/dyjets.hists[i].Integral())
	hist.SetMaximum(1.5*max(hist.GetMaximum(), dyjets.hists[i].GetMaximum()))
	hist.GetYaxis().SetTitle("1/Integral")
	leg.Draw()

	pad_ratio.cd()
	hist_ratio = hist.Clone()
	hist_ratio.Divide(dyjets.hists[i])
	hist_ratio.Draw("p e1")
	hist_ratio = helper.setRatioStyle(hist_ratio, hist)
	line = helper.makeLine(hist_ratio.GetXaxis().GetXmin(), 1.00, hist_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()
	helper.saveCanvas(canv, pad_plot, outputDir, prepend + helper.getSaveName(hist) + postpend)





# Run Over All Samples to Produce 2d Plots

canv.SetRightMargin(0.1)
pad_plot.Close()
pad_ratio.Close()
pad_plot = helper.makePad('tot')
pad_plot.cd()

for hist in data.hists:

	i = data.hists.index(hist)


	# Plot Histogram	
	if not hist.GetName() in plot2dHists: continue

	prepend = ''
	postpend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'

	# Data
	postpend = "_data"
	hist.Draw('colz')
	hist.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.GetYaxis().SetTitle(helper.getYTitle(hist))
	hist.SetTitle()
	helper.saveCanvas(canv, pad_plot, outputDir, prepend + helper.getSaveName(hist) + postpend, 0)

	# MC
	for mc in mc_samples:
		postpend = "_" + str(mc.GetName().lower())
		mc.hists[i].Draw('colz')
		mc.hists[i].GetXaxis().SetTitle(helper.getXTitle(hist))
		mc.hists[i].GetYaxis().SetTitle(helper.getYTitle(hist))
		mc.hists[i].SetTitle()
		helper.saveCanvas(canv, pad_plot, outputDir, prepend + helper.getSaveName(hist) + postpend, 0)


canv.SetRightMargin(0.0)




# Plot all Zoom's with Data, MC to compare

pad_plot.Close()
pad_ratio.Close()
pad_plot = helper.makePad('tot')
pad_plot.cd()
leg0 = helper.makeLegend(0.7, 0.6, 0.85, 0.85)
leg0.AddEntry(data  .hists[0], helper.getLegendName(data.GetName())   , 'l')
leg0.AddEntry(wjets .hists[0], helper.getLegendName(wjets.GetName())  , 'l')
leg0.AddEntry(dyjets.hists[0], helper.getLegendName(dyjets.GetName()) , 'l')
leg0.AddEntry(qcd   .hists[0], helper.getLegendName(qcd.GetName())    , 'l')
t_eta = ROOT.TLatex()
t_eta.SetNDC()
t_eta.SetTextSize(0.02)
t_eta.SetTextAlign(11)
t_eta.SetTextColor(ROOT.kBlack)
t_pt = ROOT.TLatex()
t_pt.SetNDC()
t_pt.SetTextSize(0.02)
t_pt.SetTextAlign(11)
t_pt.SetTextColor(ROOT.kBlack)

bins_eta = [0.0, 1.0, 2.4]
bins_pt  = [10.0, 20.0, 30.0, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 55.0, 60.0, 70.0]
bins_tot = (len(bins_eta)-1)*(len(bins_pt)-1)

for hist in data.hists:

	i = data.hists.index(hist)

	# Plot Histogram	
	if not "Zoom" in hist.GetName(): continue

	prepend = ''
	postpend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'

	id = hist.GetName().split('_')[-1]

	# Data
	hist.Scale(1.0/hist.Integral())
	hist.SetFillStyle(0)
	hist.SetLineStyle(2)
	hist.Draw("HIST")
	max = hist.GetMaximum()

	# MC
	for mc in mc_samples:
		mc.hists[i].Scale(1.0/mc.hists[i].Integral())
		mc.hists[i].SetFillStyle(0)
		mc.hists[i].Draw("HIST SAME")
		if mc.hists[i].GetMaximum()>max: max = mc.hists[i].GetMaximum()

	# Cosmetics
	hist.SetMaximum(1.5*max)
	hist.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.GetYaxis().SetTitle("1/Integral")
	hist.SetTitle()
	leg0.Draw()

	m = int(id)//(len(bins_pt)-1)
	n = int(id)%(len(bins_pt)-1)

	text_eta = str(bins_eta[m]) + " #leq |#eta|_{jet} < " + str(bins_eta[m+1])
	text_pt  = str(bins_pt[n])  + " #leq jet-p_{T} (corr.) < " + str(bins_pt[n+1])

	t_eta.DrawLatex(0.7, 0.55, text_eta)	
	t_pt.DrawLatex(0.7, 0.50, text_pt)

	helper.saveCanvas(canv, pad_plot, outputDir, prepend + helper.getSaveName(hist, '-2:') + postpend, 0)





# compute and plot FR for every variable

FR.PlotFR(outputDir, data, mc_samples, plot1dHists, [qcd], [wjets, dyjets])



# compute and plot FR 2d Map (+ Projections)

FR.Plot2dFRMap(outputDir, data, mc_samples, [qcd], [wjets, dyjets], True)



# hard-coded to produce FR vs LepEta and LepPt plots for different jet cuts and different Jet Pts

canv = helper.makeCanvas(900, 675)
pad_plot = helper.makePad('plot')
pad_ratio = helper.makePad('ratio')


for hist in data.hists:

	i = data.hists.index(hist)
			
	# Get Numerator Plots
	if hist.GetName() == 'h_Tight_muLepEta_30':
		histindex_eta = i
		data_numerator_eta30 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muLepEta_40':
		data_numerator_eta40 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muLepEta_50':
		data_numerator_eta50 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muLepEta_60':
		data_numerator_eta60 = copy.deepcopy(hist)

	if hist.GetName() == 'h_Tight_muLepPt_30':
		histindex_pt = i
		data_numerator_pt30 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muLepPt_40':
		data_numerator_pt40 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muLepPt_50':
		data_numerator_pt50 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muLepPt_60':
		data_numerator_pt60 = copy.deepcopy(hist)

	if hist.GetName() == 'h_Tight_muMaxJCPt':
		histindex_cpt = i
		data_numerator_cpt = copy.deepcopy(hist)
	if hist.GetName() == 'h_Tight_muMaxJRPt':
		data_numerator_rpt = copy.deepcopy(hist)
			
	# Get Denominator Plots
	if hist.GetName() == 'h_Loose_muLepEta_30':
		data_denominator_eta30 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muLepEta_40':
		data_denominator_eta40 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muLepEta_50':
		data_denominator_eta50 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muLepEta_60':
		data_denominator_eta60 = copy.deepcopy(hist)

	if hist.GetName() == 'h_Loose_muLepPt_30':
		data_denominator_pt30 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muLepPt_40':
		data_denominator_pt40 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muLepPt_50':
		data_denominator_pt50 = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muLepPt_60':
		data_denominator_pt60 = copy.deepcopy(hist)

	if hist.GetName() == 'h_Loose_muMaxJCPt':
		data_denominator_cpt = copy.deepcopy(hist)
	if hist.GetName() == 'h_Loose_muMaxJRPt':
		data_denominator_rpt = copy.deepcopy(hist)


# Compute FR
data_numerator_eta30.Divide(data_denominator_eta30)
data_numerator_eta40.Divide(data_denominator_eta40)
data_numerator_eta50.Divide(data_denominator_eta50)
data_numerator_eta60.Divide(data_denominator_eta60)

data_numerator_pt30.Divide(data_denominator_pt30)
data_numerator_pt40.Divide(data_denominator_pt40)
data_numerator_pt50.Divide(data_denominator_pt50)
data_numerator_pt60.Divide(data_denominator_pt60)

data_numerator_cpt.Divide(data_denominator_cpt)
data_numerator_rpt.Divide(data_denominator_rpt)


# this part needs adjustment
histstoplot = []
histstoplot.append([data_numerator_eta30, 'data30'])
histstoplot.append([data_numerator_eta40, 'data40'])
histstoplot.append([data_numerator_eta50, 'data50'])
histstoplot.append([data_numerator_eta60, 'data60'])

FR.make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, data.hists[histindex_eta], "muFR_LepEta_compare")

histstoplot = []
histstoplot.append([data_numerator_pt30, 'data30'])
histstoplot.append([data_numerator_pt40, 'data40'])
histstoplot.append([data_numerator_pt50, 'data50'])
histstoplot.append([data_numerator_pt60, 'data60'])

FR.make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, data.hists[histindex_pt], "muFR_LepPt_compare")

histstoplot = []
histstoplot.append([data_numerator_cpt, 'dataJCPt'])
histstoplot.append([data_numerator_rpt, 'dataJRPt'])

FR.make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, data.hists[histindex_cpt], "muFR_JetPt_compare")






