import ROOT, copy



def getMCScaleFactor(mcdataset, histforscale, datalist, mclist = [], minforint = 0, maxforint = 0):
	scalefactor = 1.0
	numerator = 0.0

	for hist in mcdataset.hists:
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



def getMCScaleFactorMutually(mcdatasets, histforscale, datalist, mclist = [], minforint = 0, maxforint = 0):

	scalefactors = [1.0 for i in range(len(mcdatasets))]
	numerator = 0.0
	denominator = 0.0

	for hist in mcdatasets[0].hists:
		i = mcdatasets[0].hists.index(hist)
		if hist.GetName() == histforscale:
			if minforint == 0: minbin = 1
			else: minbin = hist.FindBin(minforint)
			if maxforint == 0: maxbin = hist.GetNbinsX()
			else: maxbin = hist.FindBin(maxforint)

			for j in range(len(datalist)):
				#print "num+ looping over " + datalist[j].GetName() + ", " + str(datalist[j].hists[i].Integral(minbin, maxbin))
				numerator += datalist[j].hists[i].Integral(minbin, maxbin)
			for j in range(len(mclist)):
				#print "num- looping over " + mclist[j].GetName() + ", " + str(mclist[j].hists[i].Integral(minbin, maxbin))
				numerator -= mclist[j].hists[i].Integral(minbin, maxbin)
			for j in range(len(mcdatasets)):
				#print "denum looping over " + mcdatasets[j].GetName() + ", " + str(mcdatasets[j].hists[i].Integral(minbin, maxbin))
				denominator += mcdatasets[j].hists[i].Integral(minbin, maxbin)
			scalefactors = [numerator / denominator for j in range(len(mcdatasets))]

	return scalefactors



def getMCScaleFactorSimultaneouslyQCDEWK(data, qcd, ewk, hist_name = 'h_Tight_MTMET20'):

	scalefactors = [1.0 for i in range(1+len(ewk))]
	
	scind = 0
 	for i, hist in enumerate(data[0].hists): 
 		if hist.GetName() == hist_name:
			scind = i

	data_hist    = copy.deepcopy(data[0].hists[scind])
	for i in range(1, len(data)):
		data_hist.Add(data[i].hists[scind])

	qcd_hist     = copy.deepcopy(qcd[0].hists[scind])
	for i in range(1, len(qcd)):
		qcd_hist.Add(qcd[i].hists[scind])	

	ewk_hist     = copy.deepcopy(ewk[0].hists[scind])
	for i in range(1, len(ewk)):
		ewk_hist.Add(ewk[i].hists[scind])

	x    = ROOT.RooRealVar("x", "x", data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
	list = ROOT.RooArgList(x)
	set  = ROOT.RooArgSet(x)

	data_RDH    = ROOT.RooDataHist("data"  , "data"   , list, data_hist  )
	qcd_RDH     = ROOT.RooDataHist("qcd"   , "qcd"    , list, qcd_hist   )
	ewk_RDH     = ROOT.RooDataHist("ewk"   , "ewk"    , list, ewk_hist   )

	qcd_pdf     = ROOT.RooHistPdf("qcd_pdf", "qcd_pdf", set , qcd_RDH    )
	ewk_pdf     = ROOT.RooHistPdf("ewk_pdf", "ewk_pdf", set , ewk_RDH    )

	qcd_int     = qcd_hist.Integral()
	ewk_int     = ewk_hist.Integral()

	qcd_n       = ROOT.RooRealVar("qcd_n", "number of qcd", qcd_int, qcd_int*0.5, qcd_int*2.0)
	ewk_n       = ROOT.RooRealVar("ewk_n", "number of ewk", ewk_int, ewk_int*0.5, ewk_int*1.5)

	model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(qcd_pdf, ewk_pdf), ROOT.RooArgList(qcd_n, ewk_n))

	fitresult = model.fitTo(data_RDH, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1))

	for i in range(len(qcd)):
		scalefactors[i] = qcd_n.getVal() / qcd_int

	for i in range(len(qcd), len(ewk)):
		scalefactors[i] = ewk_n.getVal() / ewk_int

	return scalefactors




def getMCScaleFactorSimultaneously(data, mclist):

	scalefactors = [1.0, 1.0, 1.0, 1.0]

	scind = 0
 	for i, hist in enumerate(data.hists): 
 		if hist.GetName() == 'h_Tight_MTMET20':
			scind = i

	data_hist    = data.hists[scind]
	qcd_hist     = mclist[0].hists[scind]
	wjets_hist   = mclist[1].hists[scind]
	dyjets1_hist = mclist[2].hists[scind]
	dyjets2_hist = mclist[3].hists[scind]

	x = ROOT.RooRealVar("x", "x", data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
	list = ROOT.RooArgList(x)
	set = ROOT.RooArgSet(x)

	data_RDH    = ROOT.RooDataHist("data"   , "data"   , list, data_hist   )
	qcd_RDH     = ROOT.RooDataHist("qcd"    , "qcd"    , list, qcd_hist    )
	wjets_RDH   = ROOT.RooDataHist("wjets"  , "wjets"  , list, wjets_hist  )
	dyjets1_RDH = ROOT.RooDataHist("dyjets1", "dyjets1", list, dyjets1_hist)
	dyjets2_RDH = ROOT.RooDataHist("dyjets2", "dyjets2", list, dyjets2_hist)

	qcd_pdf     = ROOT.RooHistPdf("qcd_pdf"    , "qcd_pdf"    , set, qcd_RDH    )
	wjets_pdf   = ROOT.RooHistPdf("wjets_pdf"  , "wjets_pdf"  , set, wjets_RDH  )
	dyjets1_pdf = ROOT.RooHistPdf("dyjets1_pdf", "dyjets1_pdf", set, dyjets1_RDH)
	dyjets2_pdf = ROOT.RooHistPdf("dyjets2_pdf", "dyjets2_pdf", set, dyjets2_RDH)

	qcd_int     = qcd_hist    .Integral()
	wjets_int   = wjets_hist  .Integral()
	dyjets1_int = dyjets1_hist.Integral()
	dyjets2_int = dyjets2_hist.Integral()

	qcd_n     = ROOT.RooRealVar("qcd_n"    , "number of qcd"    , qcd_int    , qcd_int*0.5    , qcd_int*2.0    )
	wjets_n   = ROOT.RooRealVar("wjets_n"  , "number of wjets"  , wjets_int  , wjets_int*0.5  , wjets_int*1.3  )
	dyjets1_n = ROOT.RooRealVar("dyjets1_n", "number of dyjets1", dyjets1_int, dyjets1_int*0.5, dyjets1_int*1.0)
	dyjets2_n = ROOT.RooRealVar("dyjets2_n", "number of dyjets2", dyjets2_int, dyjets2_int*0.5, dyjets2_int*1.0)

	model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(qcd_pdf, wjets_pdf, dyjets1_pdf, dyjets2_pdf), ROOT.RooArgList(qcd_n, wjets_n, dyjets1_n, dyjets2_n))

	fitresult = model.fitTo(data_RDH, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1))

	scalefactors[0] = qcd_n.getVal()     / qcd_int
	scalefactors[1] = wjets_n.getVal()   / wjets_int
	scalefactors[2] = dyjets1_n.getVal() / dyjets1_int
	scalefactors[3] = dyjets2_n.getVal() / dyjets2_int

	return scalefactors



def getMCScaleFactorSimultaneouslyWithErrors(data, qcd, ewk, hist_min = 50, hist_max = 120, hist_name = 'h_Tight_MTMET20'):
	
	central = [1.0, 1.0]
	lower   = [1.0, 1.0]
	upper   = [1.0, 1.0]

	scalefactors = getMCScaleFactorSimultaneouslyQCDEWK(data, qcd, ewk, hist_name)
	central[0] = scalefactors[0]
	for mc in qcd: mc.Rescale(central[0])
	
	scalefactors = getMCScaleFactorMutually(ewk, hist_name, data, qcd, hist_min, hist_max)
	central[1] = scalefactors[0]
	
	for mc in qcd: mc.Rescale(1.5/1.0)
	upper[0] = 1.5*central[0]
	
	scalefactors = getMCScaleFactorMutually(ewk, hist_name, data, qcd, hist_min, hist_max)
	upper[1] = scalefactors[0]
	
	for mc in qcd: mc.Rescale(0.5/1.5)
	lower[0] = 0.5*central[0]
	
	scalefactors = getMCScaleFactorMutually(ewk, hist_name, data, qcd, hist_min, hist_max)
	lower[1] = scalefactors[0]
	
	for mc in qcd: mc.Rescale(1.0/(0.5*central[0]))

	return [central, lower, upper]




