import ROOT, lib

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.5f")
ROOT.TGaxis.SetMaxDigits(3)

mycolor  = ROOT.TColor()
label    = ['W', 'B', 'C', 'light-flavor', 'T', 'unmatched']
index    = [6, 1, 2, 3, 4, 5, 0] # element 1 in lines goes to element 1 in values, element 0 goes nowhere, element 6 goes to 0
values   = [0, 0, 0, 0, 0, 0, 0]
h        = [{} for i in range(len(label))]
filename = 'ttbar_mu_noprompt'

fo    = open('Plots/' + filename + '.txt', 'r')
lines = fo.readlines()

for j, line in enumerate(lines):
	if j>0:
		split = line.split(': ')	
		values[index[j]] = int(split[1])


# ttbar    6, 1, 2, 3, 4, 5 (all = 0)
#values = [168, 1147208, 142021, 9468, 27, 11937] # mu !prompt (all = 1310829)
#values = [4960545, 1147208, 142021, 9468, 27, 710057] # mu prompt (all = 6969326)

integral = sum(values[:])

canv = lib.makeCanvas(900, 675)
pad_plot = lib.makePad('tot')
pad_plot.cd()

for i in range(len(h)):  
	h[i] = ROOT.TH1F('h' + str(i), 'h' + str(i), len(h), 0, len(h))
	h[i].SetBinContent(i+1, values[i])

h[0].SetFillColor(mycolor.GetColor( 51, 153,  58))
h[1].SetFillColor(mycolor.GetColor( 12,  57, 102))
h[2].SetFillColor(mycolor.GetColor( 51, 102, 153))
h[3].SetFillColor(mycolor.GetColor( 15, 106, 196))
h[4].SetFillColor(mycolor.GetColor(191,  11,  11))
h[5].SetFillColor(mycolor.GetColor(255, 204,   0))

for i in range(len(h)): h[i].Scale(1.0/integral)

h[0].Draw("hist text")
h[0].SetMaximum(1.5*max([h[i].GetMaximum() for i in range(len(h))]))

for i in range(1, len(h)): h[i].Draw('hist text same')

y = ROOT.gPad.GetUymin() + 0.25 * h[0].GetXaxis().GetBinWidth(1)
t = ROOT.TText()
t.SetTextAngle(90)
t.SetTextSize(0.05)
t.SetTextAlign(13)
t.SetTextColor(ROOT.kBlack)

for i in range(len(h)):
	x = h[0].GetXaxis().GetBinCenter(i+1) - 0.1
	t.DrawText(x, y, label[i])

lib.saveCanvas(canv, pad_plot, 'Plots/', filename, False)
pad_plot.Close()

