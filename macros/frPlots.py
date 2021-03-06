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

args = sys.argv
dataType = args[1]
inputDir = args[2]
outputDir = args[3]



# DEFINE SAMPLE CLASS

class sample:
	def __init__(self, name, infile):
		self.name   = name
		self.file   = ROOT.TFile(infile)
		self.hists  = [self.file.Get(self.name + '/' + i.GetName()) for i in self.file.GetDirectory(self.name).GetListOfKeys() ]
		for h in self.hists: 
			h.SetMarkerColor(helper.getSampleColor(self))
			h.SetLineColor(helper.getSampleColor(self))
			h.SetFillColor(helper.getSampleColor(self))
		self.isdata = ('data' in self.name)
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
	

# LOAD SAMPLES
# note, every sample needs a color and legend name defined in lib.py

if dataType == 'el':
	data        = sample('el_data'         , inputDir + 'el_data_ratios.root'        )
	wjets       = sample('el_wjets'        , inputDir + 'el_wjets_ratios.root'       )
	dyjets50    = sample('el_dyjets50'     , inputDir + 'el_dyjets50_ratios.root'    )
	dyjets10    = sample('el_dyjets10'     , inputDir + 'el_dyjets10_ratios.root'    )

	qcdem20     = sample('el_qcdemenr20'   , inputDir + 'el_qcdemenr20_ratios.root' ) 
	qcdem30     = sample('el_qcdemenr30'   , inputDir + 'el_qcdemenr30_ratios.root' )
	qcdem80     = sample('el_qcdemenr80'   , inputDir + 'el_qcdemenr80_ratios.root' )
	#qcdem170    = sample('el_qcdemenr170'  , inputDir + 'el_qcdemenr170_ratios.root')
	#qcdem250    = sample('el_qcdemenr250'  , inputDir + 'el_qcdemenr250_ratios.root')
	#qcdem350    = sample('el_qcdemenr350'  , inputDir + 'el_qcdemenr350_ratios.root')
	qcdbc20     = sample('el_qcdbctoe20'   , inputDir + 'el_qcdbctoe20_ratios.root' )
	qcdbc30     = sample('el_qcdbctoe30'   , inputDir + 'el_qcdbctoe30_ratios.root' )
	qcdbc80     = sample('el_qcdbctoe80'   , inputDir + 'el_qcdbctoe80_ratios.root' )

	#qcdtot50    = sample('el_qcdtot50'     , inputDir + 'el_qcdtot50_ratios.root'   )
	#qcdtot80    = sample('el_qcdtot80'     , inputDir + 'el_qcdtot80_ratios.root'   )
	#qcdtot120   = sample('el_qcdtot120'    , inputDir + 'el_qcdtot120_ratios.root'  )
	#qcdtot170   = sample('el_qcdtot170'    , inputDir + 'el_qcdtot170_ratios.root'  )
	#qcdtot170v2 = sample('el_qcdtot170v2'  , inputDir + 'el_qcdtot170v2_ratios.root')
	#qcdtot300   = sample('el_qcdtot300'    , inputDir + 'el_qcdtot300_ratios.root'  )
	#qcdtot300v2 = sample('el_qcdtot300v2'  , inputDir + 'el_qcdtot300v2_ratios.root')
	#qcdtot300v3 = sample('el_qcdtot300v3'  , inputDir + 'el_qcdtot300v3_ratios.root')

	ttbar_g     = sample('el_ttbar_g'      , inputDir + 'el_ttbar_g_ratios.root'     )
	qcdem20_g   = sample('el_qcdemenr20_g' , inputDir + 'el_qcdemenr20_g_ratios.root') 
	qcdem30_g   = sample('el_qcdemenr30_g' , inputDir + 'el_qcdemenr30_g_ratios.root')
	qcdem80_g   = sample('el_qcdemenr80_g' , inputDir + 'el_qcdemenr80_g_ratios.root')
	qcdbc20_g   = sample('el_qcdbctoe20_g' , inputDir + 'el_qcdbctoe20_g_ratios.root')
	qcdbc30_g   = sample('el_qcdbctoe30_g' , inputDir + 'el_qcdbctoe30_g_ratios.root')
	qcdbc80_g   = sample('el_qcdbctoe80_g' , inputDir + 'el_qcdbctoe80_g_ratios.root')

	data_samples = []
	data_samples.append(data)

	mc_samples = []
	#mc_samples.append(qcdtot50   )
	#mc_samples.append(qcdtot80   )
	#mc_samples.append(qcdtot120  )
	#mc_samples.append(qcdtot170  )
	#mc_samples.append(qcdtot170v2)
	#mc_samples.append(qcdtot300  )
	#mc_samples.append(qcdtot300v2)
	#mc_samples.append(qcdtot300v3)

	mc_samples.append(qcdem20    )
	mc_samples.append(qcdem30    )
	mc_samples.append(qcdem80    )
	#mc_samples.append(qcdem170   )
	#mc_samples.append(qcdem250   )
	#mc_samples.append(qcdem350   )
	mc_samples.append(qcdbc20    )
	mc_samples.append(qcdbc30    )
	mc_samples.append(qcdbc80    )

	mc_samples.append(wjets      )
	mc_samples.append(dyjets50   )
	mc_samples.append(dyjets10   )


	qcd_samples = []	
	#qcd_samples.append(qcdtot50   )
	#qcd_samples.append(qcdtot80   )
	#qcd_samples.append(qcdtot120  )
	#qcd_samples.append(qcdtot170  )
	#qcd_samples.append(qcdtot170v2)
	#qcd_samples.append(qcdtot300  )
	#qcd_samples.append(qcdtot300v2)
	#qcd_samples.append(qcdtot300v3)

	qcd_samples.append(qcdem20    )
	qcd_samples.append(qcdem30    )
	qcd_samples.append(qcdem80    )
	#qcd_samples.append(qcdem170   )
	#qcd_samples.append(qcdem250   ) 
	#qcd_samples.append(qcdem350   )
	qcd_samples.append(qcdbc20    )
	qcd_samples.append(qcdbc30    )
	qcd_samples.append(qcdbc80    )

	closure_samples = []
	closure_samples.append(ttbar_g  )
	closure_samples.append(qcdem20_g)
	closure_samples.append(qcdem30_g)
	closure_samples.append(qcdem80_g)
	closure_samples.append(qcdbc20_g)
	closure_samples.append(qcdbc30_g)
	closure_samples.append(qcdbc80_g)

	qcd_g = qcdem20_g

else:
	data       = sample('mu_data'         , inputDir + 'mu_data_ratios.root'      )
	wjets      = sample('mu_wjets'        , inputDir + 'mu_wjets_ratios.root'     )
	dyjets50   = sample('mu_dyjets50'     , inputDir + 'mu_dyjets50_ratios.root'  )
	dyjets10   = sample('mu_dyjets10'     , inputDir + 'mu_dyjets10_ratios.root'  )
	qcd        = sample('mu_qcdmuenr'     , inputDir + 'mu_qcdmuenr_ratios.root'  )

	ttbar_g    = sample('mu_ttbar_g'      , inputDir + 'mu_ttbar_g_ratios.root'   )
	qcd_g      = sample('mu_qcdmuenr_g'   , inputDir + 'mu_qcdmuenr_g_ratios.root')

	data_samples = []
	data_samples.append(data)

	mc_samples = []
	mc_samples.append(qcd     )
	mc_samples.append(wjets   )
	mc_samples.append(dyjets50)
	mc_samples.append(dyjets10)

	qcd_samples = []
	qcd_samples.append(qcd)

	closure_samples = []
	closure_samples.append(ttbar_g)
	closure_samples.append(qcd_g)

	#data1      = sample('mu_data1'        , inputDir + 'mu_data1_ratios.root')
	#data2      = sample('mu_data2'        , inputDir + 'mu_data2_ratios.root')
	#data3      = sample('mu_data3'        , inputDir + 'mu_data3_ratios.root')
	#data4      = sample('mu_data4'        , inputDir + 'mu_data4_ratios.root')
	#data5      = sample('mu_data5'        , inputDir + 'mu_data5_ratios.root')
	##data6      = sample('mu_data6'        , inputDir + 'mu_data6_ratios.root')
	##data7      = sample('mu_data7'        , inputDir + 'mu_data7_ratios.root')

	#data_samples = []
	#data_samples.append(data1)
	#data_samples.append(data2)
	#data_samples.append(data3)
	#data_samples.append(data4)
	#data_samples.append(data5)
	#data_samples.append(data6)
	#data_samples.append(data7)

	#mc_samples = []

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



## LIST OF HISTOGRAMS TO PLOT

plot1dHists = ['h_Loose_AwayJetDR', 'h_Loose_AwayJetPt', 'h_Loose_ClosJetDR', 'h_Loose_ClosJetPt', 'h_Loose_ClosJetPt_0', 'h_Loose_ClosJetPt_1', 'h_Loose_ClosJetPt_2', 'h_Loose_ClosJetPt_3', 'h_Loose_ClosJetPt_4', 'h_Loose_ClosJetPt_5', 'h_Loose_HT', 'h_Loose_LepEta', 'h_Loose_LepIso', 'h_Loose_LepPt', 'h_Loose_MET', 'h_Loose_METnoMTCut', 'h_Loose_MT', 'h_Loose_MTMET20', 'h_Loose_MTMET30', 'h_Loose_MaxJPt', 'h_Loose_MaxJCSV', 'h_Loose_AllJCPt', 'h_Loose_AllJRPt', 'h_Loose_AllJEta', 'h_Loose_AllJCSV', 'h_Loose_AllJEtatest1', 'h_Loose_AllJEtatest2', 'h_Loose_AllJEtatest3', 'h_Loose_NBJets', 'h_Loose_NJets', 'h_Loose_NVertices', 'h_Loose_NVertices1', 'h_Loose_NVerticesMET20', 'h_Loose_D0', 'h_Tight_AwayJetDR', 'h_Tight_AwayJetPt', 'h_Tight_ClosJetDR', 'h_Tight_ClosJetPt', 'h_Tight_ClosJetPt_0', 'h_Tight_ClosJetPt_1', 'h_Tight_ClosJetPt_2', 'h_Tight_ClosJetPt_3', 'h_Tight_ClosJetPt_4', 'h_Tight_ClosJetPt_5', 'h_Tight_HT', 'h_Tight_LepEta', 'h_Tight_LepIso', 'h_Tight_LepPt', 'h_Tight_MET', 'h_Tight_METnoMTCut', 'h_Tight_MT', 'h_Tight_MTMET20', 'h_Tight_MTMET30', 'h_Tight_MaxJPt', 'h_Tight_MaxJCSV', 'h_Tight_AllJCPt', 'h_Tight_AllJRPt', 'h_Tight_AllJEta', 'h_Tight_AllJCSV', 'h_Tight_NBJets', 'h_Tight_NJets', 'h_Tight_NVertices', 'h_Tight_NVertices1', 'h_Tight_NVerticesMET20', 'h_Tight_D0']

plot2dHists = ['h_Loose_DJPtJEta', 'h_Loose_FJPtJEta', 'h_Loose_DJPtJPt', 'h_Loose_FJPtJPt', 'h_Tight_DJPtJEta', 'h_Tight_FJPtJEta', 'h_Tight_DJPtJPt', 'h_Tight_FJPtJPt'] 



# SET SCALING

lower = []
upper = []

if scaling == 'qcd_weighted':
	scalefactors = fit.getMCScaleFactorMutually(qcd_samples, 'h_Loose_LepIso', data_samples, [], 0.1) 
	for i, mc in enumerate(qcd_samples): mc.Rescale(scalefactors[i])

if scaling == 'qcdwjets_weighted' or scaling == 'wjets_weighted':
	if dataType == 'el': mclist = [qcdem20, qcdem30, qcdem80, qcdem170, qcdem250, qcdem350, qcdbc20, qcdbc30, qcdbc80, dyjets50, dyjets10]
	else:                mclist = [qcd, dyjets50, dyjets10]
	wjets.Rescale(fit.getMCScaleFactor(wjets, 'h_Tight_MTMET20', data_samples, mclist, 60, 90)[0])

if scaling == 'wjetsdyjets_weighted':
	scalefactors = fit.getMCScaleFactorMutually([wjets, dyjets50, dyjets10], 'h_Tight_MTMET20', data_samples, qcd_samples, 60, 90)
	wjets.Rescale(scalefactors[0])
	dyjets50.Rescale(scalefactors[1])
	dyjets10.Rescale(scalefactors[2])

if scaling == 'fit_weighted':
	#scalefactors = fit.getMCScaleFactorSimultaneously(data_samples, qcd, wjets, dyjets50, dyjets10)
	scalefactors = fit.getMCScaleFactorSimultaneouslyQCDEWK(data_samples, qcd_samples, [wjets, dyjets50, dyjets10])
	for mc in qcd_samples: mc.Rescale(scalefactors[0])
	wjets.Rescale(scalefactors[1])
	dyjets50.Rescale(scalefactors[2])
	dyjets10.Rescale(scalefactors[3])

if scaling == 'fiterror_weighted':
	scalefactors = fit.getMCScaleFactorSimultaneouslyWithErrors(data_samples, qcd_samples, [wjets, dyjets50, dyjets10])
	for mc in qcd_samples: mc.Rescale(scalefactors[0][0])
	wjets.Rescale(scalefactors[0][1])
	dyjets50.Rescale(scalefactors[0][1])
	dyjets10.Rescale(scalefactors[0][1])
	lower = scalefactors[1]
	upper = scalefactors[2]

if module == 'plots_1d' or module == 'all':
	helper.PrintScale(canv, outputDir, [qcd_samples[0], wjets, dyjets50, dyjets10], lower, upper)




# produce 1d Plots

if module == 'plots_1d' or module == 'all':
	leg = helper.makeLegend(0.6, 0.5, 0.85, 0.85)
	leg.AddEntry(data_samples[0].hists[0], helper.getLegendName(data_samples[0].GetName()), 'pe')
	leg.AddEntry(wjets          .hists[0], helper.getLegendName(wjets          .GetName()), 'f' )
	leg.AddEntry(dyjets10       .hists[0], helper.getLegendName(dyjets10       .GetName()), 'f' )
	leg.AddEntry(qcd_samples[0] .hists[0], helper.getLegendName(qcd_samples[0] .GetName()), 'f' )
	if dataType == 'el': leg.AddEntry(qcdbc20.hists[0], helper.getLegendName(qcdbc20.GetName()), 'f')
	Plot.Plot1d(dataType, outputDir, data_samples, mc_samples, plot1dHists, leg, True)



# produce 2d Plots

if module == 'plots_2d' or module == 'all':
	Plot.Plot2d(dataType, outputDir, data_samples, mc_samples, plot2dHists)



# Plot all MET Zooms

if module == 'zoom_met' or module == 'all':
	leg = helper.makeLegend(0.6, 0.5, 0.85, 0.85)
	leg.AddEntry(data_samples[0].hists[0], helper.getLegendName(data_samples[0].GetName()), 'pe')
	leg.AddEntry(wjets          .hists[0], helper.getLegendName(wjets          .GetName()), 'f' )
	leg.AddEntry(dyjets10       .hists[0], helper.getLegendName(dyjets10       .GetName()), 'f' )
	leg.AddEntry(qcd_samples[0] .hists[0], helper.getLegendName(qcd_samples[0] .GetName()), 'f' )
	if dataType == 'el': leg.AddEntry(qcdbc20.hists[0], helper.getLegendName(qcdbc20.GetName()), 'f')
	Plot.PlotMETZooms(dataType, outputDir, data_samples, mc_samples, leg)



# Plot all JPt Zooms

#if module == 'zoom_jpt' or module == 'all':
#	leg0 = helper.makeLegend(0.6, 0.5, 0.85, 0.85)
#	leg0.AddEntry(data_samples[0].hists[0], helper.getLegendName(data_samples[0].GetName()), 'l')
#	leg0.AddEntry(wjets          .hists[0], helper.getLegendName(wjets          .GetName()), 'l')
#	leg0.AddEntry(dyjets10       .hists[0], helper.getLegendName(dyjets10       .GetName()), 'l')
#	leg0.AddEntry(qcd_samples[0] .hists[0], helper.getLegendName(qcd_samples[0] .GetName()), 'l')
#	if dataType == 'el': leg.AddEntry(qcdbc20.hists[0], helper.getLegendName(qcdbc20.GetName()), 'l')
#	Plot.PlotJPtZooms(dataType, outputDir, data_samples, mc_samples, leg0)



# Compare AllJet quantities between WJets and DYjets

#if module == 'compare' or module == 'all':
#	leg = helper.makeLegend(0.6, 0.6, 0.85, 0.85)
#	leg.AddEntry(wjets   .hists[0], helper.getLegendName(wjets   .GetName()), 'l' )
#	leg.AddEntry(dyjets50.hists[0], helper.getLegendName(dyjets50.GetName()), 'l' )
#	Plot.PlotCompare(dataType, outputDir, [wjets, dyjets50], 'AllJ', leg)



# Compare ClosJetPt for different origins in TTBar and QCD

#if module == 'compare' or module == 'all':
#	leg = helper.makeLegend(0.6, 0.6, 0.85, 0.85)
#	leg.AddEntry(ttbar_g.hists[0], helper.getLegendName(ttbar_g.GetName()), 'l' )
#	leg.AddEntry(qcd_g  .hists[0], helper.getLegendName(qcd_g  .GetName()), 'l' )
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'ClosJetPt_0', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'ClosJetPt_2', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'ClosJetPt_3', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'ClosJetPt_4', leg, '-2:')
#	#Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'ClosJetPt_5', leg, '-2:')



# Compare Isolation between QCD and TTBar

#if module == 'compare' or module == 'all':
#	leg = helper.makeLegend(0.6, 0.1, 0.85, 0.35)
#	leg.AddEntry(ttbar_g.hists[0], helper.getLegendName(ttbar_g.GetName()), 'l' )
#	leg.AddEntry(qcd_g  .hists[0], helper.getLegendName(qcd_g  .GetName()), 'l' )
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'LepIso_0', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'LepIso_2', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'LepIso_3', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'LepIso_4', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd_g], 'LepIso_5', leg, '-2:')
#	Plot.PlotCompare(dataType, outputDir, [ttbar_g, qcd]  , 'h_Loose_LepIso', leg, -1, True)



# compute and plot FR for every variable

if module == 'fakerates_1d' or module == 'all':
	FR.PlotFR(dataType, outputDir, data_samples, mc_samples, plot1dHists, [], [wjets, dyjets50, dyjets10], qcd_samples, True)



# compute and plot FR 2d Map (+ Projections)

if module == 'fakerates_2d' or module == 'all':
	FR.Plot2dFRMap(dataType, outputDir, module, data_samples, mc_samples, [], [wjets, dyjets50, dyjets10], qcd_samples, True, True)

#if module == 'fakerates_2d' or module == 'all': # testing PUweight_full
#	FR.Plot2dFRMap(dataType, outputDir, module, [data1, data2, data3, data4, data5], [], [], [], [], False, False)




# compute and plot FR 2d Map for Closure Test

if module == 'fakerates_2dct' or module == 'all':
	FR.Plot2dFRMapClosureTest(dataType, outputDir, module, data_samples, mc_samples, closure_samples, [wjets, dyjets50, dyjets10], qcd_samples)


if module == 'closure' or module == 'all':
	Plot.PlotProvenance(dataType, outputDir, closure_samples, [3,4,5,6])




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



