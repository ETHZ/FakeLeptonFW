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
	

args = sys.argv
dataType = args[1]
inputDir = args[2]
outputDir = args[3]

if dataType == 'el':
	data        = sample('el_data'         , inputDir + 'el_data_ratios.root'       )
	wjets       = sample('el_wjets'        , inputDir + 'el_wjets_ratios.root'      )
	dyjets50    = sample('el_dyjets50'     , inputDir + 'el_dyjets50_ratios.root'   )
	dyjets10    = sample('el_dyjets10'     , inputDir + 'el_dyjets10_ratios.root'   )
	ttbar0      = sample('el_ttbar0'       , inputDir + 'el_ttbar0_ratios.root'     )
	ttbar1      = sample('el_ttbar1'       , inputDir + 'el_ttbar1_ratios.root'     )
	ttbar2      = sample('el_ttbar2'       , inputDir + 'el_ttbar2_ratios.root'     )
	ttbar3      = sample('el_ttbar3'       , inputDir + 'el_ttbar3_ratios.root'     )
	ttbar4      = sample('el_ttbar4'       , inputDir + 'el_ttbar4_ratios.root'     )
	ttbar5      = sample('el_ttbar5'       , inputDir + 'el_ttbar5_ratios.root'     )
	ttbar6      = sample('el_ttbar6'       , inputDir + 'el_ttbar6_ratios.root'     )
	qcd00       = sample('el_qcd00'        , inputDir + 'el_qcd00_ratios.root'      ) 
	qcd01       = sample('el_qcd01'        , inputDir + 'el_qcd01_ratios.root'      ) 
	qcd02       = sample('el_qcd02'        , inputDir + 'el_qcd02_ratios.root'      ) 
	qcd03       = sample('el_qcd03'        , inputDir + 'el_qcd03_ratios.root'      ) 
	qcd10       = sample('el_qcd10'        , inputDir + 'el_qcd10_ratios.root'      ) 
	qcd11       = sample('el_qcd11'        , inputDir + 'el_qcd11_ratios.root'      ) 
	qcd12       = sample('el_qcd12'        , inputDir + 'el_qcd12_ratios.root'      ) 
	qcd13       = sample('el_qcd13'        , inputDir + 'el_qcd13_ratios.root'      ) 
	qcd20       = sample('el_qcd20'        , inputDir + 'el_qcd20_ratios.root'      ) 
	qcd21       = sample('el_qcd21'        , inputDir + 'el_qcd21_ratios.root'      ) 
	qcd22       = sample('el_qcd22'        , inputDir + 'el_qcd22_ratios.root'      ) 
	qcd23       = sample('el_qcd23'        , inputDir + 'el_qcd23_ratios.root'      ) 
	qcd30       = sample('el_qcd30'        , inputDir + 'el_qcd30_ratios.root'      ) 
	qcd31       = sample('el_qcd31'        , inputDir + 'el_qcd31_ratios.root'      ) 
	qcd32       = sample('el_qcd32'        , inputDir + 'el_qcd32_ratios.root'      ) 
	qcd33       = sample('el_qcd33'        , inputDir + 'el_qcd33_ratios.root'      ) 
	qcd40       = sample('el_qcd40'        , inputDir + 'el_qcd40_ratios.root'      ) 
	qcd41       = sample('el_qcd41'        , inputDir + 'el_qcd41_ratios.root'      ) 
	qcd42       = sample('el_qcd42'        , inputDir + 'el_qcd42_ratios.root'      ) 
	qcd43       = sample('el_qcd43'        , inputDir + 'el_qcd43_ratios.root'      ) 
	qcd50       = sample('el_qcd50'        , inputDir + 'el_qcd50_ratios.root'      ) 
	qcd51       = sample('el_qcd51'        , inputDir + 'el_qcd51_ratios.root'      ) 
	qcd52       = sample('el_qcd52'        , inputDir + 'el_qcd52_ratios.root'      ) 
	qcd53       = sample('el_qcd53'        , inputDir + 'el_qcd53_ratios.root'      ) 
	qcd60       = sample('el_qcd60'        , inputDir + 'el_qcd60_ratios.root'      ) 
	qcd61       = sample('el_qcd61'        , inputDir + 'el_qcd61_ratios.root'      ) 
	qcd62       = sample('el_qcd62'        , inputDir + 'el_qcd62_ratios.root'      ) 
	qcd63       = sample('el_qcd63'        , inputDir + 'el_qcd63_ratios.root'      ) 
	qcd70       = sample('el_qcd70'        , inputDir + 'el_qcd70_ratios.root'      ) 
	qcd71       = sample('el_qcd71'        , inputDir + 'el_qcd71_ratios.root'      ) 
	qcd72       = sample('el_qcd72'        , inputDir + 'el_qcd72_ratios.root'      ) 
	qcd73       = sample('el_qcd73'        , inputDir + 'el_qcd73_ratios.root'      ) 
	qcd80       = sample('el_qcd80'        , inputDir + 'el_qcd80_ratios.root'      ) 
	qcd81       = sample('el_qcd81'        , inputDir + 'el_qcd81_ratios.root'      ) 
	qcd82       = sample('el_qcd82'        , inputDir + 'el_qcd82_ratios.root'      ) 
	qcd83       = sample('el_qcd83'        , inputDir + 'el_qcd83_ratios.root'      ) 

	#qcdtot50    = sample('el_qcdtot50'     , inputDir + 'el_qcdtot50_ratios.root'   )
	#qcdtot80    = sample('el_qcdtot80'     , inputDir + 'el_qcdtot80_ratios.root'   )
	#qcdtot120   = sample('el_qcdtot120'    , inputDir + 'el_qcdtot120_ratios.root'  )
	#qcdtot170   = sample('el_qcdtot170'    , inputDir + 'el_qcdtot170_ratios.root'  )
	#qcdtot170v2 = sample('el_qcdtot170v2'  , inputDir + 'el_qcdtot170v2_ratios.root')
	#qcdtot300   = sample('el_qcdtot300'    , inputDir + 'el_qcdtot300_ratios.root'  )
	#qcdtot300v2 = sample('el_qcdtot300v2'  , inputDir + 'el_qcdtot300v2_ratios.root')
	#qcdtot300v3 = sample('el_qcdtot300v3'  , inputDir + 'el_qcdtot300v3_ratios.root')

	qcdem20     = sample('el_qcdemenr20'   , inputDir + 'el_qcdemenr20_ratios.root' ) 
	qcdem30     = sample('el_qcdemenr30'   , inputDir + 'el_qcdemenr30_ratios.root' )
	qcdem80     = sample('el_qcdemenr80'   , inputDir + 'el_qcdemenr80_ratios.root' )
	qcdem170    = sample('el_qcdemenr170'  , inputDir + 'el_qcdemenr170_ratios.root')
	qcdem250    = sample('el_qcdemenr250'  , inputDir + 'el_qcdemenr250_ratios.root')
	qcdem350    = sample('el_qcdemenr350'  , inputDir + 'el_qcdemenr350_ratios.root')
	qcdbc20     = sample('el_qcdbctoe20'   , inputDir + 'el_qcdbctoe20_ratios.root' )
	qcdbc30     = sample('el_qcdbctoe30'   , inputDir + 'el_qcdbctoe30_ratios.root' )
	qcdbc80     = sample('el_qcdbctoe80'   , inputDir + 'el_qcdbctoe80_ratios.root' )

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
	mc_samples.append(qcdem170   )
	mc_samples.append(qcdem250   )
	mc_samples.append(qcdem350   )
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
	qcd_samples.append(qcdem170   )
	qcd_samples.append(qcdem250   ) 
	qcd_samples.append(qcdem350   )
	qcd_samples.append(qcdbc20    )
	qcd_samples.append(qcdbc30    )
	qcd_samples.append(qcdbc80    )

	closure_samples = []
	closure_samples.append(ttbar0)
	closure_samples.append(ttbar1)
	closure_samples.append(ttbar2)
	closure_samples.append(ttbar3)
	closure_samples.append(qcd00)
	closure_samples.append(qcd01)
	closure_samples.append(qcd02)
	closure_samples.append(qcd03)
	closure_samples.append(qcd10)
	closure_samples.append(qcd11)
	closure_samples.append(qcd12)
	closure_samples.append(qcd13)
	closure_samples.append(qcd20)
	closure_samples.append(qcd21)
	closure_samples.append(qcd22)
	closure_samples.append(qcd23)
	closure_samples.append(qcd30)
	closure_samples.append(qcd31)
	closure_samples.append(qcd32)
	closure_samples.append(qcd33)
	closure_samples.append(qcd40)
	closure_samples.append(qcd41)
	closure_samples.append(qcd42)
	closure_samples.append(qcd43)
	closure_samples.append(qcd50)
	closure_samples.append(qcd51)
	closure_samples.append(qcd52)
	closure_samples.append(qcd53)
	closure_samples.append(qcd60)
	closure_samples.append(qcd61)
	closure_samples.append(qcd62)
	closure_samples.append(qcd63)
	closure_samples.append(qcd70)
	closure_samples.append(qcd71)
	closure_samples.append(qcd72)
	closure_samples.append(qcd73)
	closure_samples.append(qcd80)
	closure_samples.append(qcd81)
	closure_samples.append(qcd82)
	closure_samples.append(qcd83)


else:
	data       = sample('mu_data'         , inputDir + 'mu_data_ratios.root'    )
	wjets      = sample('mu_wjets'        , inputDir + 'mu_wjets_ratios.root'   )
	dyjets50   = sample('mu_dyjets50'     , inputDir + 'mu_dyjets50_ratios.root')
	dyjets10   = sample('mu_dyjets10'     , inputDir + 'mu_dyjets10_ratios.root')
	qcd        = sample('mu_qcdmuenr'     , inputDir + 'mu_qcdmuenr_ratios.root')
	ttbar0     = sample('mu_ttbar0'       , inputDir + 'mu_ttbar0_ratios.root'  )
	ttbar1     = sample('mu_ttbar1'       , inputDir + 'mu_ttbar1_ratios.root'  )
	ttbar2     = sample('mu_ttbar2'       , inputDir + 'mu_ttbar2_ratios.root'  )
	ttbar3     = sample('mu_ttbar3'       , inputDir + 'mu_ttbar3_ratios.root'  )
	ttbar4     = sample('mu_ttbar4'       , inputDir + 'mu_ttbar4_ratios.root'  )
	ttbar5     = sample('mu_ttbar5'       , inputDir + 'mu_ttbar5_ratios.root'  )
	ttbar6     = sample('mu_ttbar6'       , inputDir + 'mu_ttbar6_ratios.root'  )
	qcd0       = sample('mu_qcd0'         , inputDir + 'mu_qcd0_ratios.root'    )
	qcd1       = sample('mu_qcd1'         , inputDir + 'mu_qcd1_ratios.root'    )
	qcd2       = sample('mu_qcd2'         , inputDir + 'mu_qcd2_ratios.root'    )
	qcd3       = sample('mu_qcd3'         , inputDir + 'mu_qcd3_ratios.root'    )

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
	closure_samples.append(ttbar0)
	closure_samples.append(ttbar1)
	closure_samples.append(ttbar2)
	closure_samples.append(ttbar3)
	closure_samples.append(qcd0)
	closure_samples.append(qcd1)
	closure_samples.append(qcd2)
	closure_samples.append(qcd3)

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


# Rescaling for complete PU_complete
#for mc in mc_samples:i
#	mc.Rescale(24.85/8.1)



## LIST OF HISTOGRAMS TO PLOT

plot1dHists = ['h_Loose_AwayJetDR', 'h_Loose_AwayJetPt', 'h_Loose_ClosJetDR', 'h_Loose_ClosJetPt', 'h_Loose_HT', 'h_Loose_LepEta', 'h_Loose_LepIso', 'h_Loose_LepPt', 'h_Loose_MET', 'h_Loose_METnoMTCut', 'h_Loose_MT', 'h_Loose_MTMET20', 'h_Loose_MTMET30', 'h_Loose_MaxJPt', 'h_Loose_AllJCPt', 'h_Loose_AllJRPt', 'h_Loose_AllJEta', 'h_Loose_AllJEtatest1', 'h_Loose_AllJEtatest2', 'h_Loose_AllJEtatest3', 'h_Loose_NBJets', 'h_Loose_NJets', 'h_Loose_NVertices', 'h_Loose_NVertices1', 'h_Loose_NVerticesMET20', 'h_Loose_D0', 'h_Tight_AwayJetDR', 'h_Tight_AwayJetPt', 'h_Tight_ClosJetDR', 'h_Tight_ClosJetPt', 'h_Tight_HT', 'h_Tight_LepEta', 'h_Tight_LepIso', 'h_Tight_LepPt', 'h_Tight_MET', 'h_Tight_METnoMTCut', 'h_Tight_MT', 'h_Tight_MTMET20', 'h_Tight_MTMET30', 'h_Tight_MaxJPt', 'h_Tight_AllJCPt', 'h_Tight_AllJRPt', 'h_Tight_AllJEta', 'h_Tight_NBJets', 'h_Tight_NJets', 'h_Tight_NVertices', 'h_Tight_NVertices1', 'h_Tight_NVerticesMET20', 'h_Tight_D0']

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
	if dataType == 'el': mclist = [qcdem20, qcdbc20, wjets, dyjets50, dyjets10]
	else:                mclist = [qcd, wjets, dyjets50, dyjets10]
	helper.PrintScale(canv, outputDir, mclist, lower, upper)




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

if module == 'compare' or module == 'all':
	leg = helper.makeLegend(0.6, 0.6, 0.85, 0.85)
	leg.AddEntry(wjets   .hists[0], helper.getLegendName(wjets   .GetName()), 'l' )
	leg.AddEntry(dyjets50.hists[0], helper.getLegendName(dyjets50.GetName()), 'l' )
	Plot.PlotCompare(dataType, outputDir, [wjets, dyjets50], 'AllJ', leg)


# Compare Isolation between QCD and TTBar

if module == 'compare' or module == 'all':
	leg = helper.makeLegend(0.6, 0.1, 0.85, 0.35)
	leg.AddEntry(qcd   .hists[0], helper.getLegendName(qcd   .GetName()), 'l' )
	leg.AddEntry(ttbar2.hists[0], helper.getLegendName(ttbar2.GetName()), 'l' )
	Plot.PlotCompare(dataType, outputDir, [qcd, ttbar0], 'LepIso', leg)
	Plot.PlotCompare(dataType, outputDir, [qcd, ttbar1], 'LepIso', leg)
	Plot.PlotCompare(dataType, outputDir, [qcd, ttbar2], 'LepIso', leg)



# compute and plot FR for every variable

if module == 'fakerates_1d' or module == 'all':
	FR.PlotFR(dataType, outputDir, data_samples, mc_samples, plot1dHists, [ttbar0, ttbar1, ttbar2, ttbar3], [wjets, dyjets50, dyjets10], qcd_samples, True)



# compute and plot FR 2d Map (+ Projections)

if module == 'fakerates_2d' or module == 'all':
	FR.Plot2dFRMap(dataType, outputDir, module, data_samples, mc_samples, [], [wjets, dyjets50, dyjets10], qcd_samples, True, True)
	FR.Plot2dFRMapClosureTest(dataType, outputDir, module, data_samples, mc_samples, closure_samples, [wjets, dyjets50, dyjets10], qcd_samples)

#if module == 'fakerates_2d' or module == 'all': # testing PUweight_full
#	FR.Plot2dFRMap(dataType, outputDir, module, [data1, data2, data3, data4, data5], [], [], [], [], False, False)



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



