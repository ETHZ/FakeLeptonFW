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



def make2dFRPlot(dataType, canv, outputDir, dataset, hist, title_indeces, name=''):

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
	hist.SetTitle("FR 2d Map (" + name + ")")
	helper.saveCanvas(canv, pad_plot, outputDir + "fakerates_2d/", "FR_2dmap_" + name.lower().replace(" ", "_"), 0)
	pad_plot.Close()



def PlotFR(dataType, outputDir, dataset, mcsets, histlist, mcsetsplot = [], mcsubstract = [], mcsubstractscales = False):

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
	if mcsubstractscales:
		scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(dataset, mcsetsplot, mcsubstract, 50, 120, 'h_Tight_MTMET30')
		qcd2     = scfirst[0][0]
		central12= scfirst[0][1]
		lower2   = scfirst[1][1]
		upper2   = scfirst[2][1]
		scfirst  = fit.getMCScaleFactorSimultaneouslyWithErrors(dataset, mcsetsplot, mcsubstract)
		central1 = scfirst[0][1]
		lower    = scfirst[1][1]
		upper    = scfirst[2][1]
		scsecond = fit.getMCScaleFactorMutually(mcsubstract, 'h_Tight_MTMET30', [dataset], mcsetsplot, 60, 100)
		central2 = scsecond[0]
		scsecond = fit.getMCScaleFactorMutually(mcsubstract, 'h_Tight_MTMET20', [dataset], mcsetsplot, 60, 100)
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
	index_numerators = []
	index_denominators = []
	data_numerators = []
	data_denominators = []
	mc_numerators = []
	mc_denominators = []
	mcplot_numerators = []
	mcplot_denominators = []

	for hist in dataset.hists:

		i = dataset.hists.index(hist)

		if not hist.GetName() in histlist: continue
		if hist.GetName()[-9:] == "NVertices": continue # we take "NVertices1" histograms for Fakerate Plots
			
		# Get Numerator Plots
		if 'h_Tight_' in hist.GetName():
			index_numerators.append(i)
			data_numerators.append(copy.deepcopy(hist))
			mc_numerators.append(ROOT.THStack())
			mcplot_numerators.append([{} for j in range(len(mcsetsplot))])
			m += 1
			for mc in mcsets:
				mc_numerators[m].Add(copy.deepcopy(mc.hists[i]))
			for j, mc in enumerate(mcsetsplot):
				mcplot_numerators[m][j] = copy.deepcopy(mc.hists[i])

		# Get Denominator Histograms
		if 'h_Loose_' in hist.GetName():
			index_denominators.append(i)
			data_denominators.append(copy.deepcopy(hist))
			mc_denominators.append(ROOT.THStack())
			mcplot_denominators.append([{} for j in range(len(mcsetsplot))])
			n += 1
			for mc in mcsets:
				mc_denominators[n].Add(copy.deepcopy(mc.hists[i]))
			for mc in mcsetsplot:
				mcplot_denominators[n][j] = copy.deepcopy(mc.hists[i])


	FR_bg = []
	FR_mc = []

	for i, FR_data in enumerate(data_numerators):

		FR_data_mcsub    = copy.deepcopy(FR_data)
		FR_data_mcsub_c1 = copy.deepcopy(FR_data)
		FR_data_mcsub_l1 = copy.deepcopy(FR_data)
		FR_data_mcsub_u1 = copy.deepcopy(FR_data)
		FR_data_mcsub_c2 = copy.deepcopy(FR_data)
		data_numerator_mcsub    = copy.deepcopy(FR_data_mcsub)
		data_numerator_mcsub_c1 = copy.deepcopy(FR_data_mcsub_c1)
		data_numerator_mcsub_l1 = copy.deepcopy(FR_data_mcsub_l1)
		data_numerator_mcsub_u1 = copy.deepcopy(FR_data_mcsub_u1)
		data_numerator_mcsub_c2 = copy.deepcopy(FR_data_mcsub_c2)
		data_denominator_mcsub    = copy.deepcopy(data_denominators[i])
		data_denominator_mcsub_c1 = copy.deepcopy(data_denominators[i])
		data_denominator_mcsub_l1 = copy.deepcopy(data_denominators[i])
		data_denominator_mcsub_u1 = copy.deepcopy(data_denominators[i])
		data_denominator_mcsub_c2 = copy.deepcopy(data_denominators[i])

		if len(mcsubstract)>0:
			for mc in mcsets:
				if mc in mcsubstract:
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

		#FR_data_mcsub   .Divide(data_denominator_mcsub   )
		#FR_data_mcsub_c1.Divide(data_denominator_mcsub_c1)
		#FR_data_mcsub_l1.Divide(data_denominator_mcsub_l1)
		#FR_data_mcsub_u1.Divide(data_denominator_mcsub_u1)
		#FR_data_mcsub_c2.Divide(data_denominator_mcsub_c2)
		#
		#FR_data_mcsub    = helper.doTH1ErrorPropagation(FR_data_mcsub   , data_numerator_mcsub   , data_denominator_mcsub   , 4)
		#FR_data_mcsub_c1 = helper.doTH1ErrorPropagation(FR_data_mcsub_c1, data_numerator_mcsub_c1, data_denominator_mcsub_c1, 4)
		#FR_data_mcsub_l1 = helper.doTH1ErrorPropagation(FR_data_mcsub_l1, data_numerator_mcsub_l1, data_denominator_mcsub_l1, 4)
		#FR_data_mcsub_u1 = helper.doTH1ErrorPropagation(FR_data_mcsub_u1, data_numerator_mcsub_u1, data_denominator_mcsub_u1, 4)
		#FR_data_mcsub_c2 = helper.doTH1ErrorPropagation(FR_data_mcsub_c2, data_numerator_mcsub_c2, data_denominator_mcsub_c2, 4)

		FR_data.Divide(FR_data, data_denominators[i], 1, 1, 'B')
		FR_bg.append(copy.deepcopy(mc_numerators[i].GetStack().Last()))
		FR_bg[i].Divide(FR_bg[i], copy.deepcopy(mc_denominators[i].GetStack().Last()), 1, 1, 'B')
		FR_mc.append([{} for j in range(len(mcsetsplot))])
		for j in range(len(mcsetsplot)): 
			FR_mc[i][j] = mcplot_numerators[i][j]
			FR_mc[i][j].Divide(FR_mc[i][j], mcplot_denominators[i][j], 1, 1, 'B')
		

		# this part needs adjustment
		histstoplot = []
		histstoplot.append([FR_data, 'data'])
		histstoplot.append([FR_bg[i], 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FR_data, 'FR_' + FR_data.GetName().lstrip('h_Tight_') + '_data')

		if len(mcsubstract)>0:
			histstoplot = []
			histstoplot.append([FR_data_mcsub, 'datamcsub'])
			for j in range(len(mcsetsplot)): histstoplot.append([FR_mc[i][j], 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FR_data, 'FR_' + FR_data.GetName().lstrip('h_Tight_') + '_data-ew')

		if len(mcsubstract)>0 and mcsubstractscales:
			histstoplot = []
			histstoplot.append([FR_data, 'data'])
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FR_data, 'FR_' + FR_data.GetName().lstrip('h_Tight_') + '_data-ew_data-eth', True, 'Data/ETH')

			histstoplot = []
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FR_data, 'FR_' + FR_data.GetName().lstrip('h_Tight_') + '_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			histstoplot = []
			histstoplot.append([FR_data_mcsub_c1, 'datamcsub_central1'])
			for j in range(len(mcsetsplot)): histstoplot.append([FR_mc[i][j], 'mu_qcdmuenr'])
			histstoplot.append([FR_data, 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, FR_data, 'FR_' + FR_data.GetName().lstrip('h_Tight_') + '_data-ew_data-eth-qcd', True, 'ETH/QCD')

			

	return True






def Plot2dFRMap(dataType, outputDir, module, dataset, mcsets, mcsetsplot = [], mcsubstract = [], doProjection = False, mcsubstractscales = False):
	# attention: when calling this function with substraction of certain MC (e.g. electroweak)
	#            you need to make sure that the monte carlo you want to substract already has
	#            been given in mcsets as well


	central1 = 1.0
	lower    = 1.0
	upper    = 1.0
	central2 = 1.0

	# this part needs adjustment
	if mcsubstractscales:
		scfirst = fit.getMCScaleFactorSimultaneouslyWithErrors(dataset, mcsetsplot, mcsubstract)
		central1 = scfirst[0][1]
		lower    = scfirst[1][1]
		upper    = scfirst[2][1]
		scsecond = fit.getMCScaleFactorMutually(mcsubstract, 'h_Tight_MTMET30', [dataset], mcsetsplot, 60, 100)
		central2 = scsecond[0]

	#print "------**------"
	#print "qcd       = " + str(scfirst[0][0])
	#print "central 1 = " + str(central1)
	#print "lower   1 = " + str(lower)
	#print "upper   1 = " + str(upper)
	#print "central 2 = " + str(central2)
	#print "------++------"


	if len(mcsubstract)>0:
		for mc in mcsubstract:
			if not mc in mcsets:
				print "ERROR in calling Plot2dFRMap"
				print "Every MC that shall be substracted from data must also be given in the BG"
				return False

	canv = helper.makeCanvas(900, 675, 'c2dFR')
	index_numerator = 0
	index_denominator = 0
	mcplot_numerator = [{} for j in range(len(mcsetsplot))]
	mcplot_denominator = [{} for j in range(len(mcsetsplot))]
	title_indeces = [0, 0]

	for hist in dataset.hists:

		i = dataset.hists.index(hist)

		if hist.GetName() == 'h_Loose_LepEta':
			title_indeces[1] = i
		if hist.GetName() == 'h_Loose_LepPt':
			title_indeces[0] = i
			
		# Get Numerator Plots
		if 'h_FTight' in hist.GetName():
			index_numerator = i
			data_numerator = copy.deepcopy(hist)
			mc_numerator = ROOT.THStack()
			for mc in mcsets:
				mc_numerator.Add(copy.deepcopy(mc.hists[index_numerator]))
			for j, mc in enumerate(mcsetsplot):
				mcplot_numerator[j] = copy.deepcopy(mc.hists[index_numerator])

		# Get Denominator Histograms
		if 'h_FLoose' in hist.GetName():
			index_denominator = i
			data_denominator = copy.deepcopy(hist)
			mc_denominator = ROOT.THStack()
			for mc in mcsets:
				mc_denominator.Add(copy.deepcopy(mc.hists[index_denominator]))
			for j,mc in enumerate(mcsetsplot):
				mcplot_denominator[j] = copy.deepcopy(mc.hists[index_denominator])

	FR_data      = data_numerator
	FR_data_copy = copy.deepcopy(FR_data)
	FR_data_mcsub    = copy.deepcopy(FR_data)
	FR_data_mcsub_c1 = copy.deepcopy(FR_data)
	FR_data_mcsub_l1 = copy.deepcopy(FR_data)
	FR_data_mcsub_u1 = copy.deepcopy(FR_data)
	FR_data_mcsub_c2 = copy.deepcopy(FR_data)
	data_denominator_mcsub    = copy.deepcopy(data_denominator)
	data_denominator_mcsub_c1 = copy.deepcopy(data_denominator)
	data_denominator_mcsub_l1 = copy.deepcopy(data_denominator)
	data_denominator_mcsub_u1 = copy.deepcopy(data_denominator)
	data_denominator_mcsub_c2 = copy.deepcopy(data_denominator)

	FR_mc = [{} for j in range(len(mcsetsplot))]
	FR_mc_copy = [{} for j in range(len(mcsetsplot))]
	FR_mc_px = [{} for j in range(len(mcsetsplot))]
	FR_mc_py = [{} for j in range(len(mcsetsplot))]



	# create 2d PLOT

	if len(mcsubstract)>0: 
		for mc in mcsets:
			if mc in mcsubstract:
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

	FR_data_mcsub   .Divide(FR_data_mcsub   , data_denominator_mcsub   , 1, 1, '')
	FR_data_mcsub_c1.Divide(FR_data_mcsub_c1, data_denominator_mcsub_c1, 1, 1, '')
	FR_data_mcsub_l1.Divide(FR_data_mcsub_l1, data_denominator_mcsub_l1, 1, 1, '')
	FR_data_mcsub_u1.Divide(FR_data_mcsub_u1, data_denominator_mcsub_u1, 1, 1, '')
	FR_data_mcsub_c2.Divide(FR_data_mcsub_c2, data_denominator_mcsub_c2, 1, 1, '')

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
	
	FR_data.Divide(FR_data, data_denominator, 1, 1, 'B')
	FR_bg = copy.deepcopy(mc_numerator.GetStack().Last())
	FR_bg_copy = copy.deepcopy(FR_bg)
	FR_bg.Divide(FR_bg, copy.deepcopy(mc_denominator.GetStack().Last()), 1, 1, 'B')
	for j in range(len(mcsetsplot)): 
		FR_mc[j] = mcplot_numerator[j]
		FR_mc_copy[j] = copy.deepcopy(FR_mc[j])
		FR_mc[j].Divide(FR_mc[j], mcplot_denominator[j], 1, 1, 'B')

	make2dFRPlot(dataType, canv, outputDir, dataset, FR_data, title_indeces, 'data')
	if len(mcsubstract)>0: make2dFRPlot(dataType, canv, outputDir, dataset, FR_data_mcsub, title_indeces, 'data-EW')
	if mcsubstractscales:
		make2dFRPlot(dataType, canv, outputDir, dataset, FR_data_mcsub_c1, title_indeces, 'data-EW central1')
		make2dFRPlot(dataType, canv, outputDir, dataset, FR_data_mcsub_l1, title_indeces, 'data-EW lower1')
		make2dFRPlot(dataType, canv, outputDir, dataset, FR_data_mcsub_u1, title_indeces, 'data-EW upper1')
		make2dFRPlot(dataType, canv, outputDir, dataset, FR_data_mcsub_c2, title_indeces, 'data-EW central2')

	make2dFRPlot(dataType, canv, outputDir, dataset, FR_bg, title_indeces, 'MC')
	for j in range(len(mcsetsplot)): make2dFRPlot(dataType, canv, outputDir, dataset, FR_mc[j], title_indeces, 'qcd')



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
		
		#FR_data_px_mcsub   .Divide(copy.deepcopy(data_denominator_mcsub   .ProjectionX()))
		#FR_data_px_mcsub_c1.Divide(copy.deepcopy(data_denominator_mcsub_c1.ProjectionX()))
		#FR_data_px_mcsub_l1.Divide(copy.deepcopy(data_denominator_mcsub_l1.ProjectionX()))
		#FR_data_px_mcsub_u1.Divide(copy.deepcopy(data_denominator_mcsub_u1.ProjectionX()))
		#FR_data_px_mcsub_c2.Divide(copy.deepcopy(data_denominator_mcsub_c2.ProjectionX()))

		#FR_data_px_mcsub    = helper.doTH1ErrorPropagation(FR_data_px_mcsub   , data_numerator_mcsub   .ProjectionX(), data_denominator_mcsub   .ProjectionX(), 4)
		#FR_data_px_mcsub_c1 = helper.doTH1ErrorPropagation(FR_data_px_mcsub_c1, data_numerator_mcsub_c1.ProjectionX(), data_denominator_mcsub_c1.ProjectionX(), 4)
		#FR_data_px_mcsub_l1 = helper.doTH1ErrorPropagation(FR_data_px_mcsub_l1, data_numerator_mcsub_l1.ProjectionX(), data_denominator_mcsub_l1.ProjectionX(), 4)
		#FR_data_px_mcsub_u1 = helper.doTH1ErrorPropagation(FR_data_px_mcsub_u1, data_numerator_mcsub_u1.ProjectionX(), data_denominator_mcsub_u1.ProjectionX(), 4)
		#FR_data_px_mcsub_c2 = helper.doTH1ErrorPropagation(FR_data_px_mcsub_c2, data_numerator_mcsub_c2.ProjectionX(), data_denominator_mcsub_c2.ProjectionX(), 4)

		FR_data_px = copy.deepcopy(FR_data_copy.ProjectionX())
		FR_data_px.Divide(FR_data_px, copy.deepcopy(data_denominator.ProjectionX()), 1, 1, 'B')
		FR_bg_px = copy.deepcopy(FR_bg_copy.ProjectionX())
		FR_bg_px.Divide(FR_bg_px, copy.deepcopy(mc_denominator.GetStack().Last().ProjectionX()), 1, 1, 'B')
		for j in range(len(mcsetsplot)): 
			FR_mc_px[j] = copy.deepcopy(FR_mc_copy[j].ProjectionX())
			FR_mc_px[j].Divide(FR_mc_px[j], copy.deepcopy(mcplot_denominator[j].ProjectionX()), 1, 1, 'B')

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

		#FR_data_py_mcsub   .Divide(copy.deepcopy(data_denominator_mcsub   .ProjectionY()))
		#FR_data_py_mcsub_c1.Divide(copy.deepcopy(data_denominator_mcsub_c1.ProjectionY()))
		#FR_data_py_mcsub_l1.Divide(copy.deepcopy(data_denominator_mcsub_l1.ProjectionY()))
		#FR_data_py_mcsub_u1.Divide(copy.deepcopy(data_denominator_mcsub_u1.ProjectionY()))
		#FR_data_py_mcsub_c2.Divide(copy.deepcopy(data_denominator_mcsub_c2.ProjectionY()))

		#FR_data_py_mcsub    = helper.doTH1ErrorPropagation(FR_data_py_mcsub   , data_numerator_mcsub   .ProjectionY(), data_denominator_mcsub   .ProjectionY(), 4)
		#FR_data_py_mcsub_c1 = helper.doTH1ErrorPropagation(FR_data_py_mcsub_c1, data_numerator_mcsub_c1.ProjectionY(), data_denominator_mcsub_c1.ProjectionY(), 4)
		#FR_data_py_mcsub_l1 = helper.doTH1ErrorPropagation(FR_data_py_mcsub_l1, data_numerator_mcsub_l1.ProjectionY(), data_denominator_mcsub_l1.ProjectionY(), 4)
		#FR_data_py_mcsub_u1 = helper.doTH1ErrorPropagation(FR_data_py_mcsub_u1, data_numerator_mcsub_u1.ProjectionY(), data_denominator_mcsub_u1.ProjectionY(), 4)
		#FR_data_py_mcsub_c2 = helper.doTH1ErrorPropagation(FR_data_py_mcsub_c2, data_numerator_mcsub_c2.ProjectionY(), data_denominator_mcsub_c2.ProjectionY(), 4)

		FR_data_py = copy.deepcopy(FR_data_copy.ProjectionY())
		FR_data_py.Divide(FR_data_py, copy.deepcopy(data_denominator.ProjectionY()), 1, 1, 'B')
		FR_bg_py = copy.deepcopy(FR_bg_copy.ProjectionY())
		FR_bg_py.Divide(FR_bg_py, copy.deepcopy(mc_denominator.GetStack().Last().ProjectionY()), 1, 1, 'B')
		for j in range(len(mcsetsplot)): 
			FR_mc_py[j] = copy.deepcopy(FR_mc_copy[j].ProjectionY())
			FR_mc_py[j].Divide(FR_mc_py[j], copy.deepcopy(mcplot_denominator[j].ProjectionY()), 1, 1, 'B')


		# this part needs adjustment!
		histstoplot = []
		histstoplot.append([FR_data_px, 'data'])
		histstoplot.append([FR_bg_px, 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[0]], 'FR_proj_Pt_data')

		if len(mcsubstract)>0:
			histstoplot = []
			histstoplot.append([FR_data_px_mcsub, 'datamcsub'])
			for j in range(len(mcsetsplot)): histstoplot.append([FR_mc_px[j], 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[0]], 'FR_proj_Pt_data-ew')

		if mcsubstractscales:
			histstoplot = []
			histstoplot.append([FR_data_px, 'data'])
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[0]], 'FR_proj_Pt_data-ew_data-eth', True, 'Data/ETH')

			#print "---------"
			#print "data-ETH:"
			#for k in range(1,FR_data_px.GetXaxis().GetNbins()+1):
			#	print str(FR_data_px.GetBinContent(k)) + "-" + str(FR_data_px_mcsub_c1.GetBinContent(k))

			histstoplot = []
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_px_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[0]], 'FR_proj_Pt_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			#print "---------"
			#print "ETH-UCSx:"
			#for k in range(1,FR_data_px.GetXaxis().GetNbins()+1):
			#	print str(FR_data_px_mcsub_c1.GetBinContent(k)) + "-" + str(FR_data_px_mcsub_c2.GetBinContent(k))

			histstoplot = []
			histstoplot.append([FR_data_px_mcsub_c1, 'datamcsub_central1'])
			for j in range(len(mcsetsplot)): histstoplot.append([FR_mc_px[j], 'mu_qcdmuenr'])
			histstoplot.append([FR_data_px, 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[0]], 'FR_proj_Pt_data-ew_data-eth-qcd', True, 'ETH/QCD')

			#print "---------"
			#print "ETH-QCD:"
			#for k in range(1,FR_data_px.GetXaxis().GetNbins()+1):
			#	print str(FR_data_px_mcsub_c1.GetBinContent(k)) + "-" + str(FR_mc_px[0].GetBinContent(k))



		histstoplot = []
		histstoplot.append([FR_data_py, 'data'])
		histstoplot.append([FR_bg_py, 'totbg'])
		make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[1]], 'FR_proj_Eta_data')

		if len(mcsubstract)>0:
			histstoplot = []
			histstoplot.append([FR_data_py, 'data'])
			histstoplot.append([FR_data_py_mcsub, 'datamcsub'])
			for j in range(len(mcsetsplot)): histstoplot.append([FR_mc_py[j], 'mu_qcdmuenr'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[1]], 'FR_proj_Eta_data-ew')

		if mcsubstractscales:
			histstoplot = []
			histstoplot.append([FR_data_py, 'data'])
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[1]], 'FR_proj_Eta_data-ew_data-eth', True, 'Data/ETH')

			histstoplot = []
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			histstoplot.append([FR_data_py_mcsub_c2, 'datamcsub_central2'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[1]], 'FR_proj_Eta_data-ew_eth-ucsx', True, 'ETH/UCSx', 1.01, 0.99)

			histstoplot = []
			histstoplot.append([FR_data_py_mcsub_c1, 'datamcsub_central1'])
			for j in range(len(mcsetsplot)): histstoplot.append([FR_mc_py[j], 'mu_qcdmuenr'])
			histstoplot.append([FR_data_py, 'data'])
			make1dFRPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[1]], 'FR_proj_Eta_data-ew_data-eth-qcd', True, 'ETH/QCD')



	return True









