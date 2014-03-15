#!/bin/bash
python frPlots.py ../fakeHistos/UFL_corrected_tot/ Plots/UFL_corrected_tot/unweighted/ none
python frPlots.py ../fakeHistos/UFL_corrected_tot/ Plots/UFL_corrected_tot/fit_weighted/ fit
python frPlots.py ../fakeHistos/UFL_corrected_tot/ Plots/UFL_corrected_tot/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/UFL_corrected_tot/ Plots/UFL_corrected_tot/qcdwjets_weighted/ qcdwjets
cp Plots/UFL_corrected_tot/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_tot/unweighted
cp Plots/UFL_corrected_tot/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_tot/fit_weighted
cp Plots/UFL_corrected_tot/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_tot/qcd_weighted
cp Plots/UFL_corrected_tot/qcdwtots_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected_tot/qcdwjets_weighted
