

import ROOT, lib


def SetFillStyle(hists, integral, normalize = True):

	hists[0].SetFillColor(mycolor.GetColor( 51, 153,  58))
	hists[1].SetFillColor(mycolor.GetColor( 12,  57, 102))
	hists[2].SetFillColor(mycolor.GetColor( 51, 102, 153))
	hists[3].SetFillColor(mycolor.GetColor( 15, 106, 196))
	hists[4].SetFillColor(mycolor.GetColor(191,  11,  11))
	hists[5].SetFillColor(mycolor.GetColor(255, 204,   0))

	if integral>0. and normalize:
		for i in range(len(hists)): 
			hists[i].Scale(1.0/integral)

	for i in range(len(hists)):
		hists[i].SetMaximum(1.1)

	return hists


def DrawAndPlot(canv, pad_plot, hists, filename):

	hists[0].Draw("hist text")
	for i in range(1, len(hists)): hists[i].Draw('hist text same')

	y = ROOT.gPad.GetUymin() + 0.25 * hists[0].GetXaxis().GetBinWidth(1)
	t = ROOT.TText()
	t.SetTextAngle(90)
	t.SetTextSize(0.05)
	t.SetTextAlign(13)
	t.SetTextColor(ROOT.kBlack)

	for i in range(len(hists)):
		x = hists[0].GetXaxis().GetBinCenter(i+1) - 0.1
		t.DrawText(x, y, label[i])

	lib.saveCanvas(canv, pad_plot, 'Plots/', filename, False)




ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.5f")
ROOT.TGaxis.SetMaxDigits(3)



mycolor   = ROOT.TColor()
label     = ['W', 'B', 'C', 'light-flavor', 'T', 'unmatched']
index     = [1, 2, 3, 4, 5, 0] # element 1 in lines goes to element 1 in values, element 0 goes nowhere, element 6 goes to 0
values_pl = [{} for i in range(len(label))]
values_pt = [{} for i in range(len(label))]
values_nl = [{} for i in range(len(label))]
values_nt = [{} for i in range(len(label))]
hpl       = [{} for i in range(len(label))]
hpt       = [{} for i in range(len(label))]
hpf       = [{} for i in range(len(label))]
hnl       = [{} for i in range(len(label))]
hnt       = [{} for i in range(len(label))]
hnf       = [{} for i in range(len(label))]
filename  = 'qcd_mu_counters'




fo    = open('Plots/' + filename + '.txt', 'r')
lines = fo.readlines()

for j, line in enumerate(lines):
	split = line.split(': ')[1].split(',')	
	for k in range(len(values_pl)):
		if j == 0: values_pl[index[k]] = int(split[k])
		if j == 2: values_pt[index[k]] = int(split[k])
		if j == 1: values_nl[index[k]] = int(split[k])
		if j == 3: values_nt[index[k]] = int(split[k])





canv = lib.makeCanvas(900, 675)
pad_plot = lib.makePad('tot')
pad_plot.cd()

for i in range(len(hpl)):  
	hpl[i] = ROOT.TH1F('hpl' + str(i), 'hpl' + str(i), len(hpl), 0, len(hpl))
	hpt[i] = ROOT.TH1F('hpt' + str(i), 'hpt' + str(i), len(hpt), 0, len(hpt))
	hpf[i] = ROOT.TH1F('hpf' + str(i), 'hpf' + str(i), len(hpf), 0, len(hpf))
	hnl[i] = ROOT.TH1F('hnl' + str(i), 'hnl' + str(i), len(hnl), 0, len(hnl))
	hnt[i] = ROOT.TH1F('hnt' + str(i), 'hnt' + str(i), len(hnt), 0, len(hnt))
	hnf[i] = ROOT.TH1F('hnf' + str(i), 'hnf' + str(i), len(hnf), 0, len(hnf))
	hpl[i].SetBinContent(i+1, values_pl[i])
	hpt[i].SetBinContent(i+1, values_pt[i])
	hnl[i].SetBinContent(i+1, values_nl[i])
	hnt[i].SetBinContent(i+1, values_nt[i])
	if values_pl[i]>0: 	hpf[i].SetBinContent(i+1, values_pt[i] / float(values_pl[i]))
	else:               hpf[i].SetBinContent(i+1, 0)
	if values_nl[i]>0:  hnf[i].SetBinContent(i+1, values_nt[i] / float(values_nl[i]))
	else:               hnf[i].SetBinContent(i+1, 0)


integral_pl = sum([hpl[i].Integral() for i in range(len(hpl))])
integral_pt = sum([hpt[i].Integral() for i in range(len(hpt))])
integral_pf = sum([hpf[i].Integral() for i in range(len(hpf))])
integral_nl = sum([hnl[i].Integral() for i in range(len(hnl))])
integral_nt = sum([hnt[i].Integral() for i in range(len(hnt))])
integral_nf = sum([hnf[i].Integral() for i in range(len(hnf))])

hpl = SetFillStyle(hpl, integral_pl)
hpt = SetFillStyle(hpt, integral_pt)
hpf = SetFillStyle(hpf, integral_pf, False)
hnl = SetFillStyle(hnl, integral_nl)
hnt = SetFillStyle(hnt, integral_nt)
hnf = SetFillStyle(hnf, integral_nf, False)

DrawAndPlot(canv, pad_plot, hpl, filename + '_prompt_loose')
DrawAndPlot(canv, pad_plot, hpt, filename + '_prompt_tight')
DrawAndPlot(canv, pad_plot, hpf, filename + '_prompt_rate')
DrawAndPlot(canv, pad_plot, hnl, filename + '_noprompt_loose')
DrawAndPlot(canv, pad_plot, hnt, filename + '_noprompt_tight')
DrawAndPlot(canv, pad_plot, hnf, filename + '_noprompt_rate')




pad_plot.Close()

