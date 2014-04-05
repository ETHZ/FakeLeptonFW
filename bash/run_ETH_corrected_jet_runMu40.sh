#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -c config/ETH_corrected_jet_runMu40.config -i dcap://t3se01.psi.ch:22125//pnfs/psi.ch/cms/trivcat/store/user/folguera/FakeTrees/2703_TriggerStudies_CERNETH/SingleMu.root    -n data          -x 1.
./Fakerates -v 2 -s -c config/ETH_corrected_jet_runMu40.config -i /shome/mdunser/fakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball_runDPU.root       -n wjets         -x 37509.0
./Fakerates -v 2 -s -c config/ETH_corrected_jet_runMu40.config -i /shome/mdunser/fakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball_runDPU.root  -n dyjets1       -x 3532.8
./Fakerates -v 2 -s -c config/ETH_corrected_jet_runMu40.config -i /shome/mdunser/fakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph_runDPU.root           -n dyjets2       -x 877.0
./Fakerates -v 2 -s -c config/ETH_corrected_jet_runMu40.config -i /shome/mdunser/fakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6_runDPU.root -n qcdMuEnriched -x 1.347e+05