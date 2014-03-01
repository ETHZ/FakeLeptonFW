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

#include "include/FWBaseClass.h"
#include "Utilities.hh"

class Fakerates: public FWBaseClass{

public:
	Fakerates();
	virtual ~Fakerates();

	virtual void init(bool = false); // Careful, MakeClass produces Init with capital I!

	template <class T> inline void getObjectSafe(TFile* pFile, TString name, T*& object){
		pFile->GetObject(name, object);
		if(!object){
			std::cout << name + " not found!" << std::endl;
			exit(-1);
		}
		return;
	};

	inline virtual void setVerbose   (int     v) {fVerbose   = v;};
	inline virtual void setData      (bool    d) {fIsData    = d;};
	inline virtual void setInputFile (TString f) {fInputFile = f;};
	inline virtual void setOutputDir (TString d) {fOutputDir = d;};
	inline virtual void setMaxSize   (int     m) {fMaxSize   = m;};
    inline virtual void setName      (TString n) {fName      = n;};
	inline virtual void setXS        (float   x) {if (!fIsData) fXSec = x; else fXSec = -1.;};

	int  fVerbose;
	bool fIsData;
	float fXSec;
	TString fInputFile;
	TString fOutputDir;
	TString fOutputFilename;
    int fMaxSize;
	TString fName;
	

    // FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop();

	//void fillRatios();
	void fillIsoPlots();

	bool passesUpperMETMT(int, int);
    bool passesMETCut(float, int);
    bool passesMTCut(int, int);

	bool isCalibrationRegionMuEvent(int&, int&);
	bool isCalibrationRegionElEvent(int&);

	bool isGoodJet(int, float);
	bool isGoodSynchJet(int, float);

    float getAwayJet(int, int);
    float getClosestJet(int, int);
    float getHT();
    int getNJets(int);

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
    TH1F * h_Loose_muLepIso;
    TH1F * h_Loose_muLepPt;
    TH1F * h_Loose_muMET;
    TH1F * h_Loose_muMETnoMTCut;
    TH1F * h_Loose_muMT;
    TH1F * h_Loose_muMTMET30;
    TH1F * h_Loose_muMaxJPt;
    TH1F * h_Loose_muNBJets;
    TH1F * h_Loose_muNJets;
    TH1F * h_Loose_muNVertices;
    TH1F * h_Loose_muD0;
    TH2F * h_Loose_muF;

    TH1F * h_Tight_muAwayJetDR;
    TH1F * h_Tight_muAwayJetPt;
    TH1F * h_Tight_muClosJetDR;
    TH1F * h_Tight_muClosJetPt;
    TH1F * h_Tight_muHT;
    TH1F * h_Tight_muLepEta;
    TH1F * h_Tight_muLepIso;
    TH1F * h_Tight_muLepPt;
    TH1F * h_Tight_muMET;
    TH1F * h_Tight_muMETnoMTCut;
    TH1F * h_Tight_muMT;
    TH1F * h_Tight_muMTMET30;
    TH1F * h_Tight_muMaxJPt;
    TH1F * h_Tight_muNBJets;
    TH1F * h_Tight_muNJets;
    TH1F * h_Tight_muNVertices;   
    TH1F * h_Tight_muD0;
    TH2F * h_Tight_muF;

	void bookHistos();
	void writeHistos(TFile *);

	// ===================================

	float fEventweight;
    int fCutflow_afterLepSel;
	int fCutflow_afterJetSel;
	int fCutflow_afterMETCut;
	int fCutflow_afterMTCut ;
	

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
