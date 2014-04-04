#!/bin/bash
rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted/*.pdf
#rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted/*.png
#rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted/*.pdf
#rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted/*.png
#rm Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_Mu17MC/ Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted/ none
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_Mu17MC/ Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted/ fit
#python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_Mu17MC/ Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted/ qcd
#python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_Mu17MC/ Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted/*.pdf
cp Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/unweighted
cp Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/fit_weighted
#cp Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/qcd_weighted
#cp Plots/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_Mu17MC/qcdwjets_weighted
