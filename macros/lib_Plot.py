## lib_Plot.py

import ROOT, copy
import lib as helper



def make1dPlot(dataType, canv, pad_plot, pad_ratio, outputDir, hists, title_hist, file_name, leg):


	# create PLOT

	pad_plot.cd()

	max = hists[0][0].GetMaximum()
	for i in range(1,len(hists)):
		if max < hists[i][0].GetMaximum():
			max = hists[i][0].GetMaximum()

	hists[0][0] = helper.set1dPlotStyle(dataType, hists[0][0], helper.getColor(hists[0][1]), '', title_hist)
	#for i in range(len(hists)):
	#	hists[i][0] = helper.set1dPlotStyle(hists[i][0], helper.getColor(hists[i][1]), '', title_hist)
	
	#if "Tight_muMTMET20" in hists[0][0].GetName():
	#	for i in range(1,hists[0][0].GetXaxis().GetNbins()):
	#		print hists[1][0].GetStack().Last().GetBinContent(i)

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
	data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, title_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()

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



def Plot1d(dataType, outputDir, dataset, mcsets, histlist, leg, grouping = False):

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

		if grouping:

			mcgroups = []
			mcnames  = []

			for mc in mcsets:
				label = ''.join([j for j in mc.GetName() if not j.isdigit()])
				
				foundat = -1
				for j, mcname in enumerate(mcnames): 
					if label == mcname: foundat = j

				if foundat == -1:
					#print "--- did not find anything ---"
					mcgroups.append(ROOT.THStack())
					#print mc.hists[i]
					#print mc.hists[i].GetXaxis().GetNbins()
					mcgroups[len(mcgroups)-1].Add(mc.hists[i])
					mcnames.append(label)
				else:
					#print "--- found " + str(foundat) + " ---"
					#print mc.hists[i]
					#print mc.hists[i].GetXaxis().GetNbins()
					mcgroups[foundat].Add(mc.hists[i])
		
			#print mcgroups

			for j, group in enumerate(mcgroups):
				group.Draw('hist')
				histogram = group.GetStack().Last()
				print mcnames[j] + ": " + str(histogram.Integral())
				stackint += histogram.Integral()
				stack.Add(histogram)

			print mcnames
		
		else:
			for j,mc in enumerate(mcsets):
				stackint += mc.hists[i].Integral()
				stack.Add(mc.hists[i])

		stack.Draw('hist')

		histstoplot = []
		histstoplot.append([hist, 'data'])
		histstoplot.append([stack, 'totbg'])
		make1dPlot(dataType, canv, pad_plot, pad_ratio, outputDir, histstoplot, hist, prepend + helper.getSaveName(hist) + postpend, leg)



def PlotMETZooms(dataType, outputDir, dataset, mcsets, leg):

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

	for hist in dataset.hists:

		i = dataset.hists.index(hist)
		pad_plot.cd()


		# Plot Histogram
		if not "METZoom" in hist.GetName(): continue

		prepend = ''
		postpend = ''
		if '_Loose_' in hist.GetName(): prepend = 'Loose_'
		if '_Tight_' in hist.GetName(): prepend = 'Tight_'

		id = hist.GetName().split('_')[-1]


		# Sum BG Contributions in Stack
		stack = ROOT.THStack()
		stackint = 0.
		for j,mc in enumerate(mcsets):
			stackint += mc.hists[i].Integral()
			stack.Add(mc.hists[i])

		stack.Draw('hist')

		hists = []
		hists.append([hist, 'data'])
		hists.append([stack, 'totbg'])
		#make1dPlot(canv, pad_plot, pad_ratio, outputDir, histstoplot, hist, prepend + helper.getSaveName(hist, '-2:') + postpend, leg)

		max = hists[0][0].GetMaximum()
		for i in range(1,len(hists)):
			if max < hists[i][0].GetMaximum():
				max = hists[i][0].GetMaximum()

		hists[0][0] = helper.set1dPlotStyle(dataType, hists[0][0], helper.getColor(hists[0][1]), '', hist)
		hists[0][0].Draw("p x0 e")
		hists[0][0].SetMinimum(0.001)
		hists[0][0].SetMaximum(1.5*max)
		for i in range(1,len(hists)):
			hists[i][0].Draw("hist same")
			hists[i][0].SetMinimum(0.001)
			hists[i][0].SetMaximum(1.5*max)
	
		hists[0][0].Draw("p x0 e same")
		leg.Draw()

		m = int(id)//(len(bins_pt)-1)
		n = int(id)%(len(bins_pt)-1)

		if dataType == 'el': lepton = 'e'
		else               : lepton = '#mu'

		text_eta = str(bins_eta[m]) + " #leq " + lepton + "-|#eta| < " + str(bins_eta[m+1])
		text_pt  = str(bins_pt[n])  + " #leq " + lepton + "-p_{T} < " + str(bins_pt[n+1])

		t_eta.DrawLatex(0.22, 0.8, text_eta)
		t_pt.DrawLatex(0.22, 0.73, text_pt)


		# create RATIO PLOT
		
		pad_ratio.cd()
		data_bg_ratio = copy.deepcopy(hists[0][0])
		data_bg_ratio.Divide(hists[1][0].GetStack().Last())
		data_bg_ratio.Draw("p e")
		data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, hist)
		line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
		line.Draw()

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




def Plot2d(dataType, outputDir, dataset, mcsets, histlist):

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

		make2dPlot(dataType, canv, pad_plot, outputDir, hist, 'data', prepend + helper.getSaveName(hist) + postpend)
		for mc in mcsets: make2dPlot(dataType, canv, pad_plot, outputDir, mc.hists[i], mc.GetName(), prepend + helper.getSaveName(hist) + postpend)





