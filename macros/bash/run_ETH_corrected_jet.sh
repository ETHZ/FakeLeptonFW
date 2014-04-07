#!/bin/bash
find Plots/PUweight_runD/ETH_corrected_jet_test/ -name "*.png" -type f delete
find Plots/PUweight_runD/ETH_corrected_jet_test/ -name "*.pdf" -type f delete
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/unweighted/ none
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/fit_weighted/ fit
#python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/ qcd
#python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/qcdwjets_weighted/ qcdwjets
rm -r /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/*
cp -r Plots/PUweight_runD/ETH_corrected_jet_test/unweighted/ /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/
cp -r Plots/PUweight_runD/ETH_corrected_jet_test/fit_weighted/ /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/
#cp Plots/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcd_weighted
#cp Plots/PUweight_runD/ETH_corrected_jet_test/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcdwjets_weighted
