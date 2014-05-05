#!/bin/bash
make Fakerates && \
#./Fakerates -v 2    -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DoubleElectron.root                                    -n el_data           -x 1.
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets          -x 37509.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50       -x 3532.8
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10       -x 877.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar0          -x 245.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar1          -x 245.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar2          -x 245.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar3          -x 245.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr20     -x 2.91e+06
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr30     -x 4615893.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdemenr80     -x 183448.7
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr170    -x 4586.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr250    -x 556.75
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr350    -x 89.1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe20     -x 1.67e+05
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe30     -x 1.67e+05
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcdbctoe80     -x 12.98e+03
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-50to80-TuneZ2star-8TeV-pythia6.root             -n el_qcdtot50        -x 8148778.0
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80to120-TuneZ2star-8TeV-pythia6.root            -n el_qcdtot80        -x 1033680.0
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-120to170-TuneZ2star-8TeV-pythia6.root           -n el_qcdtot120     -x 156293.3
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6.root           -n el_qcdtot170       -x 34138.2
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6-v2.root        -n el_qcdtot170v2     -x 34138.2
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6.root           -n el_qcdtot300       -x 1759.5
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v2.root        -n el_qcdtot300v2     -x 1759.5
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v3.root        -n el_qcdtot300v3     -x 1759.5
