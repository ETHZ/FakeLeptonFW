import ROOT, copy, array
import lib as helper

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.3f")
ROOT.TGaxis.SetMaxDigits(3)

file = ROOT.TFile('stufffortalk/ssFR_data_ewkcor_sync16Apr2014f.root', 'read')

canv = helper.makeCanvas(900, 675)
pad_plot = helper.makePad('tot')
pad_plot.cd()
pad_plot.SetTicks(1,1)

hold = file.Get('h_mufr40c')

etabin = array.array('d', [0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
ptbins = array.array('d', [10., 15., 20., 25., 30., 35., 45., 50.])

hist = ROOT.TH2F('hist', 'hist', len(ptbins)-1, ptbins, len(etabin)-1, etabin)

print hold.GetNbinsX()
print hold.GetNbinsY()
print hist.GetNbinsX()
print hist.GetNbinsY()

for y in range(1, hold.GetNbinsY()+1):
	for x in range(1, hold.GetNbinsX()+1):
		hist.SetBinContent(y,x,hold.GetBinContent(x,y))
		print 'x=' + str(x) + ', y=' + str(y) + ', value=' + str(hold.GetBinContent(x,y))




# draw histogram

hist.Draw("text colz e")

# cosmetics

hist.SetMarkerColor(ROOT.kBlack)
hist.SetMarkerSize(1.8)
hist.GetXaxis().SetTitle('#mu-pT')
hist.GetYaxis().SetTitle('#mu-|#eta|')
hist.GetXaxis().SetTitleSize(0.07)
hist.GetXaxis().SetLabelSize(0.07)
hist.GetYaxis().SetTitleSize(0.07)
hist.GetYaxis().SetLabelSize(0.07)
hist.SetMinimum(0.0)
hist.SetMaximum(0.4)
hist.SetTitle('')

# save plot

helper.saveCanvas(canv, pad_plot, '', 'UCSx_FR_mu', False, False)
pad_plot.Close()




