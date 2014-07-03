## lib_FakeRates.py

import ROOT, copy
import lib as helper
import lib_FitScale as fit


#___________________________________________________________________________________
def make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, hists, title_hist, file_name, usemarkers = False, ratio_title = '', ratio_max = 1.99, ratio_min = 0.0):
	#
	# produces all 1d fake rate plots (this function, among others, wants to be improved)
	# NOTE: when calling this function make sure that the first histogram in hists is the total data, and the second is the total bg (important for ratio)
	#
	# this function takes the following paramters:
	# dataType..........type of the lepton ('mu', 'el')
	# canv..............canvas to be plotted
	# pad_plot..........pad of the plot to be plotted
	# pad_ratio.........pad of the ratio to be plotted
	# outputDir.........basic output directory
	# hists.............list of histograms to be plotted to be plotted on top of each other
	# title_hist........histogram to get the X axis title from
	# file_name.........name of the output file
	# usemarkers........True if we want to plot both data and mc with markers (e.g. comparing different ewk subtraction methods), False then mc is plotted as a colored rectangle
	# ratio_title.......Y axis title of the ratio plot
	# ratio_max.........maximum Y range of the ratio plot
	# ratio_min.........minimum Y range of the ratio plot


	# define pads, draw options (we use markers for mc if 

	pad_plot.cd()
	
	if usemarkers:
		markersize_mc = 1.4
		drawoption_data = "p e1"
		drawoption_mc = "p e1 same"
		legendoption_mc = "pe"
	else:
		markersize_mc = 0
		drawoption_data = "p e1 x0"
		drawoption_mc = "e2 same"
		legendoption_mc = "f"

	# draw histograms

	hists[0][0].Draw(drawoption_data)
	hists[0][0].SetMarkerSize(1.4)
	for i in range(1,len(hists)):
		hists[i][0].SetMarkerSize(markersize_mc)
		hists[i][0].Draw(drawoption_mc)
	hists[0][0].Draw(drawoption_data + " same")

	# set plot style
	
	for i in range(len(hists)):
		hists[i][0] = helper.setFRPlotStyle(dataType, hists[i][0], helper.getColor(hists[i][1]))
		if i+1 == len(hists): 
			hists[i][0] = helper.setFRPlotStyle(dataType, hists[i][0], helper.getColor(hists[i][1]), 'FR as function of ' + helper.getXTitle(dataType, title_hist), title_hist)

	# define legend, fill and draw it

	if dataType == 'el': leg1 = helper.makeLegend(0.62, 0.08, 0.87, 0.33)
	else               : leg1 = helper.makeLegend(0.22, 0.6, 0.47, 0.85)

	leg1.AddEntry(hists[0][0], helper.getLegendName(hists[0][1]), 'pe')
	for i in range(1,len(hists)):
		leg1.AddEntry(hists[i][0], helper.getLegendName(hists[i][1]), legendoption_mc)

	leg1.Draw()


	# create RATIO PLOT

	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(hists[0][0])
	data_bg_ratio.Divide(hists[1][0])
	data_bg_ratio.Draw("p e")
	data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, title_hist, ratio_title, ratio_max, ratio_min)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()

	# produce plot
	
	helper.saveCanvas(canv, pad_plot, outputDir + "fakerates_1d/", file_name)


#___________________________________________________________________________________
def make2dFRPlot(dataType, canv, outputDir, dataset, hist, title_indeces, name='', exportinroot = False, folder = 'fakerates_2d/'):
	#
	# produces all 2d fake rate maps
	#
	# this function takes the following paramters:
	# dataType..........type of the lepton ('mu', 'el')
	# canv..............canvas to be plotted
	# outputDir.........basic output directory
	# dataset...........dataset (only to take the title of the X and Y axis from)
	# hist..............histogram to be plotted
	# title_indeces.....list of two elements which are the indeces of the histograms that carry the X anc Y axis titles in their X axis title
	# name..............name of the output file
	# exportinroot......True if we want to export the canvas in a root file
	# folder............one may change the last outputfolder to something else than fakerates_2d

	# define pad

	pad_plot = helper.makePad('tot')
	pad_plot.cd()
	pad_plot.SetTicks(1,1)

	# draw histogram

	hist.Draw("text colz e")

	# cosmetics

	hist.SetMarkerColor(ROOT.kBlack)
	hist.SetMarkerSize(1.8)
	hist.GetXaxis().SetTitle(helper.getXTitle(dataType, dataset.hists[title_indeces[0]]))
	hist.GetYaxis().SetTitle(helper.getXTitle(dataType, dataset.hists[title_indeces[1]]))
	hist.GetXaxis().SetTitleSize(0.07)
	hist.GetXaxis().SetLabelSize(0.07)
	hist.GetYaxis().SetTitleSize(0.07)
	hist.GetYaxis().SetLabelSize(0.07)
	hist.SetMinimum(0.0)

	if dataType == 'el': hist.SetMaximum(0.6)
	else               : hist.SetMaximum(0.4)
	hist.SetTitle("FR 2d Map (" + helper.getLegendName(name) + ")")

	# save plot

	helper.saveCanvas(canv, pad_plot, outputDir + folder, "FR_2dmap_" + name.lower().replace(" ", "_"), False, exportinroot)
	pad_plot.Close()


#___________________________________________________________________________________
def PlotFR(dataType, outputDir, datasets, mcsets, histlist, mcsetsplot = [], mcsubtract = [], mcsubtractplot = [], mcsubtractscales = False, bgestimation = False):
	# 
	# produce the fake rate plots (incl. ewk subtraction) for given histograms and given samples
	# NOTE: ALL SAMPLES MUST CONTAIN THE EXACT SAME LIST OF HISTOGRAMS, OTHERWISE THIS FUNCTION WILL NOT WORK
	#
	# this function takes the following paramters:
	# dataType..........type of the lepton ('mu', 'el')
	# outputDir.........basic output directory
	# datasets..........list of data samples [datasample1, datasample2, ..]
	# mcsets............list of mc samples [mcsample1, mcsample2, ..] to enter bg stack
	# histlist..........list of 1d histogram names ['h_Loose_LepIso', 'h_Loose_LepPhi', ..]
	# mcsetsplot........list of mc samples [mcsample1, mcsample2, ..] to be drawn seperately
	# mcsubtract........list of mc samples [mcsample1, mcsample2, ..] to enter ewk subtraction
	# mcsubtractplot....list of mc samples [mcsample1, mcsample2, ..] to be drawn in comparison with ewk subtraction 
	# mcsubtractscales..True if we first want to scale ewk according to ETH/UCSx methods


	# produce canvas and pads

	canv = helper.makeCanvas(900, 675, 'c1dFR')
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

	# default for ewk scales (central1 is ewk scale according to ETH method with lower and upper limit, central2 is scale according to UCSx)

	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0

	# compute the scales according to ETH and UCSx method
	# this part needs improvement

	if mcsubtractscales:
		scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(datasets, mcsubtractplot, mcsubtract, 50, 120, 'h_Tight_MTMET30')
		qcd2     = scfirst[0][0]
		central12= scfirst[0][1]
		lower2   = scfirst[1][1]
		upper2   = scfirst[2][1]
		scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(datasets, mcsubtractplot, mcsubtract)
		central1 = scfirst[0][1]
		lower    = scfirst[1][1]
		upper    = scfirst[2][1]
		scsecond = fit.getMCScaleFactorMutually(mcsubtract, 'h_Tight_MTMET30', datasets, mcsubtractplot, 60, 100)
		central2 = scsecond[0]
		scsecond = fit.getMCScaleFactorMutually(mcsubtract, 'h_Tight_MTMET20', datasets, mcsubtractplot, 60, 100)
		central22= scsecond[0]

		print "------**------"
		print "MET30:"
		print "qcd       = " + str(qcd2)
		print "central 1 = " + str(central12)
		print "lower   1 = " + str(lower2)
		print "upper   1 = " + str(upper2)
		print "central 2 = " + str(central2)
		print "------**------"
		print "MET20:"
		print "qcd       = " + str(scfirst[0][0])
		print "central 1 = " + str(central1)
		print "lower   1 = " + str(lower)
		print "upper   1 = " + str(upper)
		print "central 2 = " + str(central22)
		print "------++------"

	# we add data and mc in stacks for both numerator and denominator

	m = -1
	n = -1
	index_numerators    = []
	index_denominators  = []
	data_numerators     = []
	data_denominators   = []
	mc_numerators       = []
	mc_denominators     = []
	FRs_mcplot          = []
	mcplot_denominators = []
	mcsub_numerators    = []
	mcsub_denominators  = []

	# iterate over all histograms in root files
	# it does not matter which sample we iterate on, as all samples contain the same list of histograms

	for hist in datasets[0].hists:

		# get index of the histogram

		i = datasets[0].hists.index(hist)

		# only histograms in the parameter histlist are plotted

		if not hist.GetName() in histlist: continue

		# there are two NVertices plots in the list with different binning
		# we only plot the NVertices, but not the NVertices1 (this we use for the fake rate plots, see lib_FakeRate.py)

		if hist.GetName()[-9:] == "NVertices": continue # we take "NVertices1" histograms for Fakerate Plots
			
		# get numerator stacks

		if 'h_Tight_' in hist.GetName():

			index_numerators .append(i)
			data_numerators  .append(ROOT.THStack())
			mc_numerators    .append(ROOT.THStack())
			FRs_mcplot       .append([])
			mcsub_numerators .append(ROOT.THStack())
			m += 1

			for data in datasets:               data_numerators[m]   .Add(copy.deepcopy(data.hists[index_numerators[m]]))
			for mc in mcsets:                   mc_numerators[m]     .Add(copy.deepcopy(mc.hists  [index_numerators[m]]))
			for j, mc in enumerate(mcsetsplot): FRs_mcplot[m][j]        = copy.deepcopy(mc.hists  [index_numerators[m]])
			for mc in mcsubtractplot:           mcsub_numerators[m]  .Add(copy.deepcopy(mc.hists  [index_numerators[m]]))

		# get denominator stacks

		if 'h_Loose_' in hist.GetName():

			index_denominators .append(i)
			data_denominators  .append(ROOT.THStack())
			mc_denominators    .append(ROOT.THStack())
			mcplot_denominators.append([])
			mcsub_denominators .append(ROOT.THStack())
			n += 1

			for data in datasets:                data_denominators[n]   .Add(copy.deepcopy(data.hists[index_denominators[n]]))
			for mc in mcsets:                    mc_denominators[n]     .Add(copy.deepcopy(mc.hists  [index_denominators[n]]))
			for j, mc in enumerate(mcsetsplot):  mcplot_denominators[n][j] = copy.deepcopy(mc.hists  [index_denominators[n]])
			for mc in mcsubtractplot:            mcsub_denominators[n]  .Add(copy.deepcopy(mc.hists  [index_denominators[n]]))


	# get numerators from stack for data, mc and mcsubtract

	FRs_data        = [copy.deepcopy(data_numerator   .GetStack().Last()) for data_numerator   in data_numerators  ]
	FRs_mc          = [copy.deepcopy(mc_numerator     .GetStack().Last()) for mc_numerator     in mc_numerators    ]
	FRs_mcsub       = [copy.deepcopy(mcsub_numerator  .GetStack().Last()) for mcsub_numerator  in mcsub_numerators ]

	# perform ewk subtraction, once unscaled, once ETH method (central1, lower, upper) and once UCSx method

	for i in range(len(FRs_data)):

		FR_data_mcsub    = copy.deepcopy(FRs_data[i])
		FR_data_mcsub_c1 = copy.deepcopy(FRs_data[i])
		FR_data_mcsub_l1 = copy.deepcopy(FRs_data[i])
		FR_data_mcsub_u1 = copy.deepcopy(FRs_data[i])
		FR_data_mcsub_c2 = copy.deepcopy(FRs_data[i])

		data_denominator_mcsub    = copy.deepcopy(data_denominators[i].GetStack().Last())
		data_denominator_mcsub_c1 = copy.deepcopy(data_denominators[i].GetStack().Last())
		data_denominator_mcsub_l1 = copy.deepcopy(data_denominators[i].GetStack().Last())
		data_denominator_mcsub_u1 = copy.deepcopy(data_denominators[i].GetStack().Last())
		data_denominator_mcsub_c2 = copy.deepcopy(data_denominators[i].GetStack().Last())

		# we subtract every mc set in mcsubtract from the data 5 times (unscaled, ETH, lower, upper, UCSx)
		# both for numerator and denominator (WATCH OUT FOR THE SCALING!)

		if len(mcsubtract)>0:
			for mc in mcsubtract:
				# numerator unscaled
				FR_data_mcsub.Add(mc.hists[index_numerators[i]], -1)
				# numerator ETH central
				mc.hists[index_numerators[i]].Scale(central1)
				FR_data_mcsub_c1.Add(mc.hists[index_numerators[i]], -1)
				# numerator ETH lower bound
				mc.hists[index_numerators[i]].Scale(lower/central1)
				FR_data_mcsub_l1.Add(mc.hists[index_numerators[i]], -1)
				# numerator ETH upper bound
				mc.hists[index_numerators[i]].Scale(upper/lower)
				FR_data_mcsub_u1.Add(mc.hists[index_numerators[i]], -1)
				# numerator UCSx central
				mc.hists[index_numerators[i]].Scale(central2/upper)
				FR_data_mcsub_c2.Add(mc.hists[index_numerators[i]], -1)
				# rescale it to 1 again
				mc.hists[index_numerators[i]].Scale(1/central2)
				# denominator unscaled
				data_denominator_mcsub.Add(mc.hists[index_denominators[i]],-1)
				# denominator ETH central
				mc.hists[index_denominators[i]].Scale(central1)
				data_denominator_mcsub_c1.Add(mc.hists[index_denominators[i]],-1)
				# denominator ETH lower bound
				mc.hists[index_denominators[i]].Scale(lower/central1)
				data_denominator_mcsub_l1.Add(mc.hists[index_denominators[i]],-1)
				# denominator ETH upper bound
				mc.hists[index_denominators[i]].Scale(upper/lower)
				data_denominator_mcsub_u1.Add(mc.hists[index_denominators[i]],-1)
				# denomiantor UCSx central
				mc.hists[index_denominators[i]].Scale(central2/upper)
				data_denominator_mcsub_c2.Add(mc.hists[index_denominators[i]],-1)
				# rescale it to 1 again
				mc.hists[index_denominators[i]].Scale(1/central2)


		# ewk subtracted fake rates (non-correlated error propagation)

		FR_data_mcsub   .Divide(FR_data_mcsub   , data_denominator_mcsub   , 1, 1, '')
		FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1, 1, 1, '')
		FR_data_mcsub_l1.Divide(FR_data_mcsub_l1, data_denominator_mcsub_l1, 1, 1, '')
		FR_data_mcsub_u1.Divide(FR_data_mcsub_u1, data_denominator_mcsub_u1, 1, 1, '')
		FR_data_mcsub_c2.Divide(FR_data_mcsub_c2, data_denominator_mcsub_c2, 1, 1, '')

		# fake rates for pure data, total mc, single mc (correlated error propagation)

		FRs_data[i]  .Divide(FRs_data[i]  , data_denominators[i]  .GetStack().Last(), 1, 1, 'B')
		FRs_mc[i]    .Divide(FRs_mc[i]    , mc_denominators[i]    .GetStack().Last(), 1, 1, 'B')
		FRs_mcsub[i] .Divide(FRs_mcsub[i] , mcsub_denominators[i] .GetStack().Last(), 1, 1, 'B')
		
		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				FRs_mcplot[i][j].Divide(FRs_mcplot[i][j], mcplot_denominators[i][j], 1, 1, 'B')


		# define the list of histograms which shall be plotted
		# i.e. one has to take the histogram of the stack, not the stack itself

		# data vs. total mc

		histstoplot = []
		histstoplot.append([FRs_data[i], 'data'])
		histstoplot.append([FRs_mc[i], 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data')

		# fake rate for every single mc

		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				histstoplot = []
				histstoplot.append([FRs_data[i], 'data'])
				histstoplot.append([FRs_mcplot[i][j], mcsetsplot[j].GetName()])
				make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-' + mcsetsplot[j].GetName().lstrip(dataType + '_'))

		# ewk subtracted vs. mcsubtractplot
		# THIS PART WANTS TO BE IMPROVED: we treat all mcsubplot samples as qcd!

		if len(mcsubtract)>0:
			histstoplot = []
			histstoplot.append([FR_data_mcsub, 'datamcsub'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FRs_mcsub[i], 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew')

		# ewk subtracted one method vs. the other

		if len(mcsubtract)>0 and mcsubtractscales:

			# data vs. ETH
			histstoplot = []
			histstoplot.append([FRs_data[i], 'data'])
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew_data-eth', True, 'Data/ETH')

			# ETH vs. UCSx
			histstoplot = []
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			# ETH vs. mcsubtractplot vs. data
			# THIS PART WANTS TO BE IMPROVED: we treat all mcsubplot samples as qcd!
			histstoplot = []
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FRs_mcsub[i], 'mu_qcdmuenr'])
			histstoplot.append([FRs_data[i], 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew_data-eth-qcd', True, 'ETH/QCD')

	return True


#___________________________________________________________________________________
def DoMCSubCERN(hist_new, hist_data_small, hist_data_large, n_prompt_small, n_prompt_large, n_all_small, n_all_large):
	#
	# a first but unsatisfying attempt on the CERN ewk subtraction method
	#
	# this function takes the following paramters:
	# hist_new..........new histogram to be filled with the result
	# hist_data_small...FR map obtained in small MET bin
	# hist_data_large...FR map obtained in large MET bin
	# n_prompt_small....number of ewk events in small MET bin
	# n_prompt_large....number of ewk events in large MET bin
	# n_all_small.......number of data events in small MET bin
	# n_all_large.......number of data events in large MET bin

	r_p_sl = (n_prompt_small / float(n_prompt_large)) * (n_all_large / float(n_all_small))
	
	for i in range(1, hist_new.GetNbinsX()+1):
		for j in range(1, hist_new.GetNbinsY()+1):

			f_data_small = hist_data_small.GetBinContent(i,j)
			f_data_large = hist_data_large.GetBinContent(i,j)

			f_qcd = (f_data_small - r_p_sl * f_data_large) / (1. - r_p_sl)
			
			#print "adjusting value of bin " + str(i) + "." + str(j) + " from " + str(hist_new.GetBinContent(i,j)) + " to " + str(f_qcd)
			#print "f_data_small = " + str(f_data_small) + ", f_data_large = " + str(f_data_large) + ", r = " + str(r_p_sl)
			#print "---"
			
			hist_new.SetBinContent(i, j, f_qcd)

	return hist_new


#___________________________________________________________________________________
def Plot2dFRMap(dataType, outputDir, module, datasets, mcsets, mcsetsplot = [], mcsubtract = [], mcsubtractplot = [], doProjection = False, mcsubtractscales = False):
	# 
	# produce the fake rate 2d maps (incl. ewk subtraction) for given samples
	# NOTE: ALL SAMPLES MUST CONTAIN THE EXACT SAME LIST OF HISTOGRAMS, OTHERWISE THIS FUNCTION WILL NOT WORK
	#
	# this function takes the following paramters:
	# dataType..........type of the lepton ('mu', 'el')
	# outputDir.........basic output directory
	# module............module (the 1d projections on lepton eta and lepton pt are only created for the module 'all')
	# datasets..........list of data samples [datasample1, datasample2, ..]
	# mcsets............list of mc samples [mcsample1, mcsample2, ..] to enter bg stack
	# histlist..........list of 1d histogram names ['h_Loose_LepIso', 'h_Loose_LepPhi', ..]
	# mcsetsplot........list of mc samples [mcsample1, mcsample2, ..] to be drawn seperately
	# mcsubtract........list of mc samples [mcsample1, mcsample2, ..] to enter ewk subtraction
	# mcsubtractplot....list of mc samples [mcsample1, mcsample2, ..] to be drawn in comparison with ewk subtraction 
	# doProjection......True if the 1d projections on lepton eta and lepton pt bins shall be produced as well
	# mcsubtractscales..True if we first want to scale ewk according to ETH/UCSx methods


	# default for ewk scales (central1 is ewk scale according to ETH method with lower and upper limit, central2 is scale according to UCSx)

	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0


	# compute the scales according to ETH and UCSx method
	# this part needs improvement

	if mcsubtractscales:

		scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(datasets, mcsubtractplot, mcsubtract)
		central1 = scfirst[0][1]
		lower    = scfirst[1][1]
		upper    = scfirst[2][1]
		scsecond = fit.getMCScaleFactorMutually(mcsubtract, 'h_Tight_MTMET30', datasets, mcsubtractplot, 60, 100)
		central2 = scsecond[0]

		print "------**------"
		print "qcd       = " + str(scfirst[0][0])
		print "central 1 = " + str(central1)
		print "lower   1 = " + str(lower)
		print "upper   1 = " + str(upper)
		print "central 2 = " + str(central2)
		print "------++------"


	# define canvas

	canv = helper.makeCanvas(900, 675, 'c2dFR')

	# we add data and mc in stacks for both numerator and denominator

	index_numerator    = 0
	index_denominator  = 0
	FR_mcplot          = [{} for i in range(len(mcsetsplot))]
	FR_mcplot_copy     = [{} for i in range(len(mcsetsplot))]
	mcplot_denominator = [{} for i in range(len(mcsetsplot))]
	title_indeces = [0, 0]

	# iterate over all histograms in root files
	# it does not matter which sample we iterate on, as all samples contain the same list of histograms

	for hist in datasets[0].hists:

		# get index of histogram

		i = datasets[0].hists.index(hist)

		# get indeces of histograms which carry title for X axis (0) and Y axis (1)

		if hist.GetName() == 'h_Loose_LepEta':
			title_indeces[1] = i
		if hist.GetName() == 'h_Loose_LepPt':
			title_indeces[0] = i
		
		# get numerator histograms
	
		if hist.GetName()[-8:] == 'h_FTight':

			index_numerator = i

			data_numerator            = ROOT.THStack()
			mc_numerator              = ROOT.THStack()
			mcsub_numerator           = ROOT.THStack()

			for data in datasets:               data_numerator   .Add(copy.deepcopy(data.hists[index_numerator]))
			for mc in mcsets:                   mc_numerator     .Add(copy.deepcopy(mc  .hists[index_numerator]))
			for j, mc in enumerate(mcsetsplot): FR_mcplot[j]     =    copy.deepcopy(mc  .hists[index_numerator])
			for mc in mcsubtractplot:           mcsub_numerator  .Add(copy.deepcopy(mc  .hists[index_numerator]))

		# get denominator histograms

		if hist.GetName()[-8:] == 'h_FLoose':

			index_denominator = i

			data_denominator   = ROOT.THStack()
			mc_denominator     = ROOT.THStack()
			mcsub_denominator  = ROOT.THStack()

			for data in datasets:               data_denominator   .Add(copy.deepcopy(data.hists[index_denominator]))
			for mc in mcsets:                   mc_denominator     .Add(copy.deepcopy(mc  .hists[index_denominator]))
			for j, mc in enumerate(mcsetsplot): mcplot_denominator[j] = copy.deepcopy(mc  .hists[index_denominator])
			for mc in mcsubtractplot:           mcsub_denominator  .Add(copy.deepcopy(mc  .hists[index_denominator]))


		# Get Numerator CERN Histogram
		if hist.GetName()[-19:] == 'h_FTight_CERN_small':
			data_numerator_CERN_small = ROOT.THStack()
			for data in datasets:               data_numerator_CERN_small .Add(copy.deepcopy(data.hists[i]))

		# Get Numerator CERN Histogram
		if hist.GetName()[-19:] == 'h_FTight_CERN_large':
			data_numerator_CERN_large = ROOT.THStack()
			for data in datasets:               data_numerator_CERN_large .Add(copy.deepcopy(data.hists[i]))

		# Get Numerator CERN Histogram
		if hist.GetName()[-19:] == 'h_FLoose_CERN_small':
			data_denominator_CERN_small = ROOT.THStack()
			for data in datasets:               data_denominator_CERN_small .Add(copy.deepcopy(data.hists[i]))

		# Get Numerator CERN Histogram
		if hist.GetName()[-19:] == 'h_FLoose_CERN_small':
			data_denominator_CERN_large = ROOT.THStack()
			for data in datasets:               data_denominator_CERN_large .Add(copy.deepcopy(data.hists[i]))


	# get numerator histograms from stack

	FR_data        = copy.deepcopy(data_numerator   .GetStack().Last())
	FR_mc          = copy.deepcopy(mc_numerator     .GetStack().Last())
	FR_mcsub       = copy.deepcopy(mcsub_numerator  .GetStack().Last())

	# we copy the numerators for the projections

	FR_data_copy   = copy.deepcopy(FR_data)
	FR_mc_copy     = copy.deepcopy(FR_mc)
	FR_mcsub_copy  = copy.deepcopy(FR_mcsub)
	
	for j in range(len(mcsetsplot)): FR_mcplot_copy[j] = copy.deepcopy(FR_mcplot[j])

	# ewk numerators
	
	FR_data_mcsub    = copy.deepcopy(FR_data)
	FR_data_mcsub_c1 = copy.deepcopy(FR_data)
	FR_data_mcsub_l1 = copy.deepcopy(FR_data)
	FR_data_mcsub_u1 = copy.deepcopy(FR_data)
	FR_data_mcsub_c2 = copy.deepcopy(FR_data)

	# CERN method (not working yet)

	FR_data_CERN_small = copy.deepcopy(data_numerator_CERN_small.GetStack().Last())
	FR_data_CERN_large = copy.deepcopy(data_numerator_CERN_large.GetStack().Last())
	FR_data_CERN_small.Divide(FR_data_CERN_small, copy.deepcopy(data_denominator_CERN_small.GetStack().Last()), 1, 1, 'B')
	FR_data_CERN_large.Divide(FR_data_CERN_large, copy.deepcopy(data_denominator_CERN_large.GetStack().Last()), 1, 1, 'B')

	FR_data_mcsub_c3 = copy.deepcopy(FR_data)
	FR_data_mcsub_c3.Divide(FR_data_mcsub_c3, copy.deepcopy(data_denominator.GetStack().Last()), 1, 1, 'B')
	FR_data_mcsub_c3 = DoMCSubCERN(FR_data_mcsub_c3, FR_data_CERN_small, FR_data_CERN_large, 447731, 517016, 23680, 10089) # numbers from loose MET 
	#FR_data_mcsub_c3 = DoMCSubCERN(FR_data_mcsub_c3, FR_data_CERN_small, FR_data_CERN_large, 108963, 27751, 847, 270) # numbers from tight MET
	# you gotta fill in the numbers by hand (i know, not very nice indeed) from the counters fCounter_CERN_small/-large from Fakerates.cc

	# ewk denominators

	data_denominator_mcsub    = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_c1 = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_l1 = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_u1 = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_c2 = copy.deepcopy(data_denominator.GetStack().Last())



	# create 2d PLOT
	# we subtract every mc set in mcsubtract from the data 5 times (unscaled, ETH, lower, upper, UCSx)
	# both for numerator and denominator (WATCH OUT FOR THE SCALING!)

	if len(mcsubtract)>0: 
		for mc in mcsets:
			# numerator unscaled
			FR_data_mcsub.Add(mc.hists[index_numerator], -1)
			# numerator ETH central
			mc.hists[index_numerator].Scale(central1)
			FR_data_mcsub_c1.Add(mc.hists[index_numerator], -1)
			# numerator ETH lower bound
			mc.hists[index_numerator].Scale(lower/central1)
			FR_data_mcsub_l1.Add(mc.hists[index_numerator], -1)
			# numerator ETH upper bound
			mc.hists[index_numerator].Scale(upper/lower)
			FR_data_mcsub_u1.Add(mc.hists[index_numerator], -1)
			# numerator UCSx central
			mc.hists[index_numerator].Scale(central2/upper)
			FR_data_mcsub_c2.Add(mc.hists[index_numerator], -1)
			# rescale it to 1 again
			mc.hists[index_numerator].Scale(1/central2)
			# denominator unscaled
			data_denominator_mcsub.Add(mc.hists[index_denominator], -1)
			# denominator ETH central
			mc.hists[index_denominator].Scale(central1)
			data_denominator_mcsub_c1.Add(mc.hists[index_denominator],-1)
			# denominator ETH lower bound
			mc.hists[index_denominator].Scale(lower/central1)
			data_denominator_mcsub_l1.Add(mc.hists[index_denominator],-1)
			# denominator ETH upper bound
			mc.hists[index_denominator].Scale(upper/lower)
			data_denominator_mcsub_u1.Add(mc.hists[index_denominator],-1)
			# denominator UCSx central
			mc.hists[index_denominator].Scale(central2/upper)
			data_denominator_mcsub_c2.Add(mc.hists[index_denominator],-1)
			# rescale it to 1 again
			mc.hists[index_denominator].Scale(1/central2)


	# ewk subtracted numerators

	data_numerator_mcsub    = copy.deepcopy(FR_data_mcsub   )
	data_numerator_mcsub_c1 = copy.deepcopy(FR_data_mcsub_c1)
	data_numerator_mcsub_l1 = copy.deepcopy(FR_data_mcsub_l1)
	data_numerator_mcsub_u1 = copy.deepcopy(FR_data_mcsub_u1)
	data_numerator_mcsub_c2 = copy.deepcopy(FR_data_mcsub_c2)

	# ewk subtracted fake rates

	FR_data_mcsub   .Divide(FR_data_mcsub   , data_denominator_mcsub   , 1, 1, '')
	FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1, 1, 1, '')
	FR_data_mcsub_l1.Divide(FR_data_mcsub_l1, data_denominator_mcsub_l1, 1, 1, '')
	FR_data_mcsub_u1.Divide(FR_data_mcsub_u1, data_denominator_mcsub_u1, 1, 1, '')
	FR_data_mcsub_c2.Divide(FR_data_mcsub_c2, data_denominator_mcsub_c2, 1, 1, '')

	
	data_den = data_denominator   .GetStack().Last()
	#make2dFRPlot(dataType, canv, outputDir, datasets[0], data_den  , title_indeces, 'data_den', True)

	# fake rates for pure data, total mc and every single mc sample
	
	FR_data   .Divide(FR_data   , copy.deepcopy(data_denominator   .GetStack().Last()), 1, 1, 'B')
	FR_mc     .Divide(FR_mc     , copy.deepcopy(mc_denominator     .GetStack().Last()), 1, 1, 'B')
	FR_mcsub  .Divide(FR_mcsub  , copy.deepcopy(mcsub_denominator  .GetStack().Last()), 1, 1, 'B')

	for j in range(len(mcsetsplot)): FR_mcplot[j].Divide(FR_mcplot[j], copy.deepcopy(mcplot_denominator[j]), 1, 1, 'B')


	# call make2dFRPlot to produce fake rate maps

	# pure data
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data  , title_indeces, 'data')
	# total mc
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mc    , title_indeces, 'mc'  )
	# mcsubtractplot (i.e. qcd)
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mcsub , title_indeces, mcsubtractplot[0].GetName())

	# every single mc sample
	if len(mcsetsplot)>0:
		for j in range(len(mcsetsplot)):
			make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mcplot[j], title_indeces, mcsetsplot[j].GetName())

	# ewk subtracted unscaled
	if len(mcsubtract)>0: 
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub, title_indeces, 'datamcsub')

	# ewk subtracted ETH, lower, upper, UCSx, CERN
	if mcsubtractscales:
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c1, title_indeces, 'datamcsub_central1')
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_l1, title_indeces, 'datamcsub_lower1'  )
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_u1, title_indeces, 'datamcsub_upper1'  )
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c2, title_indeces, 'datamcsub_central2')
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c3, title_indeces, 'datamcsub_central3')

	



	# do make the lepton eta and lepton pt projections if module == 'all'

	if doProjection == True and module == 'all':

		# re-adjust the canvas margin and create some pads as we're goin 1d now, bro!

		canv.SetRightMargin(0.0)
		pad_plot = helper.makePad('plot')
		pad_ratio = helper.makePad('ratio')

		# projection on lepton pt goes first

		# ewk subtracted numerators

		FR_data_px_mcsub    = copy.deepcopy(data_numerator_mcsub   .ProjectionX())
		FR_data_px_mcsub_c1 = copy.deepcopy(data_numerator_mcsub_c1.ProjectionX())
		FR_data_px_mcsub_l1 = copy.deepcopy(data_numerator_mcsub_l1.ProjectionX())
		FR_data_px_mcsub_u1 = copy.deepcopy(data_numerator_mcsub_u1.ProjectionX())
		FR_data_px_mcsub_c2 = copy.deepcopy(data_numerator_mcsub_c2.ProjectionX())
		FR_data_px_mcsub_uf = copy.deepcopy(ufl_hist_num.ProjectionX())

		# ewk subtracted fake rates

		FR_data_px_mcsub   .Divide(FR_data_px_mcsub   , data_denominator_mcsub   .ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_c1.Divide(FR_data_px_mcsub_c1, data_denominator_mcsub_c1.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_l1.Divide(FR_data_px_mcsub_l1, data_denominator_mcsub_l1.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_u1.Divide(FR_data_px_mcsub_u1, data_denominator_mcsub_u1.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_c2.Divide(FR_data_px_mcsub_c2, data_denominator_mcsub_c2.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_uf.Divide(FR_data_px_mcsub_uf, ufl_hist_den.ProjectionX(), 1, 1, '')

		# normal numerators

		FR_data_px    = copy.deepcopy(FR_data_copy  .ProjectionX())	
		FR_mc_px      = copy.deepcopy(FR_mc_copy    .ProjectionX())
		FR_mcsub_px   = copy.deepcopy(FR_mcsub_copy .ProjectionX())

		# normal fake rates

		FR_data_px   .Divide(FR_data_px   , copy.deepcopy(data_denominator   .GetStack().Last().ProjectionX()), 1, 1, 'B')
		FR_mc_px     .Divide(FR_mc_px     , copy.deepcopy(mc_denominator     .GetStack().Last().ProjectionX()), 1, 1, 'B')
		FR_mcsub_px  .Divide(FR_mcsub_px  , copy.deepcopy(mcsub_denominator  .GetStack().Last().ProjectionX()), 1, 1, 'B')

		for j in range(len(mcsetsplot)):
			FR_mcplot_px[j] = copy.deepcopy(FR_mcplot_copy[j].ProjectionX())
			FR_mcplot_px[j].Divide(FR_mcplot_px[j], copy.deepcopy(mcplot_denominator[j].ProjectionX()), 1, 1, 'B')

		# here comes the lepton eta projection

		# ewk subtracted numerators

		FR_data_py_mcsub    = copy.deepcopy(data_numerator_mcsub   .ProjectionY())
		FR_data_py_mcsub_c1 = copy.deepcopy(data_numerator_mcsub_c1.ProjectionY())
		FR_data_py_mcsub_l1 = copy.deepcopy(data_numerator_mcsub_l1.ProjectionY())
		FR_data_py_mcsub_u1 = copy.deepcopy(data_numerator_mcsub_u1.ProjectionY())
		FR_data_py_mcsub_c2 = copy.deepcopy(data_numerator_mcsub_c2.ProjectionY())

		# ewk subtracted fake rates

		FR_data_py_mcsub   .Divide(FR_data_py_mcsub   , data_denominator_mcsub   .ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_c1.Divide(FR_data_py_mcsub_c1, data_denominator_mcsub_c1.ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_l1.Divide(FR_data_py_mcsub_l1, data_denominator_mcsub_l1.ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_u1.Divide(FR_data_py_mcsub_u1, data_denominator_mcsub_u1.ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_c2.Divide(FR_data_py_mcsub_c2, data_denominator_mcsub_c2.ProjectionY(), 1, 1, '')

		# normal numerators

		FR_data_py    = copy.deepcopy(FR_data_copy  .ProjectionY())	
		FR_mc_py      = copy.deepcopy(FR_mc_copy    .ProjectionY())
		FR_mcsub_py   = copy.deepcopy(FR_mcsub_copy .ProjectionY())

		# normal fake rates

		FR_data_py   .Divide(FR_data_py   , copy.deepcopy(data_denominator   .GetStack().Last().ProjectionY()), 1, 1, 'B')
		FR_mc_py     .Divide(FR_mc_py     , copy.deepcopy(mc_denominator     .GetStack().Last().ProjectionY()), 1, 1, 'B')
		FR_mcsub_py  .Divide(FR_mcsub_py  , copy.deepcopy(mcsub_denominator  .GetStack().Last().ProjectionY()), 1, 1, 'B')

		for j in range(len(mcsetsplot)):
			FR_mcplot_py[j] = copy.deepcopy(FR_mcplot_copy[j].ProjectionY())
			FR_mcplot_py[j].Divide(FR_mcplot_py[j], copy.deepcopy(mcplot_denominator[j].ProjectionY()), 1, 1, 'B')


		# plottin some nice plots, man! hell yeah!

		# define the list of histograms which shall be plotted
		# i.e. one has to take the histogram of the stack, not the stack itself

		# projections on lepton pt

		# data vs. total mc

		histstoplot = []
		histstoplot.append([FR_data_px, 'data'])
		histstoplot.append([FR_mc_px, 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data')

		# data vs. every mc sample

		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				histstoplot = []
				histstoplot.append([FR_data_px, 'data'])
				histstoplot.append([FR_mcplot_px[j], mcsetsplot[j].GetName()])
				make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-' + mcsetsplot[j].GetName().lstrip(dataType + '_'))

		# ewk subtracted unscaled vs. mcsubtractplot (i.e. qcd)
		# THIS PART WANTS TO BE IMPROVED: we treat all mcsubplot samples as qcd!
			
		if len(mcsubtract)>0:
			histstoplot = []
			histstoplot.append([FR_data_px_mcsub, 'datamcsub'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_px, 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew')

		# ewk subtraction methods vs. other methods

		if mcsubtractscales:

			# data vs. ETH
			histstoplot = []
			histstoplot.append([FR_data_px, 'data'])
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew_data-eth', True, 'Data/ETH')

			# ETH vs. UCSx
			histstoplot = []
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_px_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			# ETH vs. mcsubtractplot (i.e. qcd)
			# THIS PART WANTS TO BE IMPROVED: we treat all mcsubplot samples as qcd!
			histstoplot = []
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_px, 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew_data-eth-qcd', True, 'ETH/QCD')


		# projections on lepton eta

		# data vs. total mc

		histstoplot = []
		histstoplot.append([FR_data_py, 'data'])
		histstoplot.append([FR_mc_py, 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data')

		# data vs. every single mc

		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				histstoplot = []
				histstoplot.append([FR_data_py, 'data'])
				histstoplot.append([FR_mcplot_py[j], mcsetsplot[j].GetName()])
				make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Pt_data-' + mcsetsplot[j].GetName().lstrip(dataType + '_'))

		# ewk subtraction unscaled vs. mcsubtractplot (i.e. qcd) vs. data
		# THIS PART WANTS TO BE IMPROVED: we treat all mcsubplot samples as qcd!
			
		if len(mcsubtract)>0:
			histstoplot = []
			histstoplot.append([FR_data_py, 'data'])
			histstoplot.append([FR_data_py_mcsub, 'datamcsub'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_py, 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew')

		# ewk subtraction methods compared

		if mcsubtractscales:

			# data vs. ETH
			histstoplot = []
			histstoplot.append([FR_data_py, 'data'])
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew_data-eth', True, 'Data/ETH')

			# ETH vs. UCSx
			histstoplot = []
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_py_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			# ETH vs. mcsubtractplot (i.e. qcd) vs. data
			# THIS PART WANTS TO BE IMPROVED: we treat all mcsubplot samples as qcd!
			histstoplot = []
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])	
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_py, 'mu_qcdmuenr'])
			histstoplot.append([FR_data_py, 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew_data-eth-qcd', True, 'ETH/QCD')

	return True


#___________________________________________________________________________________
def Plot2dFRMapClosureTest(dataType, outputDir, module, datasets, mcsets, mcsetsplot = [], mcsubtract = [], mcsubtractplot = []):
	# 
	# basically the same function as Plot2dFRMap but only for closure test samples
	# NOTE: ALL SAMPLES MUST CONTAIN THE EXACT SAME LIST OF HISTOGRAMS, OTHERWISE THIS FUNCTION WILL NOT WORK
	#
	# this function takes the following paramters:
	# dataType..........type of the lepton ('mu', 'el')
	# outputDir.........basic output directory
	# module............module (the 1d projections on lepton eta and lepton pt are only created for the module 'all')
	# datasets..........list of data samples [datasample1, datasample2, ..]
	# mcsets............list of mc samples [mcsample1, mcsample2, ..] to enter bg stack
	# histlist..........list of 1d histogram names ['h_Loose_LepIso', 'h_Loose_LepPhi', ..]
	# mcsetsplot........list of mc samples [mcsample1, mcsample2, ..] to be drawn seperately
	# mcsubtract........list of mc samples [mcsample1, mcsample2, ..] to enter ewk subtraction
	# mcsubtractplot....list of mc samples [mcsample1, mcsample2, ..] to be drawn in comparison with ewk subtraction 


	# default for ewk scales (central1 is ewk scale according to ETH method with lower and upper limit, central2 is scale according to UCSx)

	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0

	# compute the scales according to ETH and UCSx method
	# this part needs improvement

	scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(datasets, mcsubtractplot, mcsubtract)
	central1 = scfirst[0][1]
	lower    = scfirst[1][1]
	upper    = scfirst[2][1]
	scsecond = fit.getMCScaleFactorMutually(mcsubtract, 'h_Tight_MTMET30', datasets, mcsubtractplot, 60, 100)
	central2 = scsecond[0]

	print "------**------"
	print "qcd       = " + str(scfirst[0][0])
	print "central 1 = " + str(central1)
	print "lower   1 = " + str(lower)
	print "upper   1 = " + str(upper)
	print "central 2 = " + str(central2)
	print "------++------"

	# define canvas

	canv               = helper.makeCanvas(900, 675, 'c2dFR')
	index_numerator    = 0
	index_denominator  = 0
	title_indeces      = [0, 0]
	origins            = 6

	# we add data and mc in stacks for both numerator and denominator

	FR_ttbar           = [{} for i in range(origins)]
	FR_qcd             = [{} for i in range(origins)]
	ttbar_numerator    = [ROOT.THStack() for i in range(origins)]
	qcd_numerator      = [ROOT.THStack() for i in range(origins)]
	ttbar_denominator  = [ROOT.THStack() for i in range(origins)]
	qcd_denominator    = [ROOT.THStack() for i in range(origins)]

	# iterate over all histograms in root files
	# it does not matter which sample we iterate on, as all samples contain the same list of histograms

	for hist in datasets[0].hists:

		# get index of the histogram 

		i = datasets[0].hists.index(hist)

		# get indeces of histograms which carry title for X axis (0) and Y axis (1)

		if hist.GetName() == 'h_Loose_LepEta':
			title_indeces[1] = i
		if hist.GetName() == 'h_Loose_LepPt':
			title_indeces[0] = i

		# get numerator histograms

		if hist.GetName()[-8:] == 'h_FTight':

			index_numerator = i

			data_numerator   = ROOT.THStack()
			mc_numerator     = ROOT.THStack()
			mcsub_numerator  = ROOT.THStack()

			for data in datasets:     data_numerator .Add(copy.deepcopy(data.hists[index_numerator]))
			for mc in mcsets:         mc_numerator   .Add(copy.deepcopy(mc  .hists[index_numerator]))
			for mc in mcsubtractplot: mcsub_numerator.Add(copy.deepcopy(mc  .hists[index_numerator]))

		# get denominator histograms
		
		if hist.GetName()[-8:] == 'h_FLoose':

			index_denominator = i

			data_denominator   = ROOT.THStack()
			mc_denominator     = ROOT.THStack()
			mcsub_denominator  = ROOT.THStack()

			for data in datasets:     data_denominator .Add(copy.deepcopy(data.hists[index_denominator]))
			for mc in mcsets:         mc_denominator   .Add(copy.deepcopy(mc  .hists[index_denominator]))
			for mc in mcsubtractplot: mcsub_denominator.Add(copy.deepcopy(mc  .hists[index_denominator]))


	# we stack the closure test histograms (i.e. with provenance info) seperately

	# iterate over all histograms in root files
	# it does not matter which sample we iterate on, as all samples contain the same list of histograms

	for hist in mcsetsplot[0].hists:

		# get index of the histogram

		i = mcsetsplot[0].hists.index(hist)

		# get numerator histogram

		if hist.GetName()[-10:-1] == 'h_FTight_':
		
			origin = int(hist.GetName()[-1:])
	
			for mc in mcsetsplot:
				if 'qcd'   in mc.GetName(): qcd_numerator  [origin].Add(copy.deepcopy(mc.hists[i]))
				if 'ttbar' in mc.GetName(): ttbar_numerator[origin].Add(copy.deepcopy(mc.hists[i]))

		# get denominator histogram
			
		if hist.GetName()[-10:-1] == 'h_FLoose_':
		
			origin = int(hist.GetName()[-1:])
			
			for mc in mcsetsplot:
				if 'qcd'   in mc.GetName(): qcd_denominator  [origin].Add(copy.deepcopy(mc.hists[i]))
				if 'ttbar' in mc.GetName(): ttbar_denominator[origin].Add(copy.deepcopy(mc.hists[i]))


	# get numerator histograms from stack

	FR_data          = copy.deepcopy(data_numerator .GetStack().Last())
	FR_mc            = copy.deepcopy(mc_numerator   .GetStack().Last())
	FR_mcsub         = copy.deepcopy(mcsub_numerator.GetStack().Last())
	FR_data_mcsub_c1 = copy.deepcopy(FR_data)

	for j in range(origins):
		FR_ttbar[j] = copy.deepcopy(ttbar_numerator[j].GetStack().Last())
		FR_qcd  [j] = copy.deepcopy(qcd_numerator  [j].GetStack().Last())

	data_denominator_mcsub_c1 = copy.deepcopy(data_denominator.GetStack().Last())


	# perform ewk subtraction only for ETH method

	if len(mcsubtract)>0: 
		for mc in mcsubtract:
			# numerator
			mc.hists[index_numerator].Scale(central1)
			FR_data_mcsub_c1.Add(mc.hists[index_numerator], -1)
			mc.hists[index_numerator].Scale(1.0/central1)
			# denominator
			mc.hists[index_denominator].Scale(central1)
			data_denominator_mcsub_c1.Add(mc.hists[index_denominator],-1)
			mc.hists[index_denominator].Scale(1.0/central1)


	# fake rates
	
	FR_data         .Divide(FR_data         , copy.deepcopy(data_denominator .GetStack().Last()), 1, 1, 'B')
	FR_mc           .Divide(FR_mc           , copy.deepcopy(mc_denominator   .GetStack().Last()), 1, 1, 'B')
	FR_mcsub        .Divide(FR_mcsub        , copy.deepcopy(mcsub_denominator.GetStack().Last()), 1, 1, 'B')
	FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1                         , 1, 1, '' )

	for j in range(origins):
		FR_ttbar[j].Divide(FR_ttbar[j], copy.deepcopy(ttbar_denominator[j].GetStack().Last()), 1, 1, 'B')
		FR_qcd  [j].Divide(FR_qcd  [j], copy.deepcopy(qcd_denominator  [j].GetStack().Last()), 1, 1, 'B')


	# plot 2d maps

	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data         , title_indeces, 'data'              , True, 'fakerates_2dct/')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mc           , title_indeces, 'mc'                , True, 'fakerates_2dct/')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mcsub        , title_indeces, 'qcd'               , True, 'fakerates_2dct/')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c1, title_indeces, 'datamcsub_central1', True, 'fakerates_2dct/')

	for j in range(origins):
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_ttbar[j], title_indeces, 'ttbar_g_' + str(j), True, 'fakerates_2dct/')
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_qcd[j]  , title_indeces, 'qcd_g_' + str(j)  , True, 'fakerates_2dct/')









