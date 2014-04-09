## frPlots.py

## HEADER

import ROOT, commands, sys, copy, os
import lib as helper
import lib_FitScale as fit
import lib_FakeRates as FR
import lib_Plot as Plot

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)

class sample:
	def __init__(self, name, infile):
		self.name   = name
		self.file   = ROOT.TFile(infile)
		self.hists  = [self.file.Get(self.name + '/' + i.GetName()) for i in self.file.GetDirectory(self.name).GetListOfKeys() ]
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
dataType = args[1]
inputDir = args[2]
outputDir = args[3]

if dataType == 'el':
	data       = sample('el_data'         , inputDir + 'el_data_ratios.root')
	wjets      = sample('el_wjets'        , inputDir + 'el_wjets_ratios.root')
	dyjets50   = sample('el_dyjets50'     , inputDir + 'el_dyjets50_ratios.root')
	dyjets10   = sample('el_dyjets10'     , inputDir + 'el_dyjets10_ratios.root')
	qcd30      = sample('el_qcdelenr30'   , inputDir + 'el_qcdelenr30_ratios.root')
	qcd80      = sample('el_qcdelenr80'   , inputDir + 'el_qcdelenr80_ratios.root')
	qcd250     = sample('el_qcdelenr250'  , inputDir + 'el_qcdelenr250_ratios.root')
	qcd350     = sample('el_qcdelenr350'  , inputDir + 'el_qcdelenr350_ratios.root')

	mc_samples = []
	mc_samples.append(qcd30   )
	mc_samples.append(qcd80   )
	mc_samples.append(qcd250  )
	mc_samples.append(qcd350  )
	mc_samples.append(wjets   )
	mc_samples.append(dyjets50)
	mc_samples.append(dyjets10)

else:
	data       = sample('mu_data'         , inputDir + 'mu_data_ratios.root')
	wjets      = sample('mu_wjets'        , inputDir + 'mu_wjets_ratios.root')
	dyjets50   = sample('mu_dyjets50'     , inputDir + 'mu_dyjets50_ratios.root')
	dyjets10   = sample('mu_dyjets10'     , inputDir + 'mu_dyjets10_ratios.root')
	qcd        = sample('mu_qcdmuenr'     , inputDir + 'mu_qcdmuenr_ratios.root')

	mc_samples = []
	mc_samples.append(qcd     )
	mc_samples.append(wjets   )
	mc_samples.append(dyjets50)
	mc_samples.append(dyjets10)


module = helper.getModule(outputDir)
scaling = helper.getScaling(outputDir)
outputDir = helper.CreateOutputFolders(outputDir)

if scaling == '':
	print 'SCALING NOT DEFINED'
	print 'PRODUCING MODULES UNWEIGHTED'
	scaling = 'unweighted'

if module == '': 
	print 'MODULE NOT DEFINED'
	print 'PRODUCING ALL MODULES'
	module = 'all'



canv = helper.makeCanvas(900, 675)


# Rescaling for complete PU_complete
#for mc in mc_samples:i
#	mc.Rescale(24.85/8.1)



## LIST OF HISTOGRAMS TO PLOT

plot1dHists = ['h_Loose_AwayJetDR', 'h_Loose_AwayJetPt', 'h_Loose_ClosJetDR', 'h_Loose_ClosJetPt', 'h_Loose_HT', 'h_Loose_LepEta', 'h_Loose_LepIso', 'h_Loose_LepPt', 'h_Loose_MET', 'h_Loose_METnoMTCut', 'h_Loose_MT', 'h_Loose_MTMET20', 'h_Loose_MTMET30', 'h_Loose_MaxJPt', 'h_Loose_AllJCPt', 'h_Loose_AllJRPt', 'h_Loose_AllJEta', 'h_Loose_AllJEta_test1', 'h_Loose_AllJEta_test2', 'h_Loose_AllJEta_test3', 'h_Loose_NBJets', 'h_Loose_NJets', 'h_Loose_NVertices', 'h_Loose_NVertices1', 'h_Loose_NVerticesMET20', 'h_Loose_D0', 'h_Tight_AwayJetDR', 'h_Tight_AwayJetPt', 'h_Tight_ClosJetDR', 'h_Tight_ClosJetPt', 'h_Tight_HT', 'h_Tight_LepEta', 'h_Tight_LepIso', 'h_Tight_LepPt', 'h_Tight_MET', 'h_Tight_METnoMTCut', 'h_Tight_MT', 'h_Tight_MTMET20', 'h_Tight_MTMET30', 'h_Tight_MaxJPt', 'h_Tight_AllJCPt', 'h_Tight_AllJRPt', 'h_Tight_AllJEta', 'h_Tight_NBJets', 'h_Tight_NJets', 'h_Tight_NVertices', 'h_Tight_NVertices1', 'h_Tight_NVerticesMET20', 'h_Tight_D0']

plot2dHists = ['h_Loose_DJPtJEta', 'h_Loose_FJPtJEta', 'h_Loose_DJPtJPt', 'h_Loose_FJPtJPt', 'h_Tight_DJPtJEta', 'h_Tight_FJPtJEta', 'h_Tight_DJPtJPt', 'h_Tight_FJPtJPt'] 



# SET SCALING

lower = []
upper = []

if 'qcd' in scaling:
	qcd.Rescale(fit.getMCScaleFactor(qcd, 'h_Loose_LepIso', [data], [], 0.2))

if 'wjets' in scaling and not scaling == 'wjetsdyjets':
	wjets.Rescale(fit.getMCScaleFactor(wjets, 'h_Tight_MTMET20', [data], [qcd, dyjets50, dyjets10], 60, 90))

if 'wjetsdyjets' in scaling:
	scalefactors = fit.getMCScaleFactorMutually([wjets, dyjets50, dyjets10], 'h_Tight_MTMET20', [data], [qcd], 60, 90)
	wjets.Rescale(scalefactors[0])
	dyjets50.Rescale(scalefactors[1])
	dyjets10.Rescale(scalefactors[2])

if scaling == 'fit':
	#scalefactors = fit.getMCScaleFactorSimultaneously(data, qcd, wjets, dyjets50, dyjets10)
	scalefactors = fit.getMCScaleFactorSimultaneously2(data, qcd, wjets, dyjets50, dyjets10)
	qcd.Rescale(scalefactors[0])
	wjets.Rescale(scalefactors[1])
	dyjets50.Rescale(scalefactors[2])
	dyjets10.Rescale(scalefactors[3])

if scaling == 'fiterror':
	scalefactors = fit.getMCScaleFactorSimultaneouslyWithErrors(data, qcd, wjets, dyjets50, dyjets10)
	qcd.Rescale(scalefactors[0][0])
	wjets.Rescale(scalefactors[0][1])
	dyjets50.Rescale(scalefactors[0][2])
	dyjets10.Rescale(scalefactors[0][3])
	lower = scalefactors[1]
	upper = scalefactors[2]

if module == 'plots_1d' or module == 'all':
	if dataType == 'el': mclist = [qcd30, qcd80, qcd250, qcd350, wjets, dyjets50, dyjets10]
	else:                mclist = [qcd, wjets, dyjets50, dyjets10]
	helper.PrintScale(canv, outputDir, mclist, lower, upper)




# produce 1d Plots

if module == 'plots_1d' or module == 'all':
	if dataType == 'el': qcdsample = qcd30
	else:                qcdsample = qcd
	leg = helper.makeLegend(0.6, 0.5, 0.85, 0.85)
	leg.AddEntry(data      .hists[0], helper.getLegendName(data      .GetName()), 'pe')
	leg.AddEntry(wjets     .hists[0], helper.getLegendName(wjets     .GetName()), 'f' )
	leg.AddEntry(dyjets10  .hists[0], helper.getLegendName(dyjets10  .GetName()), 'f' )
	leg.AddEntry(qcdsample .hists[0], helper.getLegendName(qcdsample .GetName()), 'f' )
	Plot.Plot1d(dataType, outputDir, data, mc_samples, plot1dHists, leg)



# produce 2d Plots

if module == 'plots_2d' or module == 'all':
	Plot.Plot2d(dataType, outputDir, data, mc_samples, plot2dHists)



# Plot all MET Zooms

if module == 'zoom_met' or module == 'all':
	if dataType == 'el': mclist = [qcd30, qcd80, qcd250, qcd350, wjets, dyjets50]
	else:                mclist = [qcd, wjets, dyjets50] 
	Plot.PlotMETZooms(dataType, outputDir, data, mclist, leg)



# Plot all JPt Zooms

if module == 'zoom_jpt' or module == 'all':
	if dataType == 'el': 
		mclist    = [qcd30, qcd80, qcd250, qcd350, wjets, dyjets50]
		qcdsample = qcd30
	else:
		mclist    = [qcd, wjets, dyjets50] 
		qcdsample = qcd
	
	leg0 = helper.makeLegend(0.6, 0.5, 0.85, 0.85)
	leg0.AddEntry(data      .hists[0], helper.getLegendName(data      .GetName()), 'l')
	leg0.AddEntry(wjets     .hists[0], helper.getLegendName(wjets     .GetName()), 'l')
	leg0.AddEntry(dyjets10  .hists[0], helper.getLegendName(dyjets10  .GetName()), 'l')
	leg0.AddEntry(qcdsample .hists[0], helper.getLegendName(qcdsample .GetName()), 'l')
	Plot.PlotJPtZooms(dataType, outputDir, data, mclist, leg0)



# compute and plot FR for every variable

if module == 'fakerates_1d' or module == 'all':
 	if dataType == 'el': qcdlist = [qcd30] #[qcd30, qcd80, qcd250, qcd350]
	else:                qcdlist = [qcd] 
	FR.PlotFR(dataType, outputDir, data, mc_samples, plot1dHists, qcdlist)#, [wjets, dyjets50, dyjets10], True)



# compute and plot FR 2d Map (+ Projections)

if module == 'fakerates_2d' or module == 'all':
	if dataType == 'el': qcdlist = [qcd30, qcd80, qcd250, qcd350]
	else:                qcdlist = [qcd] 
	FR.Plot2dFRMap(dataType, outputDir, module, data, mc_samples, qcdlist, [], True)#[wjets, dyjets50, dyjets10], True, True)



# hard-coded to produce wjets and dyjets All-Jet comparisons

if module == 'adhoc' or module == 'all':

	canv = helper.makeCanvas(900, 675)
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_ratio.cd()

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
		dyjets50.hists[i].Draw("same")
		dyjets50.hists[i].Scale(1.0/dyjets50.hists[i].Integral())
		hist.SetMaximum(1.5*max(hist.GetMaximum(), dyjets50.hists[i].GetMaximum()))
		hist.GetYaxis().SetTitle("1/Integral")
		leg.Draw()

		pad_ratio.cd()
		hist_ratio = hist.Clone()
		hist_ratio.Divide(dyjets50.hists[i])
		hist_ratio.Draw("p e1")
		hist_ratio = helper.setRatioStyle(dataType, hist_ratio, hist)
		line = helper.makeLine(hist_ratio.GetXaxis().GetXmin(), 1.00, hist_ratio.GetXaxis().GetXmax(), 1.00)
		line.Draw()
		helper.saveCanvas(canv, pad_plot, outputDir + "adhoc/", prepend + helper.getSaveName(hist) + postpend)






# hard-coded to produce FR vs LepEta and LepPt plots for different jet cuts and different Jet Pts

if module == 'fakerates_1d' or module == 'all':

	canv = helper.makeCanvas(900, 675)
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')


	for hist in data.hists:

		i = data.hists.index(hist)
			
		# Get Numerator Plots
		if hist.GetName() == 'h_Tight_LepEta_30':
			histindex_eta = i
			data_numerator_eta30 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_LepEta_40':
			data_numerator_eta40 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_LepEta_50':
			data_numerator_eta50 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_LepEta_60':
			data_numerator_eta60 = copy.deepcopy(hist)

		if hist.GetName() == 'h_Tight_LepPt_30':
			histindex_pt = i
			data_numerator_pt30 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_LepPt_40':
			data_numerator_pt40 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_LepPt_50':
			data_numerator_pt50 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_LepPt_60':
			data_numerator_pt60 = copy.deepcopy(hist)

		if hist.GetName() == 'h_Tight_MaxJCPt':
			histindex_cpt = i
			data_numerator_cpt = copy.deepcopy(hist)
		if hist.GetName() == 'h_Tight_MaxJRPt':
			data_numerator_rpt = copy.deepcopy(hist)
			
		# Get Denominator Plots
		if hist.GetName() == 'h_Loose_LepEta_30':
			data_denominator_eta30 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_LepEta_40':
			data_denominator_eta40 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_LepEta_50':
			data_denominator_eta50 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_LepEta_60':
			data_denominator_eta60 = copy.deepcopy(hist)

		if hist.GetName() == 'h_Loose_LepPt_30':
			data_denominator_pt30 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_LepPt_40':
			data_denominator_pt40 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_LepPt_50':
			data_denominator_pt50 = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_LepPt_60':
			data_denominator_pt60 = copy.deepcopy(hist)

		if hist.GetName() == 'h_Loose_MaxJCPt':
			data_denominator_cpt = copy.deepcopy(hist)
		if hist.GetName() == 'h_Loose_MaxJRPt':
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

	FR.make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, data.hists[histindex_eta], 'FR_LepEta_compare')

	histstoplot = []
	histstoplot.append([data_numerator_pt30, 'data30'])
	histstoplot.append([data_numerator_pt40, 'data40'])
	histstoplot.append([data_numerator_pt50, 'data50'])
	histstoplot.append([data_numerator_pt60, 'data60'])

	FR.make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, data.hists[histindex_pt], 'FR_LepPt_compare')

	histstoplot = []
	histstoplot.append([data_numerator_cpt, 'dataJCPt'])
	histstoplot.append([data_numerator_rpt, 'dataJRPt'])

	FR.make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, data.hists[histindex_cpt], 'FR_JetPt_compare')






