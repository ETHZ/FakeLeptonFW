#-----------
# DATA
#-----------
## make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/1lep/DoubleMu-Run2012.root
## make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/1lep/DoubleElectron-Run2012.root
#
#-----------
# QCD
#-----------
#make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/1lep/QCD-Pt-20-MuEnrichedPt-15-TuneZ2star-8TeV-pythia6.root
#-----------
# TTBAR
#-----------
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/TTJets-SemiLeptMGDecays-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/TTJets-FullLeptMGDecays-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/TTJets-HadronicMGDecays-V03-09-01.root
#-----------
# Single TOP
#-----------
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/T-s-channel-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/T-t-channel-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/T-tW-channel-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/Tbar-s-channel-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/Tbar-t-channel-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/Tbar-tW-channel-V03-09-01.root
#-----------
# WJETS
#-----------
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/W1JetsToLNu-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/W2JetsToLNu-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/W3JetsToLNu-V03-09-01.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/W4JetsToLNu-V03-09-01.root
#-----------
# RARES
#-----------
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/TTWJets-V03-09-00.root
make Closure && time ./Closure -r histos_closuretest.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/TTZJets-V03-09-00.root
#-----------
# DYJETS
#-----------
#make Closure && ./Closure -r histos_Mu17MCEle17JMC.root -o closureTest -c closure.config -i ~/fakeTrees/2leps/DYJetsToLL-M-50-TuneZ2Star-8TeV-madgraph-tarball.root
