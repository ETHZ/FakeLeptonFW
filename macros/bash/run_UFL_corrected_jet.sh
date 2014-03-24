#!/bin/bash
rm Plots/PUweight/UFL_corrected_jet/unweighted/*.png
rm Plots/PUweight/UFL_corrected_jet/unweighted/*.pdf
rm Plots/PUweight/UFL_corrected_jet/fit_weighted/*.png
rm Plots/PUweight/UFL_corrected_jet/fit_weighted/*.pdf
rm Plots/PUweight/UFL_corrected_jet/qcd_weighted/*.png
rm Plots/PUweight/UFL_corrected_jet/qcd_weighted/*.pdf
rm Plots/PUweight/UFL_corrected_jet/qcdwjets_weighted/*.png
rm Plots/PUweight/UFL_corrected_jet/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight/UFL_corrected_jet/ Plots/PUweight/UFL_corrected_jet/unweighted/ none
python frPlots.py ../fakeHistos/PUweight/UFL_corrected_jet/ Plots/PUweight/UFL_corrected_jet/fit_weighted/ fit
python frPlots.py ../fakeHistos/PUweight/UFL_corrected_jet/ Plots/PUweight/UFL_corrected_jet/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/PUweight/UFL_corrected_jet/ Plots/PUweight/UFL_corrected_jet/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/qcdwjets_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/qcdwjets_weighted/*.pdf
cp Plots/PUweight/UFL_corrected_jet/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/unweighted
cp Plots/PUweight/UFL_corrected_jet/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/fit_weighted
cp Plots/PUweight/UFL_corrected_jet/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/qcd_weighted
cp Plots/PUweight/UFL_corrected_jet/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/UFL_corrected_jet/qcdwjets_weighted
