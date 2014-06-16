#!/bin/bash
make Fakerates && \
############################################### NORMAL SAMPLES
#./Fakerates -v 2    -t 2 -c config_ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/DoubleElectron-Run2012D-PromptReco-v1.root             -n el_data             -x 1.
#./Fakerates -v 2 -s -t 2 -c config_ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets            -x 37509.0
#./Fakerates -v 2 -s -t 2 -c config_ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50         -x 3532.8
#./Fakerates -v 2 -s -t 2 -c config_ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10         -x 877.0
############################################### NORMAL QCD EMenr + BCtoE SAMPLES
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr20       -x 2.91e+06
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr30       -x 4615893.0
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdemenr80       -x 183448.7
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-170-250-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr170      -x 4586.5
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-250-350-EMEnriched-TuneZ2star-8TeV-pythia6.root -n el_qcdemenr250      -x 556.75
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-350-EMEnriched-TuneZ2star-8TeV-pythia6.root     -n el_qcdemenr350      -x 89.1
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe20       -x 1.67e+05
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe30       -x 1.67e+05
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcdbctoe80       -x 12.98e+03
############################################### NORMAL QCD tot SAMPLES
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-50to80-TuneZ2star-8TeV-pythia6.root                  -n el_qcdtot50         -x 8148778.0
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-80to120-TuneZ2star-8TeV-pythia6.root                 -n el_qcdtot80         -x 1033680.0
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-120to170-TuneZ2star-8TeV-pythia6.root                -n el_qcdtot120        -x 156293.3
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6.root                -n el_qcdtot170        -x 34138.2
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-170to300-TuneZ2star-8TeV-pythia6-v2.root             -n el_qcdtot170v2      -x 34138.2
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6.root                -n el_qcdtot300        -x 1759.5
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v2.root             -n el_qcdtot300v2      -x 1759.5
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/QCD-Pt-300to470-TuneZ2star-8TeV-pythia6-v3.root             -n el_qcdtot300v3      -x 1759.5
############################################### CLOSURE TEST SAMPLES
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/TTJets_complete.root                                        -n el_ttbar_g          -x 245.0        -g   
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/TTJets-SemiLeptMGDecays-8TeV-madgraph-tauola-Summer12-DR53X-PU-S10-START53-V19-ext1-v1-2-V03-09-01.root            -n el_ttbar_g         -x 102.5     -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/WJetsToLNu-TuneZ2Star-8TeV-madgraph-tarball.root       -n el_wjets_g          -x 37509.0      -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root  -n el_dyjets50_g       -x 3532.8       -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/DYJetsToLL-M-10To50filter-8TeV-madgraph.root           -n el_dyjets10_g       -x 877.0        -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr20_g     -x 2.91e+06     -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-EMEnriched-TuneZ2star-8TeV-pythia6.root   -n el_qcdemenr30_g     -x 4615893.0    -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-EMEnriched-TuneZ2star-8TeV-pythia6.root  -n el_qcdemenr80_g     -x 183448.7     -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-20-30-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe20_g     -x 1.67e+05     -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-30-80-BCtoE-TuneZ2star-8TeV-pythia6.root        -n el_qcdbctoe30_g     -x 1.67e+05     -g
#./Fakerates -v 2 -s -t 2 -c config/ETH_corrected_jet_PUweight_runD_Ele17JMC.config -i /shome/cheidegg/FakeTrees/new2/QCD-Pt-80-170-BCtoE-TuneZ2star-8TeV-pythia6.root       -n el_qcdbctoe80_g     -x 12.98e+03    -g
