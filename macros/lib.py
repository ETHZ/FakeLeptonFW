import ROOT, math, os, shutil


def getScaling(outputDir, printall = 0):

	list = ['unweighted', 'fit_weighted', 'qcd_weighted', 'qcdwjets_weighted']	
	struct = outputDir.split('/')
	result = ''

	if printall: return list

	for scaling in list:
		if scaling == struct[-3] or scaling == struct[-2]:
			result = scaling

	return result


def getModule(outputDir, printall = 0):

	list   = ['plots_1d', 'plots_2d', 'zoom_met', 'zoom_jpt', 'fakerates_1d', 'fakerates_2d', 'adhoc']
	struct = outputDir.split('/')
	result = ''

	if printall: return list

	for module in list:
		if module == struct[-2]:
			result = module
	
	return result


def CreateOutputFolders(outputDir):

	afsfolder = "/afs/cern.ch/user/c/cheidegg/www/workinggroup/"
	struct = outputDir.split('/')
	stripoff = False

	if getScaling(outputDir) == '': second_folder = getScaling(outputDir,1)
	else: second_folder = []

	if getModule(outputDir) == '':  final_folder = getModule(outputDir,1)
	else: final_folder = []

	for i in range(1,len(struct)): 
		if not os.path.exists('/'.join(struct[0:i])): 
			os.mkdir('/'.join(struct[0:i]))

	for i in range(2,len(struct)): 
		if not os.path.exists(afsfolder + '/'.join(struct[1:i])): 
			os.mkdir(afsfolder + '/'.join(struct[1:i]))
		if not struct[i] in getModule(outputDir,1): 
			shutil.copyfile('README.html', afsfolder + '/'.join(struct[1:i]) + '/README.html')

	if not second_folder == []:
		for folder in second_folder:
			if not os.path.exists(outputDir + folder):
				os.mkdir(outputDir + folder)
			if not os.path.exists(afsfolder + '/'.join(struct[1:]) + folder): 
				os.mkdir(afsfolder + '/'.join(struct[1:]) + folder)

	if not final_folder == []:
		for folder in final_folder:
			if not os.path.exists(outputDir + folder): 
				os.mkdir(outputDir + folder)
			if not os.path.exists(afsfolder + '/'.join(struct[1:]) + folder): 
				os.mkdir(afsfolder + '/'.join(struct[1:]) + folder)
				shutil.copyfile('index.php', afsfolder + '/'.join(struct[1:]) + folder + '/index.php')
	else:
		stripoff = True
		shutil.copyfile('index.php', afsfolder + '/'.join(struct[1:]) + 'index.php')

	if stripoff == True: outputDir = '/'.join(struct[:-2]) + '/'

	return outputDir
	


def getColor(name):
	mycolor = ROOT.TColor()
	if   name == 'el_data'            : return ROOT.kBlack
	elif name == 'mu_data'            : return ROOT.kBlack
	elif name == 'el_wjets'           : return mycolor.GetColor(102,   0,   0)
	elif name == 'mu_wjets'           : return mycolor.GetColor(102,   0,   0)
	elif name == 'el_dyjets50'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_dyjets50'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'el_dyjets10'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_dyjets10'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_qcdmuenr'        : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdelenr30'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdelenr80'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdelenr250'     : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdelenr350'     : return mycolor.GetColor( 51, 102, 153)
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
	if   name == 'el_data'            : return 'Data'
	elif name == 'mu_data'            : return 'Data'
	elif name == 'el_wjets'           : return 'W + Jets'
	elif name == 'mu_wjets'           : return 'W + Jets'
	elif name == 'el_dyjets50'        : return 'DY + Jets'
	elif name == 'mu_dyjets50'        : return 'DY + Jets'
	elif name == 'el_dyjets10'        : return 'DY + Jets'
	elif name == 'mu_dyjets10'        : return 'DY + Jets'
	elif name == 'mu_qcdmuenr'        : return 'QCD'
	elif name == 'el_qcdelenr30'      : return 'QCD'
	elif name == 'el_qcdelenr80'      : return 'QCD'
	elif name == 'el_qcdelenr250'     : return 'QCD'
	elif name == 'el_qcdelenr350'     : return 'QCD'
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

def set1dPlotStyle(dataType, hist, color, title = '', title_hist = ''):
	hist.SetMarkerColor(color)
	hist.SetMarkerSize(1.4)
	hist.SetMarkerStyle(20)
	hist.SetFillColor(color)
	hist.SetLineColor(color)
	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(dataType, title_hist))
	hist.GetXaxis().SetNdivisions(505)
	hist.GetYaxis().SetTitle("")
	hist.GetYaxis().SetTitleSize(0.08)
	hist.GetYaxis().SetLabelSize(0.08)
	hist.GetYaxis().SetNdivisions(505)
	hist.SetTitle(title)
	return hist

def setFRPlotStyle(dataType, hist, color, title = '', title_hist = ''):
	hist.SetMarkerColor(color)
	hist.SetMarkerStyle(20)
	hist.SetLineColor(color)
	hist.SetLineWidth(3)
	hist.SetFillColor(color)
	hist.SetMinimum(0.0001)
	if dataType == 'el': hist.SetMaximum(0.5)
	else               : hist.SetMaximum(0.4)
	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(dataType, title_hist))
	hist.GetYaxis().SetTitle("FR")
	hist.GetYaxis().SetTitleOffset(0.75)
	hist.GetYaxis().SetTitleSize(0.08)
	hist.GetYaxis().SetLabelSize(0.08)
	hist.SetTitle(title)
	return hist

def setRatioStyle(dataType, hist, title_hist='', title='Data/MC', max = 1.99, min = 0.0):
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
	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(dataType, title_hist))
	return hist

def getXTitle(dataType, hist):
	name = hist.GetName()
	if dataType == 'el': lepton = 'e'
	else               : lepton = '#mu'
	if   'NBJets'     in name: return 'N_{b-jets}'
	elif 'NJets'      in name: return 'N_{jets}'
	elif 'AwayJetDR'  in name: return 'dR^{away}'
	elif 'AwayJetPt'  in name: return 'p_{T}^{away}'
	elif 'ClosJetDR'  in name: return 'dR^{close}'
	elif 'ClosJetPt'  in name: return 'p_{T}^{close}'
	elif 'HT'         in name: return 'H_{T}'
	elif 'LepEta'     in name: return lepton + '-|#eta|' #'|#eta|_{lep}'
	elif 'LepIso'     in name: return lepton + '-pfIso'# 'pfIso_{lep}'
	elif 'LepPt'      in name: return lepton + '-pT' #'p_{T}^{lep}'
	elif '_MET'       in name: return 'MET'
	elif '_MT'        in name: return 'm_{T}'
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

def doErrorPropagation(value_x, error_x, value_y, error_y, operation = 1):

	if   operation == 1: # addition
		derivative_x =  1.0
		derivative_y =  1.0
	elif operation == 2: # subtraction
		derivative_x =  1.0
		derivative_y = -1.0
	elif operation == 3: # multiplication
		derivative_x = value_y
		derivative_y = value_x
	elif operation == 4: # division
		if value_y != 0:
			derivative_x = 1.0/value_y
			derivative_y = -value_x / value_y**2
		else:
			derivative_x = 0.0
			derivative_y = 0.0
	else:
		return False
		
	return math.sqrt(derivative_x**2 * error_x**2 + derivative_y**2 * error_y**2)


def doTH1ErrorPropagation(hist, hist1, hist2, operation):

	for i in range(1,hist.GetNbinsX()+1):
		hist.SetBinError(i, doErrorPropagation(hist1.GetBinContent(i), hist1.GetBinError(i), hist2.GetBinContent(i), hist2.GetBinError(i), operation))
	return hist

def doTH2ErrorPropagation(hist, hist1, hist2, operation):

	for i in range(hist.GetNbinsX()+2, (hist.GetNbinsX()+2)*(hist.GetNbinsY()+1)):
		print "bin " + str(i) + " has value " + str(hist.GetBinContent(i)) + " and error " + str(hist.GetBinError(i))
		hist.SetBinError(i, doErrorPropagation(hist1.GetBinContent(i), hist1.GetBinError(i), hist2.GetBinContent(i), hist2.GetBinError(i), operation))
		print "bin " + str(i) + " has value " + str(hist.GetBinContent(i)) + " and error " + str(hist.GetBinError(i))
	return hist

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



