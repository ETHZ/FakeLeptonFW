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
	loop("/shome/mdunser/framework/release/fakeminitree.root");

}
void Fakerates::loop(const char * filestring){


	TFile * file_ = TFile::Open(filestring);
	TTree * tree_ = (TTree *) file_->Get("Analysis"); // tree name has to be named "Analysis"
	tree_->ResetBranchAddresses();
	Init(tree_);
	Long64_t tot_events = tree_->GetEntriesFast();

	int ntot = 0;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		tree_->GetEntry(jentry);
		// if(Event % 100 == 0) cout << "Event: " << Event << endl;
		if(ElPt->size() > 0) {
			cout << "more than one electron present" << endl;
			cout << " pt of first electron: " << ElPt->at(0) << endl;
			cout << " pt of first electron: " << (*ElPt)[0] << endl;
		}
		ntot++;
	}
	cout << "i just looped on " << ntot << " events." << endl;
	delete file_, tree_;
}
