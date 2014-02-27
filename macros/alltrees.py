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


# DEFINE FILES

files = []
isdata = []

files.append("qcdMuEnriched")
files.append("wjets")
files.append("dyjets")
files.append("data")

isdata.append(0)
isdata.append(0)
isdata.append(0)
isdata.append(1)

# ATTENTION!
# Note that this is not very nice and wants to be changed!
# Later in the code, the number of mc samples is hard-coded 
# (looping over the first 3 files in the list) albeit it would
# be way better if the code could discriminate between data sample
# and mc sample, using the right ones in the right places


# DEFINE HISTOGRAMS AND AXIS LABELS

histos = []
labelx = []
labely = []

histos.append("h_muIsoPlot")
histos.append("h_muD0Plot")
histos.append("h_elIsoPlot")
histos.append("h_elD0Plot")
histos.append("h_Loose_muAwayJetDR")
histos.append("h_Loose_muAwayJetPt")
histos.append("h_Loose_muClosJetDR")
histos.append("h_Loose_muClosJetPt")
histos.append("h_Loose_muHT")
histos.append("h_Loose_muLepEta")
histos.append("h_Loose_muLepIso")
histos.append("h_Loose_muLepPt")
histos.append("h_Loose_muMET")
histos.append("h_Loose_muMETnoMTCut")
histos.append("h_Loose_muMT")
histos.append("h_Loose_muMTMET30")
histos.append("h_Loose_muMaxJPt")
histos.append("h_Loose_muNBJets")
histos.append("h_Loose_muNJets")
histos.append("h_Loose_muNVertices")
histos.append("h_Tight_muAwayJetDR")
histos.append("h_Tight_muAwayJetPt")
histos.append("h_Tight_muClosJetDR")
histos.append("h_Tight_muClosJetPt")
histos.append("h_Tight_muHT")
histos.append("h_Tight_muLepEta")
histos.append("h_Tight_muLepIso")
histos.append("h_Tight_muLepPt")
histos.append("h_Tight_muMET")
histos.append("h_Tight_muMETnoMTCut")
histos.append("h_Tight_muMT")
histos.append("h_Tight_muMTMET30")
histos.append("h_Tight_muMaxJPt")
histos.append("h_Tight_muNBJets")
histos.append("h_Tight_muNJets")
histos.append("h_Tight_muNVertices")

labelx.append("")
labelx.append("")
labelx.append("")
labelx.append("")
labelx.append("DR (Away Jet)")
labelx.append("p_{T} (Away Jet) (GeV)")
labelx.append("DR (Closest Jet)")
labelx.append("p_{T} (Closest Jet) (GeV)")
labelx.append("H_{T} (GeV)")
labelx.append("#eta")
labelx.append("Lepton PF Iso")
labelx.append("p_{T} (GeV)")
labelx.append("E_{T}^{miss} (GeV)")
labelx.append("E_{T}^{miss} (GeV)")
labelx.append("m_{T} (GeV)")
labelx.append("m_{T} (GeV)")
labelx.append("p_{T} (Hardest Jet) (GeV)")
labelx.append("N_{BJets}")
labelx.append("N_{Jets}")
labelx.append("N_{Vertices}")
labelx.append("DR (Away Jet)")
labelx.append("p_{T} (Away Jet) (GeV)")
labelx.append("DR (Closest Jet)")
labelx.append("p_{T} (Closest Jet) (GeV)")
labelx.append("H_{T} (GeV)")
labelx.append("#eta")
labelx.append("Lepton PF Iso")
labelx.append("p_{T} (GeV)")
labelx.append("E_{T}^{miss} (GeV)")
labelx.append("E_{T}^{miss} (GeV)")
labelx.append("m_{T} (GeV)")
labelx.append("m_{T} (GeV)")
labelx.append("p_{T} (Hardest Jet) (GeV)")
labelx.append("N_{BJets}")
labelx.append("N_{Jets}")
labelx.append("N_{Vertices}")

labely.append("")
labely.append("")
labely.append("")
labely.append("")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Loose}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")
labely.append("N_{Tight}")


# LOAD FILES AND HISTOGRAMS

f = [ROOT.TFile(inputdir + element + "_ratios.root") for element in files]
t = [element.Get(files[j]) for j, element in enumerate(f)]

c = ROOT.TCanvas("c0", "C0")
l = [{} for i in range(len(histos))]

h = [[element1.Get(files[j] + element2) for element2 in histos] for j, element1 in enumerate(t)]

for i in range(len(histos)):
    h[0][i].SetFillColor(ROOT.kBlue)
    h[1][i].SetFillColor(ROOT.kRed)
    h[2][i].SetFillColor(ROOT.kGreen)
    h[3][i].SetLineColor(ROOT.kBlack)


# ADD HISTOGRAMS TO STACK

s = [ROOT.THStack(histos[j] + "_stack", histos[j] + "_stack") for j in range(len(histos))]

for i in range(3):
    for j,m in enumerate(s): 
        m.Add(h[i][j])


# DRAW AND WRITE HISTOGRAMS

new = ROOT.TFile(outputdir + "alltrees.root", "RECREATE")
new.cd()

for i,m in enumerate(s):

    m.Draw("hist")
    m.GetXaxis().SetTitle(labelx[i])
    m.GetYaxis().SetTitle(labely[i])

    h[3][i].Draw("P E1 SAME")

    l[i] = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
    l[i].AddEntry(h[0][i], files[0], "F")
    l[i].AddEntry(h[1][i], files[1], "F")
    l[i].AddEntry(h[2][i], files[2], "F")
    l[i].SetFillColor(0)
    l[i].Draw()

    c.Print(outputdir + histos[i] + "_stack.pdf")
    c.Print(outputdir + histos[i] + "_stack.png")
    m.Write()

new.Close()




raw_input("press ENTER")



