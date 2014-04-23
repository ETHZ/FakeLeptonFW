#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17_d0cut/0.config -i /shome/cheidegg/FakeTrees/DoubleMu-Run2012D-PromptReco-v1-RETRY.root             -n mu_data          -x 1.
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17_d0cut/0.config -i /shome/cheidegg/FakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n mu_wjets         -x 37509.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17_d0cut/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n mu_dyjets50      -x 3532.8
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17_d0cut/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n mu_dyjets10      -x 877.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17_d0cut/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root -n mu_qcdmuenr      -x 1.347e+05
