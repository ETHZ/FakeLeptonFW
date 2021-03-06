#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/DoubleElectron.root                                    -n el_data           -x 1.
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets          -x 37509.0
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50       -x 3532.8
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10       -x 877.0
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdelenr30     -x 4615893.0
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdelenr80     -x 183448.7
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdelenr250    -x 556.75
./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele8JMC.config -i /shome/cheidegg/FakeTrees/PUweight_runD/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdelenr350    -x 556.75
