import ROOT, copy



#___________________________________________________________________________________
def getMCScaleFactor(mcdataset, histforscale, datalist, mclist = [], minforint = 0, maxforint = 0):
	#
	# performs the scaling of a single mcsample to data
	# NOTE: ALL SAMPLES MUST CONTAIN THE EXACT SAME LIST OF HISTOGRAMS, OTHERWISE THIS FUNCTION WILL NOT WORK
	#
	# this function takes the following paramters:
	# mcdataset.....mc set to scale
	# histforscale..name of histogram to be used for the scaling
	# datalist......list of datasets [dataset1, dataset2, ..]
	# mclist........list of mc sets [mcset1, mcset2, ..] we have to get rid of first before scale to data
	# minforint.....minimum value on X axis for integration
	# maxforint.....maximum value on X axis for integration
	
	scalefactor = 1.0
	numerator = 0.0

	# iterate over all histograms in root files
	# it does not matter which sample we iterate on, as all samples contain the same list of histograms	

	for hist in mcdataset.hists:

		# get the index of the histogram
		i = mcdataset.hists.index(hist)

		if hist.GetName() == histforscale:

			if minforint == 0: minbin = 1
			else: minbin = hist.FindBin(minforint)
			if maxforint == 0: maxbin = hist.GetNbinsX()
			else: maxbin = hist.FindBin(maxforint)

			for j in range(len(datalist)):
				numerator += datalist[j].hists[i].Integral(minbin, maxbin)
			for j in range(len(mclist)):
				numerator -= mclist[j].hists[i].Integral(minbin, maxbin)

			scalefactor = numerator / hist.Integral(minbin, maxbin) 

	return scalefactor


#___________________________________________________________________________________
def getMCScaleFactorMutually(mcdatasets, histforscale, datalist, mclist = [], minforint = 0, maxforint = 0):
	#
	# performs the simultaneous scaling of several mcsamples to data
	# NOTE: ALL SAMPLES MUST CONTAIN THE EXACT SAME LIST OF HISTOGRAMS, OTHERWISE THIS FUNCTION WILL NOT WORK
	#
	# this function takes the following paramters:
	# mcdatasets....list of mc sets [mcset1, mcset2, ..]
	# histforscale..name of histogram to be used for the scaling
	# datalist......list of datasets [dataset1, dataset2, ..]
	# mclist........list of mc sets [mcset1, mcset2, ..] we have to get rid of first before scale to data
	# minforint.....minimum value on X axis for integration
	# maxforint.....maximum value on X axis for integration

	scalefactors = [1.0 for i in range(len(mcdatasets))]
	numerator = 0.0
	denominator = 0.0

	# iterate over all histograms in root files
	# it does not matter which sample we iterate on, as all samples contain the same list of histograms	

	for hist in mcdatasets[0].hists:

		# get the index of the histogram
		
		i = mcdatasets[0].hists.index(hist)

		
		if hist.GetName() == histforscale:

			if minforint == 0: minbin = 1
			else: minbin = hist.FindBin(minforint)
			if maxforint == 0: maxbin = hist.GetNbinsX()
			else: maxbin = hist.FindBin(maxforint)

			for j in range(len(datalist)):   numerator += datalist[j].hists[i].Integral(minbin, maxbin)
			for j in range(len(mclist)):     numerator -= mclist[j].hists[i].Integral(minbin, maxbin)
			for j in range(len(mcdatasets)): denominator += mcdatasets[j].hists[i].Integral(minbin, maxbin)

			scalefactors = [numerator / denominator for j in range(len(mcdatasets))]

	return scalefactors


#___________________________________________________________________________________
def getMCScaleFactorSimultaneouslyQCDEWK(data, qcd, ewk, hist_name = 'h_Tight_MTMET20'):
	#
	# performs the simultaneous scaling of qcd and ewk and gives central values
	#
	# this function takes the following paramters:
	# data........list of datasets [dataset1, dataset2, ..]
	# qcd.........list of qcd mc sets [mcset1, mcset2, ..]
	# ewk.........list of ewk mc sets [mcset1, mcset2, ..]
	# hist_name...name of the histogram to be used for the scaling

	# default

	scalefactors = [1.0 for i in range(len(qcd)+len(ewk))]
	
	# get index of histogram to scale mc to data

	scind = 0
 	for i, hist in enumerate(data[0].hists): 
 		if hist.GetName() == hist_name:
			scind = i

	# data histogram
	
	data_hist    = copy.deepcopy(data[0].hists[scind])
	for i in range(1, len(data)):
		data_hist.Add(data[i].hists[scind])

	# qcd histogram

	qcd_hist     = copy.deepcopy(qcd[0].hists[scind])
	for i in range(1, len(qcd)):
		qcd_hist.Add(qcd[i].hists[scind])	

	# ewk histogram

	ewk_hist     = copy.deepcopy(ewk[0].hists[scind])
	for i in range(1, len(ewk)):
		ewk_hist.Add(ewk[i].hists[scind])

	# define RooFit variables

	x    = ROOT.RooRealVar("x", "x", data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
	list = ROOT.RooArgList(x)
	set  = ROOT.RooArgSet(x)

	# define RooFit histograms

	data_RDH    = ROOT.RooDataHist("data"  , "data"   , list, data_hist  )
	qcd_RDH     = ROOT.RooDataHist("qcd"   , "qcd"    , list, qcd_hist   )
	ewk_RDH     = ROOT.RooDataHist("ewk"   , "ewk"    , list, ewk_hist   )

	# get RooFit pdf

	qcd_pdf     = ROOT.RooHistPdf("qcd_pdf", "qcd_pdf", set , qcd_RDH    )
	ewk_pdf     = ROOT.RooHistPdf("ewk_pdf", "ewk_pdf", set , ewk_RDH    )

	# get integral

	qcd_int     = qcd_hist.Integral()
	ewk_int     = ewk_hist.Integral()

	# get RooFit scale factors
	
	qcd_n       = ROOT.RooRealVar("qcd_n", "number of qcd", qcd_int, qcd_int*0.5, qcd_int*2.0)
	ewk_n       = ROOT.RooRealVar("ewk_n", "number of ewk", ewk_int, ewk_int*0.5, ewk_int*1.5)

	# do the fit

	model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(qcd_pdf, ewk_pdf), ROOT.RooArgList(qcd_n, ewk_n))

	fitresult = model.fitTo(data_RDH, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1))

	# return scale factors
	# the return list has has many entries as qcd + ewk together, with the order as given in the paramters

	for i in range(len(qcd)):
		scalefactors[i] = qcd_n.getVal() / qcd_int

	for i in range(len(qcd), len(ewk)):
		scalefactors[i] = ewk_n.getVal() / ewk_int

	return scalefactors



#___________________________________________________________________________________
def getMCScaleFactorSimultaneously(data, mclist):
	#
	# performs the simultaneous scaling of several mc sets and gives back central values
	# NOTE: THIS IS ALL DESIGNED FOR 4 MC SETS (NOT VERY NICE)
	#
	# this function takes the following paramters:
	# data........list of datasets [dataset1, dataset2, ..]
	# mclist......list of mc sets [mcset1, mcset2, ..]

	# default

	scalefactors = [1.0, 1.0, 1.0, 1.0]

	# get index of histogram to scale mc to data

	scind = 0
 	for i, hist in enumerate(data.hists): 
 		if hist.GetName() == 'h_Tight_MTMET20':
			scind = i

	# get histogram

	data_hist    = data.hists[scind]
	qcd_hist     = mclist[0].hists[scind]
	wjets_hist   = mclist[1].hists[scind]
	dyjets1_hist = mclist[2].hists[scind]
	dyjets2_hist = mclist[3].hists[scind]

	# define RooFit variables

	x = ROOT.RooRealVar("x", "x", data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
	list = ROOT.RooArgList(x)
	set = ROOT.RooArgSet(x)

	# define RooFit histograms

	data_RDH    = ROOT.RooDataHist("data"   , "data"   , list, data_hist   )
	qcd_RDH     = ROOT.RooDataHist("qcd"    , "qcd"    , list, qcd_hist    )
	wjets_RDH   = ROOT.RooDataHist("wjets"  , "wjets"  , list, wjets_hist  )
	dyjets1_RDH = ROOT.RooDataHist("dyjets1", "dyjets1", list, dyjets1_hist)
	dyjets2_RDH = ROOT.RooDataHist("dyjets2", "dyjets2", list, dyjets2_hist)

	# define RooFit PDFs from RooFit Hist

	qcd_pdf     = ROOT.RooHistPdf("qcd_pdf"    , "qcd_pdf"    , set, qcd_RDH    )
	wjets_pdf   = ROOT.RooHistPdf("wjets_pdf"  , "wjets_pdf"  , set, wjets_RDH  )
	dyjets1_pdf = ROOT.RooHistPdf("dyjets1_pdf", "dyjets1_pdf", set, dyjets1_RDH)
	dyjets2_pdf = ROOT.RooHistPdf("dyjets2_pdf", "dyjets2_pdf", set, dyjets2_RDH)

	# get integral

	qcd_int     = qcd_hist    .Integral()
	wjets_int   = wjets_hist  .Integral()
	dyjets1_int = dyjets1_hist.Integral()
	dyjets2_int = dyjets2_hist.Integral()

	# get RooFit scale factors

	qcd_n     = ROOT.RooRealVar("qcd_n"    , "number of qcd"    , qcd_int    , qcd_int*0.5    , qcd_int*2.0    )
	wjets_n   = ROOT.RooRealVar("wjets_n"  , "number of wjets"  , wjets_int  , wjets_int*0.5  , wjets_int*1.3  )
	dyjets1_n = ROOT.RooRealVar("dyjets1_n", "number of dyjets1", dyjets1_int, dyjets1_int*0.5, dyjets1_int*1.0)
	dyjets2_n = ROOT.RooRealVar("dyjets2_n", "number of dyjets2", dyjets2_int, dyjets2_int*0.5, dyjets2_int*1.0)

	# do the fit

	model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(qcd_pdf, wjets_pdf, dyjets1_pdf, dyjets2_pdf), ROOT.RooArgList(qcd_n, wjets_n, dyjets1_n, dyjets2_n))

	fitresult = model.fitTo(data_RDH, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1))

	# output scale factors

	scalefactors[0] = qcd_n.getVal()     / qcd_int
	scalefactors[1] = wjets_n.getVal()   / wjets_int
	scalefactors[2] = dyjets1_n.getVal() / dyjets1_int
	scalefactors[3] = dyjets2_n.getVal() / dyjets2_int

	return scalefactors


#___________________________________________________________________________________
def getMCScaleFactorSimultaneouslyWithErrors(data, qcd, ewk, hist_min = 50, hist_max = 120, hist_name = 'h_Tight_MTMET20'):
	#
	# performs the simultaneous scaling of qcd and ewk and gives central values and errors
	#
	# this function takes the following paramters:
	# data........list of datasets [dataset1, dataset2, ..]
	# qcd.........list of qcd mc sets [mcset1, mcset2, ..]
	# ewk.........list of ewk mc sets [mcset1, mcset2, ..]
	# hist_min....
	# hist_max....
	# hist_name...name of the histogram to be used for the scaling
	
	central = [1.0, 1.0]
	lower   = [1.0, 1.0]
	upper   = [1.0, 1.0]

	# scale qcd and ewk simultaneously to data, which gives qcd central value

	scalefactors = getMCScaleFactorSimultaneouslyQCDEWK(data, qcd, ewk, hist_name)
	central[0] = scalefactors[0]
	for mc in qcd: mc.Rescale(central[0])

	# scale ewk samples alone, which gives ewk central value
	
	scalefactors = getMCScaleFactorMutually(ewk, hist_name, data, qcd, hist_min, hist_max)
	central[1] = scalefactors[0]

	# do the same thing with qcd + 50%
	
	for mc in qcd: mc.Rescale(1.5/1.0)
	upper[0] = 1.5*central[0]
	
	scalefactors = getMCScaleFactorMutually(ewk, hist_name, data, qcd, hist_min, hist_max)
	upper[1] = scalefactors[0]

	# do the same thing with qcd - 50%
	
	for mc in qcd: mc.Rescale(0.5/1.5)
	lower[0] = 0.5*central[0]
	
	scalefactors = getMCScaleFactorMutually(ewk, hist_name, data, qcd, hist_min, hist_max)
	lower[1] = scalefactors[0]

	# rescale qcd back to 1 again
	
	for mc in qcd: mc.Rescale(1.0/(0.5*central[0]))

	return [central, lower, upper]




