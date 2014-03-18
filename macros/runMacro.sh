#!/bin/bash
python frPlots.py ../fakeHistos/ETH_uncorrected/ ETH_uncorrected/unweighted/ none
python frPlots.py ../fakeHistos/ETH_uncorrected/ ETH_uncorrected/fit_weighted/ fit
python frPlots.py ../fakeHistos/ETH_uncorrected/ ETH_uncorrected/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/ETH_uncorrected/ ETH_uncorrected/qcdwjets_weighted/ qcdwjets
cp ETH_uncorrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/unweighted
cp ETH_uncorrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/fit_weighted
cp ETH_uncorrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcd_weighted
cp ETH_uncorrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/ETH_uncorrected/qcdwjets_weighted
