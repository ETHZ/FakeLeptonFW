#!/bin/bash
python frPlots.py ../fakeHistos/ETH_corrected_jetd0/ Plots/ETH_corrected_jetd0/unweighted/ none
python frPlots.py ../fakeHistos/ETH_corrected_jetd0/ Plots/ETH_corrected_jetd0/fit_weighted/ fit
python frPlots.py ../fakeHistos/ETH_corrected_jetd0/ Plots/ETH_corrected_jetd0/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/ETH_corrected_jetd0/ Plots/ETH_corrected_jetd0/qcdwjets_weighted/ qcdwjets
cp Plots/ETH_corrected_jetd0/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jetd0/unweighted
cp Plots/ETH_corrected_jetd0/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jetd0/fit_weighted
cp Plots/ETH_corrected_jetd0/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jetd0/qcd_weighted
cp Plots/ETH_corrected_jetd0/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jetd0/qcdwjets_weighted
