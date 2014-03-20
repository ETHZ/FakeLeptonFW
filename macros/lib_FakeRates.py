## lib_FakeRates.py

import ROOT, copy
import lib as helper


def make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, hists, title_hist, file_name):
	# calling this function make sure that
	# (1) the first histogram in hists is the total data, and the second is the total bg
	# this function wants to be improved
	# (2) we use color of wjets for total bg
	# (3) we use the same color of qcd for all single mc plots

	# create PLOT

	pad_plot.cd()

	for i in range(len(hists)):
		hists[i][0] = helper.setFRPlotStyle(hists[i][0], helper.getColor(hists[i][1]))
		if i+1 == len(hists): 
			hists[i][0] = helper.setFRPlotStyle(hists[i][0], helper.getColor(hists[i][1]), 'FR as function of ' + helper.getXTitle(title_hist), title_hist)

	hists[0][0].Draw("p x0 e")
	hists[0][0].SetMarkerSize(1.4)
	hists[0][0].SetMinimum(0.0001)
	hists[0][0].SetMaximum(0.4) #1.5*hists[0][0].GetMaximum())
	for i in range(1,len(hists)):
		hists[i][0].SetMinimum(0.0001)
		hists[i][0].SetMaximum(0.4)
		hists[i][0].SetMarkerSize(0)
		hists[i][0].Draw("E2 same")
	hists[0][0].Draw("p x0 e same")

	leg1 = helper.makeLegend(0.15, 0.6, 0.4, 0.85)
	leg1.AddEntry(hists[0][0], helper.getLegendName(hists[0][1]), 'pe')
	for i in range(1,len(hists)):
		leg1.AddEntry(hists[i][0], helper.getLegendName(hists[i][1]), 'f')
	leg1.Draw()


	# create RATIO PLOT

	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(hists[0][0])
	data_bg_ratio.Divide(hists[1][0])
	data_bg_ratio.Draw("p e")
	data_bg_ratio = helper.setRatioStyle(data_bg_ratio, title_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()
	
	helper.saveCanvas(canv, pad_plot, outputDir, file_name)



def make2dFRPlot(canv, outputDir, dataset, hist, title_indeces, name=''):

	pad_plot = helper.makePad('tot')
	pad_plot.cd()
	pad_plot.SetTicks(1,1)
	hist.Draw("text colz e")
	hist.SetMarkerColor(ROOT.kBlack)
	hist.SetMarkerSize(1.8)
	hist.GetXaxis().SetTitle(helper.getXTitle(dataset.hists[title_indeces[0]]))
	hist.GetYaxis().SetTitle(helper.getXTitle(dataset.hists[title_indeces[1]]))
	hist.GetXaxis().SetTitleSize(0.07)
	hist.GetXaxis().SetLabelSize(0.07)
	hist.GetYaxis().SetTitleSize(0.07)
	hist.GetYaxis().SetLabelSize(0.07)
	hist.SetMinimum(0.0)
	hist.SetMaximum(0.25)
	hist.SetTitle("FR 2d Map (" + name + ")")
	helper.saveCanvas(canv, pad_plot, outputDir, "muFR_2dmap_" + name.lower(), 0)
	pad_plot.Close()



def PlotFR(outputDir, dataset, mcsets, histlist, mcsetsplot = [], mcsubstract = []):

	canv = helper.makeCanvas(900, 675, 'c1dFR', 0)
	canv.SetTopMargin(0.07)
	canv.SetLeftMargin(0.25)
	canv.SetRightMargin(0.0)
	canv.SetBottomMargin(0.2)
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

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

		FR_data_mcsub = copy.deepcopy(FR_data)
		data_denominator_mcsub = copy.deepcopy(data_denominators[i])
		if len(mcsubstract)>0:
			for mc in mcsets:
				if mc in mcsubstract:
					FR_data_mcsub.Add(mc.hists[index_numerators[i]], -1)
					data_denominator_mcsub.Add(mc.hists[index_denominators[i]],-1)

		FR_data.Divide(data_denominators[i])
		FR_data_mcsub.Divide(data_denominator_mcsub)
		FR_bg.append(copy.deepcopy(mc_numerators[i].GetStack().Last()))
		FR_bg[i].Divide(copy.deepcopy(mc_denominators[i].GetStack().Last()))
		FR_mc.append([{} for j in range(len(mcsetsplot))])
		for j in range(len(mcsetsplot)): 
			FR_mc[i][j] = mcplot_numerators[i][j]
			FR_mc[i][j].Divide(mcplot_denominators[i][j])
		

		# this part needs adjustment
		histstoplot = []
		histstoplot.append([FR_data, 'data'])
		histstoplot.append([FR_bg[i], 'totbg'])
		#histstoplot.append([FR_data_mcsub, 'datamcsub'])
		#for j in range(len(mcsetsplot)): histstoplot.append([FR_mc[i][j], 'qcdMuEnriched'])
		make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, FR_data, 'muFR_' + FR_data.GetName().lstrip('h_Tight_mu'))

	return True






def Plot2dFRMap(outputDir, dataset, mcsets, mcsetsplot = [], mcsubstract = [], doProjection = False):
	# attention: when calling this function with substraction of certain MC (e.g. electroweak)
	#            you need to make sure that the monte carlo you want to substract already has
	#            been given in mcsets as well

	for mc in mcsubstract:
		if not mc in mcsets:
			print "ERROR in calling Plot2dFRMap"
			print "Every MC that shall be substracted from data must also be given in the BG"
			return False

	canv = helper.makeCanvas(900, 675, 'c2dFR', 0)
	canv.SetTopMargin(0.07)
	canv.SetLeftMargin(0.25)
	canv.SetRightMargin(0.1)
	canv.SetBottomMargin(0.2)
	index_numerator = 0
	index_denominator = 0
	mcplot_numerator = [{} for j in range(len(mcsetsplot))]
	mcplot_denominator = [{} for j in range(len(mcsetsplot))]
	title_indeces = [0, 0]

	for hist in dataset.hists:

		i = dataset.hists.index(hist)

		if hist.GetName() == 'h_Loose_muLepEta':
			title_indeces[1] = i
		if hist.GetName() == 'h_Loose_muLepPt':
			title_indeces[0] = i
			
		# Get Numerator Plots
		if hist.GetName() == 'h_muFTight':
			index_numerator = i
			data_numerator = copy.deepcopy(hist)
			mc_numerator = ROOT.THStack()
			for mc in mcsets:
				mc_numerator.Add(copy.deepcopy(mc.hists[index_numerator]))
			for j, mc in enumerate(mcsetsplot):
				mcplot_numerator[j] = copy.deepcopy(mc.hists[index_numerator])

		# Get Denominator Histograms
		if hist.GetName() == 'h_muFLoose':
			index_denominator = i
			data_denominator = copy.deepcopy(hist)
			mc_denominator = ROOT.THStack()
			for mc in mcsets:
				mc_denominator.Add(copy.deepcopy(mc.hists[index_denominator]))
			for j,mc in enumerate(mcsetsplot):
				mcplot_denominator[j] = copy.deepcopy(mc.hists[index_denominator])

	FR_data = data_numerator
	FR_data_copy = copy.deepcopy(FR_data)
	FR_data_mcsub = copy.deepcopy(FR_data)
	data_denominator_mcsub = copy.deepcopy(data_denominator)

	FR_mc = [{} for j in range(len(mcsetsplot))]
	FR_mc_copy = [{} for j in range(len(mcsetsplot))]
	FR_mc_px = [{} for j in range(len(mcsetsplot))]
	FR_mc_py = [{} for j in range(len(mcsetsplot))]



	# create 2d PLOT

	if len(mcsubstract)>0: 
		for mc in mcsets:
			if mc in mcsubstract:
				FR_data_mcsub.Add(mc.hists[index_numerator], -1)
				data_denominator_mcsub.Add(mc.hists[index_denominator], -1)

	FR_data_mcsub_copy = copy.deepcopy(FR_data_mcsub)
	FR_data.Divide(data_denominator)
	FR_data_mcsub.Divide(data_denominator_mcsub)
	FR_bg = copy.deepcopy(mc_numerator.GetStack().Last())
	FR_bg_copy = copy.deepcopy(FR_bg)
	FR_bg.Divide(copy.deepcopy(mc_denominator.GetStack().Last()))
	for j in range(len(mcsetsplot)): 
		FR_mc[j] = mcplot_numerator[j]
		FR_mc_copy[j] = copy.deepcopy(FR_mc[j])
		FR_mc[j].Divide(mcplot_denominator[j])

	make2dFRPlot(canv, outputDir, dataset, FR_data, title_indeces, 'data')
	if len(mcsubstract)>0: make2dFRPlot(canv, outputDir, dataset, FR_data_mcsub, title_indeces, 'data-EW')
	make2dFRPlot(canv, outputDir, dataset, FR_bg, title_indeces, 'bg')



	# Create Projections

	if doProjection == True:

		canv.SetRightMargin(0.0)
		pad_plot = helper.makePad('plot')
		pad_ratio = helper.makePad('ratio')

		FR_data_px = copy.deepcopy(FR_data_copy.ProjectionX())
		FR_data_px.Divide(copy.deepcopy(data_denominator.ProjectionX()))
		FR_data_px_mcsub = copy.deepcopy(FR_data_mcsub_copy.ProjectionX())
		FR_data_px_mcsub.Divide(copy.deepcopy(data_denominator_mcsub.ProjectionX()))		
		FR_bg_px = copy.deepcopy(FR_bg_copy.ProjectionX())
		FR_bg_px.Divide(copy.deepcopy(mc_denominator.GetStack().Last().ProjectionX()))
		for j in range(len(mcsetsplot)): 
			FR_mc_px[j] = copy.deepcopy(FR_mc_copy[j].ProjectionX())
			FR_mc_px[j].Divide(copy.deepcopy(mcplot_denominator[j].ProjectionX()))

		FR_data_py = copy.deepcopy(FR_data_copy.ProjectionY())
		FR_data_py.Divide(copy.deepcopy(data_denominator.ProjectionY()))
		FR_data_py_mcsub = copy.deepcopy(FR_data_mcsub_copy.ProjectionY())
		FR_data_py_mcsub.Divide(copy.deepcopy(data_denominator_mcsub.ProjectionY()))
		FR_bg_py = copy.deepcopy(FR_bg_copy.ProjectionY())
		FR_bg_py.Divide(copy.deepcopy(mc_denominator.GetStack().Last().ProjectionY()))
		for j in range(len(mcsetsplot)): 
			FR_mc_py[j] = copy.deepcopy(FR_mc_copy[j].ProjectionY())
			FR_mc_py[j].Divide(copy.deepcopy(mcplot_denominator[j].ProjectionY()))


		# this part needs adjustment!
		histstoplot = []
		histstoplot.append([FR_data_px, 'data'])
		histstoplot.append([FR_bg_px, 'totbg'])
		#histstoplot.append([FR_data_px_mcsub, 'datamcsub'])
		#for j in range(len(mcsetsplot)): histstoplot.append([FR_mc_px[j], 'qcdMuEnriched'])
		make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[0]], 'muFR_proj_Pt')

		histstoplot = []
		histstoplot.append([FR_data_py, 'data'])
		histstoplot.append([FR_bg_py, 'totbg'])
		#histstoplot.append([FR_data_py_mcsub, 'datamcsub'])
		#for j in range(len(mcsetsplot)): histstoplot.append([FR_mc_py[j], 'qcdMuEnriched'])
		make1dFRPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, dataset.hists[title_indeces[1]], 'muFR_proj_Eta')

	return True









