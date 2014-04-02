#!/bin/bash
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/unweighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/unweighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_runMu40/ Plots/PUweight_runD/ETH_corrected_jet_runMu40/unweighted/ none
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_runMu40/ Plots/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted/ fit
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_runMu40/ Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_runMu40/ Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted/*.pdf
cp Plots/PUweight_runD/ETH_corrected_jet_runMu40/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/unweighted
cp Plots/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/fit_weighted
cp Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/qcd_weighted
cp Plots/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_runMu40/qcdwjets_weighted
