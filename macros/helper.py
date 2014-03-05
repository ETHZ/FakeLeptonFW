import ROOT

def makeLegend(x1,y1,x2,y2):
	leg = ROOT.TLegend(x1,y1,x2,y2)
	leg.SetFillColor(ROOT.kWhite)
	leg.SetTextFont(42)
	leg.SetBorderSize(0)
	leg.SetMargin(0.35)
	leg.SetTextSize(0.04)
	return leg

def makeCanvas(x, y):
	canv = ROOT.TCanvas('c', 'c', x, y)
	canv.SetTicks(1,1)
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
		pad.SetTicks(1,1)

	if which == 'ratio':
		pad.SetPad(0.0, 0.0, 1.0, 0.3)
		pad.SetBorderSize(0)
		pad.SetTopMargin(0.0)
		pad.SetBottomMargin(0.4)
		pad.SetTicks(1,1)

	pad.Draw()
	return pad		

def makeLine(x1, y1, x2, y2):
	line = ROOT.TLine(x1, y1, x2, y2)
	line.SetLineWidth(2)
	line.SetLineStyle(7)
	return line

def setRatioStyle(hist, titlehist=''):
	if titlehist=='': titlehist = hist
	hist.SetTitle('')
	hist.GetYaxis().SetNdivisions(505)
	hist.GetYaxis().SetTitle('Data/Pred.')
	hist.GetYaxis().SetTitleSize(0.09)
	hist.GetYaxis().SetTitleOffset(0.35)
	hist.GetYaxis().SetLabelSize(0.09)
	hist.GetXaxis().SetNdivisions(505)
	hist.GetXaxis().SetLabelSize(0.11)
	hist.GetXaxis().SetTitle(getXTitle(titlehist))
	hist.GetXaxis().SetTitleSize(0.11)
	hist.GetXaxis().SetTitleOffset(1.0)
	hist.SetMaximum(1.99)
	hist.SetMinimum(0.0)
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
	elif 'LepEta'     in name: return '|#eta|_{lep}'
	elif 'LepIso'     in name: return 'pfIso_{lep}'
	elif 'LepPt'      in name: return 'p_{T}^{lep}'
	elif 'muMET'      in name: return 'MET'
	elif 'muMT'       in name: return 'm_{T}'
	elif 'MTMET30'    in name: return 'm_{T}'
	elif 'MaxJPt'     in name: return 'max. jet-p_{T}'
	elif 'NVertices'  in name: return 'n_{vertices}'
	elif 'D0'         in name: return 'd_{0}^{lep}'
	elif 'F'          in name: return 'F'
	else: return name

def getSaveName(hist):
	name = hist.GetName()
	return name.split('_')[-1]

def saveCanvas(canv, name):
	canv.SaveAs(name + '.pdf')
	canv.SaveAs(name + '.png')


