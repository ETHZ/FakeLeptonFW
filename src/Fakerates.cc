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
Fakerates::~Fakerates(){
	// TFile * fOutputFile = new TFile(fOutputFilename);
	// if(fOutputFile != NULL && fOutputFile->IsOpen()) fOutputFile->Close();
}

//____________________________________________________________________________
void Fakerates::init(bool verbose){
	cout << "------------------------------------" << endl;
	cout << "Initializing Fakerates Class ... " << endl;
	cout << "------------------------------------" << endl;
	fEventweight = 1.0;
	fCutflow_afterLepSel = 0;
	fCutflow_afterJetSel = 0;
	fCutflow_afterMETCut = 0;
	fCutflow_afterMTCut  = 0;
	Util::SetStyle();


	// SET THE BINNING FOR THE fr HISTO HERE.

	// ETA BINNING
	fFRbinseta.push_back(0.0);
	fFRbinseta.push_back(1.4);
	fFRbinseta.push_back(2.5);
	fFRn_binseta  = fFRbinseta.size();

	// PT BINNING
	fFRbinspt.push_back(10.);
	fFRbinspt.push_back(20.);
	fFRbinspt.push_back(25.);
	fFRbinspt.push_back(30.);
	fFRbinspt.push_back(35.);
	fFRbinspt.push_back(40.);
	fFRbinspt.push_back(45.);
	fFRbinspt.push_back(50.);
	fFRbinspt.push_back(51.);
	fFRn_binspt   = fFRbinspt .size();

	fLumi = 24.9;
}

// -------------------------------------------------------------
// -------------------------------------------------------------
// -------------------------------------------------------------


void Fakerates::doStuff(){
	//Sample * sample();
	fOutputFilename = fOutputDir + "/" + fName + "_ratios.root";
	loop();

}
void Fakerates::loop(){
	/* 
	does the main procedure looping over all events
	parameters: none
	return: none
	*/


	int ntot = 0;

	// open output file and define histograms
	TFile *pFile = new TFile(fOutputFilename, "RECREATE");
	bookHistos();

	// open input file and read the tree
	TFile * file_ = TFile::Open(fInputFile);
	TTree * tree_ = (TTree *) file_->Get("Analysis"); // tree name has to be named "Analysis"
	tree_->ResetBranchAddresses();
	Init(tree_);
	Long64_t tot_events = tree_->GetEntriesFast();
    
    // calculate the eventweight
    TH1F * EventCount = (TH1F*) file_->Get("EventCount");
    double Ngen = EventCount->GetEntries();
    if(!fIsData) fEventweight = fXSec * fLumi / (fMaxSize>0?fMaxSize:Ngen);
	else fEventweight = 1.;
    cout << "eventweight is " << fEventweight << endl;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > (fMaxSize>0?fMaxSize:Ngen)) break;
		tree_->GetEntry(jentry);
		ntot++;

		fillIsoPlots();

	}

	cout << "mu: nevents passing lepton selection: " << fCutflow_afterLepSel << endl;
	cout << "mu: nevents passing jet    selection: " << fCutflow_afterJetSel << endl;
	cout << "mu: nevents passing MET    selection: " << fCutflow_afterMETCut << endl;
	cout << "mu: nevents passing MT     selection: " << fCutflow_afterMTCut  << endl;
	cout << "i just looped on " << ntot << " events." << endl;
	delete file_, tree_;

	// write histograms in output file
	writeHistos(pFile);
	pFile->Close();
}

bool Fakerates::isCalibrationRegionMuEvent(int &mu, int &jet){
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


	// Event fails HLT muon trigger (if data)
	if(fIsData && !HLT_MU17) return false;

	// muon Pt is not reasonable then return false
	if(MuPt->size() < 1) return false;

	// count numbers of loose and veto muons in the event
	for(int i=0; i < MuPt->size(); ++i){
		if(MuPt->at(i) < 20.) continue;
		if(isLooseMuon(i)){
			nloose++;
			mu = i;
			loosemu_inds.push_back(i);
		}
		else{
			if(MuIsVeto->at(i)) nveto_add++;
		}
	}

	// require exactly one loose muon and no additional veto muons
	if(nloose != 1) return false;
	fCutflow_afterLepSel++;
	// if(nveto_add != 0) return false; // don't require this for the synching

	// Jet Pt is not reasonable then return false
	if(JetPt->size() < 1) return false;

	// count the number of away jets
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, 40.)) continue;
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
			if(JetRawPt->at(awayjet_inds[thisjet]) > JetRawPt->at(jet) ) jet = awayjet_inds[thisjet];


	// upper cuts on MT and MET
	//if(!passesUpperMETMT(0, loosemu_inds[0]) ) return false;
	//float dphi =  Util::DeltaPhi(JetPhi->at(awayjet_inds[0]), MuPhi->at(loosemu_inds[0]));
	
    return true;
}


bool Fakerates::passesMETCut(float value_met = 20., int sign = 0){
	/* 
	checks, if the event passes the MET cut
	parameters: none
	return: true (if event passes the cuts), false (else)
	*/

	if(sign == 1 && pfMET < value_met) return false;
	if(sign == 0 && pfMET > value_met) return false;
	return true;
}


bool Fakerates::passesMTCut(int type, int index){
	/* 
	checks, if the event passes the 20GeV MT cut
	parameters: type (0 = mu, 1 = el)
	return: true (if event passes the cuts), false (else)
	*/

	float value_mt  = 20.;

	// mu or el MT too large then return false
	if(type == 0){
		if(MuMT->at(index) > value_mt) return false;
	}
	else if(type == 1){
		if(ElMT->at(index) > value_mt) return false;
	}
	else{
		cout << "ERROR in passesUpperMETMT! you're not calling it right..." << endl;
		exit(0);
	}

	return true;
}


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

// MUON OBJECT FUNCTIONS
bool Fakerates::isLooseMuon(int ind){
	if(! MuIsLoose->at(ind)) return false;
	return true;
}
bool Fakerates::isTightMuon(int ind){
	if(!isLooseMuon(ind))   return false;
	if(!MuIsTight->at(ind)) return false;
	return true;
}


bool Fakerates::isGoodJet(int j, float pt = 0.){
	/*
	checks, if the given jet passes certain cuts defining it as a "good" jet
	parameters: j (jet index), pt (cut on pt)
	return: true (if jet is good), false (else)
	*/     

	float minDR = 0.4;

	// if pt too low, eta too large, jet beta star too large then return false
	if(pt>0. && JetRawPt->at(j) < pt) return false;
	if(fabs(JetEta->at(j)) > 2.5) return false;
	// if(JetBetaStar->at(j) > 0.2*TMath::Log(NVrtx-0.67)) return false; // value for jets with eta < 2.5

	// // if a tight muon with dR too small found then return false
	// for(int imu = 0; imu < MuPt->size(); ++imu){
	//     if(!MuIsTight->at(imu)) continue;
	//     if(Util::GetDeltaR(MuEta->at(imu), JetEta->at(j), MuPhi->at(imu), JetPhi->at(j)) > minDR ) continue;
	//     return false;
	// }

    // // if a tight electron with dR too small found then return false
	// for(int iel = 0; iel < ElPt->size(); ++iel){
	//     if(!ElIsTight->at(iel)) continue;
	//     if(Util::GetDeltaR(ElEta->at(iel), JetEta->at(j), ElPhi->at(iel), JetPhi->at(j)) > minDR ) continue;
	//     return false;
	// }

	return true;
}


float Fakerates::getAwayJet(int info = 0, int mu = 0){
	/*
	get information about the away jet with largest Pt
	parameters: info (0 Pt, 1 dR), mu (muon index)
	return: info
	*/

	int nawayjets(0), jetind(0);
	std::vector<int> awayjet_inds;
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, 40.)) continue;
		if(Util::GetDeltaR(JetEta->at(thisjet), MuEta->at(mu), JetPhi->at(thisjet), MuPhi->at(mu)) < 1.0 ) continue;
		nawayjets++;
		awayjet_inds.push_back(thisjet);
    }

	if(awayjet_inds.size() == 0) return 0.;

	jetind = awayjet_inds[0];
	if(awayjet_inds.size() > 1)
		for(int thisjet=0; thisjet < nawayjets; ++thisjet)
			if(JetRawPt->at(awayjet_inds[thisjet]) > JetRawPt->at(jetind) ) jetind = awayjet_inds[thisjet];

	if(info==1) return Util::GetDeltaR(JetEta->at(jetind), MuEta->at(mu), JetPhi->at(jetind), MuPhi->at(mu));
	return JetRawPt->at(jetind);
}


float Fakerates::getClosestJet(int info = 0, int mu = 0){
	/*
	get information about the closest jet (i.e. smallest dR)
	parameters: info (0 Pt, 1 dR), mu (muon index)
	return: info
	*/

	int nclosjets(0), jetind(0);
	std::vector<int> closjet_inds;
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
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
	return JetRawPt->at(jetind);
}


float Fakerates::getHT(){
	/*
	compute the scalar sum HT of Pt of good jets and return it
	parameters: none
	return: HT
	*/
	
	float HT(0.);
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, 40.)) continue;
		HT += JetRawPt->at(thisjet);
	}

	return HT;
}


int Fakerates::getNJets(int btag = 0){
	/*
	counts the number of jets and b-tagged jets
	parameters: btag (0 any jet, 1 b tagged jet)
	return: anzahl jets
	*/

	int njets(0), nbjets(0);
	
	for(int thisjet=0; thisjet < JetPt->size(); ++thisjet){
		if(!isGoodJet(thisjet, 40.)) continue;
		njets++;
		if(JetCSVBTag->at(thisjet)<0.679) continue;
		nbjets++;
	}

	if(btag==1) return nbjets;
	return njets;
}


bool Fakerates::isCalibrationRegionElEvent(int &el){
	return false;	
}


void Fakerates::fillIsoPlots(){
	/* 
	create plos for muons and electrons
	parameters: none
	return: none
	*/


	// muons, first loose, then tight
	int mu(-1), jet(-1);
	if(isCalibrationRegionMuEvent(mu, jet)){

		if(passesUpperMETMT(0,mu)) {
 
			h_Loose_muAwayJetDR ->Fill(getAwayJet(1,mu)    , fEventweight);
			h_Loose_muAwayJetPt ->Fill(getAwayJet(0,mu)    , fEventweight);
			h_Loose_muClosJetDR ->Fill(getClosestJet(1,mu) , fEventweight);
			h_Loose_muClosJetPt ->Fill(getClosestJet(0,mu) , fEventweight);

			h_Loose_muHT        ->Fill(getHT()             , fEventweight);
			h_Loose_muLepEta    ->Fill(fabs(MuEta->at(mu)) , fEventweight);
			h_Loose_muLepIso    ->Fill(MuPFIso->at(mu)     , fEventweight);
			h_Loose_muLepPt     ->Fill(MuPt->at(mu)        , fEventweight);

			h_Loose_muMaxJPt    ->Fill(JetRawPt->at(jet)   , fEventweight);
			h_Loose_muNBJets    ->Fill(getNJets(1)         , fEventweight);
			h_Loose_muNJets     ->Fill(getNJets()          , fEventweight);
			h_Loose_muNVertices ->Fill(NVrtx               , fEventweight);

			h_Loose_muD0        ->Fill(MuD0->at(mu)        , fEventweight);

			if( MuPt->at(mu) >  fFRbinspt.back() ){
				int fillbin = h_muFLoose->FindBin(fFRbinspt.back()-0.5, fabs(MuEta->at(mu)));
				h_muFLoose->AddBinContent(fillbin, fEventweight);
			}
			else{
				h_muFLoose->Fill(MuPt->at(mu), fabs(MuEta->at(mu)), fEventweight);
			}
		}

		if(passesMTCut(0, mu)) h_Loose_muMET       ->Fill(pfMET       , fEventweight);
		                       h_Loose_muMETnoMTCut->Fill(pfMET       , fEventweight);
		if(passesMETCut())     h_Loose_muMT        ->Fill(MuMT->at(mu), fEventweight);
		if(passesMETCut(20,1)) h_Loose_muMTMET30   ->Fill(MuMT->at(mu), fEventweight);


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

				h_Tight_muMaxJPt    ->Fill(JetRawPt->at(jet)   , fEventweight);
				h_Tight_muNBJets    ->Fill(getNJets(1)         , fEventweight);
				h_Tight_muNJets     ->Fill(getNJets()          , fEventweight);
				h_Tight_muNVertices ->Fill(NVrtx               , fEventweight);

				h_Tight_muD0        ->Fill(MuD0->at(mu)        , fEventweight);

				if( MuPt->at(mu) >  fFRbinspt.back() ){
					int fillbin = h_muFTight->FindBin(fFRbinspt.back(), fabs(MuEta->at(mu)));
					h_muFTight->AddBinContent(fillbin, fEventweight);
				}
				else{
					h_muFTight->Fill(MuPt->at(mu), fabs(MuEta->at(mu)), fEventweight);
				}
			}

			if(passesMTCut(0, mu)) h_Tight_muMET        -> Fill(pfMET        , fEventweight);
			                       h_Tight_muMETnoMTCut -> Fill(pfMET        , fEventweight);
			if(passesMETCut())     h_Tight_muMT         -> Fill(MuMT-> at(mu), fEventweight);
			if(passesMETCut(20,1)) h_Tight_muMTMET30    -> Fill(MuMT-> at(mu), fEventweight);

		}
	}
	h_muFRatio->Divide(h_muFTight, h_muFLoose);


    // electrons
	//int el(-1);
	//if(isCalibrationRegionElEvent(el)) {
	//	h_elIsoPlot->Fill(ElPFIso->at(el), fEventweight);
	//}
}


void Fakerates::bookHistos(){
	/*
	define histograms and binning
	parameters: none
	return: none
	*/ 

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

	h_Loose_muLepPt      = new TH1F("h_Loose_muLepPt"      , "Loose_muLepPt"     , 20 ,  10., 70.); h_Loose_muLepPt      -> Sumw2();
	h_Loose_muLepEta     = new TH1F("h_Loose_muLepEta"     , "Loose_muLepEta"    , 12 ,   0 , 2.4); h_Loose_muLepEta     -> Sumw2();
 	h_Loose_muLepIso     = new TH1F("h_Loose_muLepIso"     , "Loose_muLepIso"    , 20 ,   0 , 1  ); h_Loose_muLepIso     -> Sumw2();
	h_Loose_muD0         = new TH1F("h_Loose_muD0"         , "Loose_muD0"        , 20 ,   0., 0.2); h_Loose_muD0         -> Sumw2();

	h_Loose_muHT         = new TH1F("h_Loose_muHT"         , "Loose_muHT"        , 10 ,  50 , 500); h_Loose_muHT         -> Sumw2();
	h_Loose_muMET        = new TH1F("h_Loose_muMET"        , "Loose_muMET"       , 20 ,  0  , 100); h_Loose_muMET        -> Sumw2();
	h_Loose_muMETnoMTCut = new TH1F("h_Loose_muMETnoMTCut" , "Loose_muMETnoMTCut", 20 ,  0  , 100); h_Loose_muMETnoMTCut -> Sumw2();
	h_Loose_muMT         = new TH1F("h_Loose_muMT"         , "Loose_muMT"        , 10 ,  0  , 100); h_Loose_muMT         -> Sumw2();
	h_Loose_muMTMET30    = new TH1F("h_Loose_muMTMET30"    , "Loose_muMTMET30"   , 20 ,  0  , 200); h_Loose_muMTMET30    -> Sumw2();

	h_Loose_muMaxJPt     = new TH1F("h_Loose_muMaxJPt"     , "Loose_muMaxJPt"    , 13 ,  20 , 150); h_Loose_muMaxJPt     -> Sumw2();
	h_Loose_muNBJets     = new TH1F("h_Loose_muNBJets"     , "Loose_muNBJets"    , 3  ,  0  , 3  ); h_Loose_muNBJets     -> Sumw2();
	h_Loose_muNJets      = new TH1F("h_Loose_muNJets"      , "Loose_muNJets"     , 5  ,  1  , 6  ); h_Loose_muNJets      -> Sumw2();
	h_Loose_muNVertices  = new TH1F("h_Loose_muNVertices"  , "Loose_muNVertices" , 7  ,  5  , 40 ); h_Loose_muNVertices  -> Sumw2();

	h_Loose_muAwayJetDR  = new TH1F("h_Loose_muAwayJetDR"  , "Loose_muAwayJetDR" , 30 ,  0  , 6  ); h_Loose_muAwayJetDR  -> Sumw2();
	h_Loose_muAwayJetPt  = new TH1F("h_Loose_muAwayJetPt"  , "Loose_muAwayJetPt" , 13 ,  20 , 150); h_Loose_muAwayJetPt  -> Sumw2();
	h_Loose_muClosJetDR  = new TH1F("h_Loose_muClosJetDR"  , "Loose_muClosJetDR" , 30 ,  0  , 6  ); h_Loose_muClosJetDR  -> Sumw2();
	h_Loose_muClosJetPt  = new TH1F("h_Loose_muClosJetPt"  , "Loose_muClosJetPt" , 13 ,  20 , 150); h_Loose_muClosJetPt  -> Sumw2();


	h_Tight_muLepPt      = new TH1F("h_Tight_muLepPt"      , "Tight_muLepPt"     , 20 ,  10., 70.); h_Tight_muLepPt      -> Sumw2();
	h_Tight_muLepEta     = new TH1F("h_Tight_muLepEta"     , "Tight_muLepEta"    , 12 ,   0 , 2.4); h_Tight_muLepEta     -> Sumw2();
	h_Tight_muLepIso     = new TH1F("h_Tight_muLepIso"     , "Tight_muLepIso"    , 20 ,   0 , 1  ); h_Tight_muLepIso     -> Sumw2();
 	h_Tight_muD0         = new TH1F("h_Tight_muD0"         , "Tight_muD0"        , 20 ,   0., 0.2); h_Tight_muD0         -> Sumw2();
                                                                                                 
	h_Tight_muHT         = new TH1F("h_Tight_muHT"         , "Tight_muHT"        , 10 ,  50 , 500); h_Tight_muHT         -> Sumw2();
	h_Tight_muMET        = new TH1F("h_Tight_muMET"        , "Tight_muMET"       , 20 ,  0  , 100); h_Tight_muMET        -> Sumw2();
	h_Tight_muMETnoMTCut = new TH1F("h_Tight_muMETnoMTCut" , "Tight_muMETnoMTCut", 20 ,  0  , 100); h_Tight_muMETnoMTCut -> Sumw2();
	h_Tight_muMT         = new TH1F("h_Tight_muMT"         , "Tight_muMT"        , 10 ,  0  , 100); h_Tight_muMT         -> Sumw2();
	h_Tight_muMTMET30    = new TH1F("h_Tight_muMTMET30"    , "Tight_muMTMET30"   , 20 ,  0  , 200); h_Tight_muMTMET30    -> Sumw2();
                                                                                                 
	h_Tight_muMaxJPt     = new TH1F("h_Tight_muMaxJPt"     , "Tight_muMaxJPt"    , 13 ,  20 , 150); h_Tight_muMaxJPt     -> Sumw2();
	h_Tight_muNBJets     = new TH1F("h_Tight_muNBJets"     , "Tight_muNBJets"    , 3  ,  0  , 3  ); h_Tight_muNBJets     -> Sumw2();
	h_Tight_muNJets      = new TH1F("h_Tight_muNJets"      , "Tight_muNJets"     , 5  ,  1  , 6  ); h_Tight_muNJets      -> Sumw2();
	h_Tight_muNVertices  = new TH1F("h_Tight_muNVertices"  , "Tight_muNVertices" , 7  ,  5  , 40 ); h_Tight_muNVertices  -> Sumw2();
                                                                                                 
	h_Tight_muAwayJetDR  = new TH1F("h_Tight_muAwayJetDR"  , "Tight_muAwayJetDR" , 30 ,  0  , 6  ); h_Tight_muAwayJetDR  -> Sumw2();
	h_Tight_muAwayJetPt  = new TH1F("h_Tight_muAwayJetPt"  , "Tight_muAwayJetPt" , 13 ,  20 , 150); h_Tight_muAwayJetPt  -> Sumw2();
	h_Tight_muClosJetDR  = new TH1F("h_Tight_muClosJetDR"  , "Tight_muClosJetDR" , 30 ,  0  , 6  ); h_Tight_muClosJetDR  -> Sumw2();
	h_Tight_muClosJetPt  = new TH1F("h_Tight_muClosJetPt"  , "Tight_muClosJetPt" , 13 ,  20 , 150); h_Tight_muClosJetPt  -> Sumw2();


}


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
	h_elFRatio ->Write(fName+"_"+h_elFRatio->GetName(), TObject::kWriteDelete);
	h_muFRatio ->Write(fName+"_"+h_muFRatio->GetName(), TObject::kWriteDelete);
	h_elPRatio ->Write(fName+"_"+h_elPRatio->GetName(), TObject::kWriteDelete);
	h_muPRatio ->Write(fName+"_"+h_muPRatio->GetName(), TObject::kWriteDelete);
	
	// tight histograms for electrons and muons, f and p rate
	h_elFTight ->Write(fName+"_"+h_elFTight->GetName(), TObject::kWriteDelete);
	h_muFTight ->Write(fName+"_"+h_muFTight->GetName(), TObject::kWriteDelete);
	h_elPTight ->Write(fName+"_"+h_elPTight->GetName(), TObject::kWriteDelete);
	h_muPTight ->Write(fName+"_"+h_muPTight->GetName(), TObject::kWriteDelete);

	// loose histograms for electrons and muons, f and p rate
	h_elFLoose ->Write(fName+"_"+h_elFLoose->GetName(), TObject::kWriteDelete);
	h_muFLoose ->Write(fName+"_"+h_muFLoose->GetName(), TObject::kWriteDelete);
	h_elPLoose ->Write(fName+"_"+h_elPLoose->GetName(), TObject::kWriteDelete);
	h_muPLoose ->Write(fName+"_"+h_muPLoose->GetName(), TObject::kWriteDelete);
 
	h_Loose_muLepPt     ->Write(fName+"_"+h_Loose_muLepPt->GetName(),     TObject::kWriteDelete);
	h_Loose_muLepEta    ->Write(fName+"_"+h_Loose_muLepEta->GetName(),    TObject::kWriteDelete);
	h_Loose_muLepIso    ->Write(fName+"_"+h_Loose_muLepIso->GetName(),    TObject::kWriteDelete);
	h_Loose_muD0        ->Write(fName+"_"+h_Loose_muD0->GetName(),        TObject::kWriteDelete);

	h_Loose_muHT        ->Write(fName+"_"+h_Loose_muHT->GetName(),        TObject::kWriteDelete);
	h_Loose_muMET       ->Write(fName+"_"+h_Loose_muMET->GetName(),       TObject::kWriteDelete);
	h_Loose_muMETnoMTCut->Write(fName+"_"+h_Loose_muMETnoMTCut->GetName(),TObject::kWriteDelete);
	h_Loose_muMT        ->Write(fName+"_"+h_Loose_muMT->GetName(),        TObject::kWriteDelete);
	h_Loose_muMTMET30   ->Write(fName+"_"+h_Loose_muMTMET30->GetName(),   TObject::kWriteDelete);

	h_Loose_muMaxJPt    ->Write(fName+"_"+h_Loose_muMaxJPt->GetName(),    TObject::kWriteDelete);
	h_Loose_muNBJets    ->Write(fName+"_"+h_Loose_muNBJets->GetName(),    TObject::kWriteDelete);
	h_Loose_muNJets     ->Write(fName+"_"+h_Loose_muNJets->GetName(),     TObject::kWriteDelete);
	h_Loose_muNVertices ->Write(fName+"_"+h_Loose_muNVertices->GetName(), TObject::kWriteDelete);

	h_Loose_muAwayJetDR ->Write(fName+"_"+h_Loose_muAwayJetDR->GetName(), TObject::kWriteDelete);
	h_Loose_muAwayJetPt ->Write(fName+"_"+h_Loose_muAwayJetPt->GetName(), TObject::kWriteDelete);
	h_Loose_muClosJetDR ->Write(fName+"_"+h_Loose_muClosJetDR->GetName(), TObject::kWriteDelete);
	h_Loose_muClosJetPt ->Write(fName+"_"+h_Loose_muClosJetPt->GetName(), TObject::kWriteDelete);


	h_Tight_muLepPt     ->Write(fName+"_"+h_Tight_muLepPt->GetName(),     TObject::kWriteDelete);
	h_Tight_muLepEta    ->Write(fName+"_"+h_Tight_muLepEta->GetName(),    TObject::kWriteDelete);
	h_Tight_muLepIso    ->Write(fName+"_"+h_Tight_muLepIso->GetName(),    TObject::kWriteDelete);
	h_Tight_muD0        ->Write(fName+"_"+h_Tight_muD0->GetName(),        TObject::kWriteDelete);

	h_Tight_muHT        ->Write(fName+"_"+h_Tight_muHT->GetName(),        TObject::kWriteDelete);
	h_Tight_muMET       ->Write(fName+"_"+h_Tight_muMET->GetName(),       TObject::kWriteDelete);
	h_Tight_muMETnoMTCut->Write(fName+"_"+h_Tight_muMETnoMTCut->GetName(),TObject::kWriteDelete);
	h_Tight_muMT        ->Write(fName+"_"+h_Tight_muMT->GetName(),        TObject::kWriteDelete);
	h_Tight_muMTMET30   ->Write(fName+"_"+h_Tight_muMTMET30->GetName(),   TObject::kWriteDelete);

	h_Tight_muMaxJPt    ->Write(fName+"_"+h_Tight_muMaxJPt->GetName(),    TObject::kWriteDelete);
	h_Tight_muNBJets    ->Write(fName+"_"+h_Tight_muNBJets->GetName(),    TObject::kWriteDelete);
	h_Tight_muNJets     ->Write(fName+"_"+h_Tight_muNJets->GetName(),     TObject::kWriteDelete);
	h_Tight_muNVertices ->Write(fName+"_"+h_Tight_muNVertices->GetName(), TObject::kWriteDelete);

	h_Tight_muAwayJetDR ->Write(fName+"_"+h_Tight_muAwayJetDR->GetName(), TObject::kWriteDelete);
	h_Tight_muAwayJetPt ->Write(fName+"_"+h_Tight_muAwayJetPt->GetName(), TObject::kWriteDelete);
	h_Tight_muClosJetDR ->Write(fName+"_"+h_Tight_muClosJetDR->GetName(), TObject::kWriteDelete);
	h_Tight_muClosJetPt ->Write(fName+"_"+h_Tight_muClosJetPt->GetName(), TObject::kWriteDelete);

}





