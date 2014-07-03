//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Jun 19 13:55:15 2014 by ROOT version 5.34/18
// from TTree Analysis/AnalysisTree
// found on file: /shome/mdunser/fakeTrees/2leps/TTWJets-V03-09-00.root
//////////////////////////////////////////////////////////

#ifndef FWBaseClass_h
#define FWBaseClass_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.
#include <vector>

// Fixed size dimensions of array or collections stored in the TTree if any.

class FWBaseClass {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           Run;
   Int_t           Lumi;
   Int_t           Event;
   Int_t           HLT_MU17_MU8;
   Int_t           HLT_MU17_MU8_PS;
   Int_t           HLT_MU17_TKMU8;
   Int_t           HLT_MU17_TKMU8_PS;
   Int_t           HLT_ELE17_ELE8_TIGHT;
   Int_t           HLT_ELE17_ELE8_TIGHT_PS;
   Int_t           HLT_MU8_ELE17_TIGHT;
   Int_t           HLT_MU8_ELE17_TIGHT_PS;
   Int_t           HLT_MU17_ELE8_TIGHT;
   Int_t           HLT_MU17_ELE8_TIGHT_PS;
   Int_t           HLT_MU8;
   Int_t           HLT_MU8_PS;
   Int_t           HLT_MU17;
   Int_t           HLT_MU17_PS;
   Int_t           HLT_MU5;
   Int_t           HLT_MU5_PS;
   Int_t           HLT_MU12;
   Int_t           HLT_MU12_PS;
   Int_t           HLT_MU24;
   Int_t           HLT_MU24_PS;
   Int_t           HLT_MU40;
   Int_t           HLT_MU40_PS;
   Int_t           HLT_ELE17_TIGHT;
   Int_t           HLT_ELE17_TIGHT_PS;
   Int_t           HLT_ELE17_JET30_TIGHT;
   Int_t           HLT_ELE17_JET30_TIGHT_PS;
   Int_t           HLT_ELE8_TIGHT;
   Int_t           HLT_ELE8_TIGHT_PS;
   Int_t           HLT_ELE8_JET30_TIGHT;
   Int_t           HLT_ELE8_JET30_TIGHT_PS;
   Int_t           NVrtx;
   Int_t           NTrue;
   Float_t         Rho;
   Float_t         PUWeight;
   Float_t         PUWeightUp;
   Float_t         PUWeightDn;
   Float_t         GenWeight;
   std::vector<float>   *MuPt;
   std::vector<float>   *MuEta;
   std::vector<float>   *MuPhi;
   std::vector<int>     *MuCharge;
   std::vector<float>   *MuD0;
   std::vector<float>   *MuPFIso;
   std::vector<float>   *MuNeIso;
   std::vector<float>   *MuPhIso;
   std::vector<float>   *MuChIso;
   std::vector<float>   *MuSumPU;
   std::vector<float>   *MuIso03SumPt;
   std::vector<bool>    *MuIsVeto;
   std::vector<bool>    *MuIsLoose;
   std::vector<bool>    *MuIsTight;
   std::vector<bool>    *MuIsPrompt;
   std::vector<int>     *MuID;
   std::vector<int>     *MuMID;
   std::vector<int>     *MuGMID;
   std::vector<int>     *MuMatchID;
   std::vector<int>     *MuMatchMID;
   std::vector<int>     *MuMatchGMID;
   std::vector<float>   *ElPt;
   std::vector<float>   *ElEta;
   std::vector<float>   *ElPhi;
   std::vector<int>     *ElCharge;
   std::vector<float>   *ElD0;
   std::vector<int>     *ElChCo;
   std::vector<float>   *ElPFIso;
   std::vector<float>   *ElNeIso;
   std::vector<float>   *ElPhIso;
   std::vector<float>   *ElChIso;
   std::vector<bool>    *ElIsVeto;
   std::vector<bool>    *ElIsLoose;
   std::vector<bool>    *ElIsTight;
   std::vector<bool>    *ElIsPrompt;
   std::vector<int>     *ElID;
   std::vector<int>     *ElMID;
   std::vector<int>     *ElGMID;
   std::vector<int>     *ElMatchID;
   std::vector<int>     *ElMatchMID;
   std::vector<int>     *ElMatchGMID;
   Float_t         pfMET;
   Float_t         pfMETPhi;
   Float_t         pfMET1;
   Float_t         pfMET1Phi;
   std::vector<float>   *JetPt;
   std::vector<float>   *JetRawPt;
   std::vector<float>   *JetEta;
   std::vector<float>   *JetPhi;
   std::vector<float>   *JetEnergy;
   std::vector<float>   *JetCSVBTag;
   std::vector<int>     *JetPartonFlav;
   std::vector<float>   *JetBetaStar;

   // List of branches
   TBranch        *b_Run;   //!
   TBranch        *b_Lumi;   //!
   TBranch        *b_Event;   //!
   TBranch        *b_HLT_MU17_MU8;   //!
   TBranch        *b_HLT_MU17_MU8_PS;   //!
   TBranch        *b_HLT_MU17_TKMU8;   //!
   TBranch        *b_HLT_MU17_TKMU8_PS;   //!
   TBranch        *b_HLT_ELE17_ELE8_TIGHT;   //!
   TBranch        *b_HLT_ELE17_ELE8_TIGHT_PS;   //!
   TBranch        *b_HLT_MU8_ELE17_TIGHT;   //!
   TBranch        *b_HLT_MU8_ELE17_TIGHT_PS;   //!
   TBranch        *b_HLT_MU17_ELE8_TIGHT;   //!
   TBranch        *b_HLT_MU17_ELE8_TIGHT_PS;   //!
   TBranch        *b_HLT_MU8;   //!
   TBranch        *b_HLT_MU8_PS;   //!
   TBranch        *b_HLT_MU17;   //!
   TBranch        *b_HLT_MU17_PS;   //!
   TBranch        *b_HLT_MU5;   //!
   TBranch        *b_HLT_MU5_PS;   //!
   TBranch        *b_HLT_MU12;   //!
   TBranch        *b_HLT_MU12_PS;   //!
   TBranch        *b_HLT_MU24;   //!
   TBranch        *b_HLT_MU24_PS;   //!
   TBranch        *b_HLT_MU40;   //!
   TBranch        *b_HLT_MU40_PS;   //!
   TBranch        *b_HLT_ELE17_TIGHT;   //!
   TBranch        *b_HLT_ELE17_TIGHT_PS;   //!
   TBranch        *b_HLT_ELE17_JET30_TIGHT;   //!
   TBranch        *b_HLT_ELE17_JET30_TIGHT_PS;   //!
   TBranch        *b_HLT_ELE8_TIGHT;   //!
   TBranch        *b_HLT_ELE8_TIGHT_PS;   //!
   TBranch        *b_HLT_ELE8_JET30_TIGHT;   //!
   TBranch        *b_HLT_ELE8_JET30_TIGHT_PS;   //!
   TBranch        *b_NVrtx;   //!
   TBranch        *b_NTrue;   //!
   TBranch        *b_Rho;   //!
   TBranch        *b_PUWeight;   //!
   TBranch        *b_PUWeightUp;   //!
   TBranch        *b_PUWeightDn;   //!
   TBranch        *b_GenWeight;   //!
   TBranch        *b_MuPt;   //!
   TBranch        *b_MuEta;   //!
   TBranch        *b_MuPhi;   //!
   TBranch        *b_MuCharge;   //!
   TBranch        *b_MuD0;   //!
   TBranch        *b_MuPFIso;   //!
   TBranch        *b_MuNeIso;   //!
   TBranch        *b_MuPhIso;   //!
   TBranch        *b_MuChIso;   //!
   TBranch        *b_MuSumPU;   //!
   TBranch        *b_MuIso03SumPt;   //!
   TBranch        *b_MuIsVeto;   //!
   TBranch        *b_MuIsLoose;   //!
   TBranch        *b_MuIsTight;   //!
   TBranch        *b_MuIsPrompt;   //!
   TBranch        *b_MuID;   //!
   TBranch        *b_MuMID;   //!
   TBranch        *b_MuGMID;   //!
   TBranch        *b_MuMatchID;   //!
   TBranch        *b_MuMatchMID;   //!
   TBranch        *b_MuMatchGMID;   //!
   TBranch        *b_ElPt;   //!
   TBranch        *b_ElEta;   //!
   TBranch        *b_ElPhi;   //!
   TBranch        *b_ElCharge;   //!
   TBranch        *b_ElD0;   //!
   TBranch        *b_ElChCo;   //!
   TBranch        *b_ElPFIso;   //!
   TBranch        *b_ElNeIso;   //!
   TBranch        *b_ElPhIso;   //!
   TBranch        *b_ElChIso;   //!
   TBranch        *b_ElIsVeto;   //!
   TBranch        *b_ElIsLoose;   //!
   TBranch        *b_ElIsTight;   //!
   TBranch        *b_ElIsPrompt;   //!
   TBranch        *b_ElID;   //!
   TBranch        *b_ElMID;   //!
   TBranch        *b_ElGMID;   //!
   TBranch        *b_ElMatchID;   //!
   TBranch        *b_ElMatchMID;   //!
   TBranch        *b_ElMatchGMID;   //!
   TBranch        *b_pfMET;   //!
   TBranch        *b_pfMETPhi;   //!
   TBranch        *b_pfMET1;   //!
   TBranch        *b_pfMET1Phi;   //!
   TBranch        *b_JetPt;   //!
   TBranch        *b_JetRawPt;   //!
   TBranch        *b_JetEta;   //!
   TBranch        *b_JetPhi;   //!
   TBranch        *b_JetEnergy;   //!
   TBranch        *b_JetCSVBTag;   //!
   TBranch        *b_JetPartonFlav;   //!
   TBranch        *b_JetBetaStar;   //!

   FWBaseClass(TTree *tree=0);
   virtual ~FWBaseClass();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef FWBaseClass_cxx
FWBaseClass::FWBaseClass(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("/shome/mdunser/fakeTrees/2leps/TTWJets-V03-09-00.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("/shome/mdunser/fakeTrees/2leps/TTWJets-V03-09-00.root");
      }
      f->GetObject("Analysis",tree);

   }
   Init(tree);
}

FWBaseClass::~FWBaseClass()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t FWBaseClass::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t FWBaseClass::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void FWBaseClass::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set object pointer
   MuPt = 0;
   MuEta = 0;
   MuPhi = 0;
   MuCharge = 0;
   MuD0 = 0;
   MuPFIso = 0;
   MuNeIso = 0;
   MuPhIso = 0;
   MuChIso = 0;
   MuSumPU = 0;
   MuIso03SumPt = 0;
   MuIsVeto = 0;
   MuIsLoose = 0;
   MuIsTight = 0;
   MuIsPrompt = 0;
   MuID = 0;
   MuMID = 0;
   MuGMID = 0;
   MuMatchID = 0;
   MuMatchMID = 0;
   MuMatchGMID = 0;
   ElPt = 0;
   ElEta = 0;
   ElPhi = 0;
   ElCharge = 0;
   ElD0 = 0;
   ElChCo = 0;
   ElPFIso = 0;
   ElNeIso = 0;
   ElPhIso = 0;
   ElChIso = 0;
   ElIsVeto = 0;
   ElIsLoose = 0;
   ElIsTight = 0;
   ElIsPrompt = 0;
   ElID = 0;
   ElMID = 0;
   ElGMID = 0;
   ElMatchID = 0;
   ElMatchMID = 0;
   ElMatchGMID = 0;
   JetPt = 0;
   JetRawPt = 0;
   JetEta = 0;
   JetPhi = 0;
   JetEnergy = 0;
   JetCSVBTag = 0;
   JetPartonFlav = 0;
   JetBetaStar = 0;
   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("Run", &Run, &b_Run);
   fChain->SetBranchAddress("Lumi", &Lumi, &b_Lumi);
   fChain->SetBranchAddress("Event", &Event, &b_Event);
   fChain->SetBranchAddress("HLT_MU17_MU8", &HLT_MU17_MU8, &b_HLT_MU17_MU8);
   fChain->SetBranchAddress("HLT_MU17_MU8_PS", &HLT_MU17_MU8_PS, &b_HLT_MU17_MU8_PS);
   fChain->SetBranchAddress("HLT_MU17_TKMU8", &HLT_MU17_TKMU8, &b_HLT_MU17_TKMU8);
   fChain->SetBranchAddress("HLT_MU17_TKMU8_PS", &HLT_MU17_TKMU8_PS, &b_HLT_MU17_TKMU8_PS);
   fChain->SetBranchAddress("HLT_ELE17_ELE8_TIGHT", &HLT_ELE17_ELE8_TIGHT, &b_HLT_ELE17_ELE8_TIGHT);
   fChain->SetBranchAddress("HLT_ELE17_ELE8_TIGHT_PS", &HLT_ELE17_ELE8_TIGHT_PS, &b_HLT_ELE17_ELE8_TIGHT_PS);
   fChain->SetBranchAddress("HLT_MU8_ELE17_TIGHT", &HLT_MU8_ELE17_TIGHT, &b_HLT_MU8_ELE17_TIGHT);
   fChain->SetBranchAddress("HLT_MU8_ELE17_TIGHT_PS", &HLT_MU8_ELE17_TIGHT_PS, &b_HLT_MU8_ELE17_TIGHT_PS);
   fChain->SetBranchAddress("HLT_MU17_ELE8_TIGHT", &HLT_MU17_ELE8_TIGHT, &b_HLT_MU17_ELE8_TIGHT);
   fChain->SetBranchAddress("HLT_MU17_ELE8_TIGHT_PS", &HLT_MU17_ELE8_TIGHT_PS, &b_HLT_MU17_ELE8_TIGHT_PS);
   fChain->SetBranchAddress("HLT_MU8", &HLT_MU8, &b_HLT_MU8);
   fChain->SetBranchAddress("HLT_MU8_PS", &HLT_MU8_PS, &b_HLT_MU8_PS);
   fChain->SetBranchAddress("HLT_MU17", &HLT_MU17, &b_HLT_MU17);
   fChain->SetBranchAddress("HLT_MU17_PS", &HLT_MU17_PS, &b_HLT_MU17_PS);
   fChain->SetBranchAddress("HLT_MU5", &HLT_MU5, &b_HLT_MU5);
   fChain->SetBranchAddress("HLT_MU5_PS", &HLT_MU5_PS, &b_HLT_MU5_PS);
   fChain->SetBranchAddress("HLT_MU12", &HLT_MU12, &b_HLT_MU12);
   fChain->SetBranchAddress("HLT_MU12_PS", &HLT_MU12_PS, &b_HLT_MU12_PS);
   fChain->SetBranchAddress("HLT_MU24", &HLT_MU24, &b_HLT_MU24);
   fChain->SetBranchAddress("HLT_MU24_PS", &HLT_MU24_PS, &b_HLT_MU24_PS);
   fChain->SetBranchAddress("HLT_MU40", &HLT_MU40, &b_HLT_MU40);
   fChain->SetBranchAddress("HLT_MU40_PS", &HLT_MU40_PS, &b_HLT_MU40_PS);
   fChain->SetBranchAddress("HLT_ELE17_TIGHT", &HLT_ELE17_TIGHT, &b_HLT_ELE17_TIGHT);
   fChain->SetBranchAddress("HLT_ELE17_TIGHT_PS", &HLT_ELE17_TIGHT_PS, &b_HLT_ELE17_TIGHT_PS);
   fChain->SetBranchAddress("HLT_ELE17_JET30_TIGHT", &HLT_ELE17_JET30_TIGHT, &b_HLT_ELE17_JET30_TIGHT);
   fChain->SetBranchAddress("HLT_ELE17_JET30_TIGHT_PS", &HLT_ELE17_JET30_TIGHT_PS, &b_HLT_ELE17_JET30_TIGHT_PS);
   fChain->SetBranchAddress("HLT_ELE8_TIGHT", &HLT_ELE8_TIGHT, &b_HLT_ELE8_TIGHT);
   fChain->SetBranchAddress("HLT_ELE8_TIGHT_PS", &HLT_ELE8_TIGHT_PS, &b_HLT_ELE8_TIGHT_PS);
   fChain->SetBranchAddress("HLT_ELE8_JET30_TIGHT", &HLT_ELE8_JET30_TIGHT, &b_HLT_ELE8_JET30_TIGHT);
   fChain->SetBranchAddress("HLT_ELE8_JET30_TIGHT_PS", &HLT_ELE8_JET30_TIGHT_PS, &b_HLT_ELE8_JET30_TIGHT_PS);
   fChain->SetBranchAddress("NVrtx", &NVrtx, &b_NVrtx);
   fChain->SetBranchAddress("NTrue", &NTrue, &b_NTrue);
   fChain->SetBranchAddress("Rho", &Rho, &b_Rho);
   fChain->SetBranchAddress("PUWeight", &PUWeight, &b_PUWeight);
   fChain->SetBranchAddress("PUWeightUp", &PUWeightUp, &b_PUWeightUp);
   fChain->SetBranchAddress("PUWeightDn", &PUWeightDn, &b_PUWeightDn);
   fChain->SetBranchAddress("GenWeight", &GenWeight, &b_GenWeight);
   fChain->SetBranchAddress("MuPt", &MuPt, &b_MuPt);
   fChain->SetBranchAddress("MuEta", &MuEta, &b_MuEta);
   fChain->SetBranchAddress("MuPhi", &MuPhi, &b_MuPhi);
   fChain->SetBranchAddress("MuCharge", &MuCharge, &b_MuCharge);
   fChain->SetBranchAddress("MuD0", &MuD0, &b_MuD0);
   fChain->SetBranchAddress("MuPFIso", &MuPFIso, &b_MuPFIso);
   fChain->SetBranchAddress("MuNeIso", &MuNeIso, &b_MuNeIso);
   fChain->SetBranchAddress("MuPhIso", &MuPhIso, &b_MuPhIso);
   fChain->SetBranchAddress("MuChIso", &MuChIso, &b_MuChIso);
   fChain->SetBranchAddress("MuSumPU", &MuSumPU, &b_MuSumPU);
   fChain->SetBranchAddress("MuIso03SumPt", &MuIso03SumPt, &b_MuIso03SumPt);
   fChain->SetBranchAddress("MuIsVeto", &MuIsVeto, &b_MuIsVeto);
   fChain->SetBranchAddress("MuIsLoose", &MuIsLoose, &b_MuIsLoose);
   fChain->SetBranchAddress("MuIsTight", &MuIsTight, &b_MuIsTight);
   fChain->SetBranchAddress("MuIsPrompt", &MuIsPrompt, &b_MuIsPrompt);
   fChain->SetBranchAddress("MuID", &MuID, &b_MuID);
   fChain->SetBranchAddress("MuMID", &MuMID, &b_MuMID);
   fChain->SetBranchAddress("MuGMID", &MuGMID, &b_MuGMID);
   fChain->SetBranchAddress("MuMatchID", &MuMatchID, &b_MuMatchID);
   fChain->SetBranchAddress("MuMatchMID", &MuMatchMID, &b_MuMatchMID);
   fChain->SetBranchAddress("MuMatchGMID", &MuMatchGMID, &b_MuMatchGMID);
   fChain->SetBranchAddress("ElPt", &ElPt, &b_ElPt);
   fChain->SetBranchAddress("ElEta", &ElEta, &b_ElEta);
   fChain->SetBranchAddress("ElPhi", &ElPhi, &b_ElPhi);
   fChain->SetBranchAddress("ElCharge", &ElCharge, &b_ElCharge);
   fChain->SetBranchAddress("ElD0", &ElD0, &b_ElD0);
   fChain->SetBranchAddress("ElChCo", &ElChCo, &b_ElChCo);
   fChain->SetBranchAddress("ElPFIso", &ElPFIso, &b_ElPFIso);
   fChain->SetBranchAddress("ElNeIso", &ElNeIso, &b_ElNeIso);
   fChain->SetBranchAddress("ElPhIso", &ElPhIso, &b_ElPhIso);
   fChain->SetBranchAddress("ElChIso", &ElChIso, &b_ElChIso);
   fChain->SetBranchAddress("ElIsVeto", &ElIsVeto, &b_ElIsVeto);
   fChain->SetBranchAddress("ElIsLoose", &ElIsLoose, &b_ElIsLoose);
   fChain->SetBranchAddress("ElIsTight", &ElIsTight, &b_ElIsTight);
   fChain->SetBranchAddress("ElIsPrompt", &ElIsPrompt, &b_ElIsPrompt);
   fChain->SetBranchAddress("ElID", &ElID, &b_ElID);
   fChain->SetBranchAddress("ElMID", &ElMID, &b_ElMID);
   fChain->SetBranchAddress("ElGMID", &ElGMID, &b_ElGMID);
   fChain->SetBranchAddress("ElMatchID", &ElMatchID, &b_ElMatchID);
   fChain->SetBranchAddress("ElMatchMID", &ElMatchMID, &b_ElMatchMID);
   fChain->SetBranchAddress("ElMatchGMID", &ElMatchGMID, &b_ElMatchGMID);
   fChain->SetBranchAddress("pfMET", &pfMET, &b_pfMET);
   fChain->SetBranchAddress("pfMETPhi", &pfMETPhi, &b_pfMETPhi);
   fChain->SetBranchAddress("pfMET1", &pfMET1, &b_pfMET1);
   fChain->SetBranchAddress("pfMET1Phi", &pfMET1Phi, &b_pfMET1Phi);
   fChain->SetBranchAddress("JetPt", &JetPt, &b_JetPt);
   fChain->SetBranchAddress("JetRawPt", &JetRawPt, &b_JetRawPt);
   fChain->SetBranchAddress("JetEta", &JetEta, &b_JetEta);
   fChain->SetBranchAddress("JetPhi", &JetPhi, &b_JetPhi);
   fChain->SetBranchAddress("JetEnergy", &JetEnergy, &b_JetEnergy);
   fChain->SetBranchAddress("JetCSVBTag", &JetCSVBTag, &b_JetCSVBTag);
   fChain->SetBranchAddress("JetPartonFlav", &JetPartonFlav, &b_JetPartonFlav);
   fChain->SetBranchAddress("JetBetaStar", &JetBetaStar, &b_JetBetaStar);
   Notify();
}

Bool_t FWBaseClass::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void FWBaseClass::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t FWBaseClass::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef FWBaseClass_cxx
