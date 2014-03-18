#!/bin/bash
bash bash/run_ETH_uncorrected.sh
bash bash/run_ETH_corrected_jet.sh
bash bash/run_ETH_corrected_jetd0.sh
bash bash/run_ETH_corrected_tot.sh
bash bash/run_UFL_uncorrected.sh
bash bash/run_UFL_corrected_jet.sh
bash bash/run_UFL_corrected_jetd0.sh
bash bash/run_UFL_corrected_tot.sh
#make Fakerates && \
#./Fakerates -v 2    -c config/ETH_uncorrected.config     -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/ETH_corrected_jet.config   -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/ETH_corrected_jetd0.config -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/ETH_corrected_tot.config   -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/UFL_uncorrected.config     -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/UFL_corrected_jet.config   -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/UFL_corrected_jetd0.config -i doubleMu_complete.root          -n data          -x 1.0
#./Fakerates -v 2    -c config/UFL_corrected_tot.config   -i doubleMu_complete.root          -n data          -x 1.0
##
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config     -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/ETH_corrected_jet.config   -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/ETH_corrected_jetd0.config -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/ETH_corrected_tot.config   -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/UFL_uncorrected.config     -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/UFL_corrected_jet.config   -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/UFL_corrected_jetd0.config -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
#./Fakerates -v 2 -s -c config/UFL_corrected_tot.config   -i wjets_fakeminitrees.root        -n wjets         -x 37509.0
##
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config     -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/ETH_corrected_jet.config   -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/ETH_corrected_jetd0.config -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/ETH_corrected_tot.config   -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/UFL_uncorrected.config     -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/UFL_corrected_jet.config   -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/UFL_corrected_jetd0.config -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
#./Fakerates -v 2 -s -c config/UFL_corrected_tot.config   -i dyjets_fakeminitrees.root       -n dyjets        -x 3532.8
##
#./Fakerates -v 2 -s -c config/ETH_uncorrected.config     -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/ETH_corrected_jet.config   -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/ETH_corrected_jetd0.config -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/ETH_corrected_tot.config   -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/UFL_uncorrected.config     -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/UFL_corrected_jet.config   -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/UFL_corrected_jetd0.config -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
#./Fakerates -v 2 -s -c config/UFL_corrected_tot.config   -i qcdMuEnriched_fakeminitree.root -n qcdMuEnriched -x 1.347e+05
