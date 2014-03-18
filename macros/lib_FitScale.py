import ROOT



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



def doSimScaling(data_hist, qcd_hist, wjets_hist, dyjets_hist):

	scalefactors = [1.0, 1.0, 1.0]
	x = ROOT.RooRealVar("x", "x", data_hist.GetXaxis().GetXmin(), data_hist.GetXaxis().GetXmax())
	list = ROOT.RooArgList(x)
	set = ROOT.RooArgSet(x)

	data_RDH = ROOT.RooDataHist("data", "data", list, data_hist)
	qcd_RDH = ROOT.RooDataHist("qcd", "qcd", list, qcd_hist)
	wjets_RDH = ROOT.RooDataHist("wjets", "wjets", list, wjets_hist)
	dyjets_RDH = ROOT.RooDataHist("dyjets", "dyjets", list, dyjets_hist)

	qcd_pdf = ROOT.RooHistPdf("qcd_pdf", "qcd_pdf", set, qcd_RDH)
	wjets_pdf = ROOT.RooHistPdf("wjets_pdf", "wjets_pdf", set, wjets_RDH)
	dyjets_pdf = ROOT.RooHistPdf("dyjets_pdf", "dyjets_pdf", set, dyjets_RDH)

	qcd_int = qcd_hist.Integral()
	wjets_int = wjets_hist.Integral()
	dyjets_int = dyjets_hist.Integral()

	qcd_n = ROOT.RooRealVar("qcd_n", "number of qcd", qcd_int, qcd_int*0.5, qcd_int*2.0)
	wjets_n = ROOT.RooRealVar("wjets_n", "number of wjets", wjets_int, wjets_int*0.5, wjets_int*1.3)
	dyjets_n = ROOT.RooRealVar("dyjets_n", "number of dyjets", dyjets_int, dyjets_int*0.5, dyjets_int*1.0)

	model = ROOT.RooAddPdf("model", "model", ROOT.RooArgList(qcd_pdf, wjets_pdf, dyjets_pdf), ROOT.RooArgList(qcd_n, wjets_n, dyjets_n))

	fitresult = model.fitTo(data_RDH, ROOT.RooFit.SumW2Error(ROOT.kFALSE), ROOT.RooFit.Extended(), ROOT.RooFit.PrintLevel(-1))

	scalefactors[0] = qcd_n.getVal() / qcd_int
	scalefactors[1] = wjets_n.getVal() / wjets_int
	scalefactors[2] = dyjets_n.getVal() / dyjets_int

	return scalefactors


