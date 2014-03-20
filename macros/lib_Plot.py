## lib_Plot.py

import ROOT, copy
import lib as helper


def make1dPlot(canv, pad_plot, pad_ratio, outputDir, hists, title_hist, file_name, leg):

	# create PLOT

	pad_plot.cd()

	max = hists[0][0].GetMaximum()
	for i in range(1,len(hists)):
		if max < hists[i][0].GetMaximum():
			max = hists[i][0].GetMaximum()

	hists[0][0] = helper.set1dPlotStyle(hists[0][0], helper.getColor(hists[0][1]), '', title_hist)
	#for i in range(len(hists)):
	#	hists[i][0] = helper.set1dPlotStyle(hists[i][0], helper.getColor(hists[i][1]), '', title_hist)

	hists[0][0].Draw("p x0 e")
	hists[0][0].SetMinimum(0.001)
	hists[0][0].SetMaximum(1.5*max)
	for i in range(1,len(hists)):
		hists[i][0].Draw("hist same")
		hists[i][0].SetMinimum(0.001)
		hists[i][0].SetMaximum(1.5*max)
	
	hists[0][0].Draw("p x0 e same")
	leg.Draw()


	# create RATIO PLOT
	
	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(hists[0][0])
	data_bg_ratio.Divide(hists[1][0].GetStack().Last())
	data_bg_ratio.Draw("p e")
	data_bg_ratio = helper.setRatioStyle(data_bg_ratio, title_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()

	ROOT.gPad.RedrawAxis()

	helper.saveCanvas(canv, pad_plot, outputDir, file_name)


def make2dPlot(canv, pad_plot, outputDir, hist, postpend, file_name):

	postpend = "_" + str(postpend.lower())
	hist.Draw('colz')
	hist.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.GetYaxis().SetTitle(helper.getYTitle(hist))	
	hist.GetYaxis().SetTitleSize(0.055)
	hist.GetYaxis().SetLabelSize(0.07)
	hist.GetYaxis().SetNdivisions(505)
	hist.GetXaxis().SetTitleSize(0.07)
	hist.GetXaxis().SetLabelSize(0.07)
	hist.GetXaxis().SetNdivisions(505)
	hist.SetTitle("")
	hist.SetMarkerColor(ROOT.kBlack)
	hist.SetLineColor(ROOT.kBlack)
	ROOT.gPad.RedrawAxis()
	helper.saveCanvas(canv, pad_plot, outputDir, file_name + postpend, 0)



def Plot1d(outputDir, dataset, mcsets, histlist, leg):

	canv = helper.makeCanvas(900, 675, 'c1d')
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

	for hist in dataset.hists:
		
		i = dataset.hists.index(hist)
		pad_plot.cd()
		
		
		# Plot Histogram
		if not hist.GetName() in histlist: continue
		if hist.GetName()[-10:] == "NVertices1": continue

		prepend = ''
		postpend = ''
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'

		# Sum BG Contributions in Stack
		stack = ROOT.THStack()
		stackint = 0.
		for j,mc in enumerate(mcsets):
			stackint += mc.hists[i].Integral()
			stack.Add(mc.hists[i])

		stack.Draw('hist')

		histstoplot = []
		histstoplot.append([hist, 'data'])
		histstoplot.append([stack, 'totbg'])
		make1dPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, hist, prepend + helper.getSaveName(hist) + postpend, leg)


def PlotZooms(outputDir, dataset, mcsets, leg):

	canv = helper.makeCanvas(900, 675, 'c1dZ')
	pad_plot = helper.makePad('tot')
	pad_plot.SetTicks(1,1)
	pad_plot.cd()

	t_eta = ROOT.TLatex()
	t_eta.SetNDC()
	t_eta.SetTextSize(0.05)
	t_eta.SetTextAlign(11)
	t_eta.SetTextColor(ROOT.kBlack)

	t_pt = ROOT.TLatex()
	t_pt.SetNDC()
	t_pt.SetTextSize(0.05)
	t_pt.SetTextAlign(11)
	t_pt.SetTextColor(ROOT.kBlack)

	bins_eta = [0.0, 1.0, 2.4]
	bins_pt  = [10.0, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 40.0, 50.0, 60.0, 70.0]
	bins_tot = (len(bins_eta)-1)*(len(bins_pt)-1)

	for hist in dataset.hists:

		i = dataset.hists.index(hist)

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
		for mc in mcsets:
			mc.hists[i].Scale(1.0/mc.hists[i].Integral())
			mc.hists[i].SetFillStyle(0)
			mc.hists[i].Draw("HIST SAME")
			if mc.hists[i].GetMaximum()>max: max = mc.hists[i].GetMaximum()

		# Cosmetics
		hist.SetMaximum(1.5*max)
		hist.GetXaxis().SetTitle(helper.getXTitle(hist))
		hist.GetYaxis().SetTitle("1/Integral")
		hist.SetTitle("")
		hist.GetXaxis().SetTitleSize(0.07)
		hist.GetXaxis().SetLabelSize(0.07)
		hist.GetYaxis().SetTitleSize(0.07)
		hist.GetYaxis().SetLabelSize(0.07)
		hist.GetXaxis().SetNdivisions(505)
		hist.GetYaxis().SetNdivisions(505)
		leg.Draw()

		m = int(id)//(len(bins_pt)-1)
		n = int(id)%(len(bins_pt)-1)
	
		text_eta = str(bins_eta[m]) + " #leq |#eta|_{jet} < " + str(bins_eta[m+1])
		text_pt  = str(bins_pt[n])  + " #leq jet-p_{T} (corr.) < " + str(bins_pt[n+1])

		t_eta.DrawLatex(0.22, 0.8, text_eta)
		t_pt.DrawLatex(0.22, 0.73, text_pt)

		helper.saveCanvas(canv, pad_plot, outputDir, prepend + helper.getSaveName(hist, '-2:') + postpend, 0)




def Plot2d(outputDir, dataset, mcsets, histlist):

	canv = helper.makeCanvas(900, 675, 'c2d')
	pad_plot = helper.makePad('tot')
	pad_plot.cd()
	pad_plot.SetTicks(1,1)

	for hist in dataset.hists:
		
		i = dataset.hists.index(hist)
		
		# Plot Histogram
		if not hist.GetName() in histlist: continue

		prepend = ''
		postpend = ''
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'

		make2dPlot(canv, pad_plot, outputDir, hist, 'data', prepend + helper.getSaveName(hist) + postpend)
		for mc in mcsets: make2dPlot(canv, pad_plot, outputDir, mc.hists[i], mc.GetName(), prepend + helper.getSaveName(hist) + postpend)

