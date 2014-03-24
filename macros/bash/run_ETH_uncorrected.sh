#!/bin/bash
#rm Plots/noPUweight/ETH_uncorrected/unweighted/*.png
#rm Plots/noPUweight/ETH_uncorrected/unweighted/*.pdf
#rm Plots/noPUweight/ETH_uncorrected/fit_weighted/*.png
#rm Plots/noPUweight/ETH_uncorrected/fit_weighted/*.pdf
#rm Plots/noPUweight/ETH_uncorrected/qcd_weighted/*.png
#rm Plots/noPUweight/ETH_uncorrected/qcd_weighted/*.pdf
#rm Plots/noPUweight/ETH_uncorrected/qcdwjets_weighted/*.png
#rm Plots/noPUweight/ETH_uncorrected/qcdwjets_weighted/*.pdf
python frPlots.py ../fakeHistos/noPUweight/ETH_uncorrected/ Plots/noPUweight/ETH_uncorrected/unweighted/ none
#python frPlots.py ../fakeHistos/noPUweight/ETH_uncorrected/ Plots/noPUweight/ETH_uncorrected/fit_weighted/ fit
#python frPlots.py ../fakeHistos/noPUweight/ETH_uncorrected/ Plots/noPUweight/ETH_uncorrected/qcd_weighted/ qcd
#python frPlots.py ../fakeHistos/noPUweight/ETH_uncorrected/ Plots/noPUweight/ETH_uncorrected/qcdwjets_weighted/ qcdwjets
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/unweighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/unweighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/fit_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/fit_weighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/qcd_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/qcd_weighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/qcdwjets_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/qcdwjets_weighted/*.pdf
cp Plots/noPUweight/ETH_uncorrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/unweighted
#cp Plots/noPUweight/ETH_uncorrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/fit_weighted
#cp Plots/noPUweight/ETH_uncorrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/qcd_weighted
#cp Plots/noPUweight/ETH_uncorrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/noPUweight/ETH_uncorrected/qcdwjets_weighted
