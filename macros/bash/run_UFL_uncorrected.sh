#!/bin/bash
python frPlots.py ../fakeHistos/UFL_uncorrected/ Plots/UFL_uncorrected/unweighted/ none
python frPlots.py ../fakeHistos/UFL_uncorrected/ Plots/UFL_uncorrected/fit_weighted/ fit
python frPlots.py ../fakeHistos/UFL_uncorrected/ Plots/UFL_uncorrected/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/UFL_uncorrected/ Plots/UFL_uncorrected/qcdwjets_weighted/ qcdwjets
cp Plots/UFL_uncorrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_uncorrected/unweighted
cp Plots/UFL_uncorrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_uncorrected/fit_weighted
cp Plots/UFL_uncorrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_uncorrected/qcd_weighted
cp Plots/UFL_uncorrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_uncorrected/qcdwjets_weighted
