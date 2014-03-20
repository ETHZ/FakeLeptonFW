#!/bin/bash
rm Plots/ETH_uncorrected/unweighted/*.png
rm Plots/ETH_uncorrected/unweighted/*.pdf
#rm Plots/ETH_uncorrected/qcd_weighted/*.png
#rm Plots/ETH_uncorrected/qcd_weighted/*.pdf
#rm Plots/ETH_uncorrected/qcdwjets_weighted/*.png
#rm Plots/ETH_uncorrected/qcdwjets_weighted/*.pdf
#rm Plots/ETH_uncorrected/fit_weighted/*.png
#rm Plots/ETH_uncorrected/fit_weighted/*.pdf
python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/unweighted/ none
#python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/fit_weighted/ fit
#python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/qcd_weighted/ qcd
#python frPlots.py ../fakeHistos/ETH_uncorrected/ Plots/ETH_uncorrected/qcdwjets_weighted/ qcdwjets
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/unweighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcd_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcd_weighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcdwjets_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcdwjets_weighted/*.pdf
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/fit_weighted/*.png
#rm /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/fit_weighted/*.pdf
cp Plots/ETH_uncorrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/unweighted
#cp Plots/ETH_uncorrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/fit_weighted
#cp Plots/ETH_uncorrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcd_weighted
#cp Plots/ETH_uncorrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcdwjets_weighted
