#include "include/dps.hh"


// ClassImp(dps);
using namespace std;


//____________________________________________________________________________
dps::dps(TString configfile){
	/* 
	constructor
	*/

	init();
	loadConfigFile(configfile);

}


//____________________________________________________________________________
dps::~dps(){
	// TFile * fName = new TFile(fNamename);
	// if(fName != NULL && fName->IsOpen()) fName->Close();
	delete fRand;
}


//____________________________________________________________________________
void dps::init(bool verbose){
	/*
	initializing Class "dps"
	*/

	cout << " Initializing dps Class ...                      " << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;

	fLumiweight = 1.0;
	fCutflow_afterLepSel = 0;
	fCutflow_afterJetSel = 0;
	fCutflow_afterMETCut = 0;
	fCutflow_afterMTCut  = 0;
	Util::SetStyle();
	fRand = new TRandom3(42);

}


//____________________________________________________________________________
void dps::loadConfigFile(TString configfile){
	/*
	load configuration file
	*/

	cout << " Reading Config File ...                               " << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;
	
	char buffer[1000];
	ifstream IN(configfile);
	if(!IN.is_open()) {
		cout << "*******************************************************" << endl;
		cout << " ERROR IN LOADING CONFIG FILE                          " << endl;
		cout << " Config File " << configfile << " could not be opened. " << endl;
		cout << "*******************************************************" << endl;
		exit(1);
	}

	while(IN.getline(buffer, 700, '\n')){
		if(buffer[0] == '#') continue;
		if(strlen(buffer) == 0) continue;
		if(buffer[0] == 'v') {
			char va[1], t[100], n[100], val[100];
			TString v, type, name, value;

			if(sscanf(buffer, "%s\t%s\t%s\t%s", va, t, n, val) > 3) {
				v = va; 
				type = t; 
				name = n; 
				value = val;

				if(v != "v") { cout << " ERROR in reading variable (" << name << ")!" << endl; exit(1); }

				if      (type == "TString" && name == "fOutputDir")      fOutputDir      = value;
				else if (type == "float"   && name == "fLuminosity")     fLuminosity     = value.Atof();
				else if (type == "bool"    && name == "fJetCorrection")  fJetCorrection  = (bool) value.Atoi();
				else if (type == "float"   && name == "fJetPtCut")       fJetPtCut       = value.Atof();
				else if (type == "float"   && name == "fMuPtCut")        fMuPtCut        = value.Atof();
				else if (type == "float"   && name == "fMuD0Cut")        fMuD0Cut        = value.Atof();
				else if (type == "float"   && name == "fMuIsoCut")       fMuIsoCut       = value.Atof();
				else if (type == "float"   && name == "fAwayJetBTagCut") fAwayJetBTagCut = value.Atof();
				else if (type == "float"   && name == "fAwayJetDPhiCut") fAwayJetDPhiCut = value.Atof();
				else { cout << " ERROR in reading variable (" << name << ")!" << endl; exit(1); }
			}
			else {
				cout << "*******************************************************" << endl;
				cout << " ERROR IN READING CONFIG FILE!                         " << endl;
				cout << " Same variable definitions have wrong format.          " << endl;
				cout << " exiting...                                            " << endl;
				cout << "*******************************************************" << endl;
				exit(1);
			}
		}
	}
	
	cout << " fOutputDir:       " << fOutputDir      << endl;
	cout << " fLuminosity:      " << fLuminosity     << endl;
	cout << " fJetCorrection:   " << fJetCorrection  << endl;
	cout << " fJetPtCut:        " << fJetPtCut       << endl;
	cout << " fMuPtCut:         " << fMuPtCut        << endl;
	cout << " fMuD0Cut:         " << fMuD0Cut        << endl;
	cout << " fMuIsoCut:        " << fMuIsoCut       << endl;
	cout << " fAwayJetBTagCut:  " << fAwayJetBTagCut << endl;
	cout << " fAwayJetDPhiCut:  " << fAwayJetDPhiCut << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;
}


//____________________________________________________________________________
//____________________________________________________________________________
//____________________________________________________________________________


void dps::doStuff(){
	
	TString OutputFilename = fOutputDir + fName + "_output.root";
	if(!Util::dirExists(fOutputDir)) Util::MakeOutputDir(fOutputDir);
	TFile *pFile = new TFile(OutputFilename, "RECREATE");
	
	loop(pFile);
}


//____________________________________________________________________________
void dps::loop(TFile* pFile){
	/* 
	does the main procedure looping over all events
	parameters: none
	return: none
	*/

	fNtot = 0;
	fNss  = 0;

	// book the tree!
	bookSigTree();

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
	if(!fIsData) fLumiweight = fXSec * fLuminosity / (fMaxSize>0?fMaxSize:Ngen);
	else fLumiweight = 1.;

	cout << "total events in tree  : " << tot_events << endl;
	cout << "total events generated: " << Ngen << endl;

	cout << " going to loop over " << (fMaxSize>0?fMaxSize:tot_events) << " events..." << endl;
	cout << " eventweight is " << fLumiweight << endl;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > (fMaxSize>0?fMaxSize:Ngen)) break;
		tree_->GetEntry(jentry);
		fNtot++;

		float fEventweight = fLumiweight;
		if(!fIsData) fEventweight *= PUWeight;

		fillSigTree();


	}

	cout << " number of total events: " << fNtot << endl;
	cout << " number of ss    events: " << fNss  << endl;

	delete file_, tree_;

	// write histograms in output file
	writeSigTree(pFile);
	pFile->Close();
}

void dps::fillSigTree(){

	resetSigTree();
	int l1(-1), l2(-1), type(-1);
	if( isSameSignMMEvent(l1, l2, type) ) {

		TLorentzVector lv1, lv2, mv;
		lv1.SetPtEtaPhiM(MuPt->at(l1), MuEta->at(l1), MuPhi->at(l1), 0.105);
		lv2.SetPtEtaPhiM(MuPt->at(l2), MuEta->at(l2), MuPhi->at(l2), 0.105);
		mv .SetPtEtaPhiM(getMET(), 0., getMETPhi(), 0.);

		std::pair<float, float> rand_mts = getRandMTs(lv1, lv2, mv);

		fST_sname = fName;

		fST_run   = Run;
		fST_ls    = Lumi;
		fST_event = Event;
		fST_type  = 0;

		fST_pass3  = (int) pass3rdVeto(l1, l2,0);

		fST_weight = fLumiweight;

		fST_pt1  = MuPt->at(l1);
		fST_pt2  = MuPt->at(l2);
		fST_eta1 = MuEta->at(l1);
		fST_eta2 = MuEta->at(l2);
		fST_eta12 = MuEta->at(l1)*MuEta->at(l2);
		fST_phi1 = MuPhi->at(l1);
		fST_phi2 = MuPhi->at(l2);
		fST_dphi = Util::DeltaPhi(MuPhi->at(l1), MuPhi->at(l2));
		fST_mt1  = getMT(0, l1);
		fST_mt2  = getMT(0, l2);
		fST_mt1R  = rand_mts.first ;
		fST_mt2R  = rand_mts.second;
		fST_iso1  = MuPFIso->at(l1);
		fST_iso2  = MuPFIso->at(l2);
		fST_ch1  = MuCharge->at(l1);
		fST_ch2  = MuCharge->at(l2);

		fST_dptrel = getDPTRel(l1, l2, 0);
		fST_deltas = getDeltaS(l1, l2, 0);
		fST_lproj = lv1.Vect()*lv2.Vect();
		fST_drl = lv1.DeltaR(lv2);

		fST_mll  = getMll(l1, l2, 0);

		// first jet
		fST_j1pt  = getJetInfo(1, 1);
		fST_j1eta = getJetInfo(1, 2);
		fST_j1phi = getJetInfo(1, 3);
		fST_j1bta = getJetInfo(1, 4);
		fST_j1bst = getJetInfo(1, 5);

		// second jet
		fST_j2pt  = getJetInfo(2, 1);
		fST_j2eta = getJetInfo(2, 2);
		fST_j2phi = getJetInfo(2, 3);
		fST_j2bta = getJetInfo(2, 4);
		fST_j2bst = getJetInfo(2, 5);

		// third jet
		fST_j3pt  = getJetInfo(3, 1);
		fST_j3eta = getJetInfo(3, 2);
		fST_j3phi = getJetInfo(3, 3);
		fST_j3bta = getJetInfo(3, 4);
		fST_j3bst = getJetInfo(3, 5);

		fST_nj     = getNJets(0);
		fST_nb     = getNJets(1);
		fST_ht     = getHT();
		fST_met    = getMET();
		fST_metphi = getMETPhi();

		fST_dphi1met = Util::DeltaPhi(getMETPhi(), MuPhi->at(l1));
		fST_dphi2met = Util::DeltaPhi(getMETPhi(), MuPhi->at(l2));
		
		fSigTree->Fill();
	}

	l1 = -1; l2 = -1;
	resetSigTree();
	if( isOppSignMMEvent(l1, l2, type) ) {

		TLorentzVector lv1, lv2, mv;
		lv1.SetPtEtaPhiM(MuPt->at(l1), MuEta->at(l1), MuPhi->at(l1), 0.105);
		lv2.SetPtEtaPhiM(MuPt->at(l2), MuEta->at(l2), MuPhi->at(l2), 0.105);
		mv .SetPtEtaPhiM(getMET(), 0., getMETPhi(), 0.);

		std::pair<float, float> rand_mts = getRandMTs(lv1, lv2, mv);

		fST_sname = fName;

		fST_run   = Run;
		fST_ls    = Lumi;
		fST_event = Event;
		fST_type  = 3;

		fST_pass3  = (int) pass3rdVeto(l1, l2,0);

		fST_weight = fLumiweight;

		fST_pt1  = MuPt->at(l1);
		fST_pt2  = MuPt->at(l2);
		fST_eta1 = MuEta->at(l1);
		fST_eta2 = MuEta->at(l2);
		fST_eta12 = MuEta->at(l1)*MuEta->at(l2);
		fST_phi1 = MuPhi->at(l1);
		fST_phi2 = MuPhi->at(l2);
		fST_dphi = Util::DeltaPhi(MuPhi->at(l1), MuPhi->at(l2));
		fST_mt1  = getMT(0, l1);
		fST_mt2  = getMT(0, l2);
		fST_mt1R  = rand_mts.first ;
		fST_mt2R  = rand_mts.second;
		fST_iso1  = MuPFIso->at(l1);
		fST_iso2  = MuPFIso->at(l2);
		fST_ch1  = MuCharge->at(l1);
		fST_ch2  = MuCharge->at(l2);

		fST_dptrel = getDPTRel(l1, l2, 3);
		fST_deltas = getDeltaS(l1, l2, 3);
		fST_lproj = lv1.Vect()*lv2.Vect();
		fST_drl = lv1.DeltaR(lv2);

		fST_mll  = getMll(l1, l2, 0);

		// first jet
		fST_j1pt  = getJetInfo(1, 1);
		fST_j1eta = getJetInfo(1, 2);
		fST_j1phi = getJetInfo(1, 3);
		fST_j1bta = getJetInfo(1, 4);
		fST_j1bst = getJetInfo(1, 5);

		// second jet
		fST_j2pt  = getJetInfo(2, 1);
		fST_j2eta = getJetInfo(2, 2);
		fST_j2phi = getJetInfo(2, 3);
		fST_j2bta = getJetInfo(2, 4);
		fST_j2bst = getJetInfo(2, 5);

		// third jet
		fST_j3pt  = getJetInfo(3, 1);
		fST_j3eta = getJetInfo(3, 2);
		fST_j3phi = getJetInfo(3, 3);
		fST_j3bta = getJetInfo(3, 4);
		fST_j3bst = getJetInfo(3, 5);

		fST_nj     = getNJets(0);
		fST_nb     = getNJets(1);
		fST_ht     = getHT();
		fST_met    = getMET();
		fST_metphi = getMETPhi();

		fST_dphi1met = Util::DeltaPhi(getMETPhi(), MuPhi->at(l1));
		fST_dphi2met = Util::DeltaPhi(getMETPhi(), MuPhi->at(l2));
		
		fSigTree->Fill();
	}

}

bool dps::isOppSignMMEvent(int &l1, int &l2, int &type){

	std::vector<int> muneg;
	std::vector<int> mupos;

	for(int i=0; i< MuPt->size(); ++i){
		if(MuPt->at(i) < 10.)          continue;
		if(fabs(MuEta->at(i)) > 2.5)   continue;
		if(!isLooseMuon(i))            continue;
		if      (MuCharge->at(i) < 0) 
			muneg.push_back(i);
		else if (MuCharge->at(i) > 0) 
			mupos.push_back(i);
		else 
			cout << "ERROR: THERE IS A MUON WITH 0 CHARGE OR SOMETHING ELSE IS WRONG" << endl;
	
	}

	if(muneg.size() < 1 || mupos.size() < 1) return false;
	
	l1 = MuPt->at(muneg[0]) > MuPt->at(mupos[0]) ? muneg[0] : mupos[0];
	l2 = MuPt->at(muneg[0]) > MuPt->at(mupos[0]) ? mupos[0] : muneg[0];

	type = 3;
	
	return true;
}

//____________________________________________________________________________
bool dps::isSameSignMMEvent(int &l1, int &l2, int &type){

	std::vector<int> muneg;
	std::vector<int> mupos;

	for(int i=0; i< MuPt->size(); ++i){
		if(MuPt->at(i) < 10.)          continue;
		if(fabs(MuEta->at(i)) > 2.5)   continue;
		if(!isLooseMuon(i))            continue;
		if      (MuCharge->at(i) < 0) 
			muneg.push_back(i);
		else if (MuCharge->at(i) > 0) 
			mupos.push_back(i);
		else 
			cout << "ERROR: THERE IS A MUON WITH 0 CHARGE OR SOMETHING ELSE IS WRONG" << endl;
	
	}

	if(muneg.size() < 2 && mupos.size() < 2) return false;
	if(muneg.size() > 1){
		l1 = muneg[0];
		l2 = muneg[1];
	}
	if(mupos.size() > 1){
		l1 = mupos[0];
		l2 = mupos[1];
	}
	type = 0;
	
	return true;
}

//____________________________________________________________________________
bool dps::pass3rdVeto(int i1, int i2, int type){
	int n_add_veto_mu(0);
	int n_add_veto_el(0);

	if(type == 0){
		for(int imu = 0; imu < MuPt->size(); ++imu){
			if(imu == i1 || imu == i2) continue;
			if(isVetoMuon(imu)) n_add_veto_mu++;
		}
		for(int iel = 0; iel < ElPt->size(); ++iel){
			if(isVetoEle(iel)) n_add_veto_el++;
		}
	}

	if(n_add_veto_mu > 0 || n_add_veto_el > 0) return false;
	return true;

}


//____________________________________________________________________________
bool dps::isVetoMuon(int index){
	/* 
	checks, if the muon is loose
	parameters: index (index of the particle)
	return: true (if muon is loose), false (else)
	*/

	if(!MuIsVeto->at(index)) return false;
	if(MuPFIso->at(index) > 1.0) return false;
	return true;
}


//____________________________________________________________________________
bool dps::isLooseMuon(int index){
	/* 
	checks, if the muon is loose
	parameters: index (index of the particle)
	return: true (if muon is loose), false (else)
	*/

	if(!MuIsLoose->at(index)) return false;
	return true;
}


//____________________________________________________________________________
bool dps::isTightMuon(int index){
	/* 
	checks, if the muon is tight
	parameters: index (index of the particle)
	return: true (if muon is tight), false (else)
	*/

	if(!isLooseMuon(index)) return false;
	if(!MuIsTight->at(index)) return false;
	if(fMuIsoCut > 0.0 && MuPFIso->at(index) > fMuIsoCut) return false; // leave this commented for synching!!

	return true;
}

//____________________________________________________________________________
bool dps::isVetoEle(int index){
	/* 
	checks, if the electron is loose
	parameters: index (index of the particle)
	return: true (if electron is loose), false (else)
	*/

	if(!ElIsVeto->at(index)) return false;
	if(ElPFIso->at(index) > 1.0) return false;
	return true;
}


//____________________________________________________________________________
bool dps::isLooseEle(int index){
	/* 
	checks, if the electron is loose
	parameters: index (index of the particle)
	return: true (if electron is loose), false (else)
	*/

	if(!ElIsLoose->at(index))    return false;
	if(ElPFIso->at(index) > 0.6) return false;
	return true;
}


//____________________________________________________________________________
bool dps::isTightEle(int index){
	/* 
	checks, if the electron is tight
	parameters: index (index of the particle)
	return: true (if electron is tight), false (else)
	*/

	if(!isLooseEle(index)) return false;
	if(!ElIsTight->at(index)) return false;
	if(fMuIsoCut > 0.0 && ElPFIso->at(index) > fMuIsoCut) return false; // leave this commented for synching!!

	return true;
}


//____________________________________________________________________________
float dps::getJetPt(int index) {
	/* 
	select the right JetPt according to the JetCorrection given
	parameters: index (index of the jet)
	return: JetPt or JetRawPt of the jet
	*/

	if(fJetCorrection) return JetPt->at(index);
	else return JetRawPt->at(index);
}


//____________________________________________________________________________
float dps::getMET(){
	/* 
	select the right MET according to the level of correction
	parameters: type (type of correction)
	return: MET or MET1
	*/

	if(fJetCorrection) return pfMET1;
	else return pfMET;
}


//____________________________________________________________________________
float dps::getMETPhi(){
	/* 
	select the right METPhi according to the level of correction
	parameters: type (type of correction)
	return: METPhi or MET1Phi
	*/

	if(fJetCorrection) return pfMET1Phi;
	else return pfMETPhi;
}


//____________________________________________________________________________
float dps::getMll(int i1, int i2, int type){
	TLorentzVector l1, l2;
	if(type == 0){
		l1.SetPtEtaPhiM(MuPt->at(i1), MuEta->at(i1), MuPhi->at(i1), 0.1057);
		l2.SetPtEtaPhiM(MuPt->at(i2), MuEta->at(i2), MuPhi->at(i2), 0.1057);
		return (l1+l2).M();
	}

	return -1.;
}

//____________________________________________________________________________
float dps::getMT(int type, int ind) {
	/*
	computes MT of the event
	parameters: type (0 = muon, 1 = electron), ind (index of the particle)
	return: MT
	*/

	float pt   = -1;
	float dphi = -1.;


	if(type == 0) {
		dphi = Util::DeltaPhi(getMETPhi(), MuPhi->at(ind));
		pt   = MuPt->at(ind);
	}
	else if(type == 1) {
		dphi = Util::DeltaPhi(getMETPhi(), ElPhi->at(ind));
		pt   = ElPt->at(ind);
	}
	else {
		cout << "*******************************************************" << endl;
		cout << " ERROR in getMT(): you are not calling it correctly!   " << endl;
		cout << " exiting ...                                           " << endl;
		cout << "*******************************************************" << endl;
		exit(0);
	}

	return TMath::Sqrt( 2 * getMET() * pt * (1. - TMath::Cos(dphi)) );
}

//____________________________________________________________________________
bool dps::isGoodJet(int j, float pt = 0., float btag = 0.){
	/*
	checks, if the given jet passes certain cuts defining it as a "good" jet
	parameters: j (jet index), pt (cut on pt)
	return: true (if jet is good), false (else)
	*/     

	float minDR = 0.4;

	// if pt too low, eta too large, jet beta star too large then return false
	if(pt>0. && getJetPt(j) < pt) return false;
	if(btag>0. && JetCSVBTag->at(j) < btag) return false;
	if(fabs(JetEta->at(j)) > 2.5) return false;

	if(JetBetaStar->at(j) > 0.2*TMath::Log(NVrtx-0.67)) return false; // value for jets with eta < 2.5

	// if a tight muon with dR too small found then return false
	for(int imu = 0; imu < MuPt->size(); ++imu){
		if(isTightMuon(imu)) continue;
		if(Util::GetDeltaR(MuEta->at(imu), JetEta->at(j), MuPhi->at(imu), JetPhi->at(j)) > minDR ) continue;
		return false;
	}

    // if a tight electron with dR too small found then return false
	for(int iel = 0; iel < ElPt->size(); ++iel){
	    if(isTightEle(iel)) continue;
	    if(Util::GetDeltaR(ElEta->at(iel), JetEta->at(j), ElPhi->at(iel), JetPhi->at(j)) > minDR ) continue;
	    return false;
	}

	return true;
}

//____________________________________________________________________________
float dps::getHT(){
	/*
	compute the scalar sum HT of Pt of good jets and return it
	parameters: none
	return: HT
	*/
	
	float HT(0.);
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, fJetPtCut)) continue;
		HT += getJetPt(thisjet);
	}

	return HT;
}

//____________________________________________________________________________
float dps::getMT(float pt1, float pt2, float phi1, float phi2){
	float dphi = Util::DeltaPhi(phi1, phi2);
	float mt = TMath::Sqrt( 2*pt1*pt2 * (1. - TMath::Cos(dphi) ));
	return mt;
}


//____________________________________________________________________________
std::pair<float, float> dps::getRandMTs(TLorentzVector l1, TLorentzVector l2, TLorentzVector real_met){

	std::pair<float, float> newmts;

	bool mt1_check(false);

	float r_x(0), r_y(0);
	float mt1(0), mt2(0);
	TVector3 met1, met2;

	int n(0);
	while(!mt1_check){
		n++;
	    mt1_check = false;

	    r_x = fRand->Uniform(-80, 80);
	    r_y = fRand->Uniform(-80, 80);

	    met1.SetXYZ(r_x, r_y, 0.);
	    met2 = real_met.Vect() - met1; // the new mets must add up to the original met

  // cout << Form("newmet1: x:  %.2f y:   %.2f z:   %.2f m: %.2f  pt: %.2f", met1.X(), met1.Y(), met1.Z(), 0., met1.Pt()) << endl;
  // cout << Form("newmet2: x:  %.2f y:   %.2f z:   %.2f m: %.2f  pt: %.2f", met2.X(), met2.Y(), met2.Z(), 0., met2.Pt()) << endl;
  // cout << Form("origmet: x:  %.2f y:   %.2f z:   %.2f m: %.2f  pt: %.2f", real_met.X(), real_met.Y(), real_met.Z(), 0., real_met.Pt()) << endl;


	    // TLorentzVector res_met;
	    // res_met.SetXYZM((met1+met2).X(), (met1+met2).Y(),(met1+met2).Z(), 0.);

	    mt1 = getMT(l1.Pt(), met1.Pt(), l1.Phi(), met1.Phi());
	    mt2 = getMT(l2.Pt(), met2.Pt(), l2.Phi(), met2.Phi());

	    //cout << Form("mt1: %.2f  mt2: %.2f  sumMT: %.2f", mt1_temp, mt2_temp, mt1_temp + mt2_temp) << endl;

		newmts = make_pair(mt1, mt2);

	    if(TMath::Abs(mt1 - 80.) < 5) mt1_check = true;

		if(n>30) break; // never do more than 30 iterations
	}

	return newmts;

}

//____________________________________________________________________________
float dps::getJetInfo(int ith, int type){
	/*
	returns jet info ordered in pt: eta phi pt and tagger value
	*/

	std::vector<float> pts;
	std::vector<float> eta;
	std::vector<float> phi;
	std::vector<float> bta;
	std::vector<float> bst;
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, fJetPtCut)) continue;
		pts.push_back(JetPt      ->at(thisjet));
		eta.push_back(JetEta     ->at(thisjet));
		phi.push_back(JetPhi     ->at(thisjet));
		bta.push_back(JetCSVBTag ->at(thisjet));
		bst.push_back(JetBetaStar->at(thisjet));
	}

	if(pts.size() < ith) return -10.;
	else{
		if     (type == 1) return pts[ith-1];
		else if(type == 2) return eta[ith-1];
		else if(type == 3) return phi[ith-1];
		else if(type == 4) return bta[ith-1];
		else if(type == 5) return bst[ith-1];
	}

}

//____________________________________________________________________________
float dps::getDeltaS(int i1, int i2, int type){

	TLorentzVector l1, l2, met;
	TVector3 mt1, mt2;

	l1.SetPtEtaPhiM(MuPt->at(i1), MuEta->at(i1), MuPhi->at(i1), 0.105);
	l2.SetPtEtaPhiM(MuPt->at(i2), MuEta->at(i2), MuPhi->at(i2), 0.105);
	met.SetPtEtaPhiM(getMET(), 0., getMETPhi(), 0.);

	mt1.SetXYZ( l1.X()+met.X(), l1.Y()+met.Y(), 0.  );
	mt2.SetXYZ( l2.X()+met.X(), l2.Y()+met.Y(), 0.  );

	// float prodmt = mt1*mt2;
	// return TMath::ACos( prodmt / (getMT(0, i1) * getMT(0, i2) ) );
	float prodmt = mt1*mt2;
	return TMath::ACos( prodmt / (mt1.Pt() * mt2.Pt() ) );

}

//____________________________________________________________________________
float dps::getDPTRel(int i1, int i2, int type){

	TLorentzVector l1, l2, res;

	l1.SetPtEtaPhiM(MuPt->at(i1), MuEta->at(i1), MuPhi->at(i1), 0.105);
	l2.SetPtEtaPhiM(MuPt->at(i2), MuEta->at(i2), MuPhi->at(i2), 0.105);
	res = (l1+l2);
	return res.Pt()/ ( l1.Pt() + l2.Pt() );

}

//____________________________________________________________________________
int dps::getNJets(int btag = 0){
	/*
	counts the number of jets and b-tagged jets
	parameters: btag (0 any jet, 1 b tagged jet)
	return: anzahl jets
	*/

	int njets(0), nbjets(0);
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, fJetPtCut)) continue;
		njets++;
		if(JetCSVBTag->at(thisjet)<0.679) continue;
		nbjets++;
	}

	if(btag==1) return nbjets;
	return njets;
}



//____________________________________________________________________________
void dps::bookHistos(){
	/*
	define histograms and binning
	parameters: none
	return: none
	*/ 



}

void dps::writeSigTree(TFile *pFile){
	pFile->cd();
	fSigTree->Write("sigTree", TObject::kWriteDelete);	
}

//____________________________________________________________________________
void dps::bookSigTree(){
	fSigTree = new TTree("sigTree", "sigTree");
	fSigTree->Branch("sname" ,  &fST_sname) ;

	fSigTree->Branch("run"   ,  &fST_run,    "run/I"    ) ;
	fSigTree->Branch("ls"    ,  &fST_ls,     "ls/I"     ) ;
	fSigTree->Branch("event" ,  &fST_event,  "event/I"  ) ;
	fSigTree->Branch("type"  ,  &fST_type,   "type/I"   ) ;

	fSigTree->Branch("pass3" ,  &fST_pass3,  "pass3/I"  ) ;

	fSigTree->Branch("weight",  &fST_weight, "weight/F" ) ;

	fSigTree->Branch("pt1"   ,  &fST_pt1,    "pt1/F"    ) ;
	fSigTree->Branch("pt2"   ,  &fST_pt2,    "pt2/F"    ) ;
	fSigTree->Branch("eta1"  ,  &fST_eta1,   "eta1/F"   ) ;
	fSigTree->Branch("eta2"  ,  &fST_eta2,   "eta2/F"   ) ;
	fSigTree->Branch("eta12"  ,  &fST_eta12,   "eta12/F"   ) ;
	fSigTree->Branch("phi1"  ,  &fST_phi1,   "phi1/F"   ) ;
	fSigTree->Branch("phi2"  ,  &fST_phi2,   "phi2/F"   ) ;
	fSigTree->Branch("dphi"  ,  &fST_dphi,   "dphi/F"   ) ;
	fSigTree->Branch("mt1"   ,  &fST_mt1,    "mt1/F"    ) ;
	fSigTree->Branch("mt2"   ,  &fST_mt2,    "mt2/F"    ) ;
	fSigTree->Branch("mt1R"  ,  &fST_mt1R,   "mt1R/F"   ) ;
	fSigTree->Branch("mt2R"  ,  &fST_mt2R,   "mt2R/F"   ) ;
	fSigTree->Branch("iso1"  ,  &fST_iso1,   "iso1/F"   ) ;
	fSigTree->Branch("iso2"  ,  &fST_iso2,   "iso2/F"   ) ;
	fSigTree->Branch("ch1"   ,  &fST_ch1,    "ch1/I"    ) ;
	fSigTree->Branch("ch2"   ,  &fST_ch2,    "ch2/I"    ) ;

	fSigTree->Branch("dptrel"   ,  &fST_dptrel,    "dptrel/F"    ) ;
	fSigTree->Branch("deltas"   ,  &fST_deltas,    "deltas/F"    ) ;
	fSigTree->Branch("lproj"   ,  &fST_lproj,    "lproj/F"    ) ;
	fSigTree->Branch("drl"   ,  &fST_drl,    "drl/F"    ) ;

	fSigTree->Branch("mll"   ,  &fST_mll,    "mll/F"    ) ;

	fSigTree->Branch("j1pt"  ,  &fST_j1pt,   "j1pt/F"   ) ;
	fSigTree->Branch("j1eta" ,  &fST_j1eta,  "j1eta/F"  ) ;
	fSigTree->Branch("j1phi" ,  &fST_j1phi,  "j1phi/F"  ) ;
	fSigTree->Branch("j1bta" ,  &fST_j1bta,  "j1bta/F"  ) ;
	fSigTree->Branch("j1bst" ,  &fST_j1bst,  "j1bst/F"  ) ;
	fSigTree->Branch("j2pt"  ,  &fST_j2pt,   "j2pt/F"   ) ;
	fSigTree->Branch("j2eta" ,  &fST_j2eta,  "j2eta/F"  ) ;
	fSigTree->Branch("j2phi" ,  &fST_j2phi,  "j2phi/F"  ) ;
	fSigTree->Branch("j2bta" ,  &fST_j2bta,  "j2bta/F"  ) ;
	fSigTree->Branch("j2bst" ,  &fST_j2bst,  "j2bst/F"  ) ;
	fSigTree->Branch("j3pt"  ,  &fST_j3pt,   "j3pt/F"   ) ;
	fSigTree->Branch("j3eta" ,  &fST_j3eta,  "j3eta/F"  ) ;
	fSigTree->Branch("j3phi" ,  &fST_j3phi,  "j3phi/F"  ) ;
	fSigTree->Branch("j3bta" ,  &fST_j3bta,  "j3bta/F"  ) ;
	fSigTree->Branch("j3bst" ,  &fST_j3bst,  "j3bst/F"  ) ;

	fSigTree->Branch("nj"    ,  &fST_nj,     "nj/I"     ) ;
	fSigTree->Branch("nb"    ,  &fST_nb,     "nb/I"     ) ;
	fSigTree->Branch("ht"    ,  &fST_ht,     "ht/F"     ) ;
	fSigTree->Branch("met"   ,  &fST_met,    "met/F"    ) ;
	fSigTree->Branch("metphi",  &fST_metphi, "metphi/F" ) ;
	fSigTree->Branch("dphi1met",  &fST_dphi1met, "dphi1met/F" ) ;
	fSigTree->Branch("dphi2met",  &fST_dphi2met, "dphi2met/F" ) ;

}

void dps::resetSigTree(){
	fST_sname = "";

	fST_run = -1;
	fST_ls = -1;
	fST_event = -1;
	fST_type = -1;

	fST_pass3 = -1;

	fST_weight = -1;

	fST_pt1 = -1;
	fST_pt2 = -1;
	fST_eta1 = -1;
	fST_eta2 = -1;
	fST_eta12 = -10.;
	fST_phi1 = -1;
	fST_phi2 = -1;
	fST_dphi = -1;
	fST_mt1 = -1;
	fST_mt2 = -1;
	fST_mt1R = -1;
	fST_mt2R = -1;
	fST_iso1 = -1;
	fST_iso2 = -1;
	fST_ch1 = 0;
	fST_ch2 = 0;

	fST_dptrel = -1;
	fST_deltas = -1;
	fST_lproj = -10.;
	fST_drl = -10.;

	fST_mll = -1;

	fST_j1pt = -10;
	fST_j1eta = -10;
	fST_j1phi = -10;
	fST_j1bta = -10;
	fST_j1bst = -10;
	fST_j2pt = -10;
	fST_j2eta = -10;
	fST_j2phi = -10;
	fST_j2bta = -10;
	fST_j2bst = -10;
	fST_j3pt = -10;
	fST_j3eta = -10;
	fST_j3phi = -10;
	fST_j3bta = -10;
	fST_j3bst = -10;

	fST_nj = -1;
	fST_nb = -1;
	fST_ht = -1;
	fST_met = -1;
	fST_metphi = -1;
	fST_dphi1met = -10.;
	fST_dphi2met = -10.;
}


//____________________________________________________________________________
void dps::writeHistos(TFile* pFile){
	/* 
	write histograms in output files
	parameters: pFile (output file)
	return: none
	*/

	pFile->cd(); 
	TDirectory* sdir = Util::FindOrCreate(fName, pFile);
	sdir->cd();



}
