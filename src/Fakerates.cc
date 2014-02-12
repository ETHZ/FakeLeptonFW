/*****************************************************************************
* this should be a first go at the FR framework. marc dunser, 2014            *
*****************************************************************************/

#include "include/Fakerates.hh"

// ClassImp(Fakerates);
using namespace std;

//____________________________________________________________________________
Fakerates::Fakerates(){
	// Default constructor
	init();
}

//____________________________________________________________________________
Fakerates::~Fakerates(){}

//____________________________________________________________________________
void Fakerates::init(bool verbose){
	cout << "------------------------------------" << endl;
	cout << "Initializing Fakerates Class ... " << endl;
	cout << "------------------------------------" << endl;
	fOutputSubDir = "";
	Util::SetStyle();
}

// -------------------------------------------------------------
// -------------------------------------------------------------
// -------------------------------------------------------------


void Fakerates::doStuff(){
	Sample * sample();
	loop();

}
void Fakerates::loop(){


	TFile * file_ = TFile::Open(fInputFile);
	TTree * tree_ = (TTree *) file_->Get("Analysis"); // tree name has to be named "Analysis"
	tree_->ResetBranchAddresses();
	Init(tree_);
	Long64_t tot_events = tree_->GetEntriesFast();

	int ntot = 0;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		tree_->GetEntry(jentry);
		ntot++;

		// fillRatios();
		fillIsoPlots();
	}
	cout << "i just looped on " << ntot << " events." << endl;
	delete file_, tree_;
}

bool Fakerates::isCalibrationRegionMuEvent(int &mu){
	int nloose(0), nveto_add(0);
	for(int i=0; MuPt->size(); ++i){
		if(MuIsLoose->at(i)){
			nloose++;
			mu = i;
		}
		if(!MuIsLoose->at(i) && MuIsVeto->at(i)){
			nveto_add++;
		}
	}
	// require exactly one loose muon and no additional veto muons
	if(nloose    != 1) return false;
	if(nveto_add != 0) return false;

	// upper cuts on MT and MET
	if(pfMET > 30.)              return false;
	if(MuMT->at(mu) > 30.) return false;

	int nawayjets(0);
	for(int i=0; JetPt->size(); ++i){
		if(JetPt->at(i) < 40.) continue;
		if(Util::DeltaPhi(JetPhi->at(i), MuPhi->at(mu)) < 2.0 ) continue;
		nawawyjets++;
	}
	if(nawayjets != 1) return false;
	return true;
}

bool Fakerates::isCalibrationRegionElEvent(){
	return false;	
}

void Fakerates::fillIsoPlots(){
	int mu(-1);
	if(isCalibrationRegionMuEvent(mu)){
		muIsoPlot->Fill(MuPFIso->at(mu));
	}
	int el(-1);
	if(isCalibrationRegionElEvent(el)){
		elIsoPlot->Fill(ElPFIso->at(el));
	}
}

