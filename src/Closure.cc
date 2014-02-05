/*****************************************************************************
* this should be first go for the FR framework. marc dunser, 2014            *
*****************************************************************************/

#include "include/Closure.hh"

// ClassImp(Closure);
using namespace std;

//____________________________________________________________________________
Closure::Closure(){
	// Default constructor
	init();
}

//____________________________________________________________________________
Closure::~Closure(){}

//____________________________________________________________________________
void Closure::init(bool verbose){
	cout << "------------------------------------" << endl;
	cout << "Initializing Closure Class ... " << endl;
	cout << "------------------------------------" << endl;
	fOutputSubDir = "";
	Util::SetStyle();
}

// -------------------------------------------------------------
// -------------------------------------------------------------
// -------------------------------------------------------------


void Closure::doStuff(){
	loop("/shome/mdunser/ttW2013/CMSSW_5_3_7_patch5/src/ASAnalysis/ttz_minitrees/ttz_madgraph_newmothers.root");

}
void Closure::loop(const char * filestring){


	TFile * file_ = TFile::Open(filestring);
	TTree * tree_ = (TTree *) file_->Get("Analysis"); // tree name has to be "Analysis"
	tree_->ResetBranchAddresses();
	Init(tree_);
	Long64_t tot_events = tree_->GetEntriesFast();

	int ntot = 0;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		tree_->GetEntry(jentry);
		ntot++;
	}
	cout << "i just looped on " << ntot << " events." << endl;
	cout << " for the closure test" << endl;
	delete file_, tree_;
}
