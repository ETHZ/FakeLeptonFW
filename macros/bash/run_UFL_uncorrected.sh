#!/bin/bash
rm Plots/PUweight/UFL_uncorrected/unweighted/*.png
rm Plots/PUweight/UFL_uncorrected/unweighted/*.pdf
rm Plots/PUweight/UFL_uncorrected/fit_weighted/*.png
rm Plots/PUweight/UFL_uncorrected/fit_weighted/*.pdf
rm Plots/PUweight/UFL_uncorrected/qcd_weighted/*.png
rm Plots/PUweight/UFL_uncorrected/qcd_weighted/*.pdf
rm Plots/PUweight/UFL_uncorrected/qcdwjets_weighted/*.png
rm Plots/PUweight/UFL_uncorrected/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight/UFL_uncorrected/ Plots/PUweight/UFL_uncorrected/unweighted/ none
python frPlots.py ../fakeHistos/PUweight/UFL_uncorrected/ Plots/PUweight/UFL_uncorrected/fit_weighted/ fit
python frPlots.py ../fakeHistos/PUweight/UFL_uncorrected/ Plots/PUweight/UFL_uncorrected/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/PUweight/UFL_uncorrected/ Plots/PUweight/UFL_uncorrected/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/qcdwjets_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/qcdwjets_weighted/*.pdf
cp Plots/PUweight/UFL_uncorrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/unweighted
cp Plots/PUweight/UFL_uncorrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/fit_weighted
cp Plots/PUweight/UFL_uncorrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/qcd_weighted
cp Plots/PUweight/UFL_uncorrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_uncorrected/qcdwjets_weighted
