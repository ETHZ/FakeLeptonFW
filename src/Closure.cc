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

	fBTagSF = new BTagSF();
	fBTagRandom = new TRandom3(42);

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

	f_h_PR_dy_el        = (TH2F*) fFRFile->Get("PR_mc_el");
	f_h_PR_dy_mu        = (TH2F*) fFRFile->Get("PR_mc_mu");

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

	bookHistos();

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > (fMaxSize>0?fMaxSize:Ngen)) break;
		tree_->GetEntry(jentry);

		// fEventWeight *= PUWeight;
		fTot++;

		storePredictions();

		fillGenPlots();

	}

	cout << Form("fTot: %8d \t fSS: %8d \t fSSmm: %8d \t fSSem: %8d \t fSSee: %8d ", fTot, fSS, fSSmm, fSSem, fSSee) <<endl;
	cout << Form("      %8s \t fOS: %8d \t fOSmm: %8d \t fOSem: %8d \t fOSee: %8d ", ""  , fOS, fOSmm, fOSem, fOSee) <<endl;

	writeClosureTree(outFile);
	writeHistos(outFile);
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
		p1 = (muFirst ) ? getPRatio(0, MuPt->at(lep1), MuEta->at(lep1) ) : getPRatio(1, ElPt->at(lep1), ElEta->at(lep1)) ;
		p2 = (elSecond) ? getPRatio(1, ElPt->at(lep2), ElEta->at(lep2) ) : getPRatio(0, MuPt->at(lep2), MuEta->at(lep2)) ;
		//p1 = 1.;
		//p2 = 1.;

		if(muFirst && type < 3){
			if( abs(MuPartonID->at(lep1)) < 10) { //require leptons from quarks
				h_muPt_partonPt_SS         -> Fill(MuPt->at(lep1), MuPartonPt->at(lep1));
				if(JetPt->size() > 0) {
					int closestJet = getClosestJet(lep1);
					h_leptonPt_closestJetPt_SS -> Fill(MuPt->at(lep1), JetPt->at(closestJet)      );
					h_closestJetPt_partonPt_SS -> Fill(JetPt->at(closestJet), MuPartonPt->at(lep1));
					h_mu_closestJet_dr_SS      -> Fill(getClosestJetDR(lep1));
				}
			}
		}
		if(!elSecond && type < 3){
			if( abs(MuPartonID->at(lep2)) < 10) { //require leptons from quarks
				h_muPt_partonPt_SS         -> Fill(MuPt->at(lep2), MuPartonPt->at(lep2));
				if(JetPt->size() > 0) {
					int closestJet = getClosestJet(lep2);
					h_leptonPt_closestJetPt_SS -> Fill(MuPt->at(lep2), JetPt->at(closestJet)      );
					h_closestJetPt_partonPt_SS -> Fill(JetPt->at(closestJet), MuPartonPt->at(lep2));
					h_mu_closestJet_dr_SS      -> Fill(getClosestJetDR(lep2));
				}
			}
		}

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
		fCT_puW   = PUWeight;

		fCT_f1    = f1;
		fCT_f2    = f2;
		fCT_p1    = p1;
		fCT_p2    = p2;

		fCT_npp   = npp;
		fCT_npf   = npf;
		fCT_nfp   = nfp;
		fCT_nff   = nff;

		fCT_tlcat = cat;

		fCT_pt1     = (muFirst ) ? MuPt    ->at(lep1) : ElPt    ->at(lep1);
		fCT_eta1    = (muFirst ) ? MuEta   ->at(lep1) : ElEta   ->at(lep1);
		fCT_phi1    = (muFirst ) ? MuPhi   ->at(lep1) : ElPhi   ->at(lep1);
		fCT_mt1     = (muFirst ) ? getMT(lep1, 0)     : getMT(lep1, 1);
		fCT_ch1     = (muFirst ) ? MuCharge->at(lep1) : ElCharge->at(lep1);
		fCT_iso1    = (muFirst ) ? MuPFIso ->at(lep1) : ElPFIso ->at(lep1);
		fCT_ip1     = (muFirst ) ? MuD0    ->at(lep1) : ElD0    ->at(lep1);
		fCT_neiso1  = (muFirst ) ? MuNeIso ->at(lep1) : ElNeIso ->at(lep1);
		fCT_phiso1  = (muFirst ) ? MuPhIso ->at(lep1) : ElPhIso ->at(lep1);
		fCT_chiso1  = (muFirst ) ? MuChIso ->at(lep1) : ElChIso ->at(lep1);
		fCT_pucor1  = (muFirst ) ? MuSumPU ->at(lep1) : Rho;

		fCT_pt2     = (elSecond) ? ElPt    ->at(lep2)  : MuPt    ->at(lep2);
		fCT_eta2    = (elSecond) ? ElEta   ->at(lep2)  : MuEta   ->at(lep2);
		fCT_phi2    = (elSecond) ? ElPhi   ->at(lep2)  : MuPhi   ->at(lep2);
		fCT_mt2     = (elSecond) ? getMT(lep2, 1)      : getMT(lep2, 0);
		fCT_ch2     = (elSecond) ? ElCharge->at(lep2)  : MuCharge->at(lep2);
		fCT_iso2    = (elSecond) ? ElPFIso ->at(lep2)  : MuPFIso ->at(lep2);
		fCT_ip2     = (elSecond) ? ElD0    ->at(lep2)  : MuD0    ->at(lep2);
		fCT_neiso2  = (elSecond ) ? ElNeIso ->at(lep2) : MuNeIso ->at(lep2);
		fCT_phiso2  = (elSecond ) ? ElPhIso ->at(lep2) : MuPhIso ->at(lep2);
		fCT_chiso2  = (elSecond ) ? ElChIso ->at(lep2) : MuChIso ->at(lep2);
		fCT_pucor2  = (elSecond ) ? Rho                : MuSumPU ->at(lep1);

		fCT_lID1   = (muFirst ) ? MuID->at(lep1) : ElID->at(lep1);
		fCT_lID2   = (elSecond) ? ElID->at(lep2) : MuID->at(lep2);
		
		fCT_lProv1 = (muFirst ) ? Fakerates::getLeptonOrigin(MuMID->at(lep1), MuGMID->at(lep1), 0) : Fakerates::getLeptonOrigin(ElMID->at(lep1), ElGMID->at(lep1), 0);
		fCT_lProv2 = (elSecond) ? Fakerates::getLeptonOrigin(ElMID->at(lep2), ElGMID->at(lep2), 0) : Fakerates::getLeptonOrigin(MuMID->at(lep2), MuGMID->at(lep2), 0);

		// things that change with systematics go here

		scaleBTags(0);
		saveJetsAndMET();

		// nominal
		fCT_nj    = Fakerates::getNJets(0);
		fCT_nb    = Fakerates::getNJets(1);
		fCT_ht    = Fakerates::getHT();
		fCT_met   = Fakerates::getMET();

		// jes up
		JESJER(1);
		fCT_nj_jesup    = Fakerates::getNJets(0);
		fCT_nb_jesup    = Fakerates::getNJets(1);
		fCT_ht_jesup    = Fakerates::getHT();
		fCT_met_jesup   = Fakerates::getMET();

		// jes down
		resetJetsAndMET();
		JESJER(2);
		fCT_nj_jesdn    = Fakerates::getNJets(0);
		fCT_nb_jesdn    = Fakerates::getNJets(1);
		fCT_ht_jesdn    = Fakerates::getHT();
		fCT_met_jesdn   = Fakerates::getMET();

		// jer
		resetJetsAndMET();
		JESJER(3);
		fCT_nj_jer    = Fakerates::getNJets(0);
		fCT_nb_jer    = Fakerates::getNJets(1);
		fCT_ht_jer    = Fakerates::getHT();
		fCT_met_jer   = Fakerates::getMET();

		// b-up
		resetJetsAndMET();
		scaleBTags(1);
		fCT_nj_bup    = Fakerates::getNJets(0);
		fCT_nb_bup    = Fakerates::getNJets(1);
		fCT_ht_bup    = Fakerates::getHT();
		fCT_met_bup   = Fakerates::getMET();

		// b-dn
		resetJetsAndMET();
		scaleBTags(2);
		fCT_nj_bdn    = Fakerates::getNJets(0);
		fCT_nb_bdn    = Fakerates::getNJets(1);
		fCT_ht_bdn    = Fakerates::getHT();
		fCT_met_bdn   = Fakerates::getMET();

		fClosureTree->Fill();
	}


}

void Closure::fillGenPlots(){
	fDataType = 1; // this should be muons

	int lep(-1), jet(-1);
	if(isFRRegionLepEvent(lep, jet, 40.) ){
		if( abs(MuPartonID->at(lep)) < 10) { //require leptons from quarks
			int closestJet = getClosestJet(lep);
			h_muPt_partonPt_MR         -> Fill(MuPt->at(lep), MuPartonPt->at(lep));
			h_leptonPt_closestJetPt_MR -> Fill(MuPt->at(lep), JetPt->at(closestJet)      );
			h_closestJetPt_partonPt_MR -> Fill(JetPt->at(closestJet), MuPartonPt->at(lep));
			h_mu_closestJet_dr_MR      -> Fill(getClosestJetDR(lep));
		}
	}
	if(MuPt->size() > 0){
		for(int ind=0; ind < MuPt->size(); ++ind){
			if(!MuIsLoose->at(ind)) continue;
			if(abs(MuPartonID->at(ind)) > 10) continue;
			h_muPt_partonPt_ALL -> Fill(MuPt->at(ind), MuPartonPt->at(ind));
			if(JetPt->size() > 0) {
				int closestJet = getClosestJet(ind);
				h_leptonPt_closestJetPt_ALL -> Fill(MuPt->at(ind), JetPt->at(closestJet)      );
				h_closestJetPt_partonPt_ALL -> Fill(JetPt->at(closestJet), MuPartonPt->at(ind));
				h_mu_closestJet_dr_ALL      -> Fill(getClosestJetDR(ind));
			}
		}
	}

}

float Closure::getPRatio(int type, float pt, float eta){

	float feta = fabs(eta); //just to make sure
	if(feta >= 2.5) {
		cout << "NOT GOING TO WORK WITH ETA >= 2.5" << endl; 
		exit(-1);
	}

	float pr(-1.);

	// make sure we get the right bin if pt is too high -----
	int corr = 0;
	if(pt >= f_h_PR_dy_mu->GetXaxis()->GetXmax()) corr = 1;
	// ------------------------------------------------------

	if(type==0){
		pr = f_h_PR_dy_mu->GetBinContent( f_h_PR_dy_mu->FindBin(pt, feta) - corr);
	}
	if(type==1){
		pr = f_h_PR_dy_el->GetBinContent( f_h_PR_dy_el->FindBin(pt, feta) - corr);
	}

	return pr;

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
	fClosureTree->Branch("puW"   , &fCT_puW   , "puW/F" ) ;

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
	fClosureTree->Branch("mt1"  , &fCT_mt1  , "mt1/F"   ) ;
	fClosureTree->Branch("mt2"  , &fCT_mt2  , "mt2/F"   ) ;
	fClosureTree->Branch("ch1"   , &fCT_ch1   , "ch1/I"    ) ;
	fClosureTree->Branch("ch2"   , &fCT_ch2   , "ch2/I"    ) ;
	fClosureTree->Branch("iso1"  , &fCT_iso1  , "iso1/F"   ) ;
	fClosureTree->Branch("iso2"  , &fCT_iso2  , "iso2/F"   ) ;
	fClosureTree->Branch("ip1"  , &fCT_ip1  , "ip1/F"   ) ;
	fClosureTree->Branch("ip2"  , &fCT_ip2  , "ip2/F"   ) ;
	fClosureTree->Branch("neiso1"  , &fCT_neiso1  , "neiso1/F"   ) ;
	fClosureTree->Branch("neiso2"  , &fCT_neiso2  , "neiso2/F"   ) ;
	fClosureTree->Branch("phiso1"  , &fCT_phiso1  , "phiso1/F"   ) ;
	fClosureTree->Branch("phiso2"  , &fCT_phiso2  , "phiso2/F"   ) ;
	fClosureTree->Branch("chiso1"  , &fCT_chiso1  , "chiso1/F"   ) ;
	fClosureTree->Branch("chiso2"  , &fCT_chiso2  , "chiso2/F"   ) ;
	fClosureTree->Branch("pucor1"  , &fCT_pucor1  , "pucor1/F"   ) ;
	fClosureTree->Branch("pucor2"  , &fCT_pucor2  , "pucor2/F"   ) ;

	fClosureTree->Branch("nj"    , &fCT_nj    , "nj/I"     ) ;
	fClosureTree->Branch("nb"    , &fCT_nb    , "nb/I"     ) ;
	fClosureTree->Branch("ht"    , &fCT_ht    , "ht/F"     ) ;
	fClosureTree->Branch("met"   , &fCT_met   , "met/F"    ) ;

	fClosureTree->Branch("nj_jesup"    , &fCT_nj_jesup    , "nj_jesup/I"     ) ;
	fClosureTree->Branch("nb_jesup"    , &fCT_nb_jesup    , "nb_jesup/I"     ) ;
	fClosureTree->Branch("ht_jesup"    , &fCT_ht_jesup    , "ht_jesup/F"     ) ;
	fClosureTree->Branch("met_jesup"   , &fCT_met_jesup   , "met_jesup/F"    ) ;

	fClosureTree->Branch("nj_jesdn"    , &fCT_nj_jesdn    , "nj_jesdn/I"     ) ;
	fClosureTree->Branch("nb_jesdn"    , &fCT_nb_jesdn    , "nb_jesdn/I"     ) ;
	fClosureTree->Branch("ht_jesdn"    , &fCT_ht_jesdn    , "ht_jesdn/F"     ) ;
	fClosureTree->Branch("met_jesdn"   , &fCT_met_jesdn   , "met_jesdn/F"    ) ;

	fClosureTree->Branch("nj_jer"    , &fCT_nj_jer    , "nj_jer/I"     ) ;
	fClosureTree->Branch("nb_jer"    , &fCT_nb_jer    , "nb_jer/I"     ) ;
	fClosureTree->Branch("ht_jer"    , &fCT_ht_jer    , "ht_jer/F"     ) ;
	fClosureTree->Branch("met_jer"   , &fCT_met_jer   , "met_jer/F"    ) ;

	fClosureTree->Branch("nj_bup"    , &fCT_nj_bup    , "nj_bup/I"     ) ;
	fClosureTree->Branch("nb_bup"    , &fCT_nb_bup    , "nb_bup/I"     ) ;
	fClosureTree->Branch("ht_bup"    , &fCT_ht_bup    , "ht_bup/F"     ) ;
	fClosureTree->Branch("met_bup"   , &fCT_met_bup   , "met_bup/F"    ) ;

	fClosureTree->Branch("nj_bdn"    , &fCT_nj_bdn    , "nj_bdn/I"     ) ;
	fClosureTree->Branch("nb_bdn"    , &fCT_nb_bdn    , "nb_bdn/I"     ) ;
	fClosureTree->Branch("ht_bdn"    , &fCT_ht_bdn    , "ht_bdn/F"     ) ;
	fClosureTree->Branch("met_bdn"   , &fCT_met_bdn   , "met_bdn/F"    ) ;


	fClosureTree->Branch("lID1"   , &fCT_lID1   , "lID1/I"    ) ;
	fClosureTree->Branch("lID2"   , &fCT_lID2   , "lID2/I"    ) ;
	fClosureTree->Branch("lProv1" , &fCT_lProv1 , "lProv1/I"  ) ;
	fClosureTree->Branch("lProv2" , &fCT_lProv2 , "lProv2/I"  ) ;

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
	fCT_puW   = -1.;

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
	fCT_ip1  = -1.;
	fCT_neiso1  = -1.;
	fCT_phiso1  = -1.;
	fCT_chiso1  = -1.;
	fCT_pucor1  = -1.;
	fCT_iso2  = -1.;
	fCT_ip2  = -1.;
	fCT_neiso2  = -1.;
	fCT_phiso2  = -1.;
	fCT_chiso2  = -1.;
	fCT_pucor2  = -1.;
	fCT_mt1  = -1.;
	fCT_mt2  = -1.;
	fCT_ch1   = 0;
	fCT_ch2   = 0;

	fCT_nj    = -1;
	fCT_nb    = -1;
	fCT_ht    = -1.;
	fCT_met   = -1.;

	fCT_nj_jesup    = -1;
	fCT_nb_jesup    = -1;
	fCT_ht_jesup    = -1.;
	fCT_met_jesup   = -1.;

	fCT_nj_jesdn    = -1;
	fCT_nb_jesdn    = -1;
	fCT_ht_jesdn    = -1.;
	fCT_met_jesdn   = -1.;

	fCT_nj_jer    = -1;
	fCT_nb_jer    = -1;
	fCT_ht_jer    = -1.;
	fCT_met_jer   = -1.;

	fCT_nj_bup    = -1;
	fCT_nb_bup    = -1;
	fCT_ht_bup    = -1.;
	fCT_met_bup   = -1.;

	fCT_nj_bdn    = -1;
	fCT_nb_bdn    = -1;
	fCT_ht_bdn    = -1.;
	fCT_met_bdn   = -1.;

	fCT_lID1   = 0;
	fCT_lID2   = 0;
	fCT_lProv1 = -1;
	fCT_lProv2 = -1;

}

void Closure::bookHistos(){
	h_muPt_partonPt_MR          = new TH2F("muPt_partonPt_MR"         , "muPt_partonPt_MR"         , 150, 0., 150., 150, 0., 150.); h_muPt_partonPt_MR          -> Sumw2();
	h_closestJetPt_partonPt_MR  = new TH2F("closestJetPt_partonPt_MR" , "closestJetPt_partonPt_MR" , 150, 0., 150., 150, 0., 150.); h_closestJetPt_partonPt_MR  -> Sumw2();
	h_leptonPt_closestJetPt_MR  = new TH2F("leptonPt_closestJetPt_MR" , "leptonPt_closestJetPt_MR" , 150, 0., 150., 150, 0., 150.); h_leptonPt_closestJetPt_MR  -> Sumw2();
	h_mu_closestJet_dr_MR       = new TH1F("mu_closestJet_dr_MR"      , "mu_closestJet_dr_MR"      ,  20, 0., 1.0);                 h_mu_closestJet_dr_MR       -> Sumw2();

	h_muPt_partonPt_ALL         = new TH2F("muPt_partonPt_ALL"        , "muPt_partonPt_ALL"        , 150, 0., 150., 150, 0., 150.); h_muPt_partonPt_ALL         -> Sumw2();
	h_closestJetPt_partonPt_ALL = new TH2F("closestJetPt_partonPt_ALL", "closestJetPt_partonPt_ALL", 150, 0., 150., 150, 0., 150.); h_closestJetPt_partonPt_ALL -> Sumw2();
	h_leptonPt_closestJetPt_ALL = new TH2F("leptonPt_closestJetPt_ALL", "leptonPt_closestJetPt_ALL", 150, 0., 150., 150, 0., 150.); h_leptonPt_closestJetPt_ALL -> Sumw2();
	h_mu_closestJet_dr_ALL      = new TH1F("mu_closestJet_dr_ALL"     , "mu_closestJet_dr_ALL"     ,  20, 0., 1.0);                 h_mu_closestJet_dr_ALL      -> Sumw2();

	h_muPt_partonPt_SS          = new TH2F("muPt_partonPt_SS"         , "muPt_partonPt_SS"         , 150, 0., 150., 150, 0., 150.); h_muPt_partonPt_SS          -> Sumw2();
	h_closestJetPt_partonPt_SS  = new TH2F("closestJetPt_partonPt_SS" , "closestJetPt_partonPt_SS" , 150, 0., 150., 150, 0., 150.); h_closestJetPt_partonPt_SS  -> Sumw2();
	h_leptonPt_closestJetPt_SS  = new TH2F("leptonPt_closestJetPt_SS" , "leptonPt_closestJetPt_SS" , 150, 0., 150., 150, 0., 150.); h_leptonPt_closestJetPt_SS  -> Sumw2();
	h_mu_closestJet_dr_SS       = new TH1F("mu_closestJet_dr_SS"      , "mu_closestJet_dr_SS"      ,  20, 0., 1.0);                 h_mu_closestJet_dr_SS       -> Sumw2();
}

void Closure::writeHistos(TFile * pFile){
	pFile->cd();
	h_muPt_partonPt_MR          -> Write();
	h_closestJetPt_partonPt_MR  -> Write();
	h_leptonPt_closestJetPt_MR  -> Write();
	h_mu_closestJet_dr_MR       -> Write();

	h_muPt_partonPt_ALL         -> Write();
	h_closestJetPt_partonPt_ALL -> Write();
	h_leptonPt_closestJetPt_ALL -> Write();
	h_mu_closestJet_dr_ALL      -> Write();

	h_muPt_partonPt_SS          -> Write();
	h_closestJetPt_partonPt_SS  -> Write();
	h_leptonPt_closestJetPt_SS  -> Write();
	h_mu_closestJet_dr_SS       -> Write();
}

// SYSTEMATICS FUNCTIONS
void Closure::saveJetsAndMET(){
	fJets.clear(); // clear the jet vector first
	for(int i=0; i<JetPt->size(); ++i){
		TLorentzVector jet;
		jet.SetPtEtaPhiE(JetPt->at(i), JetEta->at(i), JetPhi->at(i), JetEnergy->at(i));
		fJets.push_back(make_pair(jet, JetCSVBTag->at(i)) );
	}

	fMET.SetPtEtaPhiM(getMET(), 0., getMETPhi(), 0.);
}

void Closure::resetJetsAndMET(){
	for(int i=0; i<JetPt->size(); ++i){
		JetPt->at(i)      = fJets[i].first.Pt();
		JetEta->at(i)     = fJets[i].first.Eta();
		JetPhi->at(i)     = fJets[i].first.Phi();
		JetEnergy->at(i)  = fJets[i].first.E();
		JetCSVBTag->at(i) = fJets[i].second;
	}

	Fakerates::setMET(fMET.Pt());
	Fakerates::setMETPhi(fMET.Phi());
}

void Closure::scaleBTags( int flag, TString model){
	// for now supports only CSVM b-tagger. can be extended if need be
	if(fIsData) return; // do nothing for data!
	bool isFastsim = false;
	if (model != "") isFastsim= true;
	for(size_t i = 0; i < JetPt->size(); ++i){
		if(isGoodJet(i, fJetPtCut) == false) continue;
		bool is_tagged_med = JetCSVBTag->at(i) > 0.679;
		float random(-1.);
		fRandom->SetSeed(  (int) (Event * JetPt->at(i) / JetEta->at(i) ) ); // set the random seed to the same value for every min/max iteration
		if (flag == 0)	random = fRandom ->Uniform(0,1); // get random number from uniform distribution
		else			random = fRandom ->Uniform(0,1); // get random number from uniform distribution
		string meanminmax = "mean";
		if(flag == 1) meanminmax = "max";
		if(flag == 2) meanminmax = "min";

		bool newTag = fBTagSF->modifyBTagsWithSF(is_tagged_med, JetPt->at(i), JetEta->at(i), JetPartonFlav->at(i), meanminmax, random, isFastsim, model);
		if(!newTag) JetCSVBTag->at(i) = 0.1; // not tagged
		if( newTag) JetCSVBTag->at(i) = 1.0; // tagged
	}
}


void Closure::JESJER(int flag){
	// Modify the jet pt for systematics studies
	// Either shifted or smeared
	// propagate to the MET!!
	if(fIsData)   return;      // do nothing for data!
	if(flag == 0) return;      // 0 makes no sense

	//std::vector<int> cleanJets = cleanedJetIndices(15.);
	TLorentzVector oldjets, newjets, tmp;                           // 4-vec of old jets, newjets and a tmp-vector
	
	for( int ijet = 0; ijet < JetPt->size(); ++ijet) {
		tmp.SetPtEtaPhiE(JetPt->at(ijet), JetEta->at(ijet), JetPhi->at(ijet), JetEnergy->at(ijet)); // set temp to the jet
		oldjets += tmp;                                                         // add jet to the old jets vector
		if(flag == 1) JetPt->at(ijet) *= (1 + JetJECUnc->at(ijet));             // vary up for flag 1
		if(flag == 2) JetPt->at(ijet) *= (1 - JetJECUnc->at(ijet));             // vary down for flag 2;
		if(flag == 3){                                                          // smear for flag 3
			float sigmaMC  = Fakerates::getSigmaMC(JetPt->at(ijet), JetEta->at(ijet))/JetPt->at(ijet);      // get the resolution
			// float jerScale = getJERScale(*it);                                  // get JER scale factors
			// float factor = fRandom->Gaus(1., sqrt(jerScale*jerScale -1.)*sigmaMC );
			float factor = fRandom->Gaus(1., sigmaMC );
			JetPt->at(ijet) = JetPt->at(ijet) * factor;
		}
		tmp.SetPtEtaPhiE(JetPt->at(ijet), JetEta->at(ijet), JetPhi->at(ijet), JetEnergy->at(ijet)); // set tmp to the scaled/smeared jet
		newjets += tmp;                                                            // add scaled/smeared jet to the new jets
	}
	propagateMET(newjets, oldjets);   // propagate this change to the MET
}

void Closure::propagateMET(TLorentzVector nVec, TLorentzVector oVec){
	TLorentzVector met;
	met.SetPtEtaPhiM(getMET(), 0., getMETPhi(), 0.);
	// set the pfMET to the old MET minus original vector plus new vector
	Fakerates::setMET( (met+oVec-nVec).Pt() );
}
