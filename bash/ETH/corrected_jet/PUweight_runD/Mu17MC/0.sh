#!/bin/bash
make Fakerates && \
############################################### 'normal' SAMPLES RECO INFO
#./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/DoubleMu-Run2012D-PromptReco-v1-RETRY.root             -n mu_data          -x 1.
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n mu_wjets         -x 37509.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n mu_dyjets50      -x 3532.8
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n mu_dyjets10      -x 877.0
./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root      -n mu_qcdmuenr      -x 1.347e+05
############################################### 'normal' SAMPLES RECO INFO
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                        -n mu_ttbar_g         -x 245.0       -g
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/TTJets-SemiLeptMGDecays-8TeV-madgraph-tauola-Summer12-DR53X-PU-S10-START53-V19-ext1-v1-2-V03-09-01.root            -n mu_ttbar_g         -x 102.5     -g
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n mu_wjets_g         -x 37509.0     -g
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n mu_dyjets50_g      -x 3532.8      -g
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n mu_dyjets10_g      -x 877.0       -g
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root      -n mu_qcdmuenr_g      -x 1.347e+05   -g
############################################### FORGET ABOUT THE REST HERE
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar0       -x 245.0       -g 0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar1       -x 245.0       -g 1
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar2       -x 245.0       -g 2
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar3       -x 245.0       -g 3
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar4       -x 245.0       -g 4
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar5       -x 245.0       -g 5
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                    -n mu_ttbar6       -x 245.0       -g 6
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root  -n mu_qcd0         -x 1.347e+05   -g 0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root  -n mu_qcd1         -x 1.347e+05   -g 1
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root  -n mu_qcd2         -x 1.347e+05   -g 2
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17MC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root  -n mu_qcd3         -x 1.347e+05   -g 3
