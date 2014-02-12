//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Wed Feb 12 10:37:51 2014 by ROOT version 5.34/14
// from TTree Analysis/AnalysisTree
// found on file: release/fakeminitree.root
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
   //using namespace std;
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

   // Declaration of leaf types
   Int_t           Run;
   Int_t           Lumi;
   Int_t           Event;
   Int_t           HLT_MU8;
   Int_t           HLT_MU8_PS;
   Int_t           HLT_MU17;
   Int_t           HLT_MU17_PS;
   Int_t           HLT_MU24_ETA2P1;
   Int_t           HLT_MU24_ETA2P1_PS;
   Int_t           HLT_ELE17_TIGHT;
   Int_t           HLT_ELE17_TIGHT_PS;
   Int_t           HLT_ELE17_JET30_TIGHT;
   Int_t           HLT_ELE17_JET30_TIGHT_PS;
   Int_t           HLT_ELE8_TIGHT;
   Int_t           HLT_ELE8_TIGHT_PS;
   Int_t           HLT_ELE8_JET30_TIGHT;
   Int_t           HLT_ELE8_JET30_TIGHT_PS;
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
   Int_t           NVrtx;
   Float_t         PUWeight;
   Float_t         PUWeightUp;
   Float_t         PUWeightDn;
   Float_t         GenWeight;
   std::vector<float>   *MuPt;
   std::vector<float>   *MuEta;
   std::vector<float>   *MuPhi;
   std::vector<int>     *MuCharge;
   std::vector<float>   *MuPFIso;
   std::vector<float>   *MuD0;
   std::vector<float>   *MuMT;
   std::vector<bool>    *MuIsVeto;
   std::vector<bool>    *MuIsLoose;
   std::vector<bool>    *MuIsTight;
   std::vector<float>   *ElPt;
   std::vector<float>   *ElEta;
   std::vector<float>   *ElPhi;
   std::vector<int>     *ElCharge;
   std::vector<float>   *ElPFIso;
   std::vector<float>   *ElD0;
   std::vector<float>   *ElMT;
   std::vector<bool>    *ElIsVeto;
   std::vector<bool>    *ElIsLoose;
   std::vector<bool>    *ElIsTight;
   Float_t         pfMET;
   Float_t         pfMETPhi;
   std::vector<float>   *JetPt;
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
   TBranch        *b_HLT_MU8;   //!
   TBranch        *b_HLT_MU8_PS;   //!
   TBranch        *b_HLT_MU17;   //!
   TBranch        *b_HLT_MU17_PS;   //!
   TBranch        *b_HLT_MU24_ETA2P1;   //!
   TBranch        *b_HLT_MU24_ETA2P1_PS;   //!
   TBranch        *b_HLT_ELE17_TIGHT;   //!
   TBranch        *b_HLT_ELE17_TIGHT_PS;   //!
   TBranch        *b_HLT_ELE17_JET30_TIGHT;   //!
   TBranch        *b_HLT_ELE17_JET30_TIGHT_PS;   //!
   TBranch        *b_HLT_ELE8_TIGHT;   //!
   TBranch        *b_HLT_ELE8_TIGHT_PS;   //!
   TBranch        *b_HLT_ELE8_JET30_TIGHT;   //!
   TBranch        *b_HLT_ELE8_JET30_TIGHT_PS;   //!
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
   TBranch        *b_NVrtx;   //!
   TBranch        *b_PUWeight;   //!
   TBranch        *b_PUWeightUp;   //!
   TBranch        *b_PUWeightDn;   //!
   TBranch        *b_GenWeight;   //!
   TBranch        *b_MuPt;   //!
   TBranch        *b_MuEta;   //!
   TBranch        *b_MuPhi;   //!
   TBranch        *b_MuCharge;   //!
   TBranch        *b_MuPFIso;   //!
   TBranch        *b_MuD0;   //!
   TBranch        *b_MuMT;   //!
   TBranch        *b_MuIsVeto;   //!
   TBranch        *b_MuIsLoose;   //!
   TBranch        *b_MuIsTight;   //!
   TBranch        *b_ElPt;   //!
   TBranch        *b_ElEta;   //!
   TBranch        *b_ElPhi;   //!
   TBranch        *b_ElCharge;   //!
   TBranch        *b_ElPFIso;   //!
   TBranch        *b_ElD0;   //!
   TBranch        *b_ElMT;   //!
   TBranch        *b_ElIsVeto;   //!
   TBranch        *b_ElIsLoose;   //!
   TBranch        *b_ElIsTight;   //!
   TBranch        *b_pfMET;   //!
   TBranch        *b_pfMETPhi;   //!
   TBranch        *b_JetPt;   //!
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
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("release/fakeminitree.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("release/fakeminitree.root");
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
   MuPFIso = 0;
   MuD0 = 0;
   MuMT = 0;
   MuIsVeto = 0;
   MuIsLoose = 0;
   MuIsTight = 0;
   ElPt = 0;
   ElEta = 0;
   ElPhi = 0;
   ElCharge = 0;
   ElPFIso = 0;
   ElD0 = 0;
   ElMT = 0;
   ElIsVeto = 0;
   ElIsLoose = 0;
   ElIsTight = 0;
   JetPt = 0;
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
   fChain->SetBranchAddress("HLT_MU8", &HLT_MU8, &b_HLT_MU8);
   fChain->SetBranchAddress("HLT_MU8_PS", &HLT_MU8_PS, &b_HLT_MU8_PS);
   fChain->SetBranchAddress("HLT_MU17", &HLT_MU17, &b_HLT_MU17);
   fChain->SetBranchAddress("HLT_MU17_PS", &HLT_MU17_PS, &b_HLT_MU17_PS);
   fChain->SetBranchAddress("HLT_MU24_ETA2P1", &HLT_MU24_ETA2P1, &b_HLT_MU24_ETA2P1);
   fChain->SetBranchAddress("HLT_MU24_ETA2P1_PS", &HLT_MU24_ETA2P1_PS, &b_HLT_MU24_ETA2P1_PS);
   fChain->SetBranchAddress("HLT_ELE17_TIGHT", &HLT_ELE17_TIGHT, &b_HLT_ELE17_TIGHT);
   fChain->SetBranchAddress("HLT_ELE17_TIGHT_PS", &HLT_ELE17_TIGHT_PS, &b_HLT_ELE17_TIGHT_PS);
   fChain->SetBranchAddress("HLT_ELE17_JET30_TIGHT", &HLT_ELE17_JET30_TIGHT, &b_HLT_ELE17_JET30_TIGHT);
   fChain->SetBranchAddress("HLT_ELE17_JET30_TIGHT_PS", &HLT_ELE17_JET30_TIGHT_PS, &b_HLT_ELE17_JET30_TIGHT_PS);
   fChain->SetBranchAddress("HLT_ELE8_TIGHT", &HLT_ELE8_TIGHT, &b_HLT_ELE8_TIGHT);
   fChain->SetBranchAddress("HLT_ELE8_TIGHT_PS", &HLT_ELE8_TIGHT_PS, &b_HLT_ELE8_TIGHT_PS);
   fChain->SetBranchAddress("HLT_ELE8_JET30_TIGHT", &HLT_ELE8_JET30_TIGHT, &b_HLT_ELE8_JET30_TIGHT);
   fChain->SetBranchAddress("HLT_ELE8_JET30_TIGHT_PS", &HLT_ELE8_JET30_TIGHT_PS, &b_HLT_ELE8_JET30_TIGHT_PS);
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
   fChain->SetBranchAddress("NVrtx", &NVrtx, &b_NVrtx);
   fChain->SetBranchAddress("PUWeight", &PUWeight, &b_PUWeight);
   fChain->SetBranchAddress("PUWeightUp", &PUWeightUp, &b_PUWeightUp);
   fChain->SetBranchAddress("PUWeightDn", &PUWeightDn, &b_PUWeightDn);
   fChain->SetBranchAddress("GenWeight", &GenWeight, &b_GenWeight);
   fChain->SetBranchAddress("MuPt", &MuPt, &b_MuPt);
   fChain->SetBranchAddress("MuEta", &MuEta, &b_MuEta);
   fChain->SetBranchAddress("MuPhi", &MuPhi, &b_MuPhi);
   fChain->SetBranchAddress("MuCharge", &MuCharge, &b_MuCharge);
   fChain->SetBranchAddress("MuPFIso", &MuPFIso, &b_MuPFIso);
   fChain->SetBranchAddress("MuD0", &MuD0, &b_MuD0);
   fChain->SetBranchAddress("MuMT", &MuMT, &b_MuMT);
   fChain->SetBranchAddress("MuIsVeto", &MuIsVeto, &b_MuIsVeto);
   fChain->SetBranchAddress("MuIsLoose", &MuIsLoose, &b_MuIsLoose);
   fChain->SetBranchAddress("MuIsTight", &MuIsTight, &b_MuIsTight);
   fChain->SetBranchAddress("ElPt", &ElPt, &b_ElPt);
   fChain->SetBranchAddress("ElEta", &ElEta, &b_ElEta);
   fChain->SetBranchAddress("ElPhi", &ElPhi, &b_ElPhi);
   fChain->SetBranchAddress("ElCharge", &ElCharge, &b_ElCharge);
   fChain->SetBranchAddress("ElPFIso", &ElPFIso, &b_ElPFIso);
   fChain->SetBranchAddress("ElD0", &ElD0, &b_ElD0);
   fChain->SetBranchAddress("ElMT", &ElMT, &b_ElMT);
   fChain->SetBranchAddress("ElIsVeto", &ElIsVeto, &b_ElIsVeto);
   fChain->SetBranchAddress("ElIsLoose", &ElIsLoose, &b_ElIsLoose);
   fChain->SetBranchAddress("ElIsTight", &ElIsTight, &b_ElIsTight);
   fChain->SetBranchAddress("pfMET", &pfMET, &b_pfMET);
   fChain->SetBranchAddress("pfMETPhi", &pfMETPhi, &b_pfMETPhi);
   fChain->SetBranchAddress("JetPt", &JetPt, &b_JetPt);
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
