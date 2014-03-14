#!/bin/bash
python frPlots.py ../fakeHistos/ETH_corrected_jet/ Plots/ETH_corrected_jet/unweighted/ none
python frPlots.py ../fakeHistos/ETH_corrected_jet/ Plots/ETH_corrected_jet/fit_weighted/ fit
python frPlots.py ../fakeHistos/ETH_corrected_jet/ Plots/ETH_corrected_jet/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/ETH_corrected_jet/ Plots/ETH_corrected_jet/qcdwjets_weighted/ qcdwjets
cp Plots/ETH_corrected_jet/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jet/unweighted
cp Plots/ETH_corrected_jet/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jet/fit_weighted
cp Plots/ETH_corrected_jet/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jet/qcd_weighted
cp Plots/ETH_corrected_jet/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_jet/qcdwjets_weighted
