/*****************************************************************************
* this should be a first go at the FR framework. marc dunser, 2014           *
*****************************************************************************/
//____________________________________________________________________________
//____________________________________________________________________________
//____________________________________________________________________________


#include "include/Fakerates.hh"


// ClassImp(Fakerates);
using namespace std;


//____________________________________________________________________________
Fakerates::Fakerates(TString configfile){
	/* 
	constructor
	*/

	init();
	loadConfigFile(configfile);

}


//____________________________________________________________________________
Fakerates::~Fakerates(){
	// TFile * fName = new TFile(fNamename);
	// if(fName != NULL && fName->IsOpen()) fName->Close();
}


//____________________________________________________________________________
void Fakerates::init(bool verbose){
	/*
	initializing Class "Fakerates"
	*/

	cout << " Initializing Fakerates Class ...                      " << endl;
	cout << "=======================================================" << endl;
	cout << "=======================================================" << endl;

	fLumiweight = 1.0;
	fCutflow_afterLepSel = 0;
	fCutflow_afterJetSel = 0;
	fCutflow_afterMETCut = 0;
	fCutflow_afterMTCut  = 0;
	Util::SetStyle();


	// Binning for FakeRate Projection Plots

	// Eta Binning
	fFRbinseta.push_back(0.0);
	fFRbinseta.push_back(0.5);
	fFRbinseta.push_back(1.0);
	fFRbinseta.push_back(1.5);
	fFRbinseta.push_back(2.0);
	fFRbinseta.push_back(2.5);
	fFRn_binseta  = fFRbinseta.size();

	// Pt Binning
	//fFRbinspt.push_back(10.);
	//fFRbinspt.push_back(15.);
	fFRbinspt.push_back(20.);
	fFRbinspt.push_back(25.);
	fFRbinspt.push_back(30.);
	fFRbinspt.push_back(35.);
	fFRbinspt.push_back(45.);
	fFRbinspt.push_back(46.);
	fFRn_binspt   = fFRbinspt .size();


	// Binning for Difference/Fraction in JetPt Projection Plots

	// Eta Binning
	fDFbinseta.push_back(0.0);
	fDFbinseta.push_back(1.0);
	fDFbinseta.push_back(2.4);
	fDFn_binseta  = fDFbinseta.size();

	// Pt Binning
	fDFbinspt.push_back(10.0);
	fDFbinspt.push_back(20.0);
	fDFbinspt.push_back(22.5);
	fDFbinspt.push_back(25.0);
	fDFbinspt.push_back(27.5);
	fDFbinspt.push_back(30.0);
	fDFbinspt.push_back(32.5);
	fDFbinspt.push_back(35.0);
	fDFbinspt.push_back(40.0);
	fDFbinspt.push_back(50.0);
	fDFbinspt.push_back(60.0);
	fDFbinspt.push_back(70.0);
	fDFn_binspt    = fDFbinspt.size();
}


//____________________________________________________________________________
void Fakerates::loadConfigFile(TString configfile){
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


void Fakerates::doStuff(){
	
	TString OutputFilename = fOutputDir + fName + "_ratios.root";
	if(!Util::dirExists(fOutputDir)) Util::MakeOutputDir(fOutputDir);
	TFile *pFile = new TFile(OutputFilename, "RECREATE");
	
	loop(pFile);
}


//____________________________________________________________________________
void Fakerates::loop(TFile* pFile){
	/* 
	does the main procedure looping over all events
	parameters: none
	return: none
	*/

	Long64_t ntot = 0;

	// define histograms
	bookHistos();

	// open input file and read the tree
	TFile * file_ = TFile::Open(fInputFile);
	if(file_ == NULL ) {
		cout << "*******************************************************" << endl;
		cout << " ERROR: THE FILE YOU ARE TRYING TO READ ISN'T OPEN. CHECK IT'S EXISTENCE!!!" << endl;
		cout << " exiting ...                                            " << endl;
		cout << "*******************************************************" << endl;
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
	cout << " going to loop over " << (fMaxSize>0?fMaxSize:Ngen) << " events..." << endl;
	cout << " eventweight is " << fLumiweight << endl;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > (fMaxSize>0?fMaxSize:Ngen)) break;
		tree_->GetEntry(jentry);
		ntot++;

		float fEventweight = fLumiweight;
		if(!fIsData) fEventweight *= PUWeight;

		fillFRPlots(fEventweight);

	}

	cout << " mu: nevents passing lepton selection: " << fCutflow_afterLepSel << endl;
	cout << " mu: nevents passing jet    selection: " << fCutflow_afterJetSel << endl;
	cout << " mu: nevents passing MET    selection: " << fCutflow_afterMETCut << endl;
	cout << " mu: nevents passing MT     selection: " << fCutflow_afterMTCut  << endl;
	cout << " i just looped on " << ntot << " events." << endl;
	delete file_, tree_;

	// write histograms in output file
	writeHistos(pFile);
	pFile->Close();
}


//____________________________________________________________________________
bool Fakerates::isFRRegionMuEvent(int &mu, int &jet, float jetcut){
	/*
	checks, whether the event contains exactly one muon and at least one away-jet in the calibration region
	parameters: &mu (address of muon index)
	return: true (if muon is in calibration region), false (else)
	*/ 

	int nloose(0), nveto_add(0);
	std::vector<int> loosemu_inds;
	int nawayjets(0);
	int jetind(-1);
	std::vector<int> awayjet_inds;


	// Event fails HLT muon trigger (if data) then return false
	if(fIsData && !HLT_MU17) return false;

	// muon Pt is not reasonable then return false
	if(MuPt->size() < 1) return false;

	// count numbers of loose and veto muons in the event
	for(int i=0; i < MuPt->size(); ++i){
		if(isLooseMuon(i) && MuPt->at(i) > fMuPtCut){
			nloose++;
			mu = i;
			loosemu_inds.push_back(i);		
		}
		else if(isLooseMuon(i) && MuPt->at(i) < fMuPtCut){
			nveto_add++;
		}
	}


	// require exactly one loose muon and no additional veto muons
	if(nloose    != 1) return false;
	// if(nveto_add  > 0) return false;
	fCutflow_afterLepSel++;
	// if(nveto_add != 0) return false; // don't require this for the synching

	// Jet Pt is not reasonable then return false
	if(JetRawPt->size() < 1) return false;

	// count the number of away jets
	for(int thisjet=0; thisjet < JetRawPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, jetcut, fAwayJetBTagCut)) continue;
		if(Util::GetDeltaR(JetEta->at(thisjet), MuEta->at(mu), JetPhi->at(thisjet), MuPhi->at(mu)) < 1.0 ) continue;
		nawayjets++;
		awayjet_inds.push_back(thisjet);
	}

	// no away jet found then return false 
	if(awayjet_inds.size() < 1) return false;
	fCutflow_afterJetSel++;

	// set jet index on the hardest jet
	jet = awayjet_inds[0];
	if(awayjet_inds.size() > 1)
		for(int thisjet=0; thisjet < nawayjets; ++thisjet)
			if(getJetPt(awayjet_inds[thisjet]) > getJetPt(jet) ) jet = awayjet_inds[thisjet];

	// upper cuts on MT and MET
	//if(!passesUpperMETMT(0, loosemu_inds[0]) ) return false;

	// phi cut
	if(fAwayJetDPhiCut > 0. && Util::DeltaPhi(JetPhi->at(jet), MuPhi->at(mu))<fAwayJetDPhiCut) return false;
	
    return true;
}


//____________________________________________________________________________
bool Fakerates::isLooseMuon(int index){
	/* 
	checks, if the muon is loose
	parameters: index (index of the particle)
	return: true (if muon is loose), false (else)
	*/

	if(!MuIsLoose->at(index)) return false;
	if(fMuD0Cut > 0.0 && fabs(MuD0->at(index)) > fMuD0Cut) return false; // leave this commented for synching!!
	return true;
}


//____________________________________________________________________________
bool Fakerates::isTightMuon(int index){
	/* 
	checks, if the muon is tight
	parameters: index (index of the particle)
	return: true (if muon is tight), false (else)
	*/

	if(!isLooseMuon(index)) return false;
	if(!MuIsTight->at(index)) return false;
	if(fMuIsoCut > 0.0 && fabs(MuPFIso->at(index)) > fMuIsoCut) return false; // leave this commented for synching!!

	return true;
}


//____________________________________________________________________________
float Fakerates::getJetPt(int index) {
	/* 
	select the right JetPt according to the JetCorrection given
	parameters: index (index of the jet)
	return: JetPt or JetRawPt of the jet
	*/

	if(fJetCorrection) return JetPt->at(index);
	else return JetRawPt->at(index);
}


//____________________________________________________________________________
float Fakerates::getMET(){
	/* 
	select the right MET according to the level of correction
	parameters: type (type of correction)
	return: MET or MET1
	*/

	if(fJetCorrection) return pfMET1;
	else return pfMET;
}


//____________________________________________________________________________
float Fakerates::getMETPhi(){
	/* 
	select the right METPhi according to the level of correction
	parameters: type (type of correction)
	return: METPhi or MET1Phi
	*/

	if(fJetCorrection) return pfMET1Phi;
	else return pfMETPhi;
}


//____________________________________________________________________________
float Fakerates::getMT(int type, int ind) {
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
bool Fakerates::passesMETCut(float value_met = 20., int sign = 0){
	/* 
	checks, if the event passes the MET cut
	parameters: none
	return: true (if event passes the cuts), false (else)
	*/

	if(sign == 1 && getMET() < value_met) return false;
	if(sign == 0 && getMET() > value_met) return false;
	return true;
}


//____________________________________________________________________________
bool Fakerates::passesMTCut(int type, int index){
	/* 
	checks, if the event passes the 20GeV MT cut
	parameters: type (0 = mu, 1 = el)
	return: true (if event passes the cuts), false (else)
	*/

	float value_mt  = 20.;

	// mu or el MT too large then return false
	if(type == 0){
		if(getMT(type, index) > value_mt) return false;
	}
	else if(type == 1){
		if(getMT(type, index) > value_mt) return false;
	}
	else{
		cout << "*******************************************************" << endl;
		cout << " ERROR in passesUpperMETMT(): you re not calling it correctly!" << endl;
		cout << " exiting ...                                           " << endl;
		cout << "*******************************************************" << endl;
		exit(0);
	}

	return true;
}


//____________________________________________________________________________
bool Fakerates::passesUpperMETMT(int type, int index){
	/* 
	checks, if the event passes upper MET and MT cuts
	parameters: type (0 = mu, 1 = el), index (index of the particle)
	return: true (if event passes the cuts), false (else)
	*/

    if(!passesMETCut()) return false;
    fCutflow_afterMETCut++;

    if(!passesMTCut(type, index)) return false;
    fCutflow_afterMTCut++;
	
	return true;
}


//____________________________________________________________________________
bool Fakerates::isGoodJet(int j, float pt = 0., float btag = 0.){
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

	// if(JetBetaStar->at(j) > 0.2*TMath::Log(NVrtx-0.67)) return false; // value for jets with eta < 2.5

	// jet-lepton cleaning: if a tight muon with dR too small found then return false
	for(int imu = 0; imu < MuPt->size(); ++imu){
		if(!MuIsTight->at(imu)) continue;
		if(Util::GetDeltaR(MuEta->at(imu), JetEta->at(j), MuPhi->at(imu), JetPhi->at(j)) > minDR ) continue;
		return false;
	}

    // // if a tight electron with dR too small found then return false
	// for(int iel = 0; iel < ElPt->size(); ++iel){
	//     if(!ElIsTight->at(iel)) continue;
	//     if(Util::GetDeltaR(ElEta->at(iel), JetEta->at(j), ElPhi->at(iel), JetPhi->at(j)) > minDR ) continue;
	//     return false;
	// }

	return true;
}


//____________________________________________________________________________
float Fakerates::getAwayJet(int info = 0, int mu = 0){
	/*
	get information about the away jet with largest Pt
	parameters: info (0 = Pt, 1 = dR), mu (muon index)
	return: info
	*/

	int nawayjets(0), jetind(0);
	std::vector<int> awayjet_inds;
	
	for(int thisjet=0; thisjet < JetRawPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, fJetPtCut)) continue;
		if(Util::GetDeltaR(JetEta->at(thisjet), MuEta->at(mu), JetPhi->at(thisjet), MuPhi->at(mu)) < 1.0 ) continue;
		nawayjets++;
		awayjet_inds.push_back(thisjet);
    }

	if(awayjet_inds.size() == 0) return 0.;

	jetind = awayjet_inds[0];
	if(awayjet_inds.size() > 1)
		for(int thisjet=0; thisjet < nawayjets; ++thisjet)
			if(getJetPt(awayjet_inds[thisjet]) > getJetPt(jetind) ) jetind = awayjet_inds[thisjet];

	if(info==1) return Util::GetDeltaR(JetEta->at(jetind), MuEta->at(mu), JetPhi->at(jetind), MuPhi->at(mu));
	return getJetPt(jetind);
}


//____________________________________________________________________________
float Fakerates::getClosestJet(int info = 0, int mu = 0){
	/*
	get information about the closest jet (i.e. smallest dR)
	parameters: info (0 = Pt, 1 = dR), mu (muon index)
	return: info
	*/

	int nclosjets(0), jetind(0);
	std::vector<int> closjet_inds;
	
	for(int thisjet=0; thisjet < JetRawPt->size(); ++thisjet){
		if(!isGoodJet(thisjet)) continue;
		if(Util::GetDeltaR(JetEta->at(thisjet), MuEta->at(mu), JetPhi->at(thisjet), MuPhi->at(mu)) > 1.0 ) continue;
		nclosjets++;
		closjet_inds.push_back(thisjet);
	}

	if(closjet_inds.size() == 0) return 0.;

	jetind = closjet_inds[0];
	if(closjet_inds.size() > 1)
		for(int thisjet=0; thisjet < nclosjets; ++thisjet)
			if(Util::GetDeltaR(JetEta->at(closjet_inds[thisjet]), MuEta->at(mu), JetPhi->at(closjet_inds[thisjet]), MuPhi->at(mu)) < Util::GetDeltaR(JetEta->at(jetind), MuEta->at(mu), JetPhi->at(jetind), MuPhi->at(mu)) ) jetind = closjet_inds[thisjet];

	if(info==1) return Util::GetDeltaR(JetEta->at(jetind), MuEta->at(mu), JetPhi->at(jetind), MuPhi->at(mu));
	return getJetPt(jetind);
}


//____________________________________________________________________________
float Fakerates::getHT(){
	/*
	compute the scalar sum HT of Pt of good jets and return it
	parameters: none
	return: HT
	*/
	
	float HT(0.);
	
	for(int thisjet=0; thisjet < JetRawPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, fJetPtCut)) continue;
		HT += getJetPt(thisjet);
	}

	return HT;
}



//____________________________________________________________________________
int Fakerates::getNJets(int btag = 0){
	/*
	counts the number of jets and b-tagged jets
	parameters: btag (0 any jet, 1 b tagged jet)
	return: anzahl jets
	*/

	int njets(0), nbjets(0);
	
	for(int thisjet=0; thisjet < JetRawPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, fJetPtCut)) continue;
		njets++;
		if(JetCSVBTag->at(thisjet)<0.679) continue;
		nbjets++;
	}

	if(btag==1) return nbjets;
	return njets;
}


//____________________________________________________________________________
bool Fakerates::isFRRegionElEvent(int &el){
	return false;	
}


//____________________________________________________________________________
void Fakerates::fillFRPlots(float fEventweight = 1.0){
	/* 
	create plos for muons and electrons
	parameters: none
	return: none
	*/

	int mu(-1), jet(-1);


	if(isFRRegionMuEvent(mu, jet, 30.)) {
		if(passesUpperMETMT(0,mu)) {
			h_Loose_muLepEta_30 ->Fill(fabs(MuEta->at(mu)), fEventweight);
			h_Loose_muLepPt_30  ->Fill(MuPt->at(mu), fEventweight);
			if(isTightMuon(mu)){
				h_Tight_muLepEta_30 ->Fill(fabs(MuEta->at(mu)), fEventweight);
				h_Tight_muLepEta_30 ->Fill(MuPt->at(mu), fEventweight);
			}
		}
	}

	if(isFRRegionMuEvent(mu, jet, 40.)) {
		if(passesUpperMETMT(0,mu)) {
			h_Loose_muLepEta_40 ->Fill(fabs(MuEta->at(mu)), fEventweight);
			h_Loose_muLepPt_40  ->Fill(MuPt->at(mu), fEventweight);
			if(isTightMuon(mu)) {
				h_Tight_muLepEta_40 ->Fill(fabs(MuEta->at(mu)), fEventweight);
				h_Tight_muLepPt_40  ->Fill(MuPt->at(mu), fEventweight);
			}
		}
	}

	if(isFRRegionMuEvent(mu, jet, 50.)) {
		if(passesUpperMETMT(0,mu)) {
			h_Loose_muLepEta_50 ->Fill(fabs(MuEta->at(mu)), fEventweight);
			h_Loose_muLepPt_50  ->Fill(MuPt->at(mu), fEventweight);
			if(isTightMuon(mu)) {
				h_Tight_muLepEta_50 ->Fill(fabs(MuEta->at(mu)), fEventweight);
				h_Tight_muLepPt_50  ->Fill(MuPt->at(mu), fEventweight);
			}
		}
	}

	if(isFRRegionMuEvent(mu, jet, 60.)) {
		if(passesUpperMETMT(0,mu)) {
			h_Loose_muLepEta_60 ->Fill(fabs(MuEta->at(mu)), fEventweight);
			h_Loose_muLepPt_60  ->Fill(MuPt->at(mu), fEventweight);
			if(isTightMuon(mu)){
				h_Tight_muLepEta_60 ->Fill(fabs(MuEta->at(mu)), fEventweight);
				h_Tight_muLepPt_60  ->Fill(MuPt->at(mu), fEventweight);
			}
		}
	}


	// muons, first loose, then tight
	if(isFRRegionMuEvent(mu, jet, fJetPtCut)){

		if(passesUpperMETMT(0,mu)) {
 
			h_Loose_muAwayJetDR ->Fill(getAwayJet(1,mu)    , fEventweight);
			h_Loose_muAwayJetPt ->Fill(getAwayJet(0,mu)    , fEventweight);
			h_Loose_muClosJetDR ->Fill(getClosestJet(1,mu) , fEventweight);
			h_Loose_muClosJetPt ->Fill(getClosestJet(0,mu) , fEventweight);

			h_Loose_muHT        ->Fill(getHT()             , fEventweight);
			h_Loose_muLepEta    ->Fill(fabs(MuEta->at(mu)) , fEventweight);
			h_Loose_muLepIso    ->Fill(MuPFIso->at(mu)     , fEventweight);
			h_Loose_muLepPt     ->Fill(MuPt->at(mu)        , fEventweight);

			h_Loose_muMaxJPt    ->Fill(getJetPt(jet)       , fEventweight);
			h_Loose_muNBJets    ->Fill(getNJets(1)         , fEventweight);
			h_Loose_muNJets     ->Fill(getNJets()          , fEventweight);
			
			h_Loose_muNVertices ->Fill((NVrtx>40)?40:NVrtx , fEventweight);
			h_Loose_muNVertices1->Fill((NVrtx>30)?30:NVrtx , fEventweight);

			h_Loose_muD0        ->Fill(MuD0->at(mu)        , fEventweight);
			h_Loose_muMaxJCPt   ->Fill(JetPt->at(jet)      , fEventweight); // always corrected Jet Pt!
			h_Loose_muMaxJRPt   ->Fill(JetRawPt->at(jet)   , fEventweight); // always raw Jet Pt!

			h_Loose_muJCPtJEta  ->Fill(fabs(JetEta->at(jet)), JetPt->at(jet), fEventweight);
			h_Loose_muJRPtJEta  ->Fill(fabs(JetEta->at(jet)), JetRawPt->at(jet), fEventweight);
			h_Loose_muJCPtJPt   ->Fill(JetPt->at(jet), JetPt->at(jet), fEventweight);
			h_Loose_muJRPtJPt   ->Fill(JetPt->at(jet), JetRawPt->at(jet), fEventweight);

			for(int thisjet = 0; thisjet < JetRawPt->size(); ++thisjet) {
				h_Loose_muAllJCPt   ->Fill(JetPt->at(thisjet)       , fEventweight);
				h_Loose_muAllJRPt   ->Fill(JetRawPt->at(thisjet)    , fEventweight);
				h_Loose_muAllJEta   ->Fill(fabs(JetEta->at(thisjet)), fEventweight);

				h_Loose_muDJPtJEta  ->Fill(fabs(JetEta->at(thisjet)), (JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
				h_Loose_muFJPtJEta  ->Fill(fabs(JetEta->at(thisjet)), (JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
				h_Loose_muDJPtJPt   ->Fill(JetPt->at(thisjet),        (JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
				h_Loose_muFJPtJPt   ->Fill(JetPt->at(thisjet),        (JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);

				int i = h_Loose_muDFZoomEta ->FindBin(fabs(JetEta->at(thisjet)));
				if(fDFbinseta[0]<=fabs(JetEta->at(thisjet)) && fabs(JetEta->at(thisjet))<fDFbinseta[fDFn_binseta-1]){
				
					if(fDFbinspt[0]<=JetPt->at(thisjet) && JetPt->at(thisjet)<fDFbinspt[fDFn_binspt-1]){
						int j = h_Loose_muDFZoomPt  ->FindBin(JetPt->at(thisjet));
						h_Loose_muDJPtZoomC[(i-1)*(fDFn_binspt-1) + j - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
						h_Loose_muFJPtZoomC[(i-1)*(fDFn_binspt-1) + j - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
					}

					if(fDFbinspt[0]<=JetRawPt->at(thisjet) && JetRawPt->at(thisjet)<fDFbinspt[fDFn_binspt-1]){
						int k = h_Loose_muDFZoomPt  ->FindBin(JetRawPt->at(thisjet));
						h_Loose_muDJPtZoomR[(i-1)*(fDFn_binspt-1) + k - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
						h_Loose_muFJPtZoomR[(i-1)*(fDFn_binspt-1) + k - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
					}
				}
			}


			if( MuPt->at(mu) >  fFRbinspt.back() ){
				int fillbin = h_muFLoose->FindBin(fFRbinspt.back()-0.5, fabs(MuEta->at(mu)));
				h_muFLoose->AddBinContent(fillbin, fEventweight);
			}
			else{
				h_muFLoose->Fill(MuPt->at(mu), fabs(MuEta->at(mu)), fEventweight);
			}
// cout << Form("%d\t%d\t%d\t%.2f\t%.2f\t%d\t%.2f\t%.2f\t%.2f", Run, Lumi, Event, MuPt->at(mu), getAwayJet(0,mu), isTightMuon(mu), getAwayJet(1,mu), getMET(), getMT(0, mu)) << endl;
// cout << Form("%d\t%d\t%d\t%.2f\t%d\t%.2f\t%.2f", Run, Lumi, Event, MuPt->at(mu), isTightMuon(mu), getMET(), getMT(0, mu)) << endl;
		}

		if(passesMTCut(0, mu)) h_Loose_muMET       ->Fill(getMET()    , fEventweight);
		                       h_Loose_muMETnoMTCut->Fill(getMET()    , fEventweight);
		if(passesMETCut())     h_Loose_muMT        ->Fill(getMT(0, mu), fEventweight);
		if(passesMETCut(20,1)) h_Loose_muMTMET20   ->Fill(getMT(0, mu), fEventweight);
		if(passesMETCut(30,1)) h_Loose_muMTMET30   ->Fill(getMT(0, mu), fEventweight);
		if(passesMETCut(20,1)) h_Loose_muNVerticesMET20 ->Fill((NVrtx>40)?40:NVrtx , fEventweight);

		// tight muons
		if(isTightMuon(mu)) {

			if(passesUpperMETMT(0,mu)) {
  
				h_Tight_muAwayJetDR ->Fill(getAwayJet(1,mu)    , fEventweight);
				h_Tight_muAwayJetPt ->Fill(getAwayJet(0,mu)    , fEventweight);
				h_Tight_muClosJetDR ->Fill(getClosestJet(1,mu) , fEventweight);
				h_Tight_muClosJetPt ->Fill(getClosestJet(0,mu) , fEventweight);

				h_Tight_muHT        ->Fill(getHT()             , fEventweight);
				h_Tight_muLepEta    ->Fill(fabs(MuEta->at(mu)) , fEventweight);
				h_Tight_muLepIso    ->Fill(MuPFIso->at(mu)     , fEventweight);
				h_Tight_muLepPt     ->Fill(MuPt->at(mu)        , fEventweight);

				h_Tight_muMaxJPt    ->Fill(getJetPt(jet)       , fEventweight);
				h_Tight_muNBJets    ->Fill(getNJets(1)         , fEventweight);
				h_Tight_muNJets     ->Fill(getNJets()          , fEventweight);
				h_Tight_muNVertices ->Fill((NVrtx>40)?40:NVrtx , fEventweight);
				h_Tight_muNVertices1->Fill((NVrtx>30)?30:NVrtx , fEventweight);

				h_Tight_muD0        ->Fill(MuD0->at(mu)        , fEventweight);
				h_Tight_muMaxJCPt   ->Fill(JetPt->at(jet)      , fEventweight); // always corrected Jet Pt!
				h_Tight_muMaxJRPt   ->Fill(JetRawPt->at(jet)   , fEventweight); // always raw Jet Pt!

				h_Tight_muJCPtJEta  ->Fill(fabs(JetEta->at(jet)), JetPt->at(jet), fEventweight);
				h_Tight_muJRPtJEta  ->Fill(fabs(JetEta->at(jet)), JetRawPt->at(jet), fEventweight);
				h_Tight_muJCPtJPt   ->Fill(JetPt->at(jet), JetPt->at(jet), fEventweight);
				h_Tight_muJRPtJPt   ->Fill(JetPt->at(jet), JetRawPt->at(jet), fEventweight);

				for(int thisjet = 0; thisjet < JetRawPt->size(); ++thisjet) {
					h_Tight_muAllJCPt   ->Fill(JetPt->at(thisjet)       , fEventweight);
					h_Tight_muAllJRPt   ->Fill(JetRawPt->at(thisjet)    , fEventweight);
					h_Tight_muAllJEta   ->Fill(fabs(JetEta->at(thisjet)), fEventweight);

					h_Tight_muDJPtJEta ->Fill(fabs(JetEta->at(thisjet)), (JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
					h_Tight_muFJPtJEta ->Fill(fabs(JetEta->at(thisjet)), (JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
					h_Tight_muDJPtJPt  ->Fill(JetPt->at(thisjet),        (JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
					h_Tight_muFJPtJPt  ->Fill(JetPt->at(thisjet),        (JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
				
					int i = h_Tight_muDFZoomEta ->FindBin(fabs(JetEta->at(thisjet)));
					if(fDFbinseta[0]<=fabs(JetEta->at(thisjet)) && fabs(JetEta->at(thisjet))<fDFbinseta[fDFn_binseta-1]){
				
						if(fDFbinspt[0]<=JetPt->at(thisjet) && JetPt->at(thisjet)<fDFbinspt[fDFn_binspt-1]){
							int j = h_Tight_muDFZoomPt  ->FindBin(JetPt->at(thisjet));
							h_Tight_muDJPtZoomC[(i-1)*(fDFn_binspt-1) + j - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
							h_Tight_muFJPtZoomC[(i-1)*(fDFn_binspt-1) + j - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
						}

						if(fDFbinspt[0]<=JetRawPt->at(thisjet) && JetRawPt->at(thisjet)<fDFbinspt[fDFn_binspt-1]){
							int k = h_Tight_muDFZoomPt  ->FindBin(JetRawPt->at(thisjet));
							h_Tight_muDJPtZoomR[(i-1)*(fDFn_binspt-1) + k - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet)),                       fEventweight);
							h_Tight_muFJPtZoomR[(i-1)*(fDFn_binspt-1) + k - 1] ->Fill((JetPt->at(thisjet)-JetRawPt->at(thisjet))/JetRawPt->at(thisjet), fEventweight);
						}
					}
				}

				if( MuPt->at(mu) >  fFRbinspt.back() ){
					int fillbin = h_muFTight->FindBin(fFRbinspt.back()-0.5, fabs(MuEta->at(mu)));
					h_muFTight->AddBinContent(fillbin, fEventweight);
				}
				else{
					h_muFTight->Fill(MuPt->at(mu), fabs(MuEta->at(mu)), fEventweight);
				}
			}

			if(passesMTCut(0, mu)) h_Tight_muMET        -> Fill(getMET()    , fEventweight);
			                       h_Tight_muMETnoMTCut -> Fill(getMET()    , fEventweight);
			if(passesMETCut())     h_Tight_muMT         -> Fill(getMT(0, mu), fEventweight);
			if(passesMETCut(20,1)) h_Tight_muMTMET20    -> Fill(getMT(0, mu), fEventweight);
			if(passesMETCut(30,1)) h_Tight_muMTMET30    -> Fill(getMT(0, mu), fEventweight);
			if(passesMETCut(20,1)) h_Tight_muNVerticesMET20 ->Fill((NVrtx>40)?40:NVrtx , fEventweight);

		}
	}
	h_muFRatio->Divide(h_muFTight, h_muFLoose);


    // electrons
	//int el(-1);
	//if(isFRRegionElEvent(el)) {
	//	h_elIsoPlot->Fill(ElPFIso->at(el), fEventweight);
	//}
}


//____________________________________________________________________________
void Fakerates::bookHistos(){
	/*
	define histograms and binning
	parameters: none
	return: none
	*/ 

	std::vector<float> nvrtx_bins;
	nvrtx_bins.push_back( 0.);
	nvrtx_bins.push_back( 5.);
	nvrtx_bins.push_back(10.);
	nvrtx_bins.push_back(15.);
	nvrtx_bins.push_back(20.);
	nvrtx_bins.push_back(25.);
	nvrtx_bins.push_back(30.);
	nvrtx_bins.push_back(31.);
	int nvrtx_nbins = nvrtx_bins.size();

	// the ratio histograms, those are just divided versions of the following
	h_elFRatio = new TH2F("h_elFRatio", "elFRatio", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_elFRatio->Sumw2(); 
	h_muFRatio = new TH2F("h_muFRatio", "muFRatio", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_muFRatio->Sumw2(); 
	h_elPRatio = new TH2F("h_elPRatio", "elPRatio", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_elPRatio->Sumw2(); 
	h_muPRatio = new TH2F("h_muPRatio", "muPRatio", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_muPRatio->Sumw2(); 
	
	// passing histograms for electrons and muons, f and p rate
	h_elFTight = new TH2F("h_elFTight", "elFTight", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_elFTight->Sumw2(); 
	h_muFTight = new TH2F("h_muFTight", "muFTight", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_muFTight->Sumw2(); 
	h_elPTight = new TH2F("h_elPTight", "elPTight", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_elPTight->Sumw2(); 
	h_muPTight = new TH2F("h_muPTight", "muPTight", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_muPTight->Sumw2(); 

	// failing histograms for electrons and muons, f and p rate
	h_elFLoose = new TH2F("h_elFLoose", "elFLoose", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_elFLoose->Sumw2(); 
	h_muFLoose = new TH2F("h_muFLoose", "muFLoose", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_muFLoose->Sumw2(); 
	h_elPLoose = new TH2F("h_elPLoose", "elPLoose", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_elPLoose->Sumw2(); 
	h_muPLoose = new TH2F("h_muPLoose", "muPLoose", fFRn_binspt-1, &fFRbinspt[0], fFRn_binseta-1, &fFRbinseta[0]); h_muPLoose->Sumw2(); 

	float eta_min = 0., eta_max = 2.4;
	float pt_min = 10., pt_max = 70.;
	int eta_bin = 12, pt_bin = 20;

	h_Loose_muLepPt      = new TH1F("h_Loose_muLepPt"      , "Loose_muLepPt"     , pt_bin  , pt_min  , pt_max);  h_Loose_muLepPt  -> Sumw2();
	h_Loose_muLepEta     = new TH1F("h_Loose_muLepEta"     , "Loose_muLepEta"    , eta_bin , eta_min , eta_max); h_Loose_muLepEta -> Sumw2();
 	h_Loose_muLepIso     = new TH1F("h_Loose_muLepIso"     , "Loose_muLepIso"    , 20 ,   0 , 1  ); h_Loose_muLepIso     -> Sumw2();
	h_Loose_muD0         = new TH1F("h_Loose_muD0"         , "Loose_muD0"        , 20 ,   0., 0.2); h_Loose_muD0         -> Sumw2();

	h_Loose_muLepEta_30  = new TH1F("h_Loose_muLepEta_30"  , "Loose_muLepEta_30" , eta_bin , eta_min , eta_max); h_Loose_muLepEta_30 -> Sumw2();
	h_Loose_muLepEta_40  = new TH1F("h_Loose_muLepEta_40"  , "Loose_muLepEta_40" , eta_bin , eta_min , eta_max); h_Loose_muLepEta_40 -> Sumw2();
	h_Loose_muLepEta_50  = new TH1F("h_Loose_muLepEta_50"  , "Loose_muLepEta_50" , eta_bin , eta_min , eta_max); h_Loose_muLepEta_50 -> Sumw2();
	h_Loose_muLepEta_60  = new TH1F("h_Loose_muLepEta_60"  , "Loose_muLepEta_60" , eta_bin , eta_min , eta_max); h_Loose_muLepEta_60 -> Sumw2();

	h_Loose_muLepPt_30   = new TH1F("h_Loose_muLepPt_30"   , "Loose_muLepPt_30"  , pt_bin  , pt_min  , pt_max);  h_Loose_muLepPt_30  -> Sumw2();
	h_Loose_muLepPt_40   = new TH1F("h_Loose_muLepPt_40"   , "Loose_muLepPt_40"  , pt_bin  , pt_min  , pt_max);  h_Loose_muLepPt_40  -> Sumw2();
	h_Loose_muLepPt_50   = new TH1F("h_Loose_muLepPt_50"   , "Loose_muLepPt_50"  , pt_bin  , pt_min  , pt_max);  h_Loose_muLepPt_50  -> Sumw2();
	h_Loose_muLepPt_60   = new TH1F("h_Loose_muLepPt_60"   , "Loose_muLepPt_60"  , pt_bin  , pt_min  , pt_max);  h_Loose_muLepPt_60  -> Sumw2();

	h_Loose_muHT         = new TH1F("h_Loose_muHT"         , "Loose_muHT"        , 10 ,  0  , 400); h_Loose_muHT         -> Sumw2();
	h_Loose_muMET        = new TH1F("h_Loose_muMET"        , "Loose_muMET"       , 10 ,  0  , 100); h_Loose_muMET        -> Sumw2();
	h_Loose_muMETnoMTCut = new TH1F("h_Loose_muMETnoMTCut" , "Loose_muMETnoMTCut", 10 ,  0  , 100); h_Loose_muMETnoMTCut -> Sumw2();
	h_Loose_muMT         = new TH1F("h_Loose_muMT"         , "Loose_muMT"        , 10 ,  0  , 100); h_Loose_muMT         -> Sumw2();
	h_Loose_muMTMET20    = new TH1F("h_Loose_muMTMET20"    , "Loose_muMTMET20"   , 20 ,  0  , 200); h_Loose_muMTMET20    -> Sumw2();
	h_Loose_muMTMET30    = new TH1F("h_Loose_muMTMET30"    , "Loose_muMTMET30"   , 20 ,  0  , 200); h_Loose_muMTMET30    -> Sumw2();

	h_Loose_muMaxJPt     = new TH1F("h_Loose_muMaxJPt"     , "Loose_muMaxJPt"    , 10 ,  20 , 120); h_Loose_muMaxJPt     -> Sumw2();
	h_Loose_muMaxJCPt    = new TH1F("h_Loose_muMaxJCPt"    , "Loose_muMaxJCPt"   , 10 ,  20 , 120); h_Loose_muMaxJCPt    -> Sumw2();
	h_Loose_muMaxJRPt    = new TH1F("h_Loose_muMaxJRPt"    , "Loose_muMaxJRPt"   , 10 ,  20 , 120); h_Loose_muMaxJRPt    -> Sumw2();

	h_Loose_muAllJRPt    = new TH1F("h_Loose_muAllJRPt"    , "Loose_muAllJRPt"   , 15 ,   0 , 150); h_Loose_muAllJRPt    -> Sumw2();
	h_Loose_muAllJCPt    = new TH1F("h_Loose_muAllJCPt"    , "Loose_muAllJCPt"   , 15 ,   0 , 150); h_Loose_muAllJCPt    -> Sumw2();
	h_Loose_muAllJEta    = new TH1F("h_Loose_muAllJEta"    , "Loose_muAllJEta"   , 12 ,   0 , 2.4); h_Loose_muAllJEta    -> Sumw2();

	h_Loose_muNBJets     = new TH1F("h_Loose_muNBJets"     , "Loose_muNBJets"    , 3  ,  0  , 3  ); h_Loose_muNBJets     -> Sumw2();
	h_Loose_muNJets      = new TH1F("h_Loose_muNJets"      , "Loose_muNJets"     , 5  ,  1  , 6  ); h_Loose_muNJets      -> Sumw2();
	h_Loose_muNVertices  = new TH1F("h_Loose_muNVertices"  , "Loose_muNVertices" , 40 ,  0  , 40 ); h_Loose_muNVertices  -> Sumw2();
	h_Loose_muNVertices1 = new TH1F("h_Loose_muNVertices1" , "Loose_muNVertices" , nvrtx_nbins-1, &nvrtx_bins[0]); h_Loose_muNVertices1 -> Sumw2();
	h_Loose_muNVerticesMET20 = new TH1F("h_Loose_muNVerticesMET20", "Loose_muNVerticesMET20", 40, 0, 40); h_Loose_muNVerticesMET20 -> Sumw2();

	h_Loose_muAwayJetDR  = new TH1F("h_Loose_muAwayJetDR"  , "Loose_muAwayJetDR" , 15 ,  0  , 6  ); h_Loose_muAwayJetDR  -> Sumw2();
	h_Loose_muAwayJetPt  = new TH1F("h_Loose_muAwayJetPt"  , "Loose_muAwayJetPt" , 10 ,  20 , 120); h_Loose_muAwayJetPt  -> Sumw2();
	h_Loose_muClosJetDR  = new TH1F("h_Loose_muClosJetDR"  , "Loose_muClosJetDR" , 15 ,  0  , 1  ); h_Loose_muClosJetDR  -> Sumw2();
	h_Loose_muClosJetPt  = new TH1F("h_Loose_muClosJetPt"  , "Loose_muClosJetPt" , 10 ,  20 , 120); h_Loose_muClosJetPt  -> Sumw2();

	h_Loose_muJCPtJEta   = new TH2F("h_Loose_muJCPtJEta"   , "Loose_muJCPtJEta"  , eta_bin, eta_min, eta_max, 10, 20, 120); h_Loose_muJCPtJEta->Sumw2();
	h_Loose_muJRPtJEta   = new TH2F("h_Loose_muJRPtJEta"   , "Loose_muJRPtJEta"  , eta_bin, eta_min, eta_max, 10, 20, 120); h_Loose_muJRPtJEta->Sumw2();
	h_Loose_muJCPtJPt    = new TH2F("h_Loose_muJCPtJPt"    , "Loose_muJCPtJPt"   , pt_bin,  pt_min,  pt_max,  10, 20, 120); h_Loose_muJCPtJPt ->Sumw2();
	h_Loose_muJRPtJPt    = new TH2F("h_Loose_muJRPtJPt"    , "Loose_muJRPtJPt"   , pt_bin,  pt_min,  pt_max,  10, 20, 120); h_Loose_muJRPtJPt ->Sumw2();

	h_Loose_muDJPtJEta   = new TH2F("h_Loose_muDJPtJEta"   , "Loose_muDJPtJEta"  , eta_bin, eta_min, eta_max, 30, -30, 30); h_Loose_muDJPtJEta->Sumw2();
	h_Loose_muFJPtJEta   = new TH2F("h_Loose_muFJPtJEta"   , "Loose_muFJPtJEta"  , eta_bin, eta_min, eta_max, 30, -1, 1);   h_Loose_muFJPtJEta->Sumw2();
	h_Loose_muDJPtJPt    = new TH2F("h_Loose_muDJPtJPt"    , "Loose_muDJPtJPt"   , pt_bin,  pt_min,  pt_max,  30, -30, 30); h_Loose_muDJPtJPt ->Sumw2();
	h_Loose_muFJPtJPt    = new TH2F("h_Loose_muFJPtJPt"    , "Loose_muFJPtJPt"   , pt_bin,  pt_min,  pt_max,  30, -1, 1);   h_Loose_muFJPtJPt ->Sumw2();

	h_Loose_muDFZoomEta  = new TH1F("h_Loose_muDFZoomEta"  , "Loose_muDFZoomEta" , fDFn_binseta-1, &fDFbinseta[0]); // empty, just to use binning
	h_Loose_muDFZoomPt   = new TH1F("h_Loose_muDFZoomPt"   , "Loose_muDFZoomPt"  , fDFn_binspt-1 , &fDFbinspt[0] ); // empty, just to use binning

	int n = 0;
	char nn[2];
	char name[150], title[150];
	for(int i=0; i<fDFn_binseta-1; ++i) {
		for(int j=0; j<fDFn_binspt-1; ++j) {
			if(n<10) sprintf(nn, "0%d", n);
			else sprintf(nn, "%d", n);
			sprintf(name, "h_Loose_muDJPtZoomC_%s", nn);
			sprintf(title, "Loose_muDJPtZoomC_%s", nn);
			h_Loose_muDJPtZoomC[n] = new TH1F(name, title, 80, -30., 10.); 
			h_Loose_muDJPtZoomC[n]->Sumw2();
			sprintf(name, "h_Loose_muDJPtZoomR_%s", nn);
			sprintf(title, "Loose_muDJPtZoomR_%s", nn);
			h_Loose_muDJPtZoomR[n] = new TH1F(name, title, 80, -30., 10.); 
			h_Loose_muDJPtZoomR[n]->Sumw2();
			sprintf(name, "h_Loose_muFJPtZoomC_%s", nn);
			sprintf(title, "Loose_muFJPtZoomC_%s", nn);
			h_Loose_muFJPtZoomC[n] = new TH1F(name, title, 50, -1., 1.);
			h_Loose_muFJPtZoomC[n]->Sumw2();
			sprintf(name, "h_Loose_muFJPtZoomR_%s", nn);
			sprintf(title, "Loose_muFJPtZoomR_%s", nn);
			h_Loose_muFJPtZoomR[n] = new TH1F(name, title, 50, -1., 1.);
			h_Loose_muFJPtZoomR[n]->Sumw2();
			++n;
		}
	}
	
	h_Tight_muLepPt      = new TH1F("h_Tight_muLepPt"      , "Tight_muLepPt"     , pt_bin  , pt_min  , pt_max ); h_Tight_muLepPt     -> Sumw2();
	h_Tight_muLepEta     = new TH1F("h_Tight_muLepEta"     , "Tight_muLepEta"    , eta_bin , eta_min , eta_max); h_Tight_muLepEta    -> Sumw2();
	h_Tight_muLepIso     = new TH1F("h_Tight_muLepIso"     , "Tight_muLepIso"    , 20,       0.,       1.0    ); h_Tight_muLepIso    -> Sumw2();
 	h_Tight_muD0         = new TH1F("h_Tight_muD0"         , "Tight_muD0"        , 20,       0.,       0.2    ); h_Tight_muD0        -> Sumw2();
    
	h_Tight_muLepEta_30  = new TH1F("h_Tight_muLepEta_30"  , "Tight_muLepEta_30" , eta_bin , eta_min , eta_max); h_Tight_muLepEta_30 -> Sumw2();
	h_Tight_muLepEta_40  = new TH1F("h_Tight_muLepEta_40"  , "Tight_muLepEta_40" , eta_bin , eta_min , eta_max); h_Tight_muLepEta_40 -> Sumw2();
	h_Tight_muLepEta_50  = new TH1F("h_Tight_muLepEta_50"  , "Tight_muLepEta_50" , eta_bin , eta_min , eta_max); h_Tight_muLepEta_50 -> Sumw2();
	h_Tight_muLepEta_60  = new TH1F("h_Tight_muLepEta_60"  , "Tight_muLepEta_60" , eta_bin , eta_min , eta_max); h_Tight_muLepEta_60 -> Sumw2();
    
	h_Tight_muLepPt_30   = new TH1F("h_Tight_muLepPt_30"   , "Tight_muLepPt_30"  , pt_bin  , pt_min  , pt_max);  h_Tight_muLepPt_30  -> Sumw2();
	h_Tight_muLepPt_40   = new TH1F("h_Tight_muLepPt_40"   , "Tight_muLepPt_40"  , pt_bin  , pt_min  , pt_max);  h_Tight_muLepPt_40  -> Sumw2();
	h_Tight_muLepPt_50   = new TH1F("h_Tight_muLepPt_50"   , "Tight_muLepPt_50"  , pt_bin  , pt_min  , pt_max);  h_Tight_muLepPt_50  -> Sumw2();
	h_Tight_muLepPt_60   = new TH1F("h_Tight_muLepPt_60"   , "Tight_muLepPt_60"  , pt_bin  , pt_min  , pt_max);  h_Tight_muLepPt_60  -> Sumw2();
                                                                                         
	h_Tight_muHT         = new TH1F("h_Tight_muHT"         , "Tight_muHT"        , 10 ,  0  , 400); h_Tight_muHT         -> Sumw2();
	h_Tight_muMET        = new TH1F("h_Tight_muMET"        , "Tight_muMET"       , 10 ,  0  , 100); h_Tight_muMET        -> Sumw2();
	h_Tight_muMETnoMTCut = new TH1F("h_Tight_muMETnoMTCut" , "Tight_muMETnoMTCut", 10 ,  0  , 100); h_Tight_muMETnoMTCut -> Sumw2();
	h_Tight_muMT         = new TH1F("h_Tight_muMT"         , "Tight_muMT"        , 10 ,  0  , 100); h_Tight_muMT         -> Sumw2();
	h_Tight_muMTMET20    = new TH1F("h_Tight_muMTMET20"    , "Tight_muMTMET20"   , 20 ,  0  , 200); h_Tight_muMTMET20    -> Sumw2();
	h_Tight_muMTMET30    = new TH1F("h_Tight_muMTMET30"    , "Tight_muMTMET30"   , 20 ,  0  , 200); h_Tight_muMTMET30    -> Sumw2();
                                                                                                 
	h_Tight_muMaxJPt     = new TH1F("h_Tight_muMaxJPt"     , "Tight_muMaxJPt"    , 10 ,  20 , 120); h_Tight_muMaxJPt     -> Sumw2();
	h_Tight_muMaxJCPt    = new TH1F("h_Tight_muMaxJCPt"    , "Tight_muMaxJCPt"   , 10 ,  20 , 120); h_Tight_muMaxJCPt    -> Sumw2();
	h_Tight_muMaxJRPt    = new TH1F("h_Tight_muMaxJRPt"    , "Tight_muMaxJRPt"   , 10 ,  20 , 120); h_Tight_muMaxJRPt    -> Sumw2();

	h_Tight_muAllJCPt    = new TH1F("h_Tight_muAllJCPt"    , "Tight_muAllJCPt"   , 15 ,   0 , 150); h_Tight_muAllJCPt    -> Sumw2();
	h_Tight_muAllJRPt    = new TH1F("h_Tight_muAllJRPt"    , "Tight_muAllJRPt"   , 15 ,   0 , 150); h_Tight_muAllJRPt    -> Sumw2();
	h_Tight_muAllJEta    = new TH1F("h_Tight_muAllJEta"    , "Tight_muAllJEta"   , 12 ,   0 , 2.4); h_Tight_muAllJEta    -> Sumw2();

	h_Tight_muNBJets     = new TH1F("h_Tight_muNBJets"     , "Tight_muNBJets"    , 3  ,  0  , 3  ); h_Tight_muNBJets     -> Sumw2();
	h_Tight_muNJets      = new TH1F("h_Tight_muNJets"      , "Tight_muNJets"     , 5  ,  1  , 6  ); h_Tight_muNJets      -> Sumw2();
	h_Tight_muNVertices  = new TH1F("h_Tight_muNVertices"  , "Tight_muNVertices" , 40 ,  0  , 40 ); h_Tight_muNVertices  -> Sumw2();
	h_Tight_muNVertices1 = new TH1F("h_Tight_muNVertices1" , "Tight_muNVertices" , nvrtx_nbins-1, &nvrtx_bins[0]); h_Tight_muNVertices1  -> Sumw2();
	h_Tight_muNVerticesMET20 = new TH1F("h_Tight_muNVerticesMET20", "Tight_muNVerticesMET20", 40, 0, 40); h_Tight_muNVerticesMET20 -> Sumw2();
                                                                                                 
	h_Tight_muAwayJetDR  = new TH1F("h_Tight_muAwayJetDR"  , "Tight_muAwayJetDR" , 15 ,  0  , 6  ); h_Tight_muAwayJetDR  -> Sumw2();
	h_Tight_muAwayJetPt  = new TH1F("h_Tight_muAwayJetPt"  , "Tight_muAwayJetPt" , 10 ,  20 , 120); h_Tight_muAwayJetPt  -> Sumw2();
	h_Tight_muClosJetDR  = new TH1F("h_Tight_muClosJetDR"  , "Tight_muClosJetDR" , 15 ,  0  , 1  ); h_Tight_muClosJetDR  -> Sumw2();
	h_Tight_muClosJetPt  = new TH1F("h_Tight_muClosJetPt"  , "Tight_muClosJetPt" , 10 ,  20 , 120); h_Tight_muClosJetPt  -> Sumw2();

	h_Tight_muJCPtJEta   = new TH2F("h_Tight_muJCPtJEta"   , "Tight_muJCPtJEta"  , eta_bin, eta_min, eta_max, 10, 20, 120); h_Tight_muJCPtJEta->Sumw2();
	h_Tight_muJRPtJEta   = new TH2F("h_Tight_muJRPtJEta"   , "Tight_muJRPtJEta"  , eta_bin, eta_min, eta_max, 10, 20, 120); h_Tight_muJRPtJEta->Sumw2();
	h_Tight_muJCPtJPt    = new TH2F("h_Tight_muJCPtJPt"    , "Tight_muJCPtJPt"   , pt_bin,  pt_min,  pt_max,  10, 20, 120); h_Tight_muJCPtJPt ->Sumw2();
	h_Tight_muJRPtJPt    = new TH2F("h_Tight_muJRPtJPt"    , "Tight_muJRPtJPt"   , pt_bin,  pt_min,  pt_max,  10, 20, 120); h_Tight_muJRPtJPt ->Sumw2();

	h_Tight_muDJPtJEta   = new TH2F("h_Tight_muDJPtJEta"   , "Tight_muDJPtJEta"  , eta_bin, eta_min, eta_max, 30, -30, 30); h_Tight_muDJPtJEta->Sumw2();
	h_Tight_muFJPtJEta   = new TH2F("h_Tight_muFJPtJEta"   , "Tight_muFJPtJEta"  , eta_bin, eta_min, eta_max, 30, -1, 1);   h_Tight_muFJPtJEta->Sumw2();
	h_Tight_muDJPtJPt    = new TH2F("h_Tight_muDJPtJPt"    , "Tight_muDJPtJPt"   , pt_bin,  pt_min,  pt_max,  30, -30, 30); h_Tight_muDJPtJPt ->Sumw2();
	h_Tight_muFJPtJPt    = new TH2F("h_Tight_muFJPtJPt"    , "Tight_muFJPtJPt"   , pt_bin,  pt_min,  pt_max,  30, -1, 1);   h_Tight_muFJPtJPt ->Sumw2();

	h_Tight_muDFZoomEta  = new TH1F("h_Tight_muDFZoomEta"  , "Tight_muDFZoomEta", fDFn_binseta-1, &fDFbinseta[0]); // empty, just to use binning
	h_Tight_muDFZoomPt   = new TH1F("h_Tight_muDFZoomPt"   , "Tight_muDFZoomPt" , fDFn_binspt-1 , &fDFbinspt[0] ); // empty, just to use binning

	n = 0;
	for(int i=0; i<fDFn_binseta-1; ++i) {
		for(int j=0; j<fDFn_binspt-1; ++j) {
			if(n<10) sprintf(nn, "0%d", n);
			else sprintf(nn, "%d", n);
			sprintf(name, "h_Tight_muDJPtZoomC_%s", nn);
			sprintf(title, "Tight_muDJPtZoomC_%s", nn);
			h_Tight_muDJPtZoomC[n] = new TH1F(name, title, 80, -30., 10.);
			h_Tight_muDJPtZoomC[n]->Sumw2();
			sprintf(name, "h_Tight_muDJPtZoomR_%s", nn);
			sprintf(title, "Tight_muDJPtZoomR_%s", nn);
			h_Tight_muDJPtZoomR[n] = new TH1F(name, title, 80, -30., 10.);
			h_Tight_muDJPtZoomR[n]->Sumw2();
			sprintf(name, "h_Tight_muFJPtZoomC_%s", nn);
			sprintf(title, "Tight_muFJPtZoomC_%s", nn);
			h_Tight_muFJPtZoomC[n] = new TH1F(name, title, 50, -1., 1.);
			h_Tight_muFJPtZoomC[n]->Sumw2();
			sprintf(name, "h_Tight_muFJPtZoomR_%s", nn);
			sprintf(title, "Tight_muFJPtZoomR_%s", nn);
			h_Tight_muFJPtZoomR[n] = new TH1F(name, title, 50, -1., 1.);
			h_Tight_muFJPtZoomR[n]->Sumw2();
			++n;
		}
	}
}


//____________________________________________________________________________
void Fakerates::writeHistos(TFile* pFile){
	/* 
	write histograms in output files
	parameters: pFile (output file)
	return: none
	*/

	pFile->cd(); 
	TDirectory* sdir = Util::FindOrCreate(fName, pFile);
	sdir->cd();


	// the ratio histograms, those are just divided versions of the following
	h_elFRatio          ->Write(fName + "_" + h_elFRatio->GetName(),          TObject::kWriteDelete);
	h_muFRatio          ->Write(fName + "_" + h_muFRatio->GetName(),          TObject::kWriteDelete);
	h_elPRatio          ->Write(fName + "_" + h_elPRatio->GetName(),          TObject::kWriteDelete);
	h_muPRatio          ->Write(fName + "_" + h_muPRatio->GetName(),          TObject::kWriteDelete);
	
	// tight histograms for electrons and muons, f and p rate
	h_elFTight          ->Write(fName + "_" + h_elFTight->GetName(),          TObject::kWriteDelete);
	h_muFTight          ->Write(fName + "_" + h_muFTight->GetName(),          TObject::kWriteDelete);
	h_elPTight          ->Write(fName + "_" + h_elPTight->GetName(),          TObject::kWriteDelete);
	h_muPTight          ->Write(fName + "_" + h_muPTight->GetName(),          TObject::kWriteDelete);

	// loose histograms for electrons and muons, f and p rate
	h_elFLoose          ->Write(fName + "_" + h_elFLoose->GetName(),          TObject::kWriteDelete);
	h_muFLoose          ->Write(fName + "_" + h_muFLoose->GetName(),          TObject::kWriteDelete);
	h_elPLoose          ->Write(fName + "_" + h_elPLoose->GetName(),          TObject::kWriteDelete);
	h_muPLoose          ->Write(fName + "_" + h_muPLoose->GetName(),          TObject::kWriteDelete);
 
	// loose histograms
	h_Loose_muLepPt     ->Write(fName + "_" + h_Loose_muLepPt->GetName(),     TObject::kWriteDelete);
	h_Loose_muLepEta    ->Write(fName + "_" + h_Loose_muLepEta->GetName(),    TObject::kWriteDelete);
	h_Loose_muLepIso    ->Write(fName + "_" + h_Loose_muLepIso->GetName(),    TObject::kWriteDelete);
	h_Loose_muD0        ->Write(fName + "_" + h_Loose_muD0->GetName(),        TObject::kWriteDelete);

	h_Loose_muLepEta_30 ->Write(fName + "_" + h_Loose_muLepEta_30->GetName(), TObject::kWriteDelete);
	h_Loose_muLepEta_40 ->Write(fName + "_" + h_Loose_muLepEta_40->GetName(), TObject::kWriteDelete);
	h_Loose_muLepEta_50 ->Write(fName + "_" + h_Loose_muLepEta_50->GetName(), TObject::kWriteDelete);
	h_Loose_muLepEta_60 ->Write(fName + "_" + h_Loose_muLepEta_60->GetName(), TObject::kWriteDelete);

	h_Loose_muLepPt_30  ->Write(fName + "_" + h_Loose_muLepPt_30->GetName(),  TObject::kWriteDelete);
	h_Loose_muLepPt_40  ->Write(fName + "_" + h_Loose_muLepPt_40->GetName(),  TObject::kWriteDelete);
	h_Loose_muLepPt_50  ->Write(fName + "_" + h_Loose_muLepPt_50->GetName(),  TObject::kWriteDelete);
	h_Loose_muLepPt_60  ->Write(fName + "_" + h_Loose_muLepPt_60->GetName(),  TObject::kWriteDelete);

	h_Loose_muHT        ->Write(fName + "_" + h_Loose_muHT->GetName(),        TObject::kWriteDelete);
	h_Loose_muMET       ->Write(fName + "_" + h_Loose_muMET->GetName(),       TObject::kWriteDelete);
	h_Loose_muMETnoMTCut->Write(fName + "_" + h_Loose_muMETnoMTCut->GetName(),TObject::kWriteDelete);
	h_Loose_muMT        ->Write(fName + "_" + h_Loose_muMT->GetName(),        TObject::kWriteDelete);
	h_Loose_muMTMET20   ->Write(fName + "_" + h_Loose_muMTMET20->GetName(),   TObject::kWriteDelete);
	h_Loose_muMTMET30   ->Write(fName + "_" + h_Loose_muMTMET30->GetName(),   TObject::kWriteDelete);

	h_Loose_muMaxJPt    ->Write(fName + "_" + h_Loose_muMaxJPt->GetName(),    TObject::kWriteDelete);
	h_Loose_muMaxJCPt   ->Write(fName + "_" + h_Loose_muMaxJCPt->GetName(),   TObject::kWriteDelete);
	h_Loose_muMaxJRPt   ->Write(fName + "_" + h_Loose_muMaxJRPt->GetName(),   TObject::kWriteDelete);

	h_Loose_muAllJCPt   ->Write(fName + "_" + h_Loose_muAllJCPt->GetName(),   TObject::kWriteDelete);
	h_Loose_muAllJRPt   ->Write(fName + "_" + h_Loose_muAllJRPt->GetName(),   TObject::kWriteDelete);
	h_Loose_muAllJEta   ->Write(fName + "_" + h_Loose_muAllJEta->GetName(),   TObject::kWriteDelete);

	h_Loose_muNBJets    ->Write(fName + "_" + h_Loose_muNBJets->GetName(),    TObject::kWriteDelete);
	h_Loose_muNJets     ->Write(fName + "_" + h_Loose_muNJets->GetName(),     TObject::kWriteDelete);
	h_Loose_muNVertices ->Write(fName + "_" + h_Loose_muNVertices->GetName(), TObject::kWriteDelete);
	h_Loose_muNVertices1->Write(fName + "_" + h_Loose_muNVertices1->GetName(),TObject::kWriteDelete);
	h_Loose_muNVerticesMET20 ->Write(fName + "_" + h_Loose_muNVerticesMET20->GetName(), TObject::kWriteDelete);

	h_Loose_muAwayJetDR ->Write(fName + "_" + h_Loose_muAwayJetDR->GetName(), TObject::kWriteDelete);
	h_Loose_muAwayJetPt ->Write(fName + "_" + h_Loose_muAwayJetPt->GetName(), TObject::kWriteDelete);
	h_Loose_muClosJetDR ->Write(fName + "_" + h_Loose_muClosJetDR->GetName(), TObject::kWriteDelete);
	h_Loose_muClosJetPt ->Write(fName + "_" + h_Loose_muClosJetPt->GetName(), TObject::kWriteDelete);

	h_Loose_muJCPtJEta  ->Write(fName + "_" + h_Loose_muJCPtJEta ->GetName(), TObject::kWriteDelete);
	h_Loose_muJRPtJEta  ->Write(fName + "_" + h_Loose_muJRPtJEta ->GetName(), TObject::kWriteDelete);
	h_Loose_muJCPtJPt   ->Write(fName + "_" + h_Loose_muJCPtJPt  ->GetName(), TObject::kWriteDelete);
	h_Loose_muJRPtJPt   ->Write(fName + "_" + h_Loose_muJRPtJPt  ->GetName(), TObject::kWriteDelete);

	h_Loose_muDJPtJEta  ->Write(fName + "_" + h_Loose_muDJPtJEta ->GetName(), TObject::kWriteDelete);
	h_Loose_muFJPtJEta  ->Write(fName + "_" + h_Loose_muFJPtJEta ->GetName(), TObject::kWriteDelete);
	h_Loose_muDJPtJPt   ->Write(fName + "_" + h_Loose_muDJPtJPt  ->GetName(), TObject::kWriteDelete);
	h_Loose_muFJPtJPt   ->Write(fName + "_" + h_Loose_muFJPtJPt  ->GetName(), TObject::kWriteDelete);

	for(int n = 0; n < (fDFn_binseta-1)*(fDFn_binspt-1); ++n) {
		h_Loose_muDJPtZoomC[n] ->Write(fName + "_" + h_Loose_muDJPtZoomC[n] ->GetName(), TObject::kWriteDelete);
		h_Loose_muFJPtZoomC[n] ->Write(fName + "_" + h_Loose_muFJPtZoomC[n] ->GetName(), TObject::kWriteDelete);
		h_Loose_muDJPtZoomR[n] ->Write(fName + "_" + h_Loose_muDJPtZoomR[n] ->GetName(), TObject::kWriteDelete);
		h_Loose_muFJPtZoomR[n] ->Write(fName + "_" + h_Loose_muFJPtZoomR[n] ->GetName(), TObject::kWriteDelete);
	}


	// tight histograms
	h_Tight_muLepPt     ->Write(fName + "_" + h_Tight_muLepPt->GetName(),     TObject::kWriteDelete);
	h_Tight_muLepEta    ->Write(fName + "_" + h_Tight_muLepEta->GetName(),    TObject::kWriteDelete);
	h_Tight_muLepIso    ->Write(fName + "_" + h_Tight_muLepIso->GetName(),    TObject::kWriteDelete);
	h_Tight_muD0        ->Write(fName + "_" + h_Tight_muD0->GetName(),        TObject::kWriteDelete);

	h_Tight_muLepEta_30 ->Write(fName + "_" + h_Tight_muLepEta_30->GetName(), TObject::kWriteDelete);
	h_Tight_muLepEta_40 ->Write(fName + "_" + h_Tight_muLepEta_40->GetName(), TObject::kWriteDelete);
	h_Tight_muLepEta_50 ->Write(fName + "_" + h_Tight_muLepEta_50->GetName(), TObject::kWriteDelete);
	h_Tight_muLepEta_60 ->Write(fName + "_" + h_Tight_muLepEta_60->GetName(), TObject::kWriteDelete);

	h_Tight_muLepPt_30  ->Write(fName + "_" + h_Tight_muLepPt_30->GetName(),  TObject::kWriteDelete);
	h_Tight_muLepPt_40  ->Write(fName + "_" + h_Tight_muLepPt_40->GetName(),  TObject::kWriteDelete);
	h_Tight_muLepPt_50  ->Write(fName + "_" + h_Tight_muLepPt_50->GetName(),  TObject::kWriteDelete);
	h_Tight_muLepPt_60  ->Write(fName + "_" + h_Tight_muLepPt_60->GetName(),  TObject::kWriteDelete);

	h_Tight_muHT        ->Write(fName + "_" + h_Tight_muHT->GetName(),        TObject::kWriteDelete);
	h_Tight_muMET       ->Write(fName + "_" + h_Tight_muMET->GetName(),       TObject::kWriteDelete);
	h_Tight_muMETnoMTCut->Write(fName + "_" + h_Tight_muMETnoMTCut->GetName(),TObject::kWriteDelete);
	h_Tight_muMT        ->Write(fName + "_" + h_Tight_muMT->GetName(),        TObject::kWriteDelete);
	h_Tight_muMTMET20   ->Write(fName + "_" + h_Tight_muMTMET20->GetName(),   TObject::kWriteDelete);
	h_Tight_muMTMET30   ->Write(fName + "_" + h_Tight_muMTMET30->GetName(),   TObject::kWriteDelete);

	h_Tight_muMaxJPt    ->Write(fName + "_" + h_Tight_muMaxJPt->GetName(),    TObject::kWriteDelete);
	h_Tight_muMaxJCPt   ->Write(fName + "_" + h_Tight_muMaxJCPt->GetName(),   TObject::kWriteDelete);
	h_Tight_muMaxJRPt   ->Write(fName + "_" + h_Tight_muMaxJRPt->GetName(),   TObject::kWriteDelete);

	h_Tight_muAllJCPt   ->Write(fName + "_" + h_Tight_muAllJCPt->GetName(),   TObject::kWriteDelete);
	h_Tight_muAllJRPt   ->Write(fName + "_" + h_Tight_muAllJRPt->GetName(),   TObject::kWriteDelete);
	h_Tight_muAllJEta   ->Write(fName + "_" + h_Tight_muAllJEta->GetName(),   TObject::kWriteDelete);

	h_Tight_muNBJets    ->Write(fName + "_" + h_Tight_muNBJets->GetName(),    TObject::kWriteDelete);
	h_Tight_muNJets     ->Write(fName + "_" + h_Tight_muNJets->GetName(),     TObject::kWriteDelete);
	h_Tight_muNVertices ->Write(fName + "_" + h_Tight_muNVertices->GetName(), TObject::kWriteDelete);
	h_Tight_muNVertices1->Write(fName + "_" + h_Tight_muNVertices1->GetName(),TObject::kWriteDelete);
	h_Tight_muNVerticesMET20 ->Write(fName + "_" + h_Tight_muNVerticesMET20->GetName(), TObject::kWriteDelete);

	h_Tight_muAwayJetDR ->Write(fName + "_" + h_Tight_muAwayJetDR->GetName(), TObject::kWriteDelete);
	h_Tight_muAwayJetPt ->Write(fName + "_" + h_Tight_muAwayJetPt->GetName(), TObject::kWriteDelete);
	h_Tight_muClosJetDR ->Write(fName + "_" + h_Tight_muClosJetDR->GetName(), TObject::kWriteDelete);
	h_Tight_muClosJetPt ->Write(fName + "_" + h_Tight_muClosJetPt->GetName(), TObject::kWriteDelete);

	h_Tight_muJCPtJEta  ->Write(fName + "_" + h_Tight_muJCPtJEta ->GetName(), TObject::kWriteDelete);
	h_Tight_muJRPtJEta  ->Write(fName + "_" + h_Tight_muJRPtJEta ->GetName(), TObject::kWriteDelete);
	h_Tight_muJCPtJPt   ->Write(fName + "_" + h_Tight_muJCPtJPt  ->GetName(), TObject::kWriteDelete);
	h_Tight_muJRPtJPt   ->Write(fName + "_" + h_Tight_muJRPtJPt  ->GetName(), TObject::kWriteDelete);

	h_Tight_muDJPtJEta  ->Write(fName + "_" + h_Tight_muDJPtJEta ->GetName(), TObject::kWriteDelete);
	h_Tight_muFJPtJEta  ->Write(fName + "_" + h_Tight_muFJPtJEta ->GetName(), TObject::kWriteDelete);
	h_Tight_muDJPtJPt   ->Write(fName + "_" + h_Tight_muDJPtJPt  ->GetName(), TObject::kWriteDelete);
	h_Tight_muFJPtJPt   ->Write(fName + "_" + h_Tight_muFJPtJPt  ->GetName(), TObject::kWriteDelete);

	for(int n = 0; n < (fDFn_binseta-1)*(fDFn_binspt-1); ++n) {
		h_Tight_muDJPtZoomC[n] ->Write(fName + "_" + h_Tight_muDJPtZoomC[n] ->GetName(), TObject::kWriteDelete);
		h_Tight_muFJPtZoomC[n] ->Write(fName + "_" + h_Tight_muFJPtZoomC[n] ->GetName(), TObject::kWriteDelete);
		h_Tight_muDJPtZoomR[n] ->Write(fName + "_" + h_Tight_muDJPtZoomR[n] ->GetName(), TObject::kWriteDelete);
		h_Tight_muFJPtZoomR[n] ->Write(fName + "_" + h_Tight_muFJPtZoomR[n] ->GetName(), TObject::kWriteDelete);
	}


}





