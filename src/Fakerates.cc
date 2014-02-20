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
	Util::SetStyle();
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

	TFile *pFile = new TFile(fOutputFilename, "RECREATE");
	bookHistos();

	TFile * file_ = TFile::Open(fInputFile);
	TTree * tree_ = (TTree *) file_->Get("Analysis"); // tree name has to be named "Analysis"
	tree_->ResetBranchAddresses();
	Init(tree_);
	Long64_t tot_events = tree_->GetEntriesFast();

	int ntot = 0;

	// loop on events in the tree
	for (Long64_t jentry=0; jentry<tot_events;jentry++) {
		if(jentry > 150000) break; // foo
		tree_->GetEntry(jentry);
		ntot++;

		// fillRatios();
		// fillIsoPlots();

		synchOutput();
	}
	// end loop on the events

	cout << "i just looped on " << ntot << " events." << endl;
	delete file_, tree_;


	writeHistos(pFile);

	// pFile->Write();
	pFile->Close();

}

void Fakerates::synchOutput(){
	int mu = -1;
	bool a = isCalibrationRegionMuEvent(mu);

}


bool Fakerates::isCalibrationRegionMuEvent(int &mu){
	if(MuPt->size() < 1) return false;
	int nloose(0), nveto_add(0);
	std::vector<int> loosemu_inds;
	for(int i=0; i < MuPt->size(); ++i){
		if(MuIsLoose->at(i)){
			nloose++;
			mu = i;
			loosemu_inds.push_back(i);
		}
		else{
			if(MuIsVeto->at(i)) nveto_add++;
		}
	}
	// require exactly one loose muon and no additional veto muons
	if(nloose    != 1) return false;
	// if(nveto_add != 0) return false; // don't require this for the synching

	// upper cuts on MT and MET
	if(pfMET > 20.)        return false;
	if(MuMT->at(loosemu_inds[0]) > 20.) return false;

	int nawayjets(0);
	int jetind(-1);
	std::vector<int> awayjet_inds;
	if(JetPt->size() < 1) return false;
	for(int jet=0; jet < JetPt->size(); ++jet){
		// if(!isGoodJet(jet, 40.)) continue;
		if(!isGoodSynchJet(jet, 40.)) continue;
		if(Util::DeltaPhi(JetPhi->at(jet), MuPhi->at(mu)) < 1.0 ) continue;
		nawayjets++;
		awayjet_inds.push_back(jet);
	}
	if(awayjet_inds.size() < 1) return false;
	// cout << awayjet_inds.size() << endl;

	float dphi =  Util::DeltaPhi(JetPhi->at(awayjet_inds[0]), MuPhi->at(loosemu_inds[0]));
	
 	cout << Form("%i\t%i\t%10i\t%.2f\t%.2f\t%i\t%.2f\t%.2f",Run, Lumi, Event, MuPt->at(loosemu_inds[0]), JetRawPt->at(awayjet_inds[0]), (int) MuIsTight->at(loosemu_inds[0]), dphi, JetCSVBTag->at(awayjet_inds[0])) << endl;
	return true;
}

bool Fakerates::isGoodSynchJet(int j, float pt){
	if(JetRawPt->at(j) < pt) return false;
	if(fabs(JetEta->at(j)) > 2.5) return false;
	// if(JetBetaStar->at(j) > 0.2*TMath::Log(NVrtx-0.67)) return false; // value for jets with eta < 2.5
	
	// no cleaning float minDR = 0.4;

	// no cleaning // Remove jets close to all tight leptons
	// no cleaning for(int imu = 0; imu < MuPt->size(); ++imu){
	// no cleaning     if(!MuIsTight->at(imu)) continue;
	// no cleaning     if(Util::GetDeltaR(MuEta->at(imu), JetEta->at(j), MuPhi->at(imu), JetPhi->at(j)) > minDR ) continue;
	// no cleaning     return false;
	// no cleaning }
	// no cleaning for(int iel = 0; iel < ElPt->size(); ++iel){
	// no cleaning     if(!ElIsTight->at(iel)) continue;
	// no cleaning     if(Util::GetDeltaR(ElEta->at(iel), JetEta->at(j), ElPhi->at(iel), JetPhi->at(j)) > minDR ) continue;
	// no cleaning     return false;
	// no cleaning }
	return true;


}
bool Fakerates::isGoodJet(int j, float pt){
	if(JetPt->at(j) < pt) return false;
	if(fabs(JetEta->at(j)) > 2.5) return false;
	if(JetBetaStar->at(j) > 0.2*TMath::Log(NVrtx-0.67)) return false; // value for jets with eta < 2.5
	
	float minDR = 0.4;

	// Remove jets close to all tight leptons
	for(int imu = 0; imu < MuPt->size(); ++imu){
	    if(!MuIsTight->at(imu)) continue;
	    if(Util::GetDeltaR(MuEta->at(imu), JetEta->at(j), MuPhi->at(imu), JetPhi->at(j)) > minDR ) continue;
	    return false;
	}
	for(int iel = 0; iel < ElPt->size(); ++iel){
	    if(!ElIsTight->at(iel)) continue;
	    if(Util::GetDeltaR(ElEta->at(iel), JetEta->at(j), ElPhi->at(iel), JetPhi->at(j)) > minDR ) continue;
	    return false;
	}
	return true;


}

bool Fakerates::isCalibrationRegionElEvent(int &el){
	return false;	
}

void Fakerates::fillIsoPlots(){
	int mu(-1);
	if(isCalibrationRegionMuEvent(mu)){
		h_muIsoPlot->Fill(MuPFIso->at(mu));
		h_muFLoose ->Fill(MuPt->at(mu), MuEta->at(mu));
		if(MuIsTight->at(mu) && MuPFIso->at(mu) < 0.1) {
			h_muFTight ->Fill(MuPt->at(mu), MuEta->at(mu));
		}
	}
	int el(-1);
	if(isCalibrationRegionElEvent(el)){
		h_elIsoPlot->Fill(ElPFIso->at(el));
	}
}

void Fakerates::bookHistos(){

	// the ratio histograms, those are just divided versions of the following
	h_elFRatio = new TH2F("h_elFRatio", "elFRatio", 4, 10, 40, 2, 0., 2.5);
	h_muFRatio = new TH2F("h_muFRatio", "muFRatio", 4, 10, 40, 2, 0., 2.5);
	h_elPRatio = new TH2F("h_elPRatio", "elPRatio", 4, 10, 40, 2, 0., 2.5);
	h_muPRatio = new TH2F("h_muPRatio", "muPRatio", 4, 10, 40, 2, 0., 2.5);
	
	// passing histograms for electrons and muons, f and p rate
	h_elFTight = new TH2F("h_elFTight", "elFTight", 4, 10, 40, 2, 0., 2.5);
	h_muFTight = new TH2F("h_muFTight", "muFTight", 4, 10, 40, 2, 0., 2.5);
	h_elPTight = new TH2F("h_elPTight", "elPTight", 4, 10, 40, 2, 0., 2.5);
	h_muPTight = new TH2F("h_muPTight", "muPTight", 4, 10, 40, 2, 0., 2.5);

	// failing histograms for electrons and muons, f and p rate
	h_elFLoose = new TH2F("h_elFLoose", "elFLoose", 4, 10, 40, 2, 0., 2.5);
	h_muFLoose = new TH2F("h_muFLoose", "muFLoose", 4, 10, 40, 2, 0., 2.5);
	h_elPLoose = new TH2F("h_elPLoose", "elPLoose", 4, 10, 40, 2, 0., 2.5);
	h_muPLoose = new TH2F("h_muPLoose", "muPLoose", 4, 10, 40, 2, 0., 2.5);

	h_muIsoPlot = new TH1F("h_muIsoPlot", "muIsoPlot", 100, 0., 1.);
	h_elIsoPlot = new TH1F("h_elIsoPlot", "elIsoPlot", 100, 0., 1.);

}
void Fakerates::writeHistos(TFile* pFile){
	pFile->cd(); 
	TDirectory* sdir = Util::FindOrCreate(fName, pFile);
	sdir->cd();


	// the ratio histograms, those are just divided versions of the following
	h_elFRatio ->Write(fName+h_elFRatio->GetName(), TObject::kWriteDelete);
	h_muFRatio ->Write(fName+h_muFRatio->GetName(), TObject::kWriteDelete);
	h_elPRatio ->Write(fName+h_elPRatio->GetName(), TObject::kWriteDelete);
	h_muPRatio ->Write(fName+h_muPRatio->GetName(), TObject::kWriteDelete);
	
	// tight histograms for electrons and muons, f and p rate
	h_elFTight ->Write(fName+h_elFTight->GetName(), TObject::kWriteDelete);
	h_muFTight ->Write(fName+h_muFTight->GetName(), TObject::kWriteDelete);
	h_elPTight ->Write(fName+h_elPTight->GetName(), TObject::kWriteDelete);
	h_muPTight ->Write(fName+h_muPTight->GetName(), TObject::kWriteDelete);

	// loose histograms for electrons and muons, f and p rate
	h_elFLoose ->Write(fName+h_elFLoose->GetName(), TObject::kWriteDelete);
	h_muFLoose ->Write(fName+h_muFLoose->GetName(), TObject::kWriteDelete);
	h_elPLoose ->Write(fName+h_elPLoose->GetName(), TObject::kWriteDelete);
	h_muPLoose ->Write(fName+h_muPLoose->GetName(), TObject::kWriteDelete);

	h_muIsoPlot ->Write(fName+h_muIsoPlot->GetName(), TObject::kWriteDelete);

	h_elIsoPlot ->Write(fName+h_elIsoPlot->GetName(), TObject::kWriteDelete);

}
