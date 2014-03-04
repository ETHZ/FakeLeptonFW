import ROOT, helper, commands, sys

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

def getColor(self):
	mycolor = ROOT.TColor()
	if   self.name == 'wjets'        : return mycolor.GetColor(102, 0, 0)
	elif self.name == 'dyjets'       : return mycolor.GetColor(255, 204, 0)
	elif self.name == 'qcdMuEnriched': return mycolor.GetColor(51, 102, 153)
	elif self.name == 'data'         : return ROOT.kBlack
	

class sample:
	def __init__(self, name, infile):
		self.name   = name
		self.file   = ROOT.TFile(infile)
		self.hists  = [self.file.Get(self.name+'/'+i.GetName()) for i in self.file.GetDirectory(self.name).GetListOfKeys() ]
		for i in self.hists:
			i.SetFillColor(getColor(self))
		self.isdata = (self.name == 'data')
		if self.isdata: 
			for i in self.hists: i.SetMarkerStyle(20)
	color  = getColor
	
args = sys.argv
print args
directory = args[1]

data   = sample('data'         , directory+'/data_ratios.root')
wjets  = sample('wjets'        , directory+'/wjets_ratios.root')
dyjets = sample('dyjets'       , directory+'/dyjets_ratios.root')
qcd    = sample('qcdMuEnriched', directory+'/qcdMuEnriched_ratios.root')

mc_samples = []
mc_samples.append(qcd   )
mc_samples.append(wjets )
mc_samples.append(dyjets)


canv = helper.makeCanvas(900, 675)
canv.cd()

leg = helper.makeLegend(0.70, 0.65, 0.95, 0.90)

leg.AddEntry(data  .hists[0], 'Data'    , 'pe')
leg.AddEntry(wjets .hists[0], 'W+Jets'  , 'f' )
leg.AddEntry(dyjets.hists[0], 'DY+Jets' , 'f' )
leg.AddEntry(qcd   .hists[0], 'QCD'     , 'f' )

## plotHists = ['h_Loose_muAwayJetDR', 'h_Loose_muAwayJetPt', 'h_Loose_muClosJetDR', 'h_Loose_muClosJetPt', 'h_Loose_muHT', 'h_Loose_muLepEta', 'h_Loose_muLepIso', 'h_Loose_muLepPt', 'h_Loose_muMET', 'h_Loose_muMETnoMTCut', 'h_Loose_muMT', 'h_Loose_muMTMET30', 'h_Loose_muMaxJPt', 'h_Loose_muNBJets', 'h_Loose_muNJets', 'h_Loose_muNVertices', 'h_Loose_muD0', 'h_Tight_muAwayJetDR', 'h_Tight_muAwayJetPt', 'h_Tight_muClosJetDR', 'h_Tight_muClosJetPt', 'h_Tight_muHT', 'h_Tight_muLepEta', 'h_Tight_muLepIso', 'h_Tight_muLepPt', 'h_Tight_muMET', 'h_Tight_muMETnoMTCut', 'h_Tight_muMT', 'h_Tight_muMTMET30', 'h_Tight_muMaxJPt', 'h_Tight_muNBJets', 'h_Tight_muNJets', 'h_Tight_muNVertices', 'h_Tight_muD0']
plotHists = []


for hist in qcd.hists:
	if hist.GetName() == 'h_muFLoose':
		FR_qcd_den = hist.ProjectionX()
		FR_qcd_den.SetName("FR_qcd_den")
	if hist.GetName() == 'h_muFTight':
		FR_qcd = hist.ProjectionX()
		FR_qcd.SetName("FR_qcd")


for hist in data.hists:

	i = data.hists.index(hist)
	if hist.GetName() == 'h_muFLoose':
		FR_data_den = hist.ProjectionX()
		FR_bg_ds = ROOT.THStack()
		for j, mc in enumerate(mc_samples):
			mc.hists[i].Draw('text colz e')
			helper.saveCanvas(canv, 'test_den_mc'+str(j))
			FR_bg_ds.Add(mc.hists[i],'e')
		
	if hist.GetName() == 'h_muFTight':
		FR_data = hist.ProjectionX()
		FR_bg_ns = ROOT.THStack()
		for j, mc in enumerate(mc_samples):
			mc.hists[i].Draw('text colz e')
			helper.saveCanvas(canv, 'test_num_mc'+str(j))
			print "mc " + str(j) + ": " + str(mc.hists[i].ProjectionX('e').GetBinContent(2))
			FR_bg_ns.Add(mc.hists[i])

	if not hist.GetName() in plotHists: continue

	prepend = ''
	postpend = ''
	if '_Loose_' in hist.GetName(): prepend = 'Loose_'
	if '_Tight_' in hist.GetName(): prepend = 'Tight_'

	stack = ROOT.THStack()
	stackint = 0.
	for mc in mc_samples:
		stackint += mc.hists[i].Integral()
		stack.Add(mc.hists[i])
	yscale = max(stack.GetMaximum(), hist.GetMaximum())
	stack.Draw('hist')
	stack.SetMaximum(1.2*yscale)
	stack.GetXaxis().SetTitle(helper.getXTitle(hist))
	hist.Draw('p e1 same')
	leg.Draw()
	helper.saveCanvas(canv, prepend + helper.getSaveName(hist) + postpend)


#print 'vorher'
#for bin in range(1,FR_qcd.GetNbinsX()+1):
#	print 'bincontent:', FR_bg.GetBinContent(bin), 'binerror:', FR_bg.GetBinError(bin)

FR_data.Divide(FR_data_den)
FR_data.SetMarkerColor(ROOT.kBlack)

FR_bg_ns.Draw()
helper.saveCanvas(canv, "test_num_stack")

FR_bg_ns.Draw("nostack")
FR_bg_num = FR_bg_ns.GetStack().Last().ProjectionX()
FR_bg_num.Draw()
helper.saveCanvas(canv, "test_num_proj")

#FR_bg_ds.Draw("nostack")
FR_bg_ds.Draw()
FR_bg_den = FR_bg_ds.GetStack().Last().ProjectionX()
FR_bg_den.Draw()
helper.saveCanvas(canv, "test_den")
print FR_bg_den.GetBinContent(5)
FR_bg = FR_bg_num

for i in range(1,FR_bg.GetNbinsX()):
	print "bin " + str(i) + ": " + str(FR_bg.GetBinContent(i))

FR_bg.Divide(FR_bg_den)

for i in range(1,FR_bg.GetNbinsX()):
	print "bin " + str(i) + ": " + str(FR_bg.GetBinContent(i))
#	if FR_bg_den.GetBinContent(i)>0:
#		FR_bg.SetBinContent(i, FR_bg_num.GetBinContent(i)*1.0/FR_bg_den.GetBinContent(i))
#		print "bin " + str(i) + ": " + str(FR_bg_num.GetBinContent(i)) + "/" + str(FR_bg_den.GetBinContent(i)) + " = " + str(FR_bg_num.GetBinContent(i)*1.0/FR_bg_den.GetBinContent(i))

FR_bg.Rebuild()
FR_bg.Draw()
helper.saveCanvas(canv, "test")

##FR_bg_num.Draw("nostack")
##helper.saveCanvas(canv, "test_num")
##FR_bg_num = FR_bg_num.GetStack().Last()
##FR_bg.Draw()
##helper.saveCanvas(canv, "test")
##FR_bg_den.Draw("nostack")
##helper.saveCanvas(canv, "test_den")
##FR_bg_test = FR_bg_den.GetStack().Last()
##FR_bg_test.Draw()
##helper.saveCanvas(canv, "test_draw")
##FR_bg.Divide(FR_bg_test)
##FR_bg.Draw()
##helper.saveCanvas(canv, "test_div")
#FR_bg.SetMarkerSize(1.2)
#FR_bg.SetMarkerStyle(20)
#FR_bg.SetMarkerColor(ROOT.kRed)

FR_qcd.Divide(FR_qcd_den)
FR_qcd.SetMarkerSize(1.2)
FR_qcd.SetMarkerStyle(20)
FR_qcd.SetMarkerColor(getColor(qcd))

#print 'nachher'
#for bin in range(1,FR_qcd.GetNbinsX()+1):
#	print 'bincontent:', FR_bg.GetBinContent(bin), 'binerror:', FR_bg.GetBinError(bin)
#	#print 'dencontetn:', FR_bg_den.GetBinContent(bin), 'denerror:', FR_bg_den.GetBinError(bin)

FR_data.Draw("pe")
FR_bg.Draw("p e same")
FR_qcd.Draw("p e same")

FR_data.SetMaximum(0.3) 

legend = helper.makeLegend(0.15, 0.65, 0.4, 0.90)
legend.AddEntry(FR_data, 'Data'  , 'pe')
legend.AddEntry(FR_bg, 'QCD + EW', 'pe')
legend.AddEntry(FR_qcd, 'QCD'    , 'pe')
legend.Draw()

helper.saveCanvas(canv, "muFakeRatio")


