#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -c config/ETH_uncorrected.config -i doubleMu_complete.root          -n data          -x 1.
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
## ./Fakerates -v 2 -s -i qcdBigFile_START53_V20.root -o fakeHistos_fix/ -n qcdMuEnriched -x 1.347e+05
