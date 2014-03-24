#!/bin/bash
rm Plots/PUweight/ETH_corrected_tot/unweighted/*.png
rm Plots/PUweight/ETH_corrected_tot/unweighted/*.pdf
rm Plots/PUweight/ETH_corrected_tot/fit_weighted/*.png
rm Plots/PUweight/ETH_corrected_tot/fit_weighted/*.pdf
rm Plots/PUweight/ETH_corrected_tot/qcd_weighted/*.png
rm Plots/PUweight/ETH_corrected_tot/qcd_weighted/*.pdf
rm Plots/PUweight/ETH_corrected_tot/qcdwjets_weighted/*.png
rm Plots/PUweight/ETH_corrected_tot/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_tot/ Plots/PUweight/ETH_corrected_tot/unweighted/ none
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_tot/ Plots/PUweight/ETH_corrected_tot/fit_weighted/ fit
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_tot/ Plots/PUweight/ETH_corrected_tot/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/PUweight/ETH_corrected_tot/ Plots/PUweight/ETH_corrected_tot/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/unweighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/fit_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/fit_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/qcd_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/qcd_weighted/*.pdf
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/qcdwjets_weighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/qcdwjets_weighted/*.pdf
cp Plots/PUweight/ETH_corrected_tot/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/unweighted
cp Plots/PUweight/ETH_corrected_tot/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/fit_weighted
cp Plots/PUweight/ETH_corrected_tot/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/qcd_weighted
cp Plots/PUweight/ETH_corrected_tot/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/PUweight/ETH_corrected_tot/qcdwjets_weighted
