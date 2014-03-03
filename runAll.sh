#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -i /scratch/mdunser/fakeTrees/doubleMu_complete.root          -o fakeHistos/ -n data          -x 1.
./Fakerates -v 2 -s -i /scratch/mdunser/fakeTrees/wjets_fakeminitrees.root        -o fakeHistos/ -n wjets         -x 37509.0
./Fakerates -v 2 -s -i /scratch/mdunser/fakeTrees/dyjets_fakeminitrees.root       -o fakeHistos/ -n dyjets        -x 3532.8
./Fakerates -v 2 -s -i /scratch/mdunser/fakeTrees/qcdMuEnriched_fakeminitree.root -o fakeHistos/ -n qcdMuEnriched -x 1.347e+05
