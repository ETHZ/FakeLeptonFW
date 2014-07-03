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

enum iTrig {
  iHLTMU5,
  iHLTMU8,
  iHLTMU12,
  iHLTMU17,
  iHLTMU24,
  iHLTMU40,
  //  iHLTEL17,
  //  iHLTEL17JET30,
  //  iHLTMU17MU8,
  //  iHLTMU17TKMU8,
  iNTRIGS
};

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
	inline virtual void setClosure      (bool    c) {fClosure      = c;};

	int  fVerbose;
	bool fIsData;
	int fDataType;
	TString fInputFile;
	TString fName;
	int fMaxSize;
	float fXSec;
	bool fClosure;

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
	bool  fCSA14;

        // FUNCTIONS
 	void doStuff(); // this one gets called by the executable
	void loop(TFile *);

	float getSigmaMC(float, float);
	void smearAllJets();	

	bool fillFHist(float);
	void fillFHistTTBar(TH2F *&, float, float, float);
	void fillFRPlots(float);
	void fillHLTPlots(float);
	void fillFRPlotsTTBar(float);

	// CUTS
	bool passesUpperMETMT(int, bool);
	bool passesMETCut(float, int);
	bool passesMTCut(int);
	bool passesMllCut(int, int, int, float, int);
	
	std::vector<float, std::allocator<float> >* getLepPt();
	std::vector<float, std::allocator<float> >* getLepEta();
	std::vector<float, std::allocator<float> >* getLepPhi();
	std::vector<float, std::allocator<float> >* getLepPFIso();
	std::vector<float, std::allocator<float> >* getLepD0();
	std::vector<float, std::allocator<float> >* getOpLepPt();
	std::vector<bool, std::allocator<bool> >* getLepIsPrompt();
	void setLepIsPrompt(int, bool);
	std::vector<int, std::allocator<int> >* getLepID();
	std::vector<int, std::allocator<int> >* getLepMID();
	std::vector<int, std::allocator<int> >* getLepGMID();

	bool isPRRegionLepEvent(int&, int&, int&, int&, float);
	bool isFRRegionLepEvent(int&, int&, float, bool);
	bool isFRRegionLepEventTTBar(int);

	// LEPTON 
	int  getLeptonOrigin(int, int, int);

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
	float getMT(int, int);

	bool  isGoodJet(int, float, float);
	bool  isGoodSynchJet(int, float);
	float getLargestCSV();

	int   getAwayJet(int);
	float getAwayJetDR(int);
	int   getClosestJet(int);
	float getClosestJetDR(int);

	float getHT();
	int   getNJets(int);

	// MET
	void  setMET(float);
	void  setMETPhi(float);
	float getMET();
	float getMETPhi();

	// HELPER 
	void fillPurities(int, float,float);
	bool PassesHLT(int);
	void fill2DWithoutOF(TH2F *&, float, float, float);
	void printProgress(Long64_t, Long64_t, TString);

	std::vector<float>::const_iterator fITFloat;
	std::vector<bool >::const_iterator fITBool;
	std::vector< int >::const_iterator fITInt;

	// ===================================
	TH2F * h_FRatio;

	TH2F * h_PLoose;
	TH2F * h_FLoose;
	TH2F * h_FLoose_CERN_small;
	TH2F * h_FLoose_CERN_large;
	TH2F * h_FLoose_0;
	TH2F * h_FLoose_1;
	TH2F * h_FLoose_2;
	TH2F * h_FLoose_3;
	TH2F * h_FLoose_4;
	TH2F * h_FLoose_5;
	TH1F * h_Loose_LepIso_0;
	TH1F * h_Loose_LepIso_1;
	TH1F * h_Loose_LepIso_2;
	TH1F * h_Loose_LepIso_3;
	TH1F * h_Loose_LepIso_4;
	TH1F * h_Loose_LepIso_5;
	TH1F * h_Loose_ClosJetPt_0;
	TH1F * h_Loose_ClosJetPt_1;
	TH1F * h_Loose_ClosJetPt_2;
	TH1F * h_Loose_ClosJetPt_3;
	TH1F * h_Loose_ClosJetPt_4;
	TH1F * h_Loose_ClosJetPt_5;
	TH1F * h_Loose_ClosJetPtLNT_0;
	TH1F * h_Loose_ClosJetPtLNT_1;
	TH1F * h_Loose_ClosJetPtLNT_2;
	TH1F * h_Loose_ClosJetPtLNT_3;
	TH1F * h_Loose_ClosJetPtLNT_4;
	TH1F * h_Loose_ClosJetPtLNT_5;
	TH1F * h_Loose_Provenance;
	TH1F * h_Loose_ProvenanceLNT;
	TH1F * h_Loose_ProvenanceAES;
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
	TH1F * h_Loose_MaxJCSV;
	TH1F * h_Loose_AllJCPt;
	TH1F * h_Loose_AllJRPt;
	TH1F * h_Loose_AllJEta;
	TH1F * h_Loose_AllJCSV;
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

	TH2F * h_PTight;
	TH2F * h_FTight;
	TH2F * h_FTight_CERN_small;
	TH2F * h_FTight_CERN_large;
	TH2F * h_FTight_0;
	TH2F * h_FTight_1;
	TH2F * h_FTight_2;
	TH2F * h_FTight_3;
	TH2F * h_FTight_4;
	TH2F * h_FTight_5;
	TH1F * h_Tight_LepIso_0;
	TH1F * h_Tight_LepIso_1;
	TH1F * h_Tight_LepIso_2;
	TH1F * h_Tight_LepIso_3;
	TH1F * h_Tight_LepIso_4;
	TH1F * h_Tight_LepIso_5;
	TH1F * h_Tight_ClosJetPt_0;
	TH1F * h_Tight_ClosJetPt_1;
	TH1F * h_Tight_ClosJetPt_2;
	TH1F * h_Tight_ClosJetPt_3;
	TH1F * h_Tight_ClosJetPt_4;
	TH1F * h_Tight_ClosJetPt_5;
	TH1F * h_Tight_Provenance;
	TH1F * h_Tight_ProvenanceAES;
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
	TH1F * h_Tight_MaxJCSV;
	TH1F * h_Tight_AllJCPt;
	TH1F * h_Tight_AllJRPt;
	TH1F * h_Tight_AllJEta;
	TH1F * h_Tight_AllJCSV;
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
  
	// =============================
	TH2F * h_FLoose_trig      [iNTRIGS];
	TH2F * h_FTight_trig      [iNTRIGS];
	TH1F * h_Tight_LepPt_trig [iNTRIGS];
	TH1F * h_Tight_LepEta_trig[iNTRIGS];
	TH1F * h_Loose_LepEta_trig[iNTRIGS];
	TH1F * h_Loose_LepPt_trig [iNTRIGS];
	
	TH1F * h_Purity           [iNTRIGS];
	TH1F * h_Purity_LepPt     [iNTRIGS];
	TH1F * h_Purity_JetPt     [iNTRIGS];
	TH1F * h_Purity_JetRawPt  [iNTRIGS];
	TH1F * h_Purity_DRLepJet  [iNTRIGS];
	TH1F * h_Purity_MET       [iNTRIGS];
	TH1F * h_Purity_MT        [iNTRIGS];

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
	int fCounter_CERN_small;
	int fCounter_CERN_large;
	int fCounter_origin;

	int fCounter_origin_pl1;
	int fCounter_origin_pl2;
	int fCounter_origin_pl3;
	int fCounter_origin_pl4;
	int fCounter_origin_pl5;
	int fCounter_origin_pl6;

	int fCounter_origin_pt1;
	int fCounter_origin_pt2;
	int fCounter_origin_pt3;
	int fCounter_origin_pt4;
	int fCounter_origin_pt5;
	int fCounter_origin_pt6;

	int fCounter_origin_nl1;
	int fCounter_origin_nl2;
	int fCounter_origin_nl3;
	int fCounter_origin_nl4;
	int fCounter_origin_nl5;
	int fCounter_origin_nl6;

	int fCounter_origin_nt1;
	int fCounter_origin_nt2;
	int fCounter_origin_nt3;
	int fCounter_origin_nt4;
	int fCounter_origin_nt5;
	int fCounter_origin_nt6;

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
	std::pair<TString , float> getNameAndXsec(TString file){
	// DATA SAMPLES
		if(file.Contains("DoubleMu")){
			setData(true);
			return std::make_pair("doublemu", 1.); }
		else if(file.Contains("DoubleElectron")){
			setData(true);
			return std::make_pair("doubleel", 1.); }
	// TTbar samples
		else if(file.Contains("TTJets") && file.Contains("MassiveB") )
			return std::make_pair("ttjets_inc", 245.8);
		else if(file.Contains("TTJets") && file.Contains("SemiLept") )
			return std::make_pair("ttjets_semi", 102.5);
		else if(file.Contains("TTJets") && file.Contains("FullLept") )
			return std::make_pair("ttjets_full", 24.6);
	// WJets samples
		else if(file.Contains("WJetsToLNu"))
			return std::make_pair("wjets", 37509.);
		else if(file.Contains("W1Jets"))
			return std::make_pair("w1jets", 6642.);
		else if(file.Contains("W2Jets"))
			return std::make_pair("w2jets", 2152.);
		else if(file.Contains("W3Jets"))
			return std::make_pair("w3jets", 638.4);
		else if(file.Contains("W4Jets"))
			return std::make_pair("w4jets", 263.2);
	// DYJets samples
		else if(file.Contains("DYJets") && file.Contains("M-50"))
			return std::make_pair("dyjets", 3504.);
		else if(file.Contains("DYJets") && file.Contains("M-10To50"))
			return std::make_pair("dyjets", 877.);
	// MuEnriched QCD
		else if(file.Contains("QCD") && file.Contains("Pt_20_MuEnrichedPt_15"))
			return std::make_pair("qcdmuenr", 3.64E8*3.7E-4);
		else if(file.Contains("QCD") && file.Contains("20to30_MuEnrichedPt5"))
			return std::make_pair("qcdmuenr", 2.87E8*0.0065);
		else if(file.Contains("QCD") && file.Contains("30to50_MuEnrichedPt5"))
			return std::make_pair("qcdmuenr", 6.609E7*0.0122);
		else if(file.Contains("QCD") && file.Contains("50to80_MuEnrichedPt5"))
			return std::make_pair("qcdmuenr", 8082000.0*0.0218);
	// EMEnriched
		else if(file.Contains("QCD") && file.Contains("Pt_20_30_EMEnriched"))
			return std::make_pair("qcdemenr", 2.886E8*0.0101);
		else if(file.Contains("QCD") && file.Contains("Pt_30_80_EMEnriched"))
			return std::make_pair("qcdemenr", 7.433E7*0.0621);
		else if(file.Contains("QCD") && file.Contains("Pt_80_170_EMEnriched"))
			return std::make_pair("qcdemenr", 1191000.0*0.1539);
	// BCTOE
		else if(file.Contains("QCD") && file.Contains("Pt_20_30_BCtoE"))
			return std::make_pair("qcdemenr", 2.886E8*5.8E-4);
		else if(file.Contains("QCD") && file.Contains("Pt_30_80_BCtoE"))
			return std::make_pair("qcdemenr", 7.433E7*0.00225);
		else if(file.Contains("QCD") && file.Contains("Pt_80_170_BCtoE"))
			return std::make_pair("qcdemenr", 1191000.0*0.0109);
	// RARES
		else if(file.Contains("TTWJets"))
			return std::make_pair("ttwjets", 0.232);
		else if(file.Contains("TTZJets"))
			return std::make_pair("ttzjets", 0.206);
		else{
			std::cout << "COULD NOT IDENTIFY SAMPLE FROM FILENAME. EXITING!" << std::endl; exit(-1);
		}
	}

private:
	
};


#endif
