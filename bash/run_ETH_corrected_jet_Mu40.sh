#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -c config/ETH_corrected_jet_Mu40.config -i /shome/cheidegg/FakeTrees/Santiago_SingleMu.root                                 -n data          -x 1.
./Fakerates -v 2 -s -c config/ETH_corrected_jet_Mu40.config -i /shome/cheidegg/FakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n wjets         -x 37509.0
./Fakerates -v 2 -s -c config/ETH_corrected_jet_Mu40.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n dyjets1       -x 3532.8
./Fakerates -v 2 -s -c config/ETH_corrected_jet_Mu40.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n dyjets2       -x 877.0
./Fakerates -v 2 -s -c config/ETH_corrected_jet_Mu40.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root -n qcdMuEnriched -x 1.347e+05
