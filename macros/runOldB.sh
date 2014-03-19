#!/bin/bash
rm Plots/runOldB/unweighted/*.png
rm Plots/runOldB/unweighted/*.pdf
python frPlots.py ../fakeHistos/runOldB/ Plots/runOldB/unweighted/ none
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/runOldB/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/runOldB/unweighted/*.pdf
cp Plots/runOldB/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/runOldB/unweighted
