#!/bin/bash
python frPlots.py ../fakeHistos/ETH_corrected_tot/ Plots/ETH_corrected_tot/unweighted/ none
python frPlots.py ../fakeHistos/ETH_corrected_tot/ Plots/ETH_corrected_tot/fit_weighted/ fit
python frPlots.py ../fakeHistos/ETH_corrected_tot/ Plots/ETH_corrected_tot/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/ETH_corrected_tot/ Plots/ETH_corrected_tot/qcdwtots_weighted/ qcdwtots
cp Plots/ETH_corrected_tot/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_tot/unweighted
cp Plots/ETH_corrected_tot/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_tot/fit_weighted
cp Plots/ETH_corrected_tot/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_tot/qcd_weighted
cp Plots/ETH_corrected_tot/qcdwtots_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_corrected_tot/qcdwtots_weighted
