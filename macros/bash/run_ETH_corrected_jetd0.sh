#!/bin/bash
rm Plots/PUweight/ETH_corrected_jetd0/unweighted/*.png
rm Plots/PUweight/ETH_corrected_jetd0/unweighted/*.pdf
rm Plots/PUweight/ETH_corrected_jetd0/fit_weighted/*.png
rm Plots/PUweight/ETH_corrected_jetd0/fit_weighted/*.pdf
rm Plots/PUweight/ETH_corrected_jetd0/qcd_weighted/*.png
rm Plots/PUweight/ETH_corrected_jetd0/qcd_weighted/*.pdf
rm Plots/PUweight/ETH_corrected_jetd0/qcdwjets_weighted/*.png
rm Plots/PUweight/ETH_corrected_jetd0/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_jetd0/ Plots/PUweight/ETH_corrected_jetd0/unweighted/ none
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_jetd0/ Plots/PUweight/ETH_corrected_jetd0/fit_weighted/ fit
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_jetd0/ Plots/PUweight/ETH_corrected_jetd0/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_jetd0/ Plots/PUweight/ETH_corrected_jetd0/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/qcdwjets_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/qcdwjets_weighted/*.pdf
cp Plots/PUweight/ETH_corrected_jetd0/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/unweighted
cp Plots/PUweight/ETH_corrected_jetd0/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/fit_weighted
cp Plots/PUweight/ETH_corrected_jetd0/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/qcd_weighted
cp Plots/PUweight/ETH_corrected_jetd0/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_jetd0/qcdwjets_weighted
