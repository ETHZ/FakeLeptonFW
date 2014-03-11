#!/bin/bash
python frPlots.py ../fakeHistos/UFL_corrected/ UFL_corrected/unweighted/ none
python frPlots.py ../fakeHistos/UFL_corrected/ UFL_corrected/fit_weighted/ fit
python frPlots.py ../fakeHistos/UFL_corrected/ UFL_corrected/qcd_weighted/ qcd
python frPlots.py ../fakeHistos/UFL_corrected/ UFL_corrected/qcdwjets_weighted/ qcdwjets
cp UFL_corrected/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected/unweighted
cp UFL_corrected/fit_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected/fit_weighted
cp UFL_corrected/qcd_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected/qcd_weighted
cp UFL_corrected/qcdwjets_weighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/UFL_corrected/qcdwjets_weighted
