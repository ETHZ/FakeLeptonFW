#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -c runOldB.config -i /scratch/mdunser/fakeTrees/runB.root                       -n data          -x -1.
./Fakerates -v 2 -s -c runOldB.config -i /scratch/mdunser/fakeTrees/wjets_fakeminitrees.root        -n wjets         -x 37509.0
./Fakerates -v 2 -s -c runOldB.config -i /scratch/mdunser/fakeTrees/dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
./Fakerates -v 2 -s -c runOldB.config -i /scratch/mdunser/fakeTrees/qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
