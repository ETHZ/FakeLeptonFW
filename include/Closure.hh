#ifndef CLOSURE_HH
#define CLOSURE_HH

#include "TMath.h"

#include "TString.h"
#include "TObject.h"
#include "TFile.h"
#include "TDirectory.h"
#include "TH1.h"
#include "TH2.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TTree.h"
#include "TRandom.h"
#include "TROOT.h"
#include "TVirtualPad.h"
#include "TLorentzVector.h"

#include "TPaveStats.h"
#include "TPaletteAxis.h"

#include <iostream>
#include <fstream>
#include <iomanip>
#include <math.h>
#include <vector>
#include <fstream>
#include <stdlib.h>
#include <stdio.h>
#include <map>
#include <time.h> // access to date/time

#include "include/FWBaseClass.h"
#include "include/FakeRatios.hh"
#include "Utilities.hh"

#include "include/Fakerates.hh"
#include "include/BTagSF.hh"



// class Closure: public FWBaseClass{
class Closure: public Fakerates{

public:
	Closure();
	Closure(TString, TString);
	virtual ~Closure();

	virtual void init(TString); // Careful, MakeClass produces Init with capital I!

	template <class T> inline void getObjectSafe(TFile* pFile, TString name, T*& object){
		pFile->GetObject(name, object);
		if(!object){
			std::cout << name + " not found!" << std::endl;
			exit(-1);
		}
		return;
	};

	TString fOutputSubDir;
	inline void setVerbose      (int     v) {fVerbose      = v;};
	inline void setData         (bool    d) {fIsData       = d;};
	inline void setInputFile    (TString i) {fInputFile    = i;};
	inline void setOutputDir    (TString o) {fOutputDir    = o;};
	inline void setName         (TString n) {fName         = n;};
	inline void setMaxSize      (int     m) {fMaxSize      = m;};
	inline void setXS           (float   x) {if (!fIsData) fXSec = x; else fXSec = -1.;};
	inline void setFRFile(TString infile){ fFRFileString = infile;};

	int     fVerbose;
	bool    fIsData;
	TString fOutputDir;
	TString fInputFile;
	TString fName;
	int     fMaxSize;
	float   fXSec;
	float   fLuminosity;

// COUNTERS
	int fTot;
	int fSS;
	int fOS;
	int fSSmm;
	int fSSem;
	int fSSee;
	int fOSmm;
	int fOSem;
	int fOSee;


// INPUT FR FILE
	TString   fFRFileString;
	TFile   * fFRFile;
// INPUT FR HISTOGRAMS
	TH2F * f_h_FR_data_el;
	TH2F * f_h_FR_data_mu;
	TH2F * f_h_FR_data_pure_el;
	TH2F * f_h_FR_data_pure_mu;
	TH2F * f_h_FR_mc_el;
	TH2F * f_h_FR_mc_mu;
	TH2F * f_h_FR_qcd_el;
	TH2F * f_h_FR_qcd_mu;
	TH2F * f_h_FR_ttbar_el;
	TH2F * f_h_FR_ttbar_mu;

// INPUT PR HISTOGRAMS
	TH2F * f_h_PR_dy_el;
	TH2F * f_h_PR_dy_mu;

	FakeRatios * fFR;
	float getFRatio(int, float, float);
	float getPRatio(int, float, float);
	void  storePredictions();
	
// FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop(TFile*);

	bool isSameSignLLEvent(int&, int&, int&);
	bool passMllCut(int, int, int, float);
	bool isSignalTrigger(int);

	void fillGenPlots();
	void bookHistos();
	void writeHistos(TFile *);

	void scaleBTags(int, TString = "");
	void JESJER(int);
	void propagateMET(TLorentzVector, TLorentzVector);
	void saveJetsAndMET();
	void resetJetsAndMET();
	
	std::vector< std::pair<TLorentzVector, float> > fJets;
	TLorentzVector fMET;
	BTagSF * fBTagSF;
	TRandom3 * fBTagRandom;

// // CLASS
// 	class variable {
// 	  public:
// 		//variable();
// 		TString name;
// 	
// 		float nominal;
// 		float jesup;
// 		float jesdn;
// 	
// 		void clean(){
// 			name    = "";
// 			nominal = -1.;
// 			jesup   = -1.;
// 			jesdn   = -1.;
// 		};
// 	};

// Eventweight
	float fEventWeight;

// OUTPUT HISTOGRAMS
	TH2F * h_muPt_partonPt_MR;
	TH2F * h_leptonPt_closestJetPt_MR;
	TH2F * h_closestJetPt_partonPt_MR;
	TH1F * h_mu_closestJet_dr_MR;

	TH2F * h_muPt_partonPt_ALL;
	TH2F * h_leptonPt_closestJetPt_ALL;
	TH2F * h_closestJetPt_partonPt_ALL;
	TH1F * h_mu_closestJet_dr_ALL;

	TH2F * h_muPt_partonPt_SS;
	TH2F * h_leptonPt_closestJetPt_SS;
	TH2F * h_closestJetPt_partonPt_SS;
	TH1F * h_mu_closestJet_dr_SS;

// OUTPUT TREE

	void bookClosureTree();
	void writeClosureTree(TFile *);
	void resetClosureTree();
	void fillClosureTree();

	TTree * fClosureTree;

	TString  fCT_sname;

	int   fCT_run;
	int   fCT_ls;
	int   fCT_event;
	int   fCT_type;
	int   fCT_passTrigger;

	float fCT_lumiW;
	float fCT_puW;

	float fCT_f1;
	float fCT_f2;
	float fCT_p1;
	float fCT_p2;

	float fCT_npp;
	float fCT_npf;
	float fCT_nfp;
	float fCT_nff;
	int   fCT_tlcat;

	float fCT_pt1;
	float fCT_pt2;
	float fCT_eta1;
	float fCT_eta2;
	float fCT_phi1;
	float fCT_phi2;
	float fCT_iso1;
	float fCT_iso2;
	float fCT_ip1;
	float fCT_ip2;
	float fCT_neiso1;
	float fCT_neiso2;
	float fCT_phiso1;
	float fCT_phiso2;
	float fCT_chiso1;
	float fCT_chiso2;
	float fCT_pucor1;
	float fCT_pucor2;
	float fCT_mt1;
	float fCT_mt2;
	int   fCT_ch1;
	int   fCT_ch2;

	int   fCT_nj;
	int   fCT_nb;
	float fCT_ht;
	float fCT_met;

	int   fCT_nj_jesup;
	int   fCT_nb_jesup;
	float fCT_ht_jesup;
	float fCT_met_jesup;

	int   fCT_nj_jesdn;
	int   fCT_nb_jesdn;
	float fCT_ht_jesdn;
	float fCT_met_jesdn;

	int   fCT_nj_jer;
	int   fCT_nb_jer;
	float fCT_ht_jer;
	float fCT_met_jer;

	int   fCT_nj_bup;
	int   fCT_nb_bup;
	float fCT_ht_bup;
	float fCT_met_bup;

	int   fCT_nj_bdn;
	int   fCT_nb_bdn;
	float fCT_ht_bdn;
	float fCT_met_bdn;


	int   fCT_lID1;
	int   fCT_lID2;
	int   fCT_lProv1;
	int   fCT_lProv2;


private:
	
};


#endif
