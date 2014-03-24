#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -c config/ETH_uncorrected.config -i /shome/mdunser/fakeTrees/DoubleMu-Run2012D-PromptReco-v1-RETRY.root       -n data          -x 1. -m 10000
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i /scratch/mdunser/fakeTrees/wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i /scratch/mdunser/fakeTrees/dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i /scratch/mdunser/fakeTrees/qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
## ./Fakerates -v 2 -s -i qcdBigFile_START53_V20.root -o fakeHistos_fix/ -n qcdMuEnriched -x 1.347e+05
