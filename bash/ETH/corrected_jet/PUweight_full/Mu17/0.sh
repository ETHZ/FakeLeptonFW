#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_full/Mu17/0.config -i /shome/cheidegg/FakeTrees/run2012/DoubleMu-Run2012A-13Jul2012-v1.root              -n mu_data1     -x 1.
./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_full/Mu17/0.config -i /shome/cheidegg/FakeTrees/run2012/DoubleMu-Run2012B-13Jul2012-v4.root              -n mu_data2     -x 1.
./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_full/Mu17/0.config -i /shome/cheidegg/FakeTrees/run2012/DoubleMu-Run2012C-EcalRecover-11Dec2012-v1.root  -n mu_data3     -x 1.
./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_full/Mu17/0.config -i /shome/cheidegg/FakeTrees/run2012/DoubleMu-Run2012C-PromptReco-v2-RETRY.root       -n mu_data4     -x 1.
./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_full/Mu17/0.config -i /shome/cheidegg/FakeTrees/run2012/DoubleMu-Run2012D.root                           -n mu_data5     -x 1. 
