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

	// the following two lines fix an error. believe it or not
	TCanvas * dummy = new TCanvas();
	delete dummy;

	fFRFileString = frfilestring;
	cout << "INPUT FILE WITH FR VALUES: " << fFRFileString << endl;
	fFRFile = new TFile(fFRFileString, "READ");

	// SET ALL THE HISTOGRAMS CORRECTLY
	f_h_FR_data_el      = (TH2F*) fFRFile->Get("FR_data_el");
	f_h_FR_data_pure_el = (TH2F*) fFRFile->Get("FR_data_pure_el");
	f_h_FR_mc_el        = (TH2F*) fFRFile->Get("FR_mc_el");
	f_h_FR_ttbar_el     = (TH2F*) fFRFile->Get("FR_ttbar_el");
	f_h_FR_qcd_el       = (TH2F*) fFRFile->Get("FR_qcd_el");

	f_h_FR_data_mu      = (TH2F*) fFRFile->Get("FR_data_mu");
	f_h_FR_data_pure_mu = (TH2F*) fFRFile->Get("FR_data_pure_mu");
	f_h_FR_mc_mu        = (TH2F*) fFRFile->Get("FR_mc_mu");
	f_h_FR_ttbar_mu     = (TH2F*) fFRFile->Get("FR_ttbar_all_mu");
	f_h_FR_qcd_mu       = (TH2F*) fFRFile->Get("FR_qcd_mu");


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

	fTot =0; 
	fSS  =0; fOS  =0;
	fSSmm=0; fOSmm=0;
	fSSem=0; fOSem=0; 
	fSSee=0; fOSee=0;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > (fMaxSize>0?fMaxSize:Ngen)) break;
		tree_->GetEntry(jentry);

		// fEventWeight *= PUWeight;
		fTot++;

		storePredictions();

	}

	cout << Form("fTot: %8d \t fSS: %8d \t fSSmm: %8d \t fSSem: %8d \t fSSee: %8d ", fTot, fSS, fSSmm, fSSem, fSSee) <<endl;
	cout << Form("      %8s \t fOS: %8d \t fOSmm: %8d \t fOSem: %8d \t fOSee: %8d ", ""  , fOS, fOSmm, fOSem, fOSee) <<endl;

	writeClosureTree(outFile);
	outFile->Close();

	delete file_, tree_;
}

void Closure::storePredictions(){

	resetClosureTree();

	float f1 (-1.), f2 (-1.), p1 (-1.), p2 (-1.);
	float npp(-1.), npf(-1.), nfp(-1.), nff(-1.);
	int   cat(-1);

	int lep1(-1), lep2(-1), type(-1);
	if(isSameSignLLEvent(lep1, lep2, type)){

		if(isSignalTrigger(type)) fCT_passTrigger = 1;
		else fCT_passTrigger = 0;

		if(type < 3) fSS++; 
		else fOS++; 

		bool isOF     = (type == 1 || type == 4);
		bool muFirst  = (type == 0 || type == 1 || type == 3 || type == 4);
		bool elSecond = (type == 1 || type == 2 || type == 4 || type == 5);

		f1 = (muFirst ) ? getFRatio(0, MuPt->at(lep1), MuEta->at(lep1) ) : getFRatio(1, ElPt->at(lep1), ElEta->at(lep1)) ;
		f2 = (elSecond) ? getFRatio(1, ElPt->at(lep2), ElEta->at(lep2) ) : getFRatio(0, MuPt->at(lep2), MuEta->at(lep2)) ;
		p1 = 1.;
		p2 = 1.;

		if     (type == 0 || type == 3){ // MU-MU
			if(type == 0) fSSmm++;
			else fOSmm++;
			if( isTightMuon(lep1) &&  isTightMuon(lep2)) cat = 0;
			if( isTightMuon(lep1) && !isTightMuon(lep2)) cat = 1;
			if(!isTightMuon(lep1) &&  isTightMuon(lep2)) cat = 2;
			if(!isTightMuon(lep1) && !isTightMuon(lep2)) cat = 3;
		}
		else if(type == 1 || type == 4){  // E-MU
			if(type == 1) fSSem++;
			else fOSem++;
			if( isTightMuon(lep1) &&  isTightElectron(lep2)) cat = 0;
			if( isTightMuon(lep1) && !isTightElectron(lep2)) cat = 1;
			if(!isTightMuon(lep1) &&  isTightElectron(lep2)) cat = 2;
			if(!isTightMuon(lep1) && !isTightElectron(lep2)) cat = 3;
		}
		else if(type == 2 || type == 5){ // E-E
			if(type == 2) fSSee++;
			else fOSee++;
			if( isTightElectron(lep1) &&  isTightElectron(lep2)) cat = 0;
			if( isTightElectron(lep1) && !isTightElectron(lep2)) cat = 1;
			if(!isTightElectron(lep1) &&  isTightElectron(lep2)) cat = 2;
			if(!isTightElectron(lep1) && !isTightElectron(lep2)) cat = 3;
		}
		else {cout << "TYPE IS NOT WHAT IT SHOULD BE!" << endl; exit(-1);}

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

		fCT_f1    = f1;
		fCT_f2    = f2;
		fCT_p1    = p1;
		fCT_p2    = p2;

		fCT_npp   = npp;
		fCT_npf   = npf;
		fCT_nfp   = nfp;
		fCT_nff   = nff;

		fCT_tlcat = cat;

		fCT_pt1   = (muFirst ) ? MuPt    ->at(lep1) : ElPt    ->at(lep1);
		fCT_eta1  = (muFirst ) ? MuEta   ->at(lep1) : ElEta   ->at(lep1);
		fCT_phi1  = (muFirst ) ? MuPhi   ->at(lep1) : ElPhi   ->at(lep1);
		fCT_iso1  = (muFirst ) ? MuPFIso ->at(lep1) : ElPFIso ->at(lep1);
		fCT_ch1   = (muFirst ) ? MuCharge->at(lep1) : ElCharge->at(lep1);

		fCT_pt2   = (elSecond) ? ElPt    ->at(lep2) : MuPt    ->at(lep2);
		fCT_eta2  = (elSecond) ? ElEta   ->at(lep2) : MuEta   ->at(lep2);
		fCT_phi2  = (elSecond) ? ElPhi   ->at(lep2) : MuPhi   ->at(lep2);
		fCT_iso2  = (elSecond) ? ElPFIso ->at(lep2) : MuPFIso ->at(lep2);
		fCT_ch2   = (elSecond) ? ElCharge->at(lep2) : MuCharge->at(lep2);

		fCT_nj    = Fakerates::getNJets(0);
		fCT_nb    = Fakerates::getNJets(1);
		fCT_ht    = Fakerates::getHT();
		fCT_met   = Fakerates::getMET();

 //cout << Form("%15d\t%+2d\t%6.2f%1d\t%+2d\t%6.2f\t%1d\t%d\t%d",Event, (muFirst ? MuID->at(lep1) : ElID->at(lep1) ), fCT_pt1, (muFirst ? isTightMuon(lep1) : isTightElectron(lep1) ), (elSecond ? ElID->at(lep2) : MuID->at(lep2) ), fCT_pt2, (elSecond ? isTightElectron(lep2) : isTightMuon(lep2) ), fCT_nj, fCT_nb) << endl;
		if(Event == 37051) {
			for(int i = 0; i<JetPt->size(); ++i){
				if(isGoodJet(i, 40, 0.)) cout << Form("%10d\t%.2f", Event, JetPt->at(i)) << endl;
			}
		}
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

	// make sure we get the right bin if pt is too high -----
	int corr = 0;
	if(pt >= f_h_FR_qcd_mu->GetXaxis()->GetXmax()) corr = 1;
	// ------------------------------------------------------

	if(type==0){
		fr = f_h_FR_qcd_mu->GetBinContent( f_h_FR_qcd_mu->FindBin(pt, feta) - corr);
	}
	if(type==1){
		fr = f_h_FR_qcd_el->GetBinContent( f_h_FR_qcd_el->FindBin(pt, feta) - corr);
	}

	return fr;

}


bool Closure::isSameSignLLEvent(int &lep1, int &lep2, int &type){

	std::vector< std::pair<int, int> > lepneg;
	std::vector< std::pair<int, int> > leppos;

	int nLooseSoft = 0;

	for(int i=0; i< MuPt->size(); ++i){
		if(!isLooseMuon(i))          continue;
		if(MuPt->at(i) < 20. && MuPt->at(i) > 10.) {
			nLooseSoft++;
			continue;
		}
		if      (MuCharge->at(i) < 0) 
			lepneg.push_back(make_pair(0,i));
		else if (MuCharge->at(i) > 0) 
			leppos.push_back(make_pair(0,i));
		else 
			cout << "ERROR: THERE IS A MUON WITH 0 CHARGE OR SOMETHING ELSE IS WRONG" << endl;
	
	}
	for(int i=0; i< ElPt->size(); ++i){
		if(!isLooseElectron(i))        continue;
		if(ElPt->at(i) < 20. && ElPt->at(i) > 10.) {
			nLooseSoft++;
			continue;
		}
		if      (ElCharge->at(i) < 0) 
			lepneg.push_back(make_pair(1,i));
		else if (ElCharge->at(i) > 0) 
			leppos.push_back(make_pair(1,i));
		else 
			cout << "ERROR: THERE IS AN ELECTRON WITH 0 CHARGE OR SOMETHING ELSE IS WRONG" << endl;
	
	}

	int nLeps = leppos.size()+lepneg.size();

	//if(lepneg.size() != 2 && leppos.size() != 2 && leppos.size()+lepneg.size() != 2) return false; // require == 2 any sign leptons
	if(nLeps     != 2) return false; // two leptons of any sign
	if(nLooseSoft > 0) return false; // veto on any third soft lepton

	std::vector< std::pair<int, int> > ssleps;
	
	bool isOS = false;

	if     (lepneg.size() == 2) ssleps = lepneg; // negative pairs
	else if(leppos.size() == 2) ssleps = leppos; // positive pairs
	else if(leppos.size()+lepneg.size() == 2) {
		isOS = true; // if OS, fill the positive first for SF, otherwise fill muon first
		if(leppos[0].first == lepneg[0].first){
			ssleps.push_back(leppos[0]);
			ssleps.push_back(lepneg[0]);
		}
		else{
			if(leppos[0].first == 0){
				ssleps.push_back(leppos[0]);
				ssleps.push_back(lepneg[0]);
			}
			else{
				ssleps.push_back(lepneg[0]);
				ssleps.push_back(leppos[0]);
			}
		}
	}
	else { cout << "SOMETHING WRONG WITH THE SAMESIGN SELECTION! CHECK THE CODE" << endl; exit(-1);}

	int sumLeps = ssleps[0].first + ssleps[1].first; // sum of leptons (mu: 0, el: 1)

	if     (sumLeps == 0) { // mu-mu
		lep1 = ssleps[0].second;
		lep2 = ssleps[1].second;
		type = isOS ? 3 : 0;
	}
	else if(sumLeps == 1 ) { // el-mu
		lep1 = ssleps[0].second; //since muons are filled first, this is always the muon
		lep2 = ssleps[1].second;
		type = isOS ? 4 : 1;
	}
	else if(sumLeps == 2 ) { // el-el
		lep1 = ssleps[0].second;
		lep2 = ssleps[1].second;
		type = isOS ? 5 : 2;
	}
	else { cout << "SOMETHING WRONG WITH THE SAMESIGN SELECTION! CHECK THE CODE" << endl; exit(-1);}

	if(!passMllCut(lep1, lep2, type, 12.)) return false;

	return true;
}

bool Closure::passMllCut(int lep1, int lep2, int type, float mass){
	TLorentzVector l1, l2;
	if     (type == 0 || type == 3) {
		l1.SetPtEtaPhiM(MuPt->at(lep1), MuEta->at(lep1), MuPhi->at(lep1), 0.105);
		l2.SetPtEtaPhiM(MuPt->at(lep2), MuEta->at(lep2), MuPhi->at(lep2), 0.105);
	}
	else if(type == 1 || type == 4) {
		l1.SetPtEtaPhiM(MuPt->at(lep1), MuEta->at(lep1), MuPhi->at(lep1), 0.105);
		l2.SetPtEtaPhiM(ElPt->at(lep2), ElEta->at(lep2), ElPhi->at(lep2), 0.005);
	}
	else if(type == 2 || type == 5) {
		l1.SetPtEtaPhiM(ElPt->at(lep1), ElEta->at(lep1), ElPhi->at(lep1), 0.005);
		l2.SetPtEtaPhiM(ElPt->at(lep2), ElEta->at(lep2), ElPhi->at(lep2), 0.005);
	}
	else { cout << "SOMETHING WRONG WITH THE Mll VETO! CHECK THE CODE" << endl; exit(-1);}

	if( (l1+l2).M()  < mass) return false;
	return true;

}

bool Closure::isSignalTrigger(int type){

	if     (type == 0 || type == 3){
		if(HLT_MU17_MU8 || HLT_MU17_TKMU8) return true;
	}
	else if(type == 1 || type == 4){
		if(HLT_MU8_ELE17_TIGHT || HLT_MU17_ELE8_TIGHT) return true;
	}
	else if(type == 2 || type == 5){
		if(HLT_ELE17_ELE8_TIGHT) return true;
	}
	else { cout << "WRONG TYPE IN THE TRIGGER FUNCTION" << endl; exit(-1);} 
	return false;
	
}

void Closure::bookClosureTree(){
	fClosureTree = new TTree("closureTree", "closureTree");
	fClosureTree->Branch("sname" ,  &fCT_sname) ;

	fClosureTree->Branch("run"   , &fCT_run   , "run/I"    ) ;
	fClosureTree->Branch("ls"    , &fCT_ls    , "ls/I"     ) ;
	fClosureTree->Branch("event" , &fCT_event , "event/I"  ) ;
	fClosureTree->Branch("type"  , &fCT_type  , "type/I"   ) ;
	fClosureTree->Branch("passTrigger"  , &fCT_passTrigger  , "passTrigger/I"   ) ;

	fClosureTree->Branch("lumiW" , &fCT_lumiW , "lumiW/F" ) ;

	fClosureTree->Branch("f1"    , &fCT_f1    , "f1/F"    ) ;
	fClosureTree->Branch("f2"    , &fCT_f2    , "f2/F"    ) ;
	fClosureTree->Branch("p1"    , &fCT_p1    , "p1/F"    ) ;
	fClosureTree->Branch("p2"    , &fCT_p2    , "p2/F"    ) ;

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
	fClosureTree->Branch("ch2"   , &fCT_ch2   , "ch2/I"    ) ;

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
	fCT_passTrigger  = -1;

	fCT_lumiW = -1.;

	fCT_f1   = -99.;
	fCT_f2   = -99.;
	fCT_p1   = -99.;
	fCT_p2   = -99.;

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
	fCT_ch2   = 0;

	fCT_nj    = -1;
	fCT_nb    = -1;
	fCT_ht    = -1.;
	fCT_met   = -1.;

}
