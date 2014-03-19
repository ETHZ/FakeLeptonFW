#!/bin/bash
rm Plots/runOld/unweighted/*.png
rm Plots/runOld/unweighted/*.pdf
python frPlots.py ../fakeHistos/runOld/ Plots/runOld/unweighted/ none
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/runOld/unweighted/*.png
rm /afs/cern.ch/user/c/cheidegg/www/pdfs/runOld/unweighted/*.pdf
cp Plots/runOld/unweighted/*.p?? /afs/cern.ch/user/c/cheidegg/www/pdfs/runOld/unweighted
