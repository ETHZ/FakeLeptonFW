## lib_Plot.py

import ROOT, copy
import lib as helper




#___________________________________________________________________________________
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




#___________________________________________________________________________________
def make1dPlot_ratio(dataType, pad_ratio, hists, title_hist):

	pad_ratio.cd()
	data_bg_ratio = copy.deepcopy(hists[0][0])
	data_bg_ratio.Divide(copy.deepcopy(hists[1][0].GetStack().Last()))
	data_bg_ratio.Draw("p e")
	data_bg_ratio = helper.setRatioStyle(dataType, data_bg_ratio, title_hist)
	line = helper.makeLine(data_bg_ratio.GetXaxis().GetXmin(), 1.00, data_bg_ratio.GetXaxis().GetXmax(), 1.00)
	line.Draw()




#___________________________________________________________________________________
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




#___________________________________________________________________________________
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




#___________________________________________________________________________________
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




#___________________________________________________________________________________
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




#___________________________________________________________________________________
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




#___________________________________________________________________________________
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




#___________________________________________________________________________________
def PlotCompare(dataType, outputDir, mcsets, histname, leg, cutoff = -1):

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
		helper.saveCanvas(canv, pad_plot, outputDir + "compare/", prepend + helper.getSaveName(hist, cutoff) + postpend)




#___________________________________________________________________________________
def setProvenanceBin(hist, bintoselect, bintoset):

	binvalue = hist.GetBinContent(bintoselect)
	for j in range(1, hist.GetNbinsX()+1): hist.SetBinContent(j, 0)
	hist.SetBinContent(bintoset, binvalue)

	return hist




#___________________________________________________________________________________
def makeProvenancePlots(hist, labels, binstoplot, normalize = True):

	integral = float(hist.Integral())
	mycolor  = ROOT.TColor()
	bincolor = []

	bincolor.append(mycolor.GetColor(255, 255, 255))
	bincolor.append(mycolor.GetColor( 12,  57, 102))
	bincolor.append(mycolor.GetColor( 15, 106, 196))
	bincolor.append(mycolor.GetColor( 51, 153,  58))
	bincolor.append(mycolor.GetColor( 51, 102, 153))
	bincolor.append(mycolor.GetColor(191,  11,  11))
	bincolor.append(mycolor.GetColor(255, 204,   0))

	if binstoplot == []: binstoplot = [i for i in range(1,hist.GetNbinsX()+1)]

	h = []

	for i in range(len(binstoplot)):
		h.append(copy.deepcopy(hist))
		h[i] = setProvenanceBin(h[i], i+1, i+1)
		h[i].SetFillColor(bincolor[binstoplot[i]])
		if normalize and integral>0.: h[i].Scale(1./integral)

	for i in range(len(binstoplot)):

		h[i].SetMaximum(1.4)
		h[i].SetMinimum(0.0001)
		h[i].SetTitle('')
		h[i].SetMarkerSize(2.0)
		h[i].GetXaxis().SetLabelSize(0.07)
		h[i].GetXaxis().SetTitleSize(0.06)
		h[i].GetXaxis().SetTitle('')
		h[i].GetXaxis().SetLabelFont(62)
		h[i].GetYaxis().SetLabelSize(0.06)
		h[i].GetYaxis().SetTitleSize(0.06)

		if normalize and integral>0.: h[i].GetYaxis().SetTitle('1/Integral')

		for j in range(len(binstoplot)):  h[i].GetXaxis().SetBinLabel(j+1, labels[binstoplot[j]-1])

	return h




#___________________________________________________________________________________
def PlotProvenance(dataType, outputDir, mcsets, binstoplot = []):

	canv = helper.makeCanvas(900, 675, 'c1dZ')
	pad_plot = helper.makePad('tot')
	pad_plot.SetTicks(1,1)
	pad_plot.cd()
	
	nbins          = len(binstoplot)
	index_loose    = 0
	index_tight    = 0
	index_lnt      = 0

	labels             = ['all', 'W', 'B', 'C', 'U/D/S', 'unm.']
	hist_plot          = []
	mcgroups_loose     = []
	mcgroups_loose_lnt = []
	mcgroups_loose_aes = []
	mcgroups_tight     = []
	mcgroups_tight_aes = []
	mcnames            = []

	for hist in mcsets[0].hists:

		i = mcsets[0].hists.index(hist)

		hist_num[j].Divide(hist_num[j], hist_den[j], 1, 1, 'B')
		hist_nums  = makeProvenancePlots(hist_num[j], labels, binstoplot, False)
	
		hist_nums[0].Draw('hist text')	
		for k in range(1, len(hist_nums)): hist_nums[k].Draw('hist text same')
	
		helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_rate')
		if not 'Provenance' in hist.GetName(): continue
	
		if hist.GetName() == 'h_Loose_Provenance'   : index_loose     = i
		if hist.GetName() == 'h_Loose_ProvenanceLNT': index_loose_lnt = i
		if hist.GetName() == 'h_Loose_ProvenanceAES': index_loose_aes = i
		hist_num[j].Divide(hist_num[j], hist_den[j], 1, 1, 'B')
		hist_nums  = makeProvenancePlots(hist_num[j], labels, binstoplot, False)
	
		hist_nums[0].Draw('hist text')	
		for k in range(1, len(hist_nums)): hist_nums[k].Draw('hist text same')
	
		helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_rate')
		if hist.GetName() == 'h_Tight_Provenance'   : index_tight     = i
		if hist.GetName() == 'h_Tight_ProvenanceAES': index_tight_aes = i
		hist_num[j].Divide(hist_num[j], hist_den[j], 1, 1, 'B')
		hist_num[j].Divide(hist_num[j], hist_den[j], 1, 1, 'B')
		hist_nums  = makeProvenancePlots(hist_num[j], labels, binstoplot, False)
	
		hist_nums[0].Draw('hist text')	
		for k in range(1, len(hist_nums)): hist_nums[k].Draw('hist text same')
	
		helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_rate')
		hist_nums  = makeProvenancePlots(hist_num[j], labels, binstoplot, False)
	
		hist_nums[0].Draw('hist text')	
		for k in range(1, len(hist_nums)): hist_nums[k].Draw('hist text same')
	
		helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_rate')



	for mcset in mcsets:
		label = ''.join([j for j in mcset.GetName() if not j.isdigit()])
			
		foundat = -1
		for j, mcname in enumerate(mcnames): 
			if label == mcname: foundat = j

		if foundat == -1:
			mcgroups_loose    .append(ROOT.THStack())
			mcgroups_loose_lnt.append(ROOT.THStack())
			mcgroups_loose_aes.append(ROOT.THStack())
			mcgroups_tight    .append(ROOT.THStack())
			mcgroups_tight_aes.append(ROOT.THStack())
			mcgroups_loose    [len(mcgroups_loose)    -1].Add(mcset.hists[index_loose]    )
			mcgroups_loose_lnt[len(mcgroups_loose_lnt)-1].Add(mcset.hists[index_loose_lnt])
			mcgroups_loose_aes[len(mcgroups_loose_aes)-1].Add(mcset.hists[index_loose_aes])
			mcgroups_tight    [len(mcgroups_tight)    -1].Add(mcset.hists[index_tight]    )
			mcgroups_tight_aes[len(mcgroups_tight_aes)-1].Add(mcset.hists[index_tight_aes])
			mcnames.append(label)
		else:
			mcgroups_loose    [foundat].Add(mcset.hists[index_loose]    )
			mcgroups_loose_lnt[foundat].Add(mcset.hists[index_loose_lnt])
			mcgroups_loose_aes[foundat].Add(mcset.hists[index_loose_aes])
			mcgroups_tight    [foundat].Add(mcset.hists[index_tight]    )
			mcgroups_tight_aes[foundat].Add(mcset.hists[index_tight_aes])


	hist_den     = [{} for j in range(len(mcnames))]
	hist_den_aes = [{} for j in range(len(mcnames))]
	hist_num     = [{} for j in range(len(mcnames))]
	hist_num_aes = [{} for j in range(len(mcnames))]

	for i, plotgroup in enumerate([mcgroups_loose, mcgroups_loose_lnt, mcgroups_loose_aes, mcgroups_tight, mcgroups_tight_aes]):

		hist_plot.append([])

		for j, group in enumerate(plotgroup):

			group.Draw('hist')
			histogram = group.GetStack().Last()

			if nbins == 0: nbins = histogram.GetNbinsX()
	
			if histogram.GetName() == 'h_Loose_Provenance'   : postpend = 'loose'
			if histogram.GetName() == 'h_Loose_ProvenanceLNT': postpend = 'loose_lnt'
			if histogram.GetName() == 'h_Loose_ProvenanceAES': postpend = 'loose_aes'
			if histogram.GetName() == 'h_Tight_Provenance'   : postpend = 'tight'
			if histogram.GetName() == 'h_Tight_ProvenanceAES': postpend = 'tight_aes'
	
			hist_plot[i].append(ROOT.TH1F(histogram.GetName() + '_plot' + str(j), histogram.GetName(), nbins, 0, nbins))
	
			n = 1
			for k in range(1, histogram.GetNbinsX()+1):
				if binstoplot == [] or k in binstoplot:
					hist_plot[i][j].SetBinContent(n, histogram.GetBinContent(k))
					n +=1 

			if hist_plot[i][j].GetName() == 'h_Loose_Provenance_plot' + str(j)   : hist_den[j]     = copy.deepcopy(hist_plot[i][j])
			if hist_plot[i][j].GetName() == 'h_Loose_ProvenanceAES_plot' + str(j): hist_den_aes[j] = copy.deepcopy(hist_plot[i][j])
			if hist_plot[i][j].GetName() == 'h_Tight_Provenance_plot' + str(j)   : hist_num[j]     = copy.deepcopy(hist_plot[i][j])
			if hist_plot[i][j].GetName() == 'h_Tight_ProvenanceAES_plot' + str(j): hist_num_aes[j] = copy.deepcopy(hist_plot[i][j])
	
			hist_plots = makeProvenancePlots(hist_plot[i][j], labels, binstoplot)
	
			hist_plots[0].Draw('hist text')
			for k in range(1,len(hist_plots)): hist_plots[k].Draw('hist text same')
	
			helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_' + postpend)



	for j in range(len(mcnames)):

		hist_num[j].Divide(hist_num[j], hist_den[j], 1, 1, 'B')
		hist_nums  = makeProvenancePlots(hist_num[j], labels, binstoplot, False)
		hist_nums[0].Draw('hist text')	
		for k in range(1, len(hist_nums)): hist_nums[k].Draw('hist text same')
		helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_rate')
		
		hist_num_aes[j].Divide(hist_num_aes[j], hist_den_aes[j], 1, 1, 'B')
		hist_nums  = makeProvenancePlots(hist_num_aes[j], labels, binstoplot, False)	
		hist_nums[0].Draw('hist text')	
		for k in range(1, len(hist_nums)): hist_nums[k].Draw('hist text same')
		helper.saveCanvas(canv, pad_plot, outputDir + "closure/", mcnames[j] + '_rate_aes')

	

		
		










