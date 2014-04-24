#!/bin/bash
make Fakerates && \
./Fakerates -v 2    -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DoubleElectron.root                                    -n el_data           -x 1.
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets          -x 37509.0
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50       -x 3532.8
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10       -x 877.0

./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr20    -x 2.91e+06
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr30     -x 4615893.0
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdemenr80     -x 183448.7

./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/     -n el_qcdemenr170    -x 4586.5
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr250    -x 556.75
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr350    -x 89.1

./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/     -n el_qcdbctoe20    -x 1.67e+05
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/     -n el_qcdbctoe30    -x 1.67e+05
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/     -n el_qcdbctoe80    -x 12.98e+03
