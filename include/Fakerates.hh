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
#include "TRandom3.h"
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
	inline virtual void setDataType     (int     t) {fDataType     = t;};
	inline virtual void setInputFile    (TString i) {fInputFile    = i;};
	inline virtual void setName         (TString n) {fName         = n;};
	inline virtual void setMaxSize      (int     m) {fMaxSize      = m;};
	inline virtual void setXS           (float   x) {if (!fIsData) fXSec = x; else fXSec = -1.;};

	int  fVerbose;
	bool fIsData;
	int fDataType;
	TString fInputFile;
	TString fName;
	int fMaxSize;
	float fXSec;

	TString fOutputDir;
	float fLuminosity;
	bool  fJetCorrection;
	float fJetPtCut;
	float fLepPtCut;
	float fLepD0Cut;
	float fLepIsoCut;
	float fAwayJetBTagCut;
	float fAwayJetDPhiCut;
	bool  fPUweight;
	TString fLepTrigger;
	bool  fLepTriggerMC;
	

    // FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop(TFile *);

	float getSigmaMC(float, float);
	void smearAllJets();	

	bool fillFHist(float);
	void fillFRPlots(float);
	void fillFRPlotsTTBar(float);

	// CUTS
	bool passesUpperMETMT(int, bool);
	bool passesMETCut(float, int);
	bool passesMTCut(int);
	
	std::vector<float, std::allocator<float> >* getLepPt();
	std::vector<float, std::allocator<float> >* getLepEta();
	std::vector<float, std::allocator<float> >* getLepPhi();
	std::vector<float, std::allocator<float> >* getLepPFIso();
	std::vector<float, std::allocator<float> >* getLepD0();

	bool isFRRegionLepEvent(int&, int&, float, bool);
	bool isFRRegionLepEventTTBar(int);

	// LEPTON 
	bool isLooseMuon(int);	
	bool isLooseElectron(int);
	bool isLooseLepton(int);
	bool isLooseOpLepton(int);

	bool isLooseMuonTTBar(int);	
	bool isLooseElectronTTBar(int);
	bool isLooseLeptonTTBar(int);

	bool isTightMuon(int);
	bool isTightElectron(int);
	bool isTightLepton(int);

	bool isTightMuonTTBar(int);
	bool isTightElectronTTBar(int);
	bool isTightLeptonTTBar(int);

	// JETS
	float getJetPt(int);	
	float getMT(int);

	bool isGoodJet(int, float, float);
	bool isGoodSynchJet(int, float);

	float getAwayJet(int, int);
	float getClosestJet(int, int);

	float getHT();
	int getNJets(int);

		// MET
	void setMET(float);
	void setMETPhi(float);
	float getMET();
	float getMETPhi();

	std::vector<float>::const_iterator fITFloat;
	std::vector<bool >::const_iterator fITBool;
	std::vector< int >::const_iterator fITInt;

	// ===================================
	TH2F * h_FRatio;
	TH2F * h_FTight;
	TH2F * h_FLoose;

	TH1F * h_Loose_AwayJetDR;
	TH1F * h_Loose_AwayJetPt;
 	TH1F * h_Loose_ClosJetDR;
	TH1F * h_Loose_ClosJetPt;
	TH1F * h_Loose_HT;
	TH1F * h_Loose_LepEta;
	TH1F * h_Loose_LepEta_30;
	TH1F * h_Loose_LepEta_40;
	TH1F * h_Loose_LepEta_50;
	TH1F * h_Loose_LepEta_60;
	TH1F * h_Loose_LepPt_30;
	TH1F * h_Loose_LepPt_40;
	TH1F * h_Loose_LepPt_50;
	TH1F * h_Loose_LepPt_60;
	TH1F * h_Loose_LepIso;
	TH1F * h_Loose_LepPt;
	TH1F * h_Loose_MET;
	TH1F * h_Loose_METnoMTCut;
	TH1F * h_Loose_MT;
	TH1F * h_Loose_MTMET20;
	TH1F * h_Loose_MTMET30;
	TH1F * h_Loose_MaxJPt;
	TH1F * h_Loose_MaxJCPt;
	TH1F * h_Loose_MaxJRPt;
	TH1F * h_Loose_AllJCPt;
	TH1F * h_Loose_AllJRPt;
	TH1F * h_Loose_AllJEta;
	TH1F * h_Loose_AllJEtatest1;
	TH1F * h_Loose_AllJEtatest2;
	TH1F * h_Loose_AllJEtatest3;
	TH1F * h_Loose_NBJets;
	TH1F * h_Loose_NJets;
	TH1F * h_Loose_NVertices;
	TH1F * h_Loose_NVertices1;
	TH1F * h_Loose_NVerticesMET20;
	TH1F * h_Loose_D0;
	TH2F * h_Loose_JCPtJEta; 
	TH2F * h_Loose_JRPtJEta;
	TH2F * h_Loose_JCPtJPt;
	TH2F * h_Loose_JRPtJPt;
	TH2F * h_Loose_DJPtJEta;
	TH2F * h_Loose_FJPtJEta;
	TH2F * h_Loose_DJPtJPt;
	TH2F * h_Loose_FJPtJPt;
	TH1F * h_Loose_DFZoomEta;
	TH1F * h_Loose_DFZoomPt;
	TH1F * h_Loose_DJPtZoomC[30];
	TH1F * h_Loose_FJPtZoomC[30];
	TH1F * h_Loose_DJPtZoomR[30];
	TH1F * h_Loose_FJPtZoomR[30];
	TH1F * h_Loose_FRZoomEta;
	TH1F * h_Loose_FRZoomPt;
	TH1F * h_Loose_FRMETZoomEta;
	TH1F * h_Loose_FRMETZoomPt;
	TH1F * h_Loose_METZoom[40];

	TH1F * h_Tight_AwayJetDR;
	TH1F * h_Tight_AwayJetPt;
	TH1F * h_Tight_ClosJetDR;
	TH1F * h_Tight_ClosJetPt;
	TH1F * h_Tight_HT;
	TH1F * h_Tight_LepEta;
	TH1F * h_Tight_LepEta_30;
	TH1F * h_Tight_LepEta_40;
	TH1F * h_Tight_LepEta_50;
	TH1F * h_Tight_LepEta_60;
	TH1F * h_Tight_LepPt_30;
	TH1F * h_Tight_LepPt_40;
	TH1F * h_Tight_LepPt_50;
	TH1F * h_Tight_LepPt_60;
	TH1F * h_Tight_LepIso;
	TH1F * h_Tight_LepPt;
	TH1F * h_Tight_MET;
	TH1F * h_Tight_METnoMTCut;
	TH1F * h_Tight_MT;
	TH1F * h_Tight_MTMET20;
	TH1F * h_Tight_MTMET30;
	TH1F * h_Tight_MaxJPt;
	TH1F * h_Tight_MaxJCPt;
	TH1F * h_Tight_MaxJRPt;
	TH1F * h_Tight_AllJCPt;
	TH1F * h_Tight_AllJRPt;
	TH1F * h_Tight_AllJEta;
	TH1F * h_Tight_NBJets;
	TH1F * h_Tight_NJets;
	TH1F * h_Tight_NVertices;   
	TH1F * h_Tight_NVertices1;
	TH1F * h_Tight_NVerticesMET20; 
	TH1F * h_Tight_D0;
	TH2F * h_Tight_JCPtJEta;
	TH2F * h_Tight_JRPtJEta;
	TH2F * h_Tight_JCPtJPt;
	TH2F * h_Tight_JRPtJPt;
	TH2F * h_Tight_DJPtJEta;
	TH2F * h_Tight_FJPtJEta;
	TH2F * h_Tight_DJPtJPt;
	TH2F * h_Tight_FJPtJPt;
	TH1F * h_Tight_DFZoomEta;
	TH1F * h_Tight_DFZoomPt;
	TH1F * h_Tight_DJPtZoomC[30];
	TH1F * h_Tight_FJPtZoomC[30];
	TH1F * h_Tight_DJPtZoomR[30];
	TH1F * h_Tight_FJPtZoomR[30];
	TH1F * h_Tight_FRZoomEta;
	TH1F * h_Tight_FRZoomPt;
	TH1F * h_Tight_FRMETZoomEta;
	TH1F * h_Tight_FRMETZoomPt;
	TH1F * h_Tight_METZoom[40];

	void bookHistos();
	void writeHistos(TFile *);

	// ===================================

	// TRandom3
	TRandom3 *fRandom;

	// Eventweight
	float fLumiweight;
	float fPlotThreshold;

	// Counters
	int fCutflow_afterLepSel;
	int fCutflow_afterJetSel;
	int fCutflow_afterMETCut;
	int fCutflow_afterMTCut;

	int fCounter_all;
	int fCounter_trigger;
	int fCounter_loose;
	int fCounter_veto;
	int fCounter_jet;
	int fCounter_jet30;
	int fCounter_met;
	int fCounter_mt;

	// Binning for FakeRate Projection Plots
	std::vector<float> fFRbinseta;
	std::vector<float> fFRbinspt;
	int fFRn_binseta;
	int fFRn_binspt ;

	// Binning for FakeRate MET Projection Plots
	std::vector<float> fFRMETbinseta;
	std::vector<float> fFRMETbinspt;
	int fFRMETn_binseta;
	int fFRMETn_binspt ;

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
