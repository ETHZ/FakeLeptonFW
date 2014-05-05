## lib_Plot.py

import ROOT, copy
import lib as helper


def make1dPlot_plot(dataType, pad_plot, hists, title_hist, leg):

	pad_plot.cd()

	max = hists[0][0].GetMaximum()
	for i in range(1,len(hists)):
		if max < hists[i][0].GetStack().Last().GetMaximum():
			max = hists[i][0].GetStack().Last().GetMaximum()

	hists[0][0] = helper.set1dPlotStyle(dataType, hists[0][0], helper.getColor(hists[0][1]), '', title_hist)

	hists[0][0].Draw("p x0 e")
	hists[0][0].SetMinimum(0.001)
	hists[0][0].SetMaximum(1.5*max)
	for i in range(1,len(hists)):
		hists[i][0].Draw("hist same")
		hists[i][0].SetMinimum(0.001)
		hists[i][0].SetMaximum(1.5*max)
	
	hists[0][0].Draw("p x0 e same")
	leg.Draw()


def make1dPlot_ratio(dataType, pad_ratio, hists, title_hist):

	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(hists[0][0])
	data_bg_ratio.Divide(copy.deepcopy(hists[1][0].GetStack().Last()))
	data_bg_ratio.Draw("p e")
	data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, title_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()



def make1dPlot(dataType, canv, pad_plot, pad_ratio, outputDir, hists, title_hist, file_name, leg):


	# create PLOT
	make1dPlot_plot(dataType, pad_plot, hists, title_hist, leg) 

	# create RATIO 
	#make1dPlot_ratio(dataType, pad_ratio, hists, title_hist)

	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(hists[0][0])
	data_bg_ratio.Divide(copy.deepcopy(hists[1][0].GetStack().Last()))
	data_bg_ratio.Draw("p e")
	data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, title_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()



	# save plot
	ROOT.gPad.RedrawAxis()
	helper.saveCanvas(canv, pad_plot, outputDir + "plots_1d/", file_name)




def make2dPlot(dataType, canv, pad_plot, outputDir, hist, postpend, file_name):

	postpend = "_" + str(postpend.lower())
	hist.Draw('colz')
	hist.GetXaxis().SetTitle(helper.getXTitle(dataType, hist))
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
	helper.saveCanvas(canv, pad_plot, outputDir + "plots_2d/", file_name + postpend, False)



def Plot1d(dataType, outputDir, datasets, mcsets, histlist, leg, grouping = False):
	
	canv = helper.makeCanvas(900, 675, 'c1d')
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

	for hist in datasets[0].hists:
		
		i = datasets[0].hists.index(hist)
		pad_plot.cd()
		
		
		# Plot Histogram
		if not hist.GetName() in histlist: continue
		if hist.GetName()[-10:] == "NVertices1": continue

		prepend = ''
		postpend = ''
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'


		# Sum BG Contributions in Stack
		data = ROOT.THStack()
		mc   = ROOT.THStack()

		for dataset in datasets:	
				data.Add(dataset.hists[i])

		if grouping:

			mcgroups = []
			mcnames  = []

			for mcset in mcsets:
				label = ''.join([j for j in mcset.GetName() if not j.isdigit()])
				
				foundat = -1
				for j, mcname in enumerate(mcnames): 
					if label == mcname: foundat = j

				if foundat == -1:
					mcgroups.append(ROOT.THStack())
					mcgroups[len(mcgroups)-1].Add(mcset.hists[i])
					mcnames.append(label)
				else:
					mcgroups[foundat].Add(mcset.hists[i])

			for j, group in enumerate(mcgroups):
				group.Draw('hist')
				histogram = group.GetStack().Last()
				mc.Add(histogram)
		
		else:
			for mc in mcsets:	
				mc.Add(mc.hists[i])

		#mc.Draw('hist')
	
		histstoplot = []
		histstoplot.append([data.GetStack().Last(), 'data' ])
		histstoplot.append([mc                    , 'totbg'])
		make1dPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, hist, prepend + helper.getSaveName(hist) + postpend, leg)




def PlotMETZooms(dataType, outputDir, datasets, mcsets, leg, grouping = False):

	canv = helper.makeCanvas(900, 675, 'c1dM')
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_plot.SetTicks(1,1)
	pad_ratio.SetTicks(1,1)

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

	bins_eta = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5]
	bins_pt  = [20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0]
	bins_tot = (len(bins_eta)-1)*(len(bins_pt)-1)

	for hist in datasets[0].hists:

		i = datasets[0].hists.index(hist)
		pad_plot.cd()


		# Plot Histogram
		if not "METZoom" in hist.GetName(): continue

		prepend = ''
		postpend = ''
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'

		id = hist.GetName().split('_')[-1]


		# Sum BG Contributions in Stack

		data = ROOT.THStack()
		mc = ROOT.THStack()

		for dataset in datasets:
			data.Add(dataset.hists[i])

		if grouping:

			mcgroups = []
			mcnames  = []

			for mcset in mcsets:
				label = ''.join([j for j in mcset.GetName() if not j.isdigit()])
				
				foundat = -1
				for j, mcname in enumerate(mcnames): 
					if label == mcname: foundat = j

				if foundat == -1:
					mcgroups.append(ROOT.THStack())
					mcgroups[len(mcgroups)-1].Add(mcset.hists[i])
					mcnames.append(label)
				else:
					mcgroups[foundat].Add(mcset.hists[i])
		

			for j, group in enumerate(mcgroups):
				group.Draw('hist')
				histogram = group.GetStack().Last()
				mc.Add(histogram)
		
		else:
			for mcset in mcsets:
				mc.Add(mcset.hists[i])

		mc.Draw('hist')


		# Create Plot

		hists = []
		hists.append([data.GetStack().Last(), 'data' ])
		hists.append([mc                    , 'totbg'])
		make1dPlot_plot(dataType, pad_plot, hists, hists[0][0], leg)


		# Write Text

		m = int(id)//(len(bins_pt)-1)
		n = int(id)%(len(bins_pt)-1)

		if dataType == 'el': lepton = 'e'
		else               : lepton = '#mu'

		text_eta = str(bins_eta[m]) + " #leq " + lepton + "-|#eta| < " + str(bins_eta[m+1])
		text_pt  = str(bins_pt[n])  + " #leq " + lepton + "-p_{T} < " + str(bins_pt[n+1])

		t_eta.DrawLatex(0.22, 0.8, text_eta)
		t_pt.DrawLatex(0.22, 0.73, text_pt)


		# Create RATIO PLOT

		#make1dPlot_ratio(dataType, pad_ratio, hists, hists[0][0])

		pad_ratio.cd()
		data_bg_ratio = copy.deepcopy(hists[0][0])
		data_bg_ratio.Divide(copy.deepcopy(hists[1][0].GetStack().Last()))
		data_bg_ratio.Draw("p e")
		data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, hists[0][0])
		line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
		line.Draw()


		# Save Plot

		ROOT.gPad.RedrawAxis()
		helper.saveCanvas(canv, pad_plot, outputDir + "zoom_met/", prepend + helper.getSaveName(hist, '-2:') + postpend)




def PlotJPtZooms(dataType, outputDir, dataset, mcsets, leg):

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
	#bins_pt = [10.0, 20.0, 30.0, 35.0, 37.5, 40.0, 42.5, 45.0, 47.5, 50.0, 55.0, 60.0, 70.0] # old
	bins_pt  = [10.0, 20.0, 22.5, 25.0, 27.5, 30.0, 32.5, 35.0, 40.0, 50.0, 60.0, 70.0] # new
	bins_tot = (len(bins_eta)-1)*(len(bins_pt)-1)


	for hist in dataset.hists:

		i = dataset.hists.index(hist)

		# Plot Histogram
		if not "JPtZoom" in hist.GetName(): continue

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
		hist.GetXaxis().SetTitle(helper.getXTitle(dataType, hist))
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

		if "ZoomC" in hist.GetName(): write = "corr."
		else:                         write = "raw"
	
		text_eta = str(bins_eta[m]) + " #leq jet-|#eta| < " + str(bins_eta[m+1])
		text_pt  = str(bins_pt[n])  + " #leq jet-p_{T} (" + write + ") < " + str(bins_pt[n+1])

		t_eta.DrawLatex(0.22, 0.8, text_eta)
		t_pt.DrawLatex(0.22, 0.73, text_pt)

		helper.saveCanvas(canv, pad_plot, outputDir + "zoom_jpt/", prepend + helper.getSaveName(hist, '-2:') + postpend, False)



def PlotCompare(dataType, outputDir, mcsets, histname, leg):

	canv = helper.makeCanvas(900, 675)
	pad_plot = helper.makePad('plot')
	pad_ratio = helper.makePad('ratio')
	pad_ratio.cd()


	for hist in mcsets[0].hists:

		i = mcsets[0].hists.index(hist)
		pad_plot.cd()

		if not histname in hist.GetName(): continue

		prepend = ''
		postpend = '_compare'
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'

		hist.Draw('hist')
		hist.SetFillStyle(0)
		hist.Scale(1.0/hist.Integral())
		max = hist.GetMaximum()

		for j in range(1,len(mcsets)):	
			mcsets[j].hists[i].Draw('hist same')
			mcsets[j].hists[i].SetFillStyle(0)
			mcsets[j].hists[i].SetLineStyle(2)
			mcsets[j].hists[i].Scale(1.0/mcsets[j].hists[i].Integral())
			if max < mcsets[j].hists[i].GetMaximum(): max = mcsets[j].hists[i].GetMaximum()

		hist.SetMinimum(0.0001)
		hist.SetMaximum(1.5 * max)
		hist = helper.set1dPlotStyle(dataType, hist, helper.getColor(mcsets[0].GetName()), '', hist, '1/Integral')
		leg.Draw()

		pad_ratio.cd()
		hist_ratio = copy.deepcopy(hist)
		hist_ratio.Divide(copy.deepcopy(mcsets[1].hists[i]))
		hist_ratio.Draw("p e1")
		hist_ratio = helper.setRatioStyle(dataType, hist_ratio, hist)
		line = helper.makeLine(hist_ratio.GetXaxis().GetXmin(), 1.00, hist_ratio.GetXaxis().GetXmax(), 1.00)
		line.Draw()
		helper.saveCanvas(canv, pad_plot, outputDir + "compare/", prepend + helper.getSaveName(hist) + postpend)






def Plot2d(dataType, outputDir, datasets, mcsets, histlist):

	canv = helper.makeCanvas(900, 675, 'c2d')
	pad_plot = helper.makePad('tot')
	pad_plot.cd()
	pad_plot.SetTicks(1,1)

	for hist in datasets[0].hists:
		
		i = datasets[0].hists.index(hist)
		
		# Plot Histogram
		if not hist.GetName() in histlist: continue

		prepend = ''
		postpend = ''
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'

		data = ROOT.THStack()
		mc   = ROOT.THStack()

		for dataset in datasets: data.Add(dataset.hists[i])
		for mcset   in mcsets:   mc  .Add(mcset  .hists[i])

		make2dPlot(dataType, canv, pad_plot, outputDir, data.GetStack().Last(), 'data', prepend + helper.getSaveName(hist) + postpend)
		make2dPlot(dataType, canv, pad_plot, outputDir, mc  .GetStack().Last(), 'MC'  , prepend + helper.getSaveName(hist) + postpend)
		for mcset in mcsets: make2dPlot(dataType, canv, pad_plot, outputDir, mcset.hists[i], mcset.GetName(), prepend + helper.getSaveName(hist) + postpend)








