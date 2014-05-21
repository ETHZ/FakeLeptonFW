import ROOT

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)

file = ROOT.TFile('muFRdata.root', 'read')

canv = ROOT.TCanvas('c', 'c', 900, 675)
canv.SetTopMargin(0.1)
canv.SetBottomMargin(0.14)
canv.SetLeftMargin(0.13)
canv.SetRightMargin(0.14)
canv.SetBorderSize(0)
canv.SetTicks(1,1)

hist = file.Get('name42')

hist.SetMarkerSize(1.8)
hist.SetMarkerColor(ROOT.kBlack)
hist.GetYaxis().SetTitleOffset(0.8)
hist.Draw('text colz e')

canv.SaveAs('UF_FR_mu.png')

