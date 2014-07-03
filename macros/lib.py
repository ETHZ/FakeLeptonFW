import ROOT, math, os, shutil


#___________________________________________________________________________________
def getScaling(outputDir, printall = 0):
	#
	# either return the current scaling from output directory or return all scalings
	#
	# this function takes the following paramters:
	# outputDir...basic output directory
	# printall....if 1 then we return the full list of scalings

	list = ['unweighted', 'fit_weighted', 'qcd_weighted', 'qcdwjets_weighted']	
	struct = outputDir.split('/')
	result = ''

	if printall: return list

	for scaling in list:
		if scaling == struct[-3] or scaling == struct[-2]:
			result = scaling

	return result


#___________________________________________________________________________________
def getModule(outputDir, printall = 0):
	#
	# either return current module from output directory or return all modules
	#
	# this function takes the following paramters:
	# outputDir...basic output directory
	# printall....if 1 then we return the full list of modules

	list   = ['plots_1d', 'plots_2d', 'zoom_met', 'zoom_jpt', 'fakerates_1d', 'fakerates_2d', 'fakerates_2dct', 'adhoc', 'compare', 'closure']
	struct = outputDir.split('/')
	result = ''

	if printall: return list

	for module in list:
		if module == struct[-2]:
			result = module
	
	return result


#___________________________________________________________________________________
def CreateOutputFolders(outputDir):
	#
	# create the output directory structure both on Plots/ and on the afs folder and copy readme and index files
	#
	# this function takes the following paramters:
	# outputDir...basic output directory

	afsfolder = "/afs/cern.ch/user/c/cheidegg/www/workinggroup/"
	struct = outputDir.split('/')
	stripoff = False

	# get second last foler (= scaling) to produce

	if getScaling(outputDir) == '': second_folder = getScaling(outputDir,1)
	else: second_folder = []

	# get last folder (= module) to produce

	if getModule(outputDir) == '':  final_folder = getModule(outputDir,1)
	else: final_folder = []

	# produce output folder structure

	for i in range(1,len(struct)): 
		if not os.path.exists('/'.join(struct[0:i])): 
			os.mkdir('/'.join(struct[0:i]))

	# produce afs folder strucuture and copy readme file

	for i in range(2,len(struct)): 
		if not os.path.exists(afsfolder + '/'.join(struct[1:i])): 
			os.mkdir(afsfolder + '/'.join(struct[1:i]))
		if not struct[i] in getModule(outputDir,1): 
			shutil.copyfile('README.html', afsfolder + '/'.join(struct[1:i]) + '/README.html')

	# if necessary, produce second last folder

	if not second_folder == []:
		for folder in second_folder:
			if not os.path.exists(outputDir + folder):
				os.mkdir(outputDir + folder)
			if not os.path.exists(afsfolder + '/'.join(struct[1:]) + folder): 
				os.mkdir(afsfolder + '/'.join(struct[1:]) + folder)

	# if necessary, produce last folder and copy index file

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
	

#___________________________________________________________________________________
def getColor(name):
	#
	# return the color according to a specific (legend) name
	#
	# this function takes the following paramters:
	# name........(dataset) name

	mycolor = ROOT.TColor()

	if   name == 'el_data'            : return ROOT.kBlack
	elif name == 'mu_data'            : return ROOT.kBlack
	elif name == 'mu_data1'           : return ROOT.kBlack
	elif name == 'mu_data2'           : return ROOT.kBlack
	elif name == 'mu_data3'           : return ROOT.kBlack
	elif name == 'mu_data4'           : return ROOT.kBlack
	elif name == 'mu_data5'           : return ROOT.kBlack
	elif name == 'mu_data6'           : return ROOT.kBlack
	elif name == 'mu_data7'           : return ROOT.kBlack
	elif name == 'el_wjets'           : return mycolor.GetColor(102,   0,   0)
	elif name == 'mu_wjets'           : return mycolor.GetColor(102,   0,   0)
	elif name == 'el_dyjets50'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_dyjets50'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'el_dyjets10'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_dyjets10'        : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_qcdmuenr'        : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdtot50'        : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot80'        : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot120'       : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot170'       : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot170v2'     : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot300'       : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot300v2'     : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdtot300v3'     : return mycolor.GetColor( 15, 106, 196)
	elif name == 'el_qcdemenr20'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr30'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr80'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr170'     : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr250'     : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr350'     : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdbctoe20'      : return mycolor.GetColor( 12,  57, 102)
	elif name == 'el_qcdbctoe30'      : return mycolor.GetColor( 12,  57, 102)
	elif name == 'el_qcdbctoe80'      : return mycolor.GetColor( 12,  57, 102)
	elif name == 'el_wjets_g'         : return mycolor.GetColor(102,   0,   0)
	elif name == 'mu_wjets_g'         : return mycolor.GetColor(102,   0,   0)
	elif name == 'el_dyjets50_g'      : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_dyjets50_g'      : return mycolor.GetColor(255, 204,   0)
	elif name == 'el_dyjets10_g'      : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_dyjets10_g'      : return mycolor.GetColor(255, 204,   0)
	elif name == 'mu_ttbar_g'         : return mycolor.GetColor( 51, 153,  58)
	elif name == 'el_ttbar_g'         : return mycolor.GetColor( 51, 153,  58)
	elif name == 'mu_qcdmuenr_g'      : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr20_g'    : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr30_g'    : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdemenr80_g'    : return mycolor.GetColor( 51, 102, 153)
	elif name == 'el_qcdbctoe20_g'    : return mycolor.GetColor( 12,  57, 102)
	elif name == 'el_qcdbctoe30_g'    : return mycolor.GetColor( 12,  57, 102)
	elif name == 'el_qcdbctoe80_g'    : return mycolor.GetColor( 12,  57, 102)
	elif name == 'qcd'                : return mycolor.GetColor( 51, 102, 153)
	elif name == 'mc'                 : return mycolor.GetColor(191,  11,  11)
	elif name == 'totbg'              : return mycolor.GetColor(191,  11,  11)
	elif name == 'data'               : return ROOT.kBlack
	elif name == 'data_num'               : return ROOT.kBlack
	elif name == 'data_den'               : return ROOT.kBlack
	elif name == 'datamcsub'          : return ROOT.kOrange
	elif name == 'datamcsub_central1' : return mycolor.GetColor( 51, 153,  51)
	elif name == 'datamcsub_lower1'   : return mycolor.GetColor(106,  90, 205)
	elif name == 'datamcsub_upper1'   : return mycolor.GetColor(  0,   0, 128)
	elif name == 'datamcsub_central2' : return ROOT.kRed
	elif name == 'datamcsub_central3' : return ROOT.kPink
	elif name == 'datamcsub_ufsupp'   : return ROOT.kPink
	elif name == 'data30'             : return ROOT.kBlack
	elif name == 'data40'             : return ROOT.kRed
	elif name == 'data50'             : return ROOT.kBlue
	elif name == 'data60'             : return ROOT.kGreen
	elif name == 'dataJCPt'           : return ROOT.kRed
	elif name == 'dataJRPt'           : return ROOT.kBlue
	elif name == 'wjets'              : return mycolor.GetColor(102,   0,   0)
	elif name == 'doublemu'           : return ROOT.kBlack
	elif name == 'doubleel'           : return ROOT.kBlack
	elif name == 'ttjets_sl'          : return mycolor.GetColor( 51, 153,  58)
	elif name == 'ttjets_fl'          : return mycolor.GetColor(102, 153,  58)
	elif name == 'ttwjets'            : return mycolor.GetColor(102, 102, 102)
	elif name == 'ttzjets'            : return mycolor.GetColor(102, 102, 102)
	elif name == 'rares'              : return mycolor.GetColor(102, 102, 102)
	elif name == 'dyjets'             : return mycolor.GetColor(255, 204,   0)

#___________________________________________________________________________________
def getSampleColor(self):
	# 
	# return the color according to the sample name
	#
	# this function takes the following paramters:
	# self........dataset

	return getColor(self.name)


#___________________________________________________________________________________
def getLegendName(name):
	# 
	# return the legend name for a data sample
	# 
	# this function takes the following paramters:
	# name........dataset name

	if   name == 'el_data'            : return 'Data'
	elif name == 'mu_data'            : return 'Data'
	elif name == 'mu_data1'           : return 'Data'
	elif name == 'mu_data2'           : return 'Data'
	elif name == 'mu_data3'           : return 'Data'
	elif name == 'mu_data4'           : return 'Data'
	elif name == 'mu_data5'           : return 'Data'
	elif name == 'mu_data6'           : return 'Data'
	elif name == 'mu_data7'           : return 'Data'
	elif name == 'el_wjets'           : return 'W + Jets'
	elif name == 'mu_wjets'           : return 'W + Jets'
	elif name == 'el_dyjets50'        : return 'DY + Jets'
	elif name == 'mu_dyjets50'        : return 'DY + Jets'
	elif name == 'el_dyjets10'        : return 'DY + Jets'
	elif name == 'mu_dyjets10'        : return 'DY + Jets'
	elif name == 'mu_qcdmuenr'        : return 'QCD'
	elif name == 'el_qcdtot50'        : return 'QCD (tot)'
	elif name == 'el_qcdtot80'        : return 'QCD (tot)'
	elif name == 'el_qcdtot120'       : return 'QCD (tot)'
	elif name == 'el_qcdtot170'       : return 'QCD (tot)'
	elif name == 'el_qcdtot170v2'     : return 'QCD (tot)'
	elif name == 'el_qcdtot300'       : return 'QCD (tot)'
	elif name == 'el_qcdtot300v2'     : return 'QCD (tot)'
	elif name == 'el_qcdtot300v3'     : return 'QCD (tot)'
	elif name == 'el_qcdemenr20'      : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr30'      : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr80'      : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr170'     : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr250'     : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr350'     : return 'QCD (EMenr)'
	elif name == 'el_qcdbctoe20'      : return 'QCD (BCtoE)'
	elif name == 'el_qcdbctoe30'      : return 'QCD (BCtoE)'
	elif name == 'el_qcdbctoe80'      : return 'QCD (BCtoE)'
	elif name == 'el_wjets_g'         : return 'W + Jets'
	elif name == 'mu_wjets_g'         : return 'W + Jets'
	elif name == 'el_dyjets50_g'      : return 'DY + Jets'
	elif name == 'mu_dyjets50_g'      : return 'DY + Jets'
	elif name == 'el_dyjets10_g'      : return 'DY + Jets'
	elif name == 'mu_dyjets10_g'      : return 'DY + Jets'
	elif name == 'mu_ttbar_g'         : return 'TTBar (SL)'
	elif name == 'el_ttbar_g'         : return 'TTBar (SL)'
	elif name == 'mu_qcdmuenr_g'      : return 'QCD'
	elif name == 'el_qcdemenr20_g'    : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr30_g'    : return 'QCD (EMenr)'
	elif name == 'el_qcdemenr80_g'    : return 'QCD (EMenr)'
	elif name == 'el_qcdbctoe20_g'    : return 'QCD (BCtoE)'
	elif name == 'el_qcdbctoe30_g'    : return 'QCD (BCtoE)'
	elif name == 'el_qcdbctoe80_g'    : return 'QCD (BCtoE)'
	elif name == 'ttbar_g_0'          : return 'TTBar (all)'
	elif name == 'ttbar_g_1'          : return 'TTBar (W)'
	elif name == 'ttbar_g_2'          : return 'TTBar (B)'
	elif name == 'ttbar_g_3'          : return 'TTBar (C)'
	elif name == 'ttbar_g_4'          : return 'TTBar (U/D/S)'
	elif name == 'ttbar_g_5'          : return 'TTBar (unm.)'
	elif name == 'qcd_g_0'            : return 'QCD (all)'
	elif name == 'qcd_g_1'            : return 'QCD (W)'
	elif name == 'qcd_g_2'            : return 'QCD (B)'
	elif name == 'qcd_g_3'            : return 'QCD (C)'
	elif name == 'qcd_g_4'            : return 'QCD (U/D/S)'
	elif name == 'qcd_g_5'            : return 'QCD (unm.)'
	elif name == 'qcd'                : return 'QCD'
	elif name == 'mc'                 : return 'MC'
	elif name == 'totbg'              : return 'QCD + EW'
	elif name == 'data'               : return 'Data'
	elif name == 'data_num'               : return 'Data'
	elif name == 'data_den'               : return 'Data'
	elif name == 'datamcsub'          : return 'Data - EW'
	elif name == 'datamcsub_central1' : return 'Data - EW (ETH)'
	elif name == 'datamcsub_lower1'   : return 'Data - EW (ETH lower)'
	elif name == 'datamcsub_upper1'   : return 'Data - EW (ETH upper)'
	elif name == 'datamcsub_central2' : return 'Data - EW (UCSx)'
	elif name == 'datamcsub_central3' : return 'Data - EW (CERN)'
	elif name == 'datamcsub_ufsupp'   : return 'Data - EW (UF)'
	elif name == 'data30'             : return 'Data (30GeV)'
	elif name == 'data40'             : return 'Data (40GeV)'
	elif name == 'data50'             : return 'Data (50GeV)'
	elif name == 'data60'             : return 'Data (60GeV)'
	elif name == 'dataJCPt'           : return 'Data (corr. Jet Pt)'
	elif name == 'dataJRPt'           : return 'Data (raw Jet Pt)'


#___________________________________________________________________________________
def makeLegend(x1,y1,x2,y2):
	#
	# draw a legend
	# 
	# this function takes the following paramters:
	# x1..........x coordinate of bottom left corner
	# y1..........y coordinate of bottom left corner
	# x2..........x coordinate of top right corner
	# y2..........y coordiante of top right corner

	leg = ROOT.TLegend(x1,y1,x2,y2)
	leg.SetFillColor(ROOT.kWhite)
	leg.SetTextFont(42)
	leg.SetBorderSize(0)
	leg.SetMargin(0.35)
	leg.SetTextSize(0.07)

	return leg


#___________________________________________________________________________________
def makeCanvas(x, y, name='c', setmargin = 1):
	# 
	# draw a canvas
	# 
	# this function takes the following paramters:
	# x...........size along x axis
	# y...........size along y axis
	# name........canvas name
	# setmargin...1 if we shall set default margins

	canv = ROOT.TCanvas(name, 'c', x, y)
	canv.SetTicks(1,1)
	if setmargin == 1:
		canv.SetBottomMargin(0.15)
		canv.SetLeftMargin(0.12)
		canv.SetRightMargin(0.03)
		canv.SetTopMargin(0.07)

	return canv


#___________________________________________________________________________________
def makePad(which):
	# 
	# drwa a pad
	# 
	# this function takes the following paramters:
	# which.......'plot' for plot pad above ratio, 'ratio' for ratio pad, 'tot' for pad without ratio

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


#___________________________________________________________________________________
def makeLine(x1, y1, x2, y2):
	# 
	# drwa a line
	#
	# this function takes the following paramters:
	# x1..........x coordinate of point 1
	# y1..........y coordinate of point 1 
	# x2..........x coordinate of point 2 
	# y2..........y coordiante of point 2 

	line = ROOT.TLine(x1, y1, x2, y2)
	line.SetLineWidth(2)
	line.SetLineStyle(7)

	return line


#___________________________________________________________________________________
def set1dPlotStyle(dataType, hist, color, title = '', title_hist = '', ytitle = ''):
	#
	# set default style of the 1d plots
	#
	# this function takes the following parameters:
	# dataType....type of the lepton ('mu', 'el')
	# hist........histogram to set style to
	# color.......marker, line, fill color to set
	# title.......title for the histogram
	# title_hist..histogram to take X axis title from
	# ytitle......title to set to Y axis

	hist.SetMarkerColor(color)
	hist.SetMarkerSize(1.4)
	hist.SetMarkerStyle(20)
	hist.SetFillColor(color)
	hist.SetLineColor(color)

	if not title_hist=='': hist.GetXaxis().SetTitle(getXTitle(dataType, title_hist))
	hist.GetXaxis().SetNdivisions(505)
	hist.GetYaxis().SetTitle(ytitle)
	hist.GetYaxis().SetTitleSize(0.08)
	hist.GetYaxis().SetLabelSize(0.08)
	hist.GetYaxis().SetNdivisions(505)
	hist.SetTitle(title)

	return hist


#___________________________________________________________________________________
def setFRPlotStyle(dataType, hist, color, title = '', title_hist = ''):
	# 
	# set default style of the fake rate 1d plots
	#
	# this function takes the following parameters:
	# dataType....type of the lepton ('mu', 'el')
	# hist........histogram to set style to
	# color.......marker, line, fill color to set
	# title.......title for the histogram
	# title_hist..histogram to take X axis title from

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


#___________________________________________________________________________________
def setRatioStyle(dataType, hist, title_hist='', title='Data/MC', max = 2.0, min = 0.0):
	# 
	# set default style of the ratio plots
	#
	# this function takes the following parameters:
	# dataType....type of the lepton ('mu', 'el')
	# hist........histogram to set style to
	# title_hist..histogram to take X axis title from
	# title.......title to set to Y axis
	# max.........upper limit for Y axis
	# min.........lower limit for Y axis

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


#___________________________________________________________________________________
def getXTitle(dataType, hist):
	#
	# return the title of the x axis for any histogram
	#
	# this function takes the following parameters:
	# dataType....type of the lepton ('mu', 'el')
	# hist........histogram to get X axis title from

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
	elif 'MaxJCSV'    in name: return 'max. b-tag'
	elif 'AllJCPt'    in name: return 'jet-p_{T} (corr.)'
	elif 'AllJRPt'    in name: return 'jet-p_{T} (raw)'
	elif 'AllJEta'    in name: return '|#eta|_{jet}'
	elif 'AllJCSV'    in name: return 'b-tag'
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


#___________________________________________________________________________________
def getYTitle(hist):
	#
	# return the title of the y axis for 2d histogram
	#
	# this function takes the following parameters:
	# hist........histogram to get Y axis title from

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


#___________________________________________________________________________________
def doErrorPropagation(value_x, error_x, value_y, error_y, operation = 1):
	# 
	# perform error propagation for a function depending on two variables
	#
	# this function takes the following parameters:
	# value_x.....value of variable 1
	# error_x.....error of variable 1
	# value_y.....value of variable 2
	# error_y.....error of variable 2
	# operation...1 for addition, 2 for subtraction, 3 for multiplication, 4 for division

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


#___________________________________________________________________________________
def doTH1ErrorPropagation(hist, hist1, hist2, operation):
	#
	# perform error propagation for a given operation of 1d histograms
	# 
	# this function takes the following parameters:
	# hist........histogram containing the result of the operation
	# hist1.......one of the input histograms
	# hist2.......the other one of the input histograms
	# operation...1 for addition, 2 for subtraction, 3 for multiplication, 4 for division

	for i in range(1,hist.GetNbinsX()+1):
		hist.SetBinError(i, doErrorPropagation(hist1.GetBinContent(i), hist1.GetBinError(i), hist2.GetBinContent(i), hist2.GetBinError(i), operation))
	return hist


#___________________________________________________________________________________
def doTH2ErrorPropagation(hist, hist1, hist2, operation):
	# 
	# perform error propagation for a given operation of 2d histograms
	#
	# this function takes the following parameters:
	# hist........histogram containing the result of the operation
	# hist1.......one of the input histograms
	# hist2.......the other one of the input histograms
	# operation...1 for addition, 2 for subtraction, 3 for multiplication, 4 for division

	for i in range(hist.GetNbinsX()+2, (hist.GetNbinsX()+2)*(hist.GetNbinsY()+1)):
		#print "bin " + str(i) + " has value " + str(hist.GetBinContent(i)) + " and error " + str(hist.GetBinError(i))
		hist.SetBinError(i, doErrorPropagation(hist1.GetBinContent(i), hist1.GetBinError(i), hist2.GetBinContent(i), hist2.GetBinError(i), operation))
		#print "bin " + str(i) + " has value " + str(hist.GetBinContent(i)) + " and error " + str(hist.GetBinError(i))
	return hist


#___________________________________________________________________________________
def getSaveName(hist, el = -1):
	#
	# strip off selected element from the historam name to create the save name
	#
	# this function takes the following parameters:
	# hist........histogram to get save name from
	# el..........element to strip off

	name = hist.GetName()
	if isinstance(el, str) and ':' in el: exec("savename = '_'.join(name.split('_')[" + el + "])")
	else: savename = name.split('_')[el]

	return savename


#___________________________________________________________________________________
def saveCanvas(canv, pad_plot, outputDir, name, plotlog = True, exportinroot = False):
	#
	# save canvas, linearly and log scale, png and pdf, maybe root
	#
	# this function takes the following parameters:
	# canv........canvas to plot
	# pad_plot....pad to plot
	# outputDir...full output directory
	# name........name for the output file
	# plotlog.....True if we also want to plot log-scale
	# exportinroot..True if we also want to export in root file

	canv.SaveAs(outputDir + name + '_lin.pdf')
	canv.SaveAs(outputDir + name + '_lin.png')

	if plotlog:
		pad_plot.SetLogy(1)
		canv.SaveAs(outputDir + name + '_log.pdf')
		canv.SaveAs(outputDir + name + '_log.png')
		pad_plot.SetLogy(0)

	if exportinroot:
		canv.SaveAs(outputDir + name + '.root')


#___________________________________________________________________________________
def PrintScale(canv, outputDir, datasets, lower = [], upper = []):
	#
	# create the plots that visualize the scale of selected samples
	#
	# this function takes the following parameters:
	# canv........canvas to plot
	# outputDir...basic output directory
	# datasets....datasets to plot
	# lower.......list of lower bounds of the scale
	# upper.......list of upper bounds of the scale

	write = ''
	pad_plot = makePad('tot')
	pad_plot.cd()

	# create histogram for every dataset such that we can set different colors for different bins

	hists = [ROOT.TH1F("h" + str(i), "H" + str(i), len(datasets), 0, len(datasets)) for i in range(len(datasets))]
	
	for i, set in enumerate(datasets): 
		hists[i].SetBinContent(i+1, set.GetScale())
		hists[i].SetFillColor(getColor(set.GetName()))
		if len(lower) == len(datasets): write = " (" + str(lower[i]) + ", " + str(upper[i]) + ")"
		print "scale " + set.GetName() + " = " + str(set.GetScale()) + write 
	
	# draw histograms

	hists[0].Draw("hist text")
	for i in range(1,len(hists)): hists[i].Draw("hist text same")
	
	hists[0].SetMaximum(math.ceil(max([set.GetScale() for set in datasets])))
	hists[0].GetYaxis().SetTitle('Scale Factor')
	hists[0].GetXaxis().SetLabelSize(0)
	hists[0].SetTitle('Scale Factors')

	# draw vertical legend names
	
	y = ROOT.gPad.GetUymin() + 0.15*hists[0].GetXaxis().GetBinWidth(1)
	t = ROOT.TText()
	t.SetTextAngle(90)
	t.SetTextSize(0.08)
	t.SetTextAlign(13)
	t.SetTextColor(ROOT.kWhite)
	for i in range(len(hists)): 
		x = hists[0].GetXaxis().GetBinCenter(i+1) - 0.1
		t.DrawText(x, y, getLegendName(datasets[i].GetName()))
	
	# save plot

	saveCanvas(canv, pad_plot, outputDir + 'plots_1d/', 'scales', False)
	pad_plot.Close()
	return True



