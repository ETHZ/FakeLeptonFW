/*****************************************************************************
* this should be a first go at the FR framework. marc dunser, 2014            *
*****************************************************************************/

#include "include/Closure.hh"
#include "include/FakeRatios.hh"
#include "include/Fakerates.hh"


// ClassImp(Closure);
using namespace std;

//____________________________________________________________________________
Closure::Closure(TString frfilestring, TString configfile):Fakerates(configfile){
	// Default constructor
	init(frfilestring);
}

//____________________________________________________________________________
Closure::~Closure(){
	fFRFile->Close();
	delete fFR;
}

//____________________________________________________________________________
void Closure::init(TString frfilestring){
	cout << "------------------------------------" << endl;
	cout << "Initializing Closure Class ... " << endl;
	cout << "------------------------------------" << endl;
	fOutputSubDir = "";
	Util::SetStyle();

	fFRFileString = frfilestring;
	cout << "INPUT FILE WITH FR VALUES: " << fFRFileString << endl;
	fFRFile = new TFile(fFRFileString, "READ");

	// SET ALL THE HISTOGRAMS CORRECTLY
	f_h_FR_data_el      = (TH2F*) fFRFile->Get("FR_data_el");
	f_h_FR_data_mu      = (TH2F*) fFRFile->Get("FR_data_mu");
	f_h_FR_data_pure_el = (TH2F*) fFRFile->Get("FR_data_pure_el");
	f_h_FR_data_pure_mu = (TH2F*) fFRFile->Get("FR_data_pure_mu");
	f_h_FR_mc_el        = (TH2F*) fFRFile->Get("FR_mc_el");
	f_h_FR_mc_mu        = (TH2F*) fFRFile->Get("FR_mc_mu");
	f_h_FR_ttbar_el     = (TH2F*) fFRFile->Get("FR_ttbar_el");
	f_h_FR_ttbar_mu     = (TH2F*) fFRFile->Get("FR_ttbar_mu");


	fLuminosity = 19500.;

	fFR = new FakeRatios();

}

// -------------------------------------------------------------
// -------------------------------------------------------------
// -------------------------------------------------------------


void Closure::doStuff(){
	
	cout << "fOutputDir: " << fOutputDir << endl;
	cout << "fName: " << fName << endl;
	TString OutputFilename = fOutputDir + "/"+ fName + "_closureOutput.root";
	//TString OutputFilename = fName + "_closureOutput.root";
	if(!Util::dirExists(fOutputDir)) Util::MakeOutputDir(fOutputDir);
	TFile *outFile = new TFile(OutputFilename, "RECREATE");
	
	loop(outFile);
}

void Closure::loop(TFile * outFile){
	/* 
	does the main procedure looping over all events
	parameters: none
	return: none
	*/

	// book the output tree!
	bookClosureTree();


	// open input file and read the tree
	TFile * file_ = TFile::Open(fInputFile);
	if(file_ == NULL ) {
		cout << "**************************************************************************" << endl;
		cout << " ERROR: THE FILE YOU ARE TRYING TO READ ISN'T OPEN. CHECK ITS EXISTENCE!!!" << endl;
		cout << " exiting ...                                            " << endl;
		cout << "**************************************************************************" << endl;
		exit(0);
	}
	TTree * tree_ = (TTree *) file_->Get("Analysis"); // tree name has to be named "Analysis"
	tree_->ResetBranchAddresses();
	Init(tree_);
	Long64_t tot_events = tree_->GetEntriesFast();
    
	// calculate the eventweight
	TH1F * EventCount = (TH1F*) file_->Get("EventCount");
	Double_t Ngen = EventCount->GetEntries();
	if(!fIsData) fEventWeight = fXSec * fLuminosity / (fMaxSize>0?fMaxSize:Ngen);
	else fEventWeight = 1.;

	cout << "total events in tree  : " << tot_events << endl;
	cout << "total events generated: " << Ngen << endl;

	cout << " going to loop over " << (fMaxSize>0?fMaxSize:tot_events) << " events..." << endl;
	cout << " eventweight is " << fEventWeight << endl;

	fTot = 0; fSS = 0; fSSmm = 0;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > (fMaxSize>0?fMaxSize:Ngen)) break;
		tree_->GetEntry(jentry);

		fEventWeight *= PUWeight;
		fTot++;

		storePredictions();

	}

	cout << Form("fTot: %d \t fSS: %d \t fSSmm: %d", fTot, fSS, fSSmm) <<endl;

	writeClosureTree(outFile);
	outFile->Close();

	delete file_, tree_;
}

void Closure::storePredictions(){

	resetClosureTree();

	float f1 (-1.), f2 (-1.), p1 (-1.), p2 (-1.);
	float npp(-1.), npf(-1.), nfp(-1.), nff(-1.);
	int   cat(-1);

	int mu1(-1), mu2(-1), type(-1);
	if(isSameSignLLEvent(mu1, mu2, type)){
		fSS++; fSSmm++;

		f1 = getFRatio(0, MuPt->at(mu1), fabs(MuEta->at(mu1)) );
		f2 = getFRatio(0, MuPt->at(mu2), fabs(MuEta->at(mu2)) );
		p1 = 1.;
		p2 = 1.;

		if( Fakerates::isTightMuon(mu1) &&  Fakerates::isTightMuon(mu2)) cat = 0;
		if( Fakerates::isTightMuon(mu1) && !Fakerates::isTightMuon(mu2)) cat = 1;
		if(!Fakerates::isTightMuon(mu1) &&  Fakerates::isTightMuon(mu2)) cat = 2;
		if(!Fakerates::isTightMuon(mu1) && !Fakerates::isTightMuon(mu2)) cat = 3;

		// Get the weights (don't depend on event selection)
		npp = fFR->getWpp(FakeRatios::gTLCat(cat), f1, f2, p1, p2);
		npf = fFR->getWpf(FakeRatios::gTLCat(cat), f1, f2, p1, p2);
		nfp = fFR->getWfp(FakeRatios::gTLCat(cat), f1, f2, p1, p2);
		nff = fFR->getWff(FakeRatios::gTLCat(cat), f1, f2, p1, p2);

		// cout << Form("category: %d \n npp: %.3f  npf: %.3f  nfp: %.3f  nff: %.3f", cat, npp, npf, nfp, nff) << endl;


		fCT_sname = fName;

		fCT_run   = Run;
		fCT_ls    = Lumi;
		fCT_event = Event;
		fCT_type  = type;

		fCT_lumiW = fEventWeight;
		fCT_npp   = npp;
		fCT_npf   = npf;
		fCT_nfp   = nfp;
		fCT_nff   = nff;

		fCT_tlcat = cat;

		fCT_pt1   = MuPt->at(mu1);
		fCT_pt2   = MuPt->at(mu2);
		fCT_eta1  = MuEta->at(mu1);
		fCT_eta2  = MuEta->at(mu2);
		fCT_phi1  = MuPhi->at(mu1);
		fCT_phi2  = MuPhi->at(mu2);
		fCT_iso1  = MuPFIso->at(mu1);
		fCT_iso2  = MuPFIso->at(mu2);
		fCT_ch1   = MuCharge->at(mu1);

		fCT_nj    = Fakerates::getNJets(0);
		fCT_nb    = Fakerates::getNJets(1);
		fCT_ht    = Fakerates::getHT();
		fCT_met   = Fakerates::getMET();

		fClosureTree->Fill();
	}


}

float Closure::getFRatio(int type, float pt, float eta){

	float feta = fabs(eta); //just to make sure
	if(feta >= 2.5) {
		cout << "NOT GOING TO WORK WITH ETA >= 2.5" << endl; 
		exit(-1);
	}

	float fr(-1.);

	int corr = 0;
	if(pt >= f_h_FR_mc_mu->GetXaxis()->GetXmax()) corr = 1; // make sure we get the right bin if pt is too high

	if(type==0){
		fr = f_h_FR_ttbar_mu->GetBinContent( f_h_FR_ttbar_mu->FindBin(pt, feta) - corr);
		//fr = f_h_FR_mc_mu->GetBinContent( f_h_FR_mc_mu->FindBin(pt, feta) - corr);
	}

	return fr;

}


bool Closure::isSameSignLLEvent(int &mu1, int &mu2, int &type){

	std::vector<int> muneg;
	std::vector<int> mupos;

	for(int i=0; i< MuPt->size(); ++i){
		if(MuPt->at(i) < 20.)        continue;
		if(fabs(MuEta->at(i)) > 2.5) continue;
		//if(!MuIsLoose->at(i))        continue;
		if(!isLooseMuon(i))        continue;
		if      (MuCharge->at(i) < 0) 
			muneg.push_back(i);
		else if (MuCharge->at(i) > 0) 
			mupos.push_back(i);
		else 
			cout << "ERROR: THERE IS A MUON WITH 0 CHARGE OR SOMETHING ELSE IS WRONG" << endl;
	
	}

	if(muneg.size() < 2 && mupos.size() < 2) return false;
	if(muneg.size() > 1){
		mu1 = muneg[0];
		mu2 = muneg[1];
	}
	if(mupos.size() > 1){
		mu1 = mupos[0];
		mu2 = mupos[1];
	}
	type = 0;
	
	return true;
}

void Closure::bookClosureTree(){
	fClosureTree = new TTree("closureTree", "closureTree");
	fClosureTree->Branch("sname" ,  &fCT_sname) ;

	fClosureTree->Branch("run"   , &fCT_run   , "run/I"    ) ;
	fClosureTree->Branch("ls"    , &fCT_ls    , "ls/I"     ) ;
	fClosureTree->Branch("event" , &fCT_event , "event/I"  ) ;
	fClosureTree->Branch("type"  , &fCT_type  , "type/I"   ) ;

	fClosureTree->Branch("lumiW" , &fCT_lumiW , "lumiW/F" ) ;
	fClosureTree->Branch("npp"   , &fCT_npp   , "npp/F"   ) ;
	fClosureTree->Branch("npf"   , &fCT_npf   , "npf/F"   ) ;
	fClosureTree->Branch("nfp"   , &fCT_nfp   , "nfp/F"   ) ;
	fClosureTree->Branch("nff"   , &fCT_nff   , "nff/F"   ) ;
	fClosureTree->Branch("tlcat" , &fCT_tlcat , "tlcat/I" ) ;

	fClosureTree->Branch("pt1"   , &fCT_pt1   , "pt1/F"    ) ;
	fClosureTree->Branch("pt2"   , &fCT_pt2   , "pt2/F"    ) ;
	fClosureTree->Branch("eta1"  , &fCT_eta1  , "eta1/F"   ) ;
	fClosureTree->Branch("eta2"  , &fCT_eta2  , "eta2/F"   ) ;
	fClosureTree->Branch("phi1"  , &fCT_phi1  , "phi1/F"   ) ;
	fClosureTree->Branch("phi2"  , &fCT_phi2  , "phi2/F"   ) ;
	fClosureTree->Branch("iso1"  , &fCT_iso1  , "iso1/F"   ) ;
	fClosureTree->Branch("iso2"  , &fCT_iso2  , "iso2/F"   ) ;
	fClosureTree->Branch("ch1"   , &fCT_ch1   , "ch1/I"    ) ;

	fClosureTree->Branch("nj"    , &fCT_nj    , "nj/I"     ) ;
	fClosureTree->Branch("nb"    , &fCT_nb    , "nb/I"     ) ;
	fClosureTree->Branch("ht"    , &fCT_ht    , "ht/F"     ) ;
	fClosureTree->Branch("met"   , &fCT_met   , "met/F"    ) ;

}
void Closure::writeClosureTree(TFile *pFile){
	pFile->cd();
	fClosureTree->Write("closureTree", TObject::kWriteDelete);	
}
void Closure::resetClosureTree(){
	fCT_sname = "";

	fCT_run   = -1;
	fCT_ls    = -1;
	fCT_event = -1;
	fCT_type  = -1;

	fCT_lumiW = -1.;
	fCT_npp   = -99.;
	fCT_npf   = -99.;
	fCT_nfp   = -99.;
	fCT_nff   = -99.;
	fCT_tlcat = -1;

	fCT_pt1   = -1.;
	fCT_pt2   = -1.;
	fCT_eta1  = -1.;
	fCT_eta2  = -1.;
	fCT_phi1  = -99.;
	fCT_phi2  = -99.;
	fCT_iso1  = -1.;
	fCT_iso2  = -1.;
	fCT_ch1   = 0;

	fCT_nj    = -1;
	fCT_nb    = -1;
	fCT_ht    = -1.;
	fCT_met   = -1.;

}
