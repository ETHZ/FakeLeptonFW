###############################################
# python script to stack all histograms from  #
# qcdMuEnhanced, Wjets, DYJets                #
# Constantin, 2014-02-26                      #
###############################################


# IMPORT LIBRARIES

import ROOT


# DEFINE VARIABLES

inputdir = "../outputDir/"

outputdir = "../outputDir/"

files = []
files.append("qcdMuEnriched")
files.append("wjets")
files.append("dyjets")

histos = []
histos.append("h_muIsoPlot")
histos.append("h_muD0Plot")
histos.append("h_elIsoPlot")
histos.append("h_elD0Plot")


# LOAD FILES AND HISTOGRAMS

f = [ROOT.TFile(inputdir + element + "_ratios.root") for element in files]
t = [element.Get(files[j]) for j, element in enumerate(f)]

c = [ROOT.TCanvas("c" + str(i), "C" + str(i)) for i in range(len(histos))]
h = [[element1.Get(files[j] + element2) for element2 in histos] for j, element1 in enumerate(t)]


# ADD HISTOGRAMS TO STACK

s = [ROOT.THStack(histos[j] + "_stack", histos[j] + "_stack") for j in range(len(histos))]

for i in range(len(t)):
    for j,m in enumerate(s): 
        m.Add(h[i][j])


# DRAW AND WRITE HISTOGRAMS

new = ROOT.TFile(outputdir + "alltrees.root", "RECREATE")
new.cd()

for i,m in enumerate(s):
    c[i] = ROOT.TCanvas("c" + str(i), "C" + str(i))
    m.Draw()
    c[i].Print(outputdir + histos[i] + "_stack.pdf")
    m.Write()

new.Close()








