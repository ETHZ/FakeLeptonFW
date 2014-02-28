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
	elif 'muMT'       in name: return 'N_{b-jets}'
	elif 'MTMET30'    in name: return 'N_{b-jets}'
	elif 'MaxJPt'     in name: return 'max. jet-p_{T}'
	elif 'NVertices'  in name: return 'n_{vertices}'
	elif 'D0'         in name: return 'd_{0}^{lep}'
	elif 'F'          in name: return 'F'
	else: return name

def getSaveName(hist):
	name = hist.GetName()
	return name.split('_')[-1]
