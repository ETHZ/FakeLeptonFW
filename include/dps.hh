#ifndef DPS_HH
#define DPS_HH

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
#include "TRandom3.h"
#include "TROOT.h"
#include "TVirtualPad.h"
#include "TLorentzVector.h"
#include "TVector3.h"

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

class dps: public FWBaseClass{

public:
	dps(TString);
	virtual ~dps();

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
	TRandom3 * fRand;

	TString fOutputDir;
	float fLuminosity;
	bool  fJetCorrection;
	float fJetPtCut;
	float fMuPtCut;
	float fMuD0Cut;
	float fMuIsoCut;
	float fAwayJetBTagCut;
	float fAwayJetDPhiCut;
	

    // FUNCTIONS
	void doStuff(); // this one gets called by the executable
	void loop(TFile *);
	bool isSameSignMMEvent(int&, int&, int&);
	bool isOppSignMMEvent(int&, int&, int&);

	bool pass3rdVeto(int, int, int);


	// OBJECT FUNCTIONS
	bool isVetoMuon(int);
	bool isLooseMuon(int);
	bool isTightMuon(int);

	bool isVetoEle(int);
	bool isLooseEle(int);
	bool isTightEle(int);

	float getJetPt(int);
	float getMll(int, int, int);
	float getMT(int, int);
	float getMT(float, float, float, float);
	float getMET();
	float getMETPhi();
	float getHT();
	int getNJets(int);
	float getJetInfo(int, int);
	float getDPTRel(int, int, int);
	float getDeltaS(int, int, int);

	std::pair<float,float> getRandMTs(TLorentzVector, TLorentzVector, TLorentzVector);

		// JETS
	bool isGoodJet(int, float, float);


	std::vector<float>::const_iterator fITFloat;
	std::vector<bool >::const_iterator fITBool;
	std::vector< int >::const_iterator fITInt;

	void bookHistos();
	void writeHistos(TFile *);

	// ===================================

	// Eventweight
	float fLumiweight;

	// Counters
	Long64_t fNtot;
	Long64_t fNss;
	
	int fCutflow_afterLepSel;
	int fCutflow_afterJetSel;
	int fCutflow_afterMETCut;
	int fCutflow_afterMTCut;


	void bookSigTree();
	void writeSigTree(TFile *);
	void resetSigTree();
	void fillSigTree();

	TTree * fSigTree;
	TString  fST_sname;

	int   fST_run;
	int   fST_ls;
	int   fST_event;
	int   fST_type;

	int   fST_pass3;

	float fST_weight;

	float fST_pt1;
	float fST_pt2;
	float fST_eta1;
	float fST_eta2;
	float fST_eta12;
	float fST_phi1;
	float fST_phi2;
	float fST_dphi;
	float fST_mt1;
	float fST_mt2;
	float fST_mt1R;
	float fST_mt2R;
	float fST_iso1;
	float fST_iso2;
	int fST_ch1;
	int fST_ch2;

	float fST_dptrel;
	float fST_deltas;
	float fST_lproj;
	float fST_drl;

	float fST_mll;

	float fST_j1pt;
	float fST_j1eta;
	float fST_j1phi;
	float fST_j1bta;
	float fST_j1bst;
	float fST_j2pt;
	float fST_j2eta;
	float fST_j2phi;
	float fST_j2bta;
	float fST_j2bst;
	float fST_j3pt;
	float fST_j3eta;
	float fST_j3phi;
	float fST_j3bta;
	float fST_j3bst;

	int   fST_nj;
	int   fST_nb;
	float fST_ht;
	float fST_met;
	float fST_metphi;

	float fST_dphi1met;
	float fST_dphi2met;


private:
	
};


#endif
