#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -c config/ETH_uncorrected.config -i /shome/mdunser/fakeTrees/DoubleMu-Run2012D-PromptReco-v1-RETRY.root             -n data          -x 1.
./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i /shome/mdunser/fakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n wjets         -x 37509.0
./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i /shome/mdunser/fakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n dyjets        -x 3532.8
./Fakerates -v 2 -s -c config/ETH_uncorrected.config -i /shome/mdunser/fakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root -n qcdMuEnriched -x 1.347e+05
