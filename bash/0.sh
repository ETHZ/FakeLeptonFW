#!/bin/bash
######################################### MUON SCRIPTS
#bash bash/ETH/uncorrected/noPUweight/Mu17/0.sh
#bash bash/ETH/corrected_jet/noPUweight/Mu17/0.sh
#bash bash/ETH/corrected_jetd0/noPUweight/Mu17/0.sh
#bash bash/ETH/corrected_tot/noPUweight/Mu17/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17_nojlcvetojec/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17_jlc/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17_veto/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17MC/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu24/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu24MC/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu40/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu40MC/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17_jec/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17_oldmrregion/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Mu17/0.sh
######################################### ELECTRON SCRIPTS
#bash bash/ETH/corrected_jet/PUweight_runD/Ele17J_oldmrregion/0.sh
#bash bash/ETH/corrected_jet/PUweight_runD/Ele17J/0.sh
######################################### MAKE FAKERATES
make Fakerates && \
######################################### MUON TREES
#./Fakerates -v 2    -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17/0.config -i /shome/cheidegg/FakeTrees/DoubleMu-Run2012D-PromptReco-v1-RETRY.root                 -n mu_data          -x 1.
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root         -n mu_wjets          -x 37509.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root    -n mu_dyjets50       -x 3532.8
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph.root               -n mu_dyjets10      -x 877.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root     -n mu_qcdmuenr      -x 1.347e+05
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n mu_ttbar0        -x 245.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n mu_ttbar1        -x 245.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Mu17/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n mu_ttbar2        -x 245.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runa/Mu17/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n mu_ttbar3        -x 245.0
######################################### ELECTRON TREES
#./Fakerates -v 2    -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DoubleElectron.root                                        -n el_data           -x 1.
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root           -n el_wjets          -x 37509.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root      -n el_dyjets50       -x 3532.8
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/DYJetsToLL-M-10To50filter-8TeV-madgraph.root               -n el_dyjets10       -x 877.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n el_ttbar0          -x 245.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n el_ttbar1          -x 245.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n el_ttbar2          -x 245.0
#./Fakerates -v 2 -s -t 1 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                       -n el_ttbar3          -x 245.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root       -n el_qcdemenr20     -x 2.91e+06
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root       -n el_qcdemenr30     -x 4615893.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root      -n el_qcdemenr80     -x 183448.7
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr170    -x 4586.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr250    -x 556.75
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root         -n el_qcdemenr350    -x 89.1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root            -n el_qcdbctoe20     -x 1.67e+05
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root            -n el_qcdbctoe30     -x 1.67e+05
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root           -n el_qcdbctoe80     -x 12.98e+03
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-50to80-TuneZ2star-8TeV-pythia6.root                 -n el_qcdtot50        -x 8148778.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80to120-TuneZ2star-8TeV-pythia6.root                -n el_qcdtot80        -x 1033680.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-120to170-TuneZ2star-8TeV-pythia6.root               -n el_qcdtot120     -x 156293.3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6.root               -n el_qcdtot170       -x 34138.2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6-v2.root            -n el_qcdtot170v2     -x 34138.2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6.root               -n el_qcdtot300       -x 1759.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v2.root            -n el_qcdtot300v2     -x 1759.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v3.root            -n el_qcdtot300v3     -x 1759.5
######################################### ELECTRON TREES
#./Fakerates -v 2    -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/synching/eleSynch_data_minitree.root                        -n el_datatest     -x 1.0 >& evtlist_synch_data.txt
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17J/0.config -i /shome/cheidegg/FakeTrees/synching/eleSynch_mc_minitree.root                          -n el_mctest       -x 1.0 >& evtlist_synch_mc.txt
