#!/bin/bash
python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/unweighted/ none
python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/fit_weighted/ fit
python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/qcdwjets_weighted/ qcdwjets
cp Plots/ETH_uncorrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/unweighted
cp Plots/ETH_uncorrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/fit_weighted
cp Plots/ETH_uncorrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcd_weighted
cp Plots/ETH_uncorrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcdwjets_weighted
