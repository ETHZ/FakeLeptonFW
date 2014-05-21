## lib_FakeRates.py

import ROOT, copy
import lib as helper
import lib_FitScale as fit


def make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, hists, title_hist, file_name, usemarkers = False, ratio_title = '', ratio_max = 1.99, ratio_min = 0.0):
	# calling this function make sure that
	# (1) the first histogram in hists is the total data, and the second is the total bg
	# this function wants to be improved
	# (2) we use color of wjets for total bg
	# (3) we use the same color of qcd for all single mc plots

	# create PLOT

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

	hists[0][0].Draw(drawoption_data)
	hists[0][0].SetMarkerSize(1.4)
	for i in range(1,len(hists)):
		hists[i][0].SetMarkerSize(markersize_mc)
		hists[i][0].Draw(drawoption_mc)
	hists[0][0].Draw(drawoption_data + " same")
	
	for i in range(len(hists)):
		hists[i][0] = helper.setFRPlotStyle(dataType, hists[i][0], helper.getColor(hists[i][1]))
		if i+1 == len(hists): 
			hists[i][0] = helper.setFRPlotStyle(dataType, hists[i][0], helper.getColor(hists[i][1]), 'FR as function of ' + helper.getXTitle(dataType, title_hist), title_hist)

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
	
	helper.saveCanvas(canv, pad_plot, outputDir + "fakerates_1d/", file_name)



def make2dFRPlot(dataType, canv, outputDir, dataset, hist, title_indeces, name='', exportinroot = False, folder = 'fakerates_2d/'):

	pad_plot = helper.makePad('tot')
	pad_plot.cd()
	pad_plot.SetTicks(1,1)
	hist.Draw("text colz e")
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

	helper.saveCanvas(canv, pad_plot, outputDir + folder, "FR_2dmap_" + name.lower().replace(" ", "_"), False, exportinroot)
	pad_plot.Close()



def PlotFR(dataType, outputDir, datasets, mcsets, histlist, mcsetsplot = [], mcsubtract = [], mcsubtractplot = [], mcsubtractscales = False, bgestimation = False):

	canv = helper.makeCanvas(900, 675, 'c1dFR')
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0

	# this part needs adjustment
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

	#print "------**------"
	#print "MET30:"
	#print "qcd       = " + str(qcd2)
	#print "central 1 = " + str(central12)
	#print "lower   1 = " + str(lower2)
	#print "upper   1 = " + str(upper2)
	#print "central 2 = " + str(central2)
	#print "------**------"
	#print "MET20:"
	#print "qcd       = " + str(scfirst[0][0])
	#print "central 1 = " + str(central1)
	#print "lower   1 = " + str(lower)
	#print "upper   1 = " + str(upper)
	#print "central 2 = " + str(central22)
	#print "------++------"


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

	for hist in datasets[0].hists:

		i = datasets[0].hists.index(hist)

		if not hist.GetName() in histlist: continue
		if hist.GetName()[-9:] == "NVertices": continue # we take "NVertices1" histograms for Fakerate Plots
			
		# Get Numerator Plots
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


		# Get Denominator Histograms
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


	FRs_data        = [copy.deepcopy(data_numerator   .GetStack().Last()) for data_numerator   in data_numerators  ]
	FRs_mc          = [copy.deepcopy(mc_numerator     .GetStack().Last()) for mc_numerator     in mc_numerators    ]
	FRs_mcsub       = [copy.deepcopy(mcsub_numerator  .GetStack().Last()) for mcsub_numerator  in mcsub_numerators ]

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

		if len(mcsubtract)>0:
			for mc in mcsets:
				if mc in mcsubtract:
					FR_data_mcsub.Add(mc.hists[index_numerators[i]], -1)
					mc.hists[index_numerators[i]].Scale(central1)
					FR_data_mcsub_c1.Add(mc.hists[index_numerators[i]], -1)
					mc.hists[index_numerators[i]].Scale(lower/central1)
					FR_data_mcsub_l1.Add(mc.hists[index_numerators[i]], -1)
					mc.hists[index_numerators[i]].Scale(upper/lower)
					FR_data_mcsub_u1.Add(mc.hists[index_numerators[i]], -1)
					mc.hists[index_numerators[i]].Scale(central2/upper)
					FR_data_mcsub_c2.Add(mc.hists[index_numerators[i]], -1)
					mc.hists[index_numerators[i]].Scale(1/central2)
					data_denominator_mcsub.Add(mc.hists[index_denominators[i]],-1)
					mc.hists[index_denominators[i]].Scale(central1)
					data_denominator_mcsub_c1.Add(mc.hists[index_denominators[i]],-1)
					mc.hists[index_denominators[i]].Scale(lower/central1)
					data_denominator_mcsub_l1.Add(mc.hists[index_denominators[i]],-1)
					mc.hists[index_denominators[i]].Scale(upper/lower)
					data_denominator_mcsub_u1.Add(mc.hists[index_denominators[i]],-1)
					mc.hists[index_denominators[i]].Scale(central2/upper)
					data_denominator_mcsub_c2.Add(mc.hists[index_denominators[i]],-1)
					mc.hists[index_denominators[i]].Scale(1/central2)


		FR_data_mcsub   .Divide(FR_data_mcsub   , data_denominator_mcsub   , 1, 1, '')
		FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1, 1, 1, '')
		FR_data_mcsub_l1.Divide(FR_data_mcsub_l1, data_denominator_mcsub_l1, 1, 1, '')
		FR_data_mcsub_u1.Divide(FR_data_mcsub_u1, data_denominator_mcsub_u1, 1, 1, '')
		FR_data_mcsub_c2.Divide(FR_data_mcsub_c2, data_denominator_mcsub_c2, 1, 1, '')

		FRs_data[i]  .Divide(FRs_data[i]  , data_denominators[i]  .GetStack().Last(), 1, 1, 'B')
		FRs_mc[i]    .Divide(FRs_mc[i]    , mc_denominators[i]    .GetStack().Last(), 1, 1, 'B')
		FRs_mcsub[i] .Divide(FRs_mcsub[i] , mcsub_denominators[i] .GetStack().Last(), 1, 1, 'B')
		
		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				FRs_mcplot[i][j].Divide(FRs_mcplot[i][j], mcplot_denominators[i][j], 1, 1, 'B')



		# this part needs adjustment
		histstoplot = []
		histstoplot.append([FRs_data[i], 'data'])
		histstoplot.append([FRs_mc[i], 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data')

		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				histstoplot = []
				histstoplot.append([FRs_data[i], 'data'])
				histstoplot.append([FRs_mcplot[i][j], mcsetsplot[j].GetName()])
				make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-' + mcsetsplot[j].GetName().lstrip(dataType + '_'))

		if len(mcsubtract)>0:
			histstoplot = []
			histstoplot.append([FR_data_mcsub, 'datamcsub'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FRs_mcsub[i], 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew')

		if len(mcsubtract)>0 and mcsubtractscales:
			histstoplot = []
			histstoplot.append([FRs_data[i], 'data'])
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew_data-eth', True, 'Data/ETH')

			histstoplot = []
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			histstoplot = []
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FRs_mcsub[i], 'mu_qcdmuenr'])
			histstoplot.append([FRs_data[i], 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FRs_data[i], 'FR_' + FRs_data[i].GetName().lstrip('h_Tight_') + '_data-ew_data-eth-qcd', True, 'ETH/QCD')

		

	return True




def DoMCSubCERN(hist_new, hist_data_small, hist_data_large, n_prompt_small, n_prompt_large, n_all_small, n_all_large):

	r_p_sl = (n_prompt_small / float(n_prompt_large)) * (n_all_large / float(n_all_small))
	
	for i in range(1, hist_new.GetNbinsX()+1):
		for j in range(1, hist_new.GetNbinsY()+1):

			f_data_small = hist_data_small.GetBinContent(i,j)
			f_data_large = hist_data_large.GetBinContent(i,j)

			f_qcd = (f_data_small - r_p_sl * f_data_large) / (1. - r_p_sl)
			
			print "adjusting value of bin " + str(i) + "." + str(j) + " from " + str(hist_new.GetBinContent(i,j)) + " to " + str(f_qcd)
			print "f_data_small = " + str(f_data_small) + ", f_data_large = " + str(f_data_large) + ", r = " + str(r_p_sl)
			print "---"
			
			hist_new.SetBinContent(i, j, f_qcd)

	return hist_new




def Plot2dFRMap(dataType, outputDir, module, datasets, mcsets, mcsetsplot = [], mcsubtract = [], mcsubtractplot = [], doProjection = False, mcsubtractscales = False):
	# attention: when calling this function with substraction of certain MC (e.g. electroweak)
	#            you need to make sure that the monte carlo you want to substract already has
	#            been given in mcsets as well


	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0

	# this part needs adjustment
	if mcsubtractscales:
		scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(datasets, mcsubtractplot, mcsubtract)
		central1 = scfirst[0][1]
		lower    = scfirst[1][1]
		upper    = scfirst[2][1]
		scsecond = fit.getMCScaleFactorMutually(mcsubtract, 'h_Tight_MTMET30', datasets, mcsubtractplot, 60, 100)
		central2 = scsecond[0]

	#print "------**------"
	#print "qcd       = " + str(scfirst[0][0])
	#print "central 1 = " + str(central1)
	#print "lower   1 = " + str(lower)
	#print "upper   1 = " + str(upper)
	#print "central 2 = " + str(central2)
	#print "------++------"


	if len(mcsubtract)>0:
		for mc in mcsubtract:
			if not mc in mcsets:
				print "ERROR in calling Plot2dFRMap"
				print "Every MC that shall be substracted from data must also be given in the BG"
				return False

	canv = helper.makeCanvas(900, 675, 'c2dFR')
	index_numerator    = 0
	index_denominator  = 0
	FR_mcplot          = [{} for i in range(len(mcsetsplot))]
	FR_mcplot_copy     = [{} for i in range(len(mcsetsplot))]
	mcplot_denominator = [{} for i in range(len(mcsetsplot))]
	title_indeces = [0, 0]

	for hist in datasets[0].hists:

		i = datasets[0].hists.index(hist)

		if hist.GetName() == 'h_Loose_LepEta':
			title_indeces[1] = i
		if hist.GetName() == 'h_Loose_LepPt':
			title_indeces[0] = i
		
	
		# Get Numerator Plots
		if hist.GetName()[-8:] == 'h_FTight':

			index_numerator = i

			data_numerator            = ROOT.THStack()
			mc_numerator              = ROOT.THStack()
			mcsub_numerator           = ROOT.THStack()

			for data in datasets:               data_numerator   .Add(copy.deepcopy(data.hists[index_numerator]))
			for mc in mcsets:                   mc_numerator     .Add(copy.deepcopy(mc  .hists[index_numerator]))
			for j, mc in enumerate(mcsetsplot): FR_mcplot[j]     =    copy.deepcopy(mc  .hists[index_numerator])
			for mc in mcsubtractplot:           mcsub_numerator  .Add(copy.deepcopy(mc  .hists[index_numerator]))


		# Get Denominator Histograms
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



	FR_data        = copy.deepcopy(data_numerator   .GetStack().Last())
	FR_mc          = copy.deepcopy(mc_numerator     .GetStack().Last())
	FR_mcsub       = copy.deepcopy(mcsub_numerator  .GetStack().Last())

	FR_data_copy   = copy.deepcopy(FR_data)
	FR_mc_copy     = copy.deepcopy(FR_mc)
	FR_mcsub_copy  = copy.deepcopy(FR_mcsub)
	
	for j in range(len(mcsetsplot)): FR_mcplot_copy[j] = copy.deepcopy(FR_mcplot[j])


	FR_data_CERN_small = copy.deepcopy(data_numerator_CERN_small.GetStack().Last())
	FR_data_CERN_large = copy.deepcopy(data_numerator_CERN_large.GetStack().Last())

	FR_data_CERN_small.Divide(FR_data_CERN_small, copy.deepcopy(data_denominator_CERN_small.GetStack().Last()), 1, 1, 'B')
	FR_data_CERN_large.Divide(FR_data_CERN_large, copy.deepcopy(data_denominator_CERN_large.GetStack().Last()), 1, 1, 'B')


	#sum = 0 
	#for i in range(FR_data.GetNbinsX()+2, (FR_data.GetNbinsX()+2)*(FR_data.GetNbinsY()+1)):
	#	print "numerator bin " + str(i) + " has value " + str(FR_data.GetBinContent(i)) + " and error " + str(FR_data.GetBinError(i))
	#	sum += FR_data.GetBinContent(i)
	#print "numerator has sum " + str(sum)
	#print "---"

	#sum = 0
	#for i in range(FR_data.GetNbinsX()+2, (FR_data.GetNbinsX()+2)*(FR_data.GetNbinsY()+1)):
	#	print "denominator bin " + str(i) + " has value " + str(data_denominator.GetBinContent(i)) + " and error " + str(data_denominator.GetBinError(i))
	#	sum += data_denominator.GetBinContent(i)
	#print "denominator has sum " + str(sum)
	#print "---"

	FR_data_mcsub    = copy.deepcopy(FR_data)
	FR_data_mcsub_c1 = copy.deepcopy(FR_data)
	FR_data_mcsub_l1 = copy.deepcopy(FR_data)
	FR_data_mcsub_u1 = copy.deepcopy(FR_data)
	FR_data_mcsub_c2 = copy.deepcopy(FR_data)
	FR_data_mcsub_c3 = copy.deepcopy(FR_data)
	FR_data_mcsub_c3.Divide(FR_data_mcsub_c3, copy.deepcopy(data_denominator.GetStack().Last()), 1, 1, 'B')
	FR_data_mcsub_c3 = DoMCSubCERN(FR_data_mcsub_c3, FR_data_CERN_small, FR_data_CERN_large, 117683, 32137, 12139, 3750)
	# you gotta fill in the numbers by hand (i know, not very nice indeed) from the counters fCounter_CERN_small/-large from Fakerates.cc

	data_denominator_mcsub    = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_c1 = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_l1 = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_u1 = copy.deepcopy(data_denominator.GetStack().Last())
	data_denominator_mcsub_c2 = copy.deepcopy(data_denominator.GetStack().Last())

	##FR_mc      = [{} for j in range(len(mcsetsplot))]
	##FR_mc_copy = [{} for j in range(len(mcsetsplot))]
	##FR_mc_px   = [{} for j in range(len(mcsetsplot))]
	##FR_mc_py   = [{} for j in range(len(mcsetsplot))]

	##FR_mcsub      = [{} for j in range(len(mcsubtractplot))]
	##FR_mcsub_copy = [{} for j in range(len(mcsubtractplot))]
	##FR_mcsub_px   = [{} for j in range(len(mcsubtractplot))]
	##FR_mcsub_py   = [{} for j in range(len(mcsubtractplot))]


	# create 2d PLOT

	if len(mcsubtract)>0: 
		for mc in mcsets:
			if mc in mcsubtract:
				FR_data_mcsub.Add(mc.hists[index_numerator], -1)
				mc.hists[index_numerator].Scale(central1)
				FR_data_mcsub_c1.Add(mc.hists[index_numerator], -1)
				mc.hists[index_numerator].Scale(lower/central1)
				FR_data_mcsub_l1.Add(mc.hists[index_numerator], -1)
				mc.hists[index_numerator].Scale(upper/lower)
				FR_data_mcsub_u1.Add(mc.hists[index_numerator], -1)
				mc.hists[index_numerator].Scale(central2/upper)
				FR_data_mcsub_c2.Add(mc.hists[index_numerator], -1)
				mc.hists[index_numerator].Scale(1/central2)
				data_denominator_mcsub.Add(mc.hists[index_denominator], -1)
				mc.hists[index_denominator].Scale(central1)
				data_denominator_mcsub_c1.Add(mc.hists[index_denominator],-1)
				mc.hists[index_denominator].Scale(lower/central1)
				data_denominator_mcsub_l1.Add(mc.hists[index_denominator],-1)
				mc.hists[index_denominator].Scale(upper/lower)
				data_denominator_mcsub_u1.Add(mc.hists[index_denominator],-1)
				mc.hists[index_denominator].Scale(central2/upper)
				data_denominator_mcsub_c2.Add(mc.hists[index_denominator],-1)
				mc.hists[index_denominator].Scale(1/central2)


	data_numerator_mcsub    = copy.deepcopy(FR_data_mcsub   )
	data_numerator_mcsub_c1 = copy.deepcopy(FR_data_mcsub_c1)
	data_numerator_mcsub_l1 = copy.deepcopy(FR_data_mcsub_l1)
	data_numerator_mcsub_u1 = copy.deepcopy(FR_data_mcsub_u1)
	data_numerator_mcsub_c2 = copy.deepcopy(FR_data_mcsub_c2)


	#FR_data_mcsub_c1t = copy.deepcopy(FR_data_mcsub_c1)
	#FR_data_mcsub_c1t .Divide(FR_data_mcsub_c1t, data_denominator_mcsub_c1, 1, 1, 'B')

	#print "correlated:"
	#for i in range(FR_data_mcsub_c1t.GetNbinsX()+2, (FR_data_mcsub_c1t.GetNbinsX()+2)*(FR_data_mcsub_c1t.GetNbinsY()+1)):
	#	print "bin " + str(i) + " has value " + str(FR_data_mcsub_c1t.GetBinContent(i)) + " and error " + str(FR_data_mcsub_c1t.GetBinError(i))
	#print "---"
	#print "uncorrelated:"

	FR_data_mcsub   .Divide(FR_data_mcsub   , data_denominator_mcsub   , 1, 1, '')
	FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1, 1, 1, '')
	FR_data_mcsub_l1.Divide(FR_data_mcsub_l1, data_denominator_mcsub_l1, 1, 1, '')
	FR_data_mcsub_u1.Divide(FR_data_mcsub_u1, data_denominator_mcsub_u1, 1, 1, '')
	FR_data_mcsub_c2.Divide(FR_data_mcsub_c2, data_denominator_mcsub_c2, 1, 1, '')

	#for i in range(FR_data_mcsub_c1.GetNbinsX()+2, (FR_data_mcsub_c1.GetNbinsX()+2)*(FR_data_mcsub_c1.GetNbinsY()+1)):
	#	if FR_data_mcsub_c1t.GetBinError(i)>0: frac = FR_data_mcsub_c1.GetBinError(i) / FR_data_mcsub_c1t.GetBinError(i)
	#	else: frac = 0
	#	print "bin " + str(i) + " has value " + str(FR_data_mcsub_c1.GetBinContent(i)) + " and error " + str(FR_data_mcsub_c1.GetBinError(i)) + " (uncorrelated) " + str(FR_data_mcsub_c1t.GetBinError(i)) + " (correlated) which is a " + str(frac) + " difference"

	#FR_data_mcsub   .Divide(data_denominator_mcsub   )
	#FR_data_mcsub_c1.Divide(data_denominator_mcsub_c1)
	#FR_data_mcsub_l1.Divide(data_denominator_mcsub_l1)
	#FR_data_mcsub_u1.Divide(data_denominator_mcsub_u1)
	#FR_data_mcsub_c2.Divide(data_denominator_mcsub_c2)

	#FR_data_mcsub    = helper.doTH2ErrorPropagation(FR_data_mcsub   , data_numerator_mcsub   , data_denominator_mcsub   , 4)
	#FR_data_mcsub_c1 = helper.doTH2ErrorPropagation(FR_data_mcsub_c1, data_numerator_mcsub_c1, data_denominator_mcsub_c1, 4)
	#FR_data_mcsub_l1 = helper.doTH2ErrorPropagation(FR_data_mcsub_l1, data_numerator_mcsub_l1, data_denominator_mcsub_l1, 4)
	#FR_data_mcsub_u1 = helper.doTH2ErrorPropagation(FR_data_mcsub_u1, data_numerator_mcsub_u1, data_denominator_mcsub_u1, 4)
	#FR_data_mcsub_c2 = helper.doTH2ErrorPropagation(FR_data_mcsub_c2, data_numerator_mcsub_c2, data_denominator_mcsub_c2, 4)
	
	FR_data   .Divide(FR_data   , copy.deepcopy(data_denominator   .GetStack().Last()), 1, 1, 'B')
	FR_mc     .Divide(FR_mc     , copy.deepcopy(mc_denominator     .GetStack().Last()), 1, 1, 'B')
	FR_mcsub  .Divide(FR_mcsub  , copy.deepcopy(mcsub_denominator  .GetStack().Last()), 1, 1, 'B')

	for j in range(len(mcsetsplot)): FR_mcplot[j].Divide(FR_mcplot[j], copy.deepcopy(mcplot_denominator[j]), 1, 1, 'B')


	# plot 2d maps
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data  , title_indeces, 'data')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mc    , title_indeces, 'mc'  )
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mcsub , title_indeces, mcsubtractplot[0].GetName())

	if len(mcsetsplot)>0:
		for j in range(len(mcsetsplot)):
			make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mcplot[j], title_indeces, mcsetsplot[j].GetName())

	if len(mcsubtract)>0: 
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub, title_indeces, 'datamcsub')

	if mcsubtractscales:
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c1, title_indeces, 'datamcsub_central1')
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_l1, title_indeces, 'datamcsub_lower1'  )
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_u1, title_indeces, 'datamcsub_upper1'  )
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c2, title_indeces, 'datamcsub_central2')
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c3, title_indeces, 'datamcsub_central3')




	# Create Projections

	if doProjection == True and module == 'all':

		canv.SetRightMargin(0.0)
		pad_plot = helper.makePad('plot')
		pad_ratio = helper.makePad('ratio')


		# X projection
		FR_data_px_mcsub    = copy.deepcopy(data_numerator_mcsub   .ProjectionX())
		FR_data_px_mcsub_c1 = copy.deepcopy(data_numerator_mcsub_c1.ProjectionX())
		FR_data_px_mcsub_l1 = copy.deepcopy(data_numerator_mcsub_l1.ProjectionX())
		FR_data_px_mcsub_u1 = copy.deepcopy(data_numerator_mcsub_u1.ProjectionX())
		FR_data_px_mcsub_c2 = copy.deepcopy(data_numerator_mcsub_c2.ProjectionX())

		FR_data_px_mcsub   .Divide(FR_data_px_mcsub   , data_denominator_mcsub   .ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_c1.Divide(FR_data_px_mcsub_c1, data_denominator_mcsub_c1.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_l1.Divide(FR_data_px_mcsub_l1, data_denominator_mcsub_l1.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_u1.Divide(FR_data_px_mcsub_u1, data_denominator_mcsub_u1.ProjectionX(), 1, 1, '')
		FR_data_px_mcsub_c2.Divide(FR_data_px_mcsub_c2, data_denominator_mcsub_c2.ProjectionX(), 1, 1, '')

		FR_data_px    = copy.deepcopy(FR_data_copy  .ProjectionX())	
		FR_mc_px      = copy.deepcopy(FR_mc_copy    .ProjectionX())
		FR_mcsub_px   = copy.deepcopy(FR_mcsub_copy .ProjectionX())

		FR_data_px   .Divide(FR_data_px   , copy.deepcopy(data_denominator   .GetStack().Last().ProjectionX()), 1, 1, 'B')
		FR_mc_px     .Divide(FR_mc_px     , copy.deepcopy(mc_denominator     .GetStack().Last().ProjectionX()), 1, 1, 'B')
		FR_mcsub_px  .Divide(FR_mcsub_px  , copy.deepcopy(mcsub_denominator  .GetStack().Last().ProjectionX()), 1, 1, 'B')

		for j in range(len(mcsetsplot)):
			FR_mcplot_px[j] = copy.deepcopy(FR_mcplot_copy[j].ProjectionX())
			FR_mcplot_px[j].Divide(FR_mcplot_px[j], copy.deepcopy(mcplot_denominator[j].ProjectionX()), 1, 1, 'B')

		# Y projection
		FR_data_py_mcsub    = copy.deepcopy(data_numerator_mcsub   .ProjectionY())
		FR_data_py_mcsub_c1 = copy.deepcopy(data_numerator_mcsub_c1.ProjectionY())
		FR_data_py_mcsub_l1 = copy.deepcopy(data_numerator_mcsub_l1.ProjectionY())
		FR_data_py_mcsub_u1 = copy.deepcopy(data_numerator_mcsub_u1.ProjectionY())
		FR_data_py_mcsub_c2 = copy.deepcopy(data_numerator_mcsub_c2.ProjectionY())

		FR_data_py_mcsub   .Divide(FR_data_py_mcsub   , data_denominator_mcsub   .ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_c1.Divide(FR_data_py_mcsub_c1, data_denominator_mcsub_c1.ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_l1.Divide(FR_data_py_mcsub_l1, data_denominator_mcsub_l1.ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_u1.Divide(FR_data_py_mcsub_u1, data_denominator_mcsub_u1.ProjectionY(), 1, 1, '')
		FR_data_py_mcsub_c2.Divide(FR_data_py_mcsub_c2, data_denominator_mcsub_c2.ProjectionY(), 1, 1, '')

		FR_data_py    = copy.deepcopy(FR_data_copy  .ProjectionY())	
		FR_mc_py      = copy.deepcopy(FR_mc_copy    .ProjectionY())
		FR_mcsub_py   = copy.deepcopy(FR_mcsub_copy .ProjectionY())

		FR_data_py   .Divide(FR_data_py   , copy.deepcopy(data_denominator   .GetStack().Last().ProjectionY()), 1, 1, 'B')
		FR_mc_py     .Divide(FR_mc_py     , copy.deepcopy(mc_denominator     .GetStack().Last().ProjectionY()), 1, 1, 'B')
		FR_mcsub_py  .Divide(FR_mcsub_py  , copy.deepcopy(mcsub_denominator  .GetStack().Last().ProjectionY()), 1, 1, 'B')

		for j in range(len(mcsetsplot)):
			FR_mcplot_py[j] = copy.deepcopy(FR_mcplot_copy[j].ProjectionY())
			FR_mcplot_py[j].Divide(FR_mcplot_py[j], copy.deepcopy(mcplot_denominator[j].ProjectionY()), 1, 1, 'B')

		# plot X projection
		histstoplot = []
		histstoplot.append([FR_data_px, 'data'])
		histstoplot.append([FR_mc_px, 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data')

		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				histstoplot = []
				histstoplot.append([FR_data_px, 'data'])
				histstoplot.append([FR_mcplot_px[j], mcsetsplot[j].GetName()])
				make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-' + mcsetsplot[j].GetName().lstrip(dataType + '_'))
			
		if len(mcsubtract)>0:
			histstoplot = []
			histstoplot.append([FR_data_px_mcsub, 'datamcsub'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_px, 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew')

		if mcsubtractscales:
			histstoplot = []
			histstoplot.append([FR_data_px, 'data'])
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew_data-eth', True, 'Data/ETH')

			histstoplot = []
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_px_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			histstoplot = []
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_px, 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[0]], 'FR_proj_Pt_data-ew_data-eth-qcd', True, 'ETH/QCD')


		# plot Y projection
		histstoplot = []
		histstoplot.append([FR_data_py, 'data'])
		histstoplot.append([FR_mc_py, 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data')

		if len(mcsetsplot)>0:
			for j in range(len(mcsetsplot)):
				histstoplot = []
				histstoplot.append([FR_data_py, 'data'])
				histstoplot.append([FR_mcplot_py[j], mcsetsplot[j].GetName()])
				make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Pt_data-' + mcsetsplot[j].GetName().lstrip(dataType + '_'))
			
		if len(mcsubtract)>0:
			histstoplot = []
			histstoplot.append([FR_data_py, 'data'])
			histstoplot.append([FR_data_py_mcsub, 'datamcsub'])
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_py, 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew')

		if mcsubtractscales:
			histstoplot = []
			histstoplot.append([FR_data_py, 'data'])
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew_data-eth', True, 'Data/ETH')

			histstoplot = []
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_py_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			histstoplot = []
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])	
			if len(mcsubtractplot)>0:
				histstoplot.append([FR_mcsub_py, 'mu_qcdmuenr'])
			histstoplot.append([FR_data_py, 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, datasets[0].hists[title_indeces[1]], 'FR_proj_Eta_data-ew_data-eth-qcd', True, 'ETH/QCD')



	return True





def Plot2dFRMapClosureTest(dataType, outputDir, module, datasets, mcsets, mcsetsplot = [], mcsubtract = [], mcsubtractplot = []):
	# attention: when calling this function with substraction of certain MC (e.g. electroweak)
	#            you need to make sure that the monte carlo you want to substract already has
	#            been given in mcsets as well



	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0

	# this part needs adjustment
	scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(datasets, mcsubtractplot, mcsubtract)
	central1 = scfirst[0][1]
	lower    = scfirst[1][1]
	upper    = scfirst[2][1]
	scsecond = fit.getMCScaleFactorMutually(mcsubtract, 'h_Tight_MTMET30', datasets, mcsubtractplot, 60, 100)
	central2 = scsecond[0]

	#print "------**------"
	#print "qcd       = " + str(scfirst[0][0])
	#print "central 1 = " + str(central1)
	#print "lower   1 = " + str(lower)
	#print "upper   1 = " + str(upper)
	#print "central 2 = " + str(central2)
	#print "------++------"


	if len(mcsubtract)>0:
		for mc in mcsubtract:
			if not mc in mcsets:
				print "ERROR in calling Plot2dFRMapClosureTest"
				print "Every MC that shall be substracted from data must also be given in the BG"
				return False

	canv = helper.makeCanvas(900, 675, 'c2dFR')
	index_numerator    = 0
	index_denominator  = 0
	FR_ttbar           = [{} for i in range(4)]
	FR_qcd             = [{} for i in range(4)]
	ttbar_numerator    = [ROOT.THStack() for i in range(4)]
	qcd_numerator      = [ROOT.THStack() for i in range(4)]
	ttbar_denominator  = [ROOT.THStack() for i in range(4)]
	qcd_denominator    = [ROOT.THStack() for i in range(4)]
	title_indeces      = [0, 0]


	for hist in datasets[0].hists:

		i = datasets[0].hists.index(hist)

		if hist.GetName() == 'h_Loose_LepEta':
			title_indeces[1] = i
		if hist.GetName() == 'h_Loose_LepPt':
			title_indeces[0] = i

			
		# Get Numerator Plots
		if hist.GetName()[-8:] == 'h_FTight':

			index_numerator = i

			data_numerator   = ROOT.THStack()
			mc_numerator     = ROOT.THStack()
			mcsub_numerator  = ROOT.THStack()

			for data in datasets:     data_numerator .Add(copy.deepcopy(data.hists[index_numerator]))
			for mc in mcsets:         mc_numerator   .Add(copy.deepcopy(mc  .hists[index_numerator]))
			for mc in mcsubtractplot: mcsub_numerator.Add(copy.deepcopy(mc  .hists[index_numerator]))
			
			for mc in mcsetsplot:
				label = ''.join([j for j in mc.GetName() if not j.isdigit()])
				index = int(mc.GetName()[-1])

				if 'qcd'   in label: qcd_numerator  [index].Add(copy.deepcopy(mc.hists[index_numerator]))
				if 'ttbar' in label: ttbar_numerator[index].Add(copy.deepcopy(mc.hists[index_numerator]))


		# Get Denominator Histograms
		if hist.GetName()[-8:] == 'h_FLoose':

			index_denominator = i

			data_denominator   = ROOT.THStack()
			mc_denominator     = ROOT.THStack()
			mcsub_denominator  = ROOT.THStack()

			for data in datasets:     data_denominator .Add(copy.deepcopy(data.hists[index_denominator]))
			for mc in mcsets:         mc_denominator   .Add(copy.deepcopy(mc  .hists[index_denominator]))
			for mc in mcsubtractplot: mcsub_denominator.Add(copy.deepcopy(mc  .hists[index_denominator]))
			
			for mc in mcsetsplot:
				label = ''.join([j for j in mc.GetName() if not j.isdigit()])
				index = int(mc.GetName()[-1])

				if 'qcd'   in label: qcd_denominator  [index].Add(copy.deepcopy(mc.hists[index_denominator]))
				if 'ttbar' in label: ttbar_denominator[index].Add(copy.deepcopy(mc.hists[index_denominator]))



	FR_data          = copy.deepcopy(data_numerator .GetStack().Last())
	FR_mc            = copy.deepcopy(mc_numerator   .GetStack().Last())
	FR_mcsub         = copy.deepcopy(mcsub_numerator.GetStack().Last())
	FR_data_mcsub_c1 = copy.deepcopy(FR_data)

	for j in range(4):
		FR_ttbar[j] = copy.deepcopy(ttbar_numerator[j].GetStack().Last())
		FR_qcd  [j] = copy.deepcopy(qcd_numerator  [j].GetStack().Last())

	data_denominator_mcsub_c1 = copy.deepcopy(data_denominator.GetStack().Last())


	# create 2d PLOT

	if len(mcsubtract)>0: 
		for mc in mcsets:
			if mc in mcsubtract:
				mc.hists[index_numerator].Scale(central1)
				FR_data_mcsub_c1.Add(mc.hists[index_numerator], -1)
				mc.hists[index_numerator].Scale(1.0/central1)

				mc.hists[index_denominator].Scale(central1)
				data_denominator_mcsub_c1.Add(mc.hists[index_denominator],-1)
				mc.hists[index_denominator].Scale(1.0/central1)

	
	FR_data         .Divide(FR_data         , copy.deepcopy(data_denominator .GetStack().Last()), 1, 1, 'B')
	FR_mc           .Divide(FR_mc           , copy.deepcopy(mc_denominator   .GetStack().Last()), 1, 1, 'B')
	FR_mcsub        .Divide(FR_mcsub        , copy.deepcopy(mcsub_denominator.GetStack().Last()), 1, 1, 'B')
	FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1                         , 1, 1, '' )

	for j in range(4):
		FR_ttbar[j].Divide(FR_ttbar[j], copy.deepcopy(ttbar_denominator[j].GetStack().Last()), 1, 1, 'B')
		FR_qcd  [j].Divide(FR_qcd  [j], copy.deepcopy(qcd_denominator  [j].GetStack().Last()), 1, 1, 'B')


	# plot 2d maps
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data         , title_indeces, 'data'              , True, 'fakerates_2dct/')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mc           , title_indeces, 'mc'                , True, 'fakerates_2dct/')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_mcsub        , title_indeces, 'qcd'               , True, 'fakerates_2dct/')
	make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_data_mcsub_c1, title_indeces, 'datamcsub_central1', True, 'fakerates_2dct/')

	for j in range(4):
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_ttbar[j], title_indeces, dataType + '_ttbar' + str(j), True, 'fakerates_2dct/')
		make2dFRPlot(dataType, canv, outputDir, datasets[0], FR_qcd[j]  , title_indeces, dataType + '_qcd' + str(j)  , True, 'fakerates_2dct/')









