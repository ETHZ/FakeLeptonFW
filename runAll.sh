#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -i /scratch/mdunser/fakeTrees/doubleMu_complete.root          -o fakeHistos/UFL_corrected/ -n data          -x 1.
./Fakerates -v 2 -s -i /scratch/mdunser/fakeTrees/wjets_fakeminitrees.root        -o fakeHistos/UFL_corrected/ -n wjets         -x 37509.0
./Fakerates -v 2 -s -i /scratch/mdunser/fakeTrees/dyjets_fakeminitrees.root       -o fakeHistos/UFL_corrected/ -n dyjets        -x 3532.8
./Fakerates -v 2 -s -i /scratch/mdunser/fakeTrees/qcdMuEnriched_fakeminitree.root -o fakeHistos/UFL_corrected/ -n qcdMuEnriched -x 1.347e+05
## ./Fakerates -v 2 -s -i qcdBigFile_START53_V20.root -o fakeHistos_fix/ -n qcdMuEnriched -x 1.347e+05
