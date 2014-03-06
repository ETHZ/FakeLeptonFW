## lib_FakeRates.py

import ROOT, copy
import lib as helper


def make1dFRPlot(canv, pad_plot, pad_ratio, data_hist, mc_hist, mcplot_hists, title_hist, file_name):
	# this function wants to be improved
	# (1) we use color of wjets for total bg
	# (2) we use the same color of qcd for all single mc plots
	# (3) we use a shit legend definition with the names hard-coded

	# create PLOT

	pad_plot.cd()

	data_hist = helper.setFRPlotStyle(data_hist, 'FR as function of ' + helper.getXTitle(title_hist), helper.getColor('data'))
	mc_hist = helper.setFRPlotStyle(mc_hist, '', helper.getColor('totbg'))
	for mc in mcplot_hists: mc = helper.setFRPlotStyle(mc, '', helper.getColor('qcdMuEnriched'))

	data_hist.Draw("p e1")
	mc_hist.Draw("p e1 same")
	for mc in mcplot_hists: mc.Draw("p e1 same")

	leg1 = helper.makeLegend(0.4, 0.5, 0.60, 0.85)
	leg1.AddEntry(data_hist, 'Data', 'pe')
	leg1.AddEntry(mc_hist, 'QCD + EW', 'pe')
	for mc in mcplot_hists: leg1.AddEntry(mc, 'QCD', 'pe')
	leg1.Draw()

	# create RATIO PLOT

	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(data_hist)
	data_bg_ratio.Divide(mc_hist)
	data_bg_ratio.Draw("p e1")
	data_bg_ratio = helper.setRatioStyle(data_bg_ratio, data_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()
	
	helper.saveCanvas(canv, file_name)



def make2dFRPlot(canv, dataset, hist, name=""):

	hist.Draw("text colz e")
	hist.GetXaxis().SetTitle(helper.getXTitle(dataset.hists[12]))
	hist.GetYaxis().SetTitle(helper.getXTitle(dataset.hists[13]))
	hist.SetMinimum(0.0)
	hist.SetMaximum(0.25)
	hist.SetTitle("FR 2d Map (" + name + ")")
	helper.saveCanvas(canv, "muFR_2dmap_" + name)



def PlotFR(dataset, mcsets, mcsetsplot):

	canv = helper.makeCanvas(900, 675)
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	m = -1
	n = -1
	data_numerators = []
	data_denominators = []
	mc_numerators = []
	mc_denominators = []
	mcplot_numerators = []
	mcplot_denominators = []

	for hist in dataset.hists:

		i = dataset.hists.index(hist)
			
		# Get Numerator Plots
		if 'h_Tight_' in hist.GetName():
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

		FR_data.Divide(data_denominators[i])
		FR_bg.append(copy.deepcopy(mc_numerators[i].GetStack().Last()))
		FR_bg[i].Divide(copy.deepcopy(mc_denominators[i].GetStack().Last()))
		FR_mc.append([{} for j in range(len(mcsetsplot))])
		for j in range(len(mcsetsplot)): 
			FR_mc[i][j] = mcplot_numerators[i][j]
			FR_mc[i][j].Divide(mcplot_denominators[i][j])
		
		make1dFRPlot(canv, pad_plot, pad_ratio, FR_data, FR_bg[i], FR_mc[i], FR_data, 'muFR_' + FR_data.GetName().lstrip('h_Tight_mu'))

	return True






def Plot2dFRMap(dataset, mcsets, mcsetsplot, doProjection = False):


	canv = helper.makeCanvas(900, 675)
	l = -1
	n = -1
	data_numerators = []
	data_denominators = []
	mc_numerators = []
	mc_denominators = []
	mcplot_numerators = []
	mcplot_denominators = []

	for hist in dataset.hists:

		i = dataset.hists.index(hist)
			
		# Get Numerator Plots
		if hist.GetName() == 'h_muFTight':
			data_numerators.append(copy.deepcopy(hist))
			mc_numerators.append(ROOT.THStack())
			mcplot_numerators.append([{} for j in range(len(mcsetsplot))])
			l += 1
			for mc in mcsets:
				mc_numerators[l].Add(copy.deepcopy(mc.hists[i]))
			for j, mc in enumerate(mcsetsplot):
				mcplot_numerators[l][j] = copy.deepcopy(mc.hists[i])

		# Get Denominator Histograms
		if hist.GetName() == 'h_muFLoose':
			data_denominators.append(copy.deepcopy(hist))
			mc_denominators.append(ROOT.THStack())
			mcplot_denominators.append([{} for j in range(len(mcsetsplot))])
			n += 1
			for mc in mcsets:
				mc_denominators[n].Add(copy.deepcopy(mc.hists[i]))
			for mc in mcsetsplot:
				mcplot_denominators[n][j] = copy.deepcopy(mc.hists[i])



	FR_bg_copy = []
	FR_bg = []
	FR_bg_px = []
	FR_bg_py = []
	FR_mc = []
	FR_mc_copy = []
	FR_mc_px = []
	FR_mc_py = []

	for i, FR_data in enumerate(data_numerators):


		# create 2d PLOT

		canv = helper.makeCanvas(900, 675)
		canv.SetRightMargin(0.1)
		FR_data_copy = copy.deepcopy(FR_data)
		FR_data.Divide(data_denominators[i])
		FR_bg.append(copy.deepcopy(mc_numerators[i].GetStack().Last()))
		FR_bg_copy.append(copy.deepcopy(FR_bg[i]))
		FR_bg[i].Divide(copy.deepcopy(mc_denominators[i].GetStack().Last()))
		FR_mc.append([{} for j in range(len(mcsetsplot))])
		FR_mc_copy.append([{} for j in range(len(mcsetsplot))])
		for j in range(len(mcsetsplot)): 
			FR_mc[i][j] = mcplot_numerators[i][j]
			FR_mc_copy[i][j] = copy.deepcopy(FR_mc[i][j])
			FR_mc[i][j].Divide(mcplot_denominators[i][j])

		make2dFRPlot(canv, dataset, FR_data, "data")
		make2dFRPlot(canv, dataset, FR_bg[i], "bg")



		# Create Projections

		if doProjection == True:

			canv.SetRightMargin(0.0)
			pad_plot = helper.makePad('plot')
			pad_ratio = helper.makePad('ratio')

			FR_data_px = copy.deepcopy(FR_data_copy.ProjectionX())
			FR_data_px.Divide(copy.deepcopy(data_denominators[i].ProjectionX()))
			FR_bg_px.append(copy.deepcopy(FR_bg_copy[i].ProjectionX()))
			FR_bg_px[i].Divide(copy.deepcopy(mc_denominators[i].GetStack().Last().ProjectionX()))
			FR_mc_px.append([{} for j in range(len(mcsetsplot))])
			for j in range(len(mcsetsplot)): 
				FR_mc_px[i][j] = copy.deepcopy(FR_mc_copy[i][j].ProjectionX())
				FR_mc_px[i][j].Divide(copy.deepcopy(mcplot_denominators[i][j].ProjectionX()))

			FR_data_py = copy.deepcopy(FR_data_copy.ProjectionY())
			FR_data_py.Divide(copy.deepcopy(data_denominators[i].ProjectionY()))
			FR_bg_py.append(copy.deepcopy(FR_bg_copy[i].ProjectionY()))
			FR_bg_py[i].Divide(copy.deepcopy(mc_denominators[i].GetStack().Last().ProjectionY()))
			FR_mc_py.append([{} for j in range(len(mcsetsplot))])
			for j in range(len(mcsetsplot)): 
				FR_mc_py[i][j] = copy.deepcopy(FR_mc_copy[i][j].ProjectionY())
				FR_mc_py[i][j].Divide(copy.deepcopy(mcplot_denominators[i][j].ProjectionY()))


			make1dFRPlot(canv, pad_plot, pad_ratio, FR_data_px, FR_bg_px[i], FR_mc_px[i], dataset.hists[12], 'muFR_proj_Pt')
			make1dFRPlot(canv, pad_plot, pad_ratio, FR_data_py, FR_bg_py[i], FR_mc_py[i], dataset.hists[13], 'muFR_proj_Eta')

	return True









