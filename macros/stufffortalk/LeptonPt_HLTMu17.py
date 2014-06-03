import ROOT

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)

file = ROOT.TFile('LeptonPt_HLTMu17.root', 'read')

c= file.Get('c1')

canv = ROOT.TCanvas('c', 'c', 900, 675)
h1 = c.GetListOfPrimitives().At(1)

canv.SetCanvasSize(900, 675)
canv.SetTopMargin(0.1)
canv.SetBottomMargin(0.14)
canv.SetLeftMargin(0.13)
canv.SetRightMargin(0.14)
canv.SetBorderSize(0)
canv.SetTicks(1,1)

h1.GetXaxis().SetLabelSize(0.05)
h1.GetXaxis().SetTitleSize(0.05)
h1.GetXaxis().SetTitle('#mu-pT')
h1.GetYaxis().SetLabelSize(0.05)
h1.SetTitle('')
h1.SetStats(0)

h1.Draw()

canv.SaveAs('LeptonPt_HLTMu17.png')

