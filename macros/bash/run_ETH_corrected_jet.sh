#!/bin/bash
rm Plots/noPUweight/ETH_corrected_jet/unweighted/*.png
rm Plots/noPUweight/ETH_corrected_jet/unweighted/*.pdf
rm Plots/noPUweight/ETH_corrected_jet/fit_weighted/*.png
rm Plots/noPUweight/ETH_corrected_jet/fit_weighted/*.pdf
rm Plots/noPUweight/ETH_corrected_jet/qcd_weighted/*.png
rm Plots/noPUweight/ETH_corrected_jet/qcd_weighted/*.pdf
rm Plots/noPUweight/ETH_corrected_jet/qcdwjets_weighted/*.png
rm Plots/noPUweight/ETH_corrected_jet/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/noPUweight/ETH_corrected_jet/ Plots/noPUweight/ETH_corrected_jet/unweighted/ none
python frPlots.py ../fakeHistos/noPUweight/ETH_corrected_jet/ Plots/noPUweight/ETH_corrected_jet/fit_weighted/ fit
python frPlots.py ../fakeHistos/noPUweight/ETH_corrected_jet/ Plots/noPUweight/ETH_corrected_jet/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/noPUweight/ETH_corrected_jet/ Plots/noPUweight/ETH_corrected_jet/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/qcdwjets_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/qcdwjets_weighted/*.pdf
cp Plots/noPUweight/ETH_corrected_jet/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/unweighted
cp Plots/noPUweight/ETH_corrected_jet/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/fit_weighted
cp Plots/noPUweight/ETH_corrected_jet/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/qcd_weighted
cp Plots/noPUweight/ETH_corrected_jet/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_corrected_jet/qcdwjets_weighted
