#!/bin/bash
python frPlots.py ../fakeHistos/UFL_corrected_jetd0/ Plots/UFL_corrected_jetd0/unweighted/ none
python frPlots.py ../fakeHistos/UFL_corrected_jetd0/ Plots/UFL_corrected_jetd0/fit_weighted/ fit
python frPlots.py ../fakeHistos/UFL_corrected_jetd0/ Plots/UFL_corrected_jetd0/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/UFL_corrected_jetd0/ Plots/UFL_corrected_jetd0/qcdwjetd0s_weighted/ qcdwjetd0s
cp Plots/UFL_corrected_jetd0/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_jetd0/unweighted
cp Plots/UFL_corrected_jetd0/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_jetd0/fit_weighted
cp Plots/UFL_corrected_jetd0/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_jetd0/qcd_weighted
cp Plots/UFL_corrected_jetd0/qcdwjetd0s_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_jetd0/qcdwjetd0s_weighted
