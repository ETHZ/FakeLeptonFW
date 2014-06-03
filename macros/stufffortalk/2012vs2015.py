import ROOT

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)

file = ROOT.TFile('2012vs2015.root', 'read')

c= file.Get('c1')

canv = ROOT.TCanvas('c', 'c', 900, 675)
h1 = c.GetListOfPrimitives().At(1)
h2 = c.GetListOfPrimitives().At(3)

leg = ROOT.TLegend(0.3, 0.25, 0.45, 0.4)
leg.AddEntry(h2, '2012', 'l')
leg.AddEntry(h1, '2015', 'l')
leg.SetFillColor(ROOT.kWhite)
leg.SetTextFont(42)
leg.SetBorderSize(0)
leg.SetMargin(0.35)
leg.SetTextSize(0.05)

canv.SetCanvasSize(900, 675)
canv.SetTopMargin(0.1)
canv.SetBottomMargin(0.14)
canv.SetLeftMargin(0.13)
canv.SetRightMargin(0.14)
canv.SetBorderSize(0)
canv.SetTicks(1,1)

h1.GetXaxis().SetLabelSize(0.05)
h1.GetXaxis().SetTitleSize(0.05)
h1.GetXaxis().SetTitle('#mu-pfIso')
h1.GetYaxis().SetLabelSize(0.05)
h1.SetTitle('')
h1.SetStats(0)

h1.Draw()
h2.Draw('same')
leg.Draw()

canv.SaveAs('2012vs2015_iso.png')

