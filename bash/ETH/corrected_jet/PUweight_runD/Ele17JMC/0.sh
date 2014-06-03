#!/bin/bash
make Fakerates && \
############################################### 'normal' SAMPLES RECO INFO
#./Fakerates -v 2    -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/DoubleElectron-Run2012D-PromptReco-v1.root             -n el_data           -x 1.
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets          -x 37509.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50       -x 3532.8
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10       -x 877.0
############################################### QCD EMenr + BCtoE SAMPLES
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr20     -x 2.91e+06
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr30     -x 4615893.0
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdemenr80     -x 183448.7
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr170    -x 4586.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr250    -x 556.75
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr350    -x 89.1
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe20     -x 1.67e+05
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe30     -x 1.67e+05
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcdbctoe80     -x 12.98e+03
############################################### QCD tot SAMPLES
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-50to80-TuneZ2star-8TeV-pythia6.root             -n el_qcdtot50        -x 8148778.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80to120-TuneZ2star-8TeV-pythia6.root            -n el_qcdtot80        -x 1033680.0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-120to170-TuneZ2star-8TeV-pythia6.root           -n el_qcdtot120     -x 156293.3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6.root           -n el_qcdtot170       -x 34138.2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6-v2.root        -n el_qcdtot170v2     -x 34138.2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6.root           -n el_qcdtot300       -x 1759.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v2.root        -n el_qcdtot300v2     -x 1759.5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v3.root        -n el_qcdtot300v3     -x 1759.5
############################################### CLOSURE TEST SAMPLES
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                        -n el_ttbar_g          -x 245.0        -g   
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/TTJets-SemiLeptMGDecays-8TeV-madgraph-tauola-Summer12-DR53X-PU-S10-START53-V19-ext1-v1-2-V03-09-01.root            -n el_ttbar_g         -x 102.5     -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets_g          -x 37509.0      -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50_g       -x 3532.8       -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10_g       -x 877.0        -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr20_g     -x 2.91e+06     -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr30_g     -x 4615893.0    -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdemenr80_g     -x 183448.7     -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe20_g     -x 1.67e+05     -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe30_g     -x 1.67e+05     -g
./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcdbctoe80_g     -x 12.98e+03    -g
############################################### FORGET ABOUT THIS HERE
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar0         -x 245.0     -g 0   
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar1         -x 245.0     -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar2         -x 245.0     -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar3         -x 245.0     -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar4         -x 245.0     -g 4
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar5         -x 245.0     -g 5
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                   -n el_ttbar6         -x 245.0     -g 6
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd00          -x 2.91e+06  -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd01          -x 2.91e+06  -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd02          -x 2.91e+06  -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd03          -x 2.91e+06  -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd10          -x 4615893.0 -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd11          -x 4615893.0 -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd12          -x 4615893.0 -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcd13          -x 4615893.0 -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcd20          -x 183448.7  -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcd21          -x 183448.7  -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcd22          -x 183448.7  -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcd23          -x 183448.7  -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd30          -x 4586.5    -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd31          -x 4586.5    -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd32          -x 4586.5    -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd33          -x 4586.5    -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd40          -x 556.75    -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd41          -x 556.75    -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd42          -x 556.75    -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcd43          -x 556.75    -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcd50          -x 89.1      -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcd51          -x 89.1      -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcd52          -x 89.1      -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcd53          -x 89.1      -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd60          -x 1.67e+05  -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd61          -x 1.67e+05  -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd62          -x 1.67e+05  -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd63          -x 1.67e+05  -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd70          -x 1.67e+05  -g 0 
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd71          -x 1.67e+05  -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd72          -x 1.67e+05  -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcd73          -x 1.67e+05  -g 3
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcd80          -x 12.98e+03 -g 0
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcd81          -x 12.98e+03 -g 1
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcd82          -x 12.98e+03 -g 2
#./Fakerates -v 2 -s -t 2 -c config/ETH/corrected_jet/PUweight_runD/Ele17JMC/0.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcd83          -x 12.98e+03 -g 3
