import ROOT, math, os, shutil

def CreateOutputFolders(outputDir):

	afsfolder = "/afs/cern.ch/user/c/cheidegg/www/pdfs/"
	folders = ['plots_1d', 'plots_2d', 'zoom_met', 'zoom_jpt', 'fakerates_1d', 'fakerates_2d', 'adhoc']
	struct = outputDir.split('/')
	
	for i in range(1,len(struct)): 
		if not os.path.exists('/'.join(struct[0:i])): 
			os.mkdir('/'.join(struct[0:i]))
	
	for i in range(2,len(struct)): 
		if not os.path.exists(afsfolder + '/'.join(struct[1:i])): 
			os.mkdir(afsfolder + '/'.join(struct[1:i]))

	for final in folders:
		if not os.path.exists(outputDir + final): 
			os.mkdir(outputDir + final)
		if not os.path.exists(afsfolder + '/'.join(struct[1:]) + final): 
			os.mkdir(afsfolder + '/'.join(struct[1:]) + final)
			shutil.copyfile('index.php', afsfolder + '/'.join(struct[1:]) + final + '/index.php')

def getColor(name):
	mycolor = ROOT.TColor()
	if   name == 'wjets'              : return mycolor.GetColor(102,   0,   0)
	elif name == 'dyjets1'            : return mycolor.GetColor(255, 204,   0)
	elif name == 'dyjets2'            : return mycolor.GetColor(255, 204,   0)
	elif name == 'qcdMuEnriched'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'totbg'              : return mycolor.GetColor(172,   0,   0)
	elif name == 'data'               : return ROOT.kBlack
	elif name == 'datamcsub'          : return ROOT.kOrange
	elif name == 'datamcsub_central1' : return mycolor.GetColor( 51, 153,  51)
	elif name == 'datamcsub_lower1'   : return mycolor.GetColor(106,  90, 205)
	elif name == 'datamcsub_upper1'   : return mycolor.GetColor(  0,   0, 128)
	elif name == 'datamcsub_central2' : return ROOT.kRed
	elif name == 'data30'             : return ROOT.kBlack
	elif name == 'data40'             : return ROOT.kRed
	elif name == 'data50'             : return ROOT.kBlue
	elif name == 'data60'             : return ROOT.kGreen
	elif name == 'dataJCPt'           : return ROOT.kRed
	elif name == 'dataJRPt'           : return ROOT.kBlue

def getSampleColor(self):
	return getColor(self.name)

def getLegendName(name):
	if   name == 'wjets'              : return 'W + Jets'
	elif name == 'dyjets1'            : return 'DY + Jets'
	elif name == 'dyjets2'            : return 'DY + Jets'
	elif name == 'qcdMuEnriched'      : return 'QCD'
	elif name == 'totbg'              : return 'QCD + EW'
	elif name == 'data'               : return 'Data'
	elif name == 'datamcsub'          : return 'Data - EW'
	elif name == 'datamcsub_central1' : return 'Data - EW (ETH)'
	elif name == 'datamcsub_lower1'   : return 'Data - EW (ETH lower)'
	elif name == 'datamcsub_upper1'   : return 'Data - EW (ETH upper)'
	elif name == 'datamcsub_central2' : return 'Data - EW (UCSx)'
	elif name == 'data30'             : return 'Data (30GeV)'
	elif name == 'data40'             : return 'Data (40GeV)'
	elif name == 'data50'             : return 'Data (50GeV)'
	elif name == 'data60'             : return 'Data (60GeV)'
	elif name == 'dataJCPt'           : return 'Data (corr. Jet Pt)'
	elif name == 'dataJRPt'           : return 'Data (raw Jet Pt)'

def makeLegend(x1,y1,x2,y2):
	leg = ROOT.TLegend(x1,y1,x2,y2)
	leg.SetFillColor(ROOT.kWhite)
	leg.SetTextFont(42)
	leg.SetBorderSize(0)
	leg.SetMargin(0.35)
	leg.SetTextSize(0.07)
	return leg

def makeCanvas(x, y, name='c', setmargin = 1):
	canv = ROOT.TCanvas(name, 'c', x, y)
	canv.SetTicks(1,1)
	if setmargin == 1:
		canv.SetBottomMargin(0.15)
		canv.SetLeftMargin(0.12)
		canv.SetRightMargin(0.03)
		canv.SetTopMargin(0.07)
	return canv

def makePad(which):
	pad = ROOT.TPad('p', 'p', 0.0, 0.0, 1.0, 1.0, 0, 0)

	if which == 'plot':
		pad.SetPad(0.0, 0.3, 1.0, 1.0)
		pad.SetBorderSize(0)
		pad.SetBottomMargin(0.0)
		pad.SetLeftMargin(0.17)
		pad.SetTicks(1,1)

	if which == 'ratio':
		pad.SetPad(0.0, 0.0, 1.0, 0.3)
		pad.SetBorderSize(0)
		pad.SetTopMargin(0.0)
		pad.SetBottomMargin(0.47)
		pad.SetLeftMargin(0.17)
		pad.SetTicks(1,1)

	if which == 'tot':
		pad.SetPad(0.0, 0.0, 1.0, 1.0)
		pad.SetTopMargin(0.1)
		pad.SetBottomMargin(0.2)
		pad.SetLeftMargin(0.17)
		pad.SetRightMargin(0.1)
		pad.SetBorderSize(0)
		pad.SetTicks(1,1)

	pad.Draw()
	return pad		

def makeLine(x1, y1, x2, y2):
	line = ROOT.TLine(x1, y1, x2, y2)
	line.SetLineWidth(2)
	line.SetLineStyle(7)
	return line

def set1dPlotStyle(hist, color, title = '', title_hist = ''):
	hist.SetMarkerColor(color)
	hist.SetMarkerSize(1.4)
	hist.SetMarkerStyle(20)
	hist.SetFillColor(color)
	hist.SetLineColor(color)
	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(title_hist))
	hist.GetXaxis().SetNdivisions(505)
	hist.GetYaxis().SetTitle("")
	hist.GetYaxis().SetTitleSize(0.08)
	hist.GetYaxis().SetLabelSize(0.08)
	hist.GetYaxis().SetNdivisions(505)
	hist.SetTitle(title)
	return hist

def setFRPlotStyle(hist, color, title = '', title_hist = ''):
	hist.SetMarkerColor(color)
	hist.SetMarkerStyle(20)
	hist.SetLineColor(color)
	hist.SetLineWidth(3)
	hist.SetFillColor(color)
	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(title_hist))
	hist.GetYaxis().SetRangeUser(0., 0.25)
	hist.GetYaxis().SetTitle("FR")
	hist.GetYaxis().SetTitleOffset(0.75)
	hist.GetYaxis().SetTitleSize(0.08)
	hist.GetYaxis().SetLabelSize(0.08)
	hist.SetTitle(title)
	return hist

def setRatioStyle(hist, title_hist='', title='Data/MC', max = 1.99, min = 0.0):
	hist.SetMaximum(max)
	hist.SetMinimum(min)
	hist.SetTitle('')
	hist.GetYaxis().SetNdivisions(502)
	hist.GetYaxis().SetTitle(title)
	hist.GetYaxis().SetLabelSize(0.18)
	hist.GetYaxis().SetTitleSize(0.18)
	hist.GetYaxis().SetTitleOffset(0.3)
	hist.GetXaxis().SetNdivisions(505)
	hist.GetXaxis().SetLabelSize(0.18)
	hist.GetXaxis().SetTitleSize(0.2)
	hist.GetXaxis().SetTitleOffset(1.0)
	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(title_hist))
	return hist

def getXTitle(hist):
	name = hist.GetName()
	if   'NBJets'     in name: return 'N_{b-jets}'
	elif 'NJets'      in name: return 'N_{jets}'
	elif 'AwayJetDR'  in name: return 'dR^{away}'
	elif 'AwayJetPt'  in name: return 'p_{T}^{away}'
	elif 'ClosJetDR'  in name: return 'dR^{close}'
	elif 'ClosJetPt'  in name: return 'p_{T}^{close}'
	elif 'HT'         in name: return 'H_{T}'
	elif 'LepEta'     in name: return '#mu-|#eta|' #'|#eta|_{lep}'
	elif 'LepIso'     in name: return '#mu-pfIso'# 'pfIso_{lep}'
	elif 'LepPt'      in name: return '#mu-pT' #'p_{T}^{lep}'
	elif 'muMET'      in name: return 'MET'
	elif 'muMT'       in name: return 'm_{T}'
	elif 'MTMET30'    in name: return 'm_{T}'
	elif 'MaxJPt'     in name: return 'max. jet-p_{T}'
	elif 'MaxJCPt'    in name: return 'max. jet-p_{T} (corr.)'
	elif 'MaxJRPt'    in name: return 'max. jet-p_{T} (raw)'
	elif 'AllJCPt'    in name: return 'jet-p_{T} (corr.)'
	elif 'AllJRPt'    in name: return 'jet-p_{T} (raw)'
	elif 'AllJEta'    in name: return '|#eta|_{jet}'
	elif 'JCPtJEta'   in name: return '|#eta|_{jet}'
	elif 'JRPtJEta'   in name: return '|#eta|_{jet}'
	elif 'JCPtJPt'    in name: return 'max. jet-p_{T} (corr.)'
	elif 'JRPtJPt'    in name: return 'max. jet-p_{T} (corr.)'
	elif 'DJPtJEta'   in name: return '|#eta|_{jet}'
	elif 'FJPtJEta'   in name: return '|#eta|_{jet}'
	elif 'DJPtJPt'    in name: return 'jet-p_{T} (corr.)'
	elif 'FJPtJPt'    in name: return 'jet-p_{T} (corr.)'
	elif 'DJPtZoom'   in name: return 'jet-p_{T} (corr.) - jet-p_{T} (raw)'
	elif 'FJPtZoom'   in name: return '(jet-p_{T} (corr.) - jet-p_{T} (raw))/jet-p_{T} (raw)'
	elif 'NVertices'  in name: return 'NVertices' #'n_{vertices}'
	elif 'D0'         in name: return 'd_{0}^{lep}'
	else: return name

def getYTitle(hist):
	name = hist.GetName()
	if   'JCPtJEta'   in name: return 'jet-p_{T} (corr.)'
	elif 'JRPtJEta'   in name: return 'jet-p_{T} (raw)'
	elif 'JCPtJPt'    in name: return 'jet-p_{T} (corr.)'
	elif 'JRPtJPt'    in name: return 'jet-p_{T} (raw)'
	elif 'DJPtJEta'   in name: return 'jet-p_{T} (corr.) - jet-p_{T} (raw)'
	elif 'FJPtJEta'   in name: return '(jet-p_{T} (corr.) - jet-p_{T} (raw)/jet-p_{T} (raw)'
	elif 'DJPtJPt'    in name: return 'jet-p_{T} (corr.) - jet-p_{T} (raw)'
	elif 'FJPtJPt'    in name: return '(jet-p_{T} (corr.) - jet-p_{T} (raw))/jet-p_{T} (raw)'
	else: return name

def getSaveName(hist, el = -1):
	name = hist.GetName()
	if isinstance(el, str) and ':' in el: exec("savename = '_'.join(name.split('_')[" + el + "])")
	else: savename = name.split('_')[el]
	return savename

def saveCanvas(canv, pad_plot, outputDir, name, plotlog = 1):
	canv.SaveAs(outputDir + name + '_lin.pdf')
	canv.SaveAs(outputDir + name + '_lin.png')

	if plotlog == 1:
		pad_plot.SetLogy(1)
		canv.SaveAs(outputDir + name + '_log.pdf')
		canv.SaveAs(outputDir + name + '_log.png')
		pad_plot.SetLogy(0)


def PrintScale(canv, outputDir, datasets, lower = [], upper = []):

	write = ""

	pad_plot = makePad('tot')
	pad_plot.cd()

	hists = [ROOT.TH1F("h" + str(i), "H" + str(i), len(datasets), 0, len(datasets)) for i in range(len(datasets))]
	
	for i, set in enumerate(datasets): 
		hists[i].SetBinContent(i+1, set.GetScale())
		hists[i].SetFillColor(getColor(set.GetName()))
		if len(lower) == len(datasets): write = " (" + str(lower[i]) + ", " + str(upper[i]) + ")"
		print "scale " + set.GetName() + " = " + str(set.GetScale()) + write 
	
	hists[0].Draw("hist text")
	for i in range(1,len(hists)): hists[i].Draw("hist text same")
	
	hists[0].SetMaximum(math.ceil(max([set.GetScale() for set in datasets])))
	hists[0].GetYaxis().SetTitle('Scale Factor')
	hists[0].GetXaxis().SetLabelSize(0)
	hists[0].SetTitle('Scale Factors')
	
	y = ROOT.gPad.GetUymin() + 0.15*hists[0].GetXaxis().GetBinWidth(1)
	t = ROOT.TText()
	t.SetTextAngle(90)
	t.SetTextSize(0.08)
	t.SetTextAlign(13)
	t.SetTextColor(ROOT.kWhite)
	for i in range(len(hists)): 
		x = hists[0].GetXaxis().GetBinCenter(i+1) - 0.1
		t.DrawText(x, y, getLegendName(datasets[i].GetName()))
	
	saveCanvas(canv, pad_plot, outputDir + 'plots_1d/', 'scales', 0)
	pad_plot.Close()
	return True



