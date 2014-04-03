#!/bin/bash
rm Plots/PUweight_runD/ETH_corrected_jet_test/unweighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_test/unweighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_test/fit_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_test/fit_weighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/*.pdf
rm Plots/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted/*.png
rm Plots/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/unweighted/ none
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/fit_weighted/ fit
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/PUweight_runD/ETH_corrected_jet_test/ Plots/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted/ qcdwjet_tests
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted/*.pdf
cp Plots/PUweight_runD/ETH_corrected_jet_test/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/unweighted
cp Plots/PUweight_runD/ETH_corrected_jet_test/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/fit_weighted
cp Plots/PUweight_runD/ETH_corrected_jet_test/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcd_weighted
cp Plots/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight_runD/ETH_corrected_jet_test/qcdwjet_tests_weighted
