#ifndef FAKERATES_HH
#define FAKERATES_HH

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
//#include <windows.h>

#include "include/FWBaseClass.h"
#include "Utilities.hh"

class Fakerates: public FWBaseClass{

public:
	Fakerates(TString);
	virtual ~Fakerates();

	virtual void init(bool = false); // Careful, MakeClass produces Init with capital I!
	void loadConfigFile(TString);

	template <class T> inline void getObjectSafe(TFile* pFile, TString name, T*& object){
		pFile->GetObject(name, object);
		if(!object){
			std::cout << name + " not found!" << std::endl;
			exit(-1);
		}
		return;
	};

	inline virtual void setVerbose      (int     v) {fVerbose      = v;};
	inline virtual void setData         (bool    d) {fIsData       = d;};
	inline virtual void setInputFile    (TString i) {fInputFile    = i;};
	inline virtual void setName         (TString n) {fName         = n;};
	inline virtual void setMaxSize      (int     m) {fMaxSize      = m;};
	inline virtual void setXS           (float   x) {if (!fIsData) fXSec = x; else fXSec = -1.;};

	int  fVerbose;
	bool fIsData;
	TString fInputFile;
	TString fName;
	int fMaxSize;
	float fXSec;

	TString fOutputDir;
	TString fInputDir;
	float fLuminosity;
	bool  fJetCorrection;
	float fJetPtCut;
	float fMuD0Cut;
	float fMuIsoCut;
	float fAwayJetBTagCut;
	float fAwayJetDPhiCut;
	

    // FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop(TFile *);

	//void fillRatios();
	void fillFRPlots();

	bool passesUpperMETMT(int, int);
	bool passesMETCut(float, int);
	bool passesMTCut(int, int);

	bool isFRRegionMuEvent(int&, int&, float);
	bool isFRRegionElEvent(int&);


	// OBJECT FUNCTIONS
		// MUONS
	bool isLooseMuon(int);
	bool isTightMuon(int);

	float getJetPt(int);
	float getMT(int, int);

		// JETS
	bool isGoodJet(int, float, float);
	bool isGoodSynchJet(int, float);
	float getAwayJet(int, int);
	float getClosestJet(int, int);

	float getHT();
	int getNJets(int);

		// MET
	float getMET();
	float getMETPhi();

	std::vector<float>::const_iterator fITFloat;
	std::vector<bool >::const_iterator fITBool;
	std::vector< int >::const_iterator fITInt;

	// ===================================
	// the ratio histograms, those are just divided versions of the following
	TH2F * h_elFRatio;
	TH2F * h_muFRatio;
	TH2F * h_elPRatio;
	TH2F * h_muPRatio;
	
	// passing histograms for electrons and muons, f and p rate
	TH2F * h_elFTight;
	TH2F * h_muFTight;
	TH2F * h_elPTight;
	TH2F * h_muPTight;

	// failing histograms for electrons and muons, f and p rate
	TH2F * h_elFLoose;
	TH2F * h_muFLoose;
	TH2F * h_elPLoose;
	TH2F * h_muPLoose;

	TH1F * h_Loose_muAwayJetDR;
	TH1F * h_Loose_muAwayJetPt;
 	TH1F * h_Loose_muClosJetDR;
	TH1F * h_Loose_muClosJetPt;
	TH1F * h_Loose_muHT;
	TH1F * h_Loose_muLepEta;
	TH1F * h_Loose_muLepEta_30;
	TH1F * h_Loose_muLepEta_40;
	TH1F * h_Loose_muLepEta_50;
	TH1F * h_Loose_muLepEta_60;
	TH1F * h_Loose_muLepPt_30;
	TH1F * h_Loose_muLepPt_40;
	TH1F * h_Loose_muLepPt_50;
	TH1F * h_Loose_muLepPt_60;
	TH1F * h_Loose_muLepIso;
	TH1F * h_Loose_muLepPt;
	TH1F * h_Loose_muMET;
	TH1F * h_Loose_muMETnoMTCut;
	TH1F * h_Loose_muMT;
	TH1F * h_Loose_muMTMET30;
	TH1F * h_Loose_muMaxJPt;
	TH1F * h_Loose_muMaxJCPt;
	TH1F * h_Loose_muMaxJRPt;
	TH1F * h_Loose_muAllJCPt;
	TH1F * h_Loose_muAllJRPt;
	TH1F * h_Loose_muAllJEta;
	TH1F * h_Loose_muNBJets;
	TH1F * h_Loose_muNJets;
	TH1F * h_Loose_muNVertices;
	TH1F * h_Loose_muD0;
	TH2F * h_Loose_muJCPtJEta; 
	TH2F * h_Loose_muJRPtJEta;
	TH2F * h_Loose_muJCPtJPt;
	TH2F * h_Loose_muJRPtJPt;
	TH2F * h_Loose_muDJPtJEta;
	TH2F * h_Loose_muFJPtJEta;
	TH2F * h_Loose_muDJPtJPt;
	TH2F * h_Loose_muFJPtJPt;
	TH1F * h_Loose_muDFZoomEta;
	TH1F * h_Loose_muDFZoomPt;
	TH1F * h_Loose_muDJPtZoom[30];
	TH1F * h_Loose_muFJPtZoom[30];

	TH1F * h_Tight_muAwayJetDR;
	TH1F * h_Tight_muAwayJetPt;
	TH1F * h_Tight_muClosJetDR;
	TH1F * h_Tight_muClosJetPt;
	TH1F * h_Tight_muHT;
	TH1F * h_Tight_muLepEta;
	TH1F * h_Tight_muLepEta_30;
	TH1F * h_Tight_muLepEta_40;
	TH1F * h_Tight_muLepEta_50;
	TH1F * h_Tight_muLepEta_60;
	TH1F * h_Tight_muLepPt_30;
	TH1F * h_Tight_muLepPt_40;
	TH1F * h_Tight_muLepPt_50;
	TH1F * h_Tight_muLepPt_60;
	TH1F * h_Tight_muLepIso;
	TH1F * h_Tight_muLepPt;
	TH1F * h_Tight_muMET;
	TH1F * h_Tight_muMETnoMTCut;
	TH1F * h_Tight_muMT;
	TH1F * h_Tight_muMTMET30;
	TH1F * h_Tight_muMaxJPt;
	TH1F * h_Tight_muMaxJCPt;
	TH1F * h_Tight_muMaxJRPt;
	TH1F * h_Tight_muAllJCPt;
	TH1F * h_Tight_muAllJRPt;
	TH1F * h_Tight_muAllJEta;
	TH1F * h_Tight_muNBJets;
	TH1F * h_Tight_muNJets;
	TH1F * h_Tight_muNVertices;   
	TH1F * h_Tight_muD0;
	TH2F * h_Tight_muJCPtJEta;
	TH2F * h_Tight_muJRPtJEta;
	TH2F * h_Tight_muJCPtJPt;
	TH2F * h_Tight_muJRPtJPt;
	TH2F * h_Tight_muDJPtJEta;
	TH2F * h_Tight_muFJPtJEta;
	TH2F * h_Tight_muDJPtJPt;
	TH2F * h_Tight_muFJPtJPt;
	TH1F * h_Tight_muDFZoomEta;
	TH1F * h_Tight_muDFZoomPt;
	TH1F * h_Tight_muDJPtZoom[30];
	TH1F * h_Tight_muFJPtZoom[30];

	void bookHistos();
	void writeHistos(TFile *);

	// ===================================

	// Eventweight
	float fEventweight;

	// Counters
	int fCutflow_afterLepSel;
	int fCutflow_afterJetSel;
	int fCutflow_afterMETCut;
	int fCutflow_afterMTCut;

	// Binning for FakeRate Projection Plots
	std::vector<float> fFRbinseta;
	std::vector<float> fFRbinspt;
	int fFRn_binseta;
	int fFRn_binspt ;

	// Binning for Difference/Fraction in JetPt Projection Plots
	std::vector<float> fDFbinseta;
	std::vector<float> fDFbinspt;
	int fDFn_binseta;
	int fDFn_binspt;	

    // SAMPLE CLASS
	class Sample{
		public:
			// Sample(){};
			Sample(TString name, float xs){
				xsec = xs;
				sname = name;
			};
			~Sample(){};
			float xsec;
			TString sname;

	};

private:
	
};


#endif
