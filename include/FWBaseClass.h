//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Mar  6 14:10:15 2014 by ROOT version 5.34/14
// from TTree Analysis/AnalysisTree
// found on file: qcdBigFile_START53_V20.root
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
   Int_t           HLT_MU8;
   Int_t           HLT_MU8_PS;
   Int_t           HLT_MU17;
   Int_t           HLT_MU17_PS;
   Int_t           HLT_MU40;
   Int_t           HLT_MU40_PS;
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

   std::vector<bool>    *MuIsGlobal;
   std::vector<bool>    *MuIsPF;
   std::vector<float>   *MuChi2;
   std::vector<int>     *MuChamberHits;
   std::vector<int>     *MuMatchedStations;
   std::vector<float>   *MuDz;
   std::vector<int>     *MuPixelHits;
   std::vector<int>     *MuNLayers;
   std::vector<bool>    *MuIsVeto;
   std::vector<bool>    *MuIsLoose;
   std::vector<bool>    *MuIsTight;
   std::vector<float>   *ElPt;
   std::vector<float>   *ElEta;
   std::vector<float>   *ElPhi;
   std::vector<int>     *ElCharge;
   std::vector<float>   *ElPFIso;
   std::vector<float>   *ElD0;

   std::vector<bool>    *ElIsVeto;
   std::vector<bool>    *ElIsLoose;
   std::vector<bool>    *ElIsTight;
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
   TBranch        *b_HLT_MU8;   //!
   TBranch        *b_HLT_MU8_PS;   //!
   TBranch        *b_HLT_MU17;   //!
   TBranch        *b_HLT_MU17_PS;   //!
   TBranch        *b_HLT_MU40; //!
   TBranch        *b_HLT_MU40_PS; //!
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
   TBranch        *b_MuIsGlobal;   //!
   TBranch        *b_MuIsPF;   //!
   TBranch        *b_MuChi2;   //!
   TBranch        *b_MuChamberHits;   //!
   TBranch        *b_MuMatchedStations;   //!
   TBranch        *b_MuDz;   //!
   TBranch        *b_MuPixelHits;   //!
   TBranch        *b_MuNLayers;   //!
   TBranch        *b_MuIsVeto;   //!
   TBranch        *b_MuIsLoose;   //!
   TBranch        *b_MuIsTight;   //!
   TBranch        *b_ElPt;   //!
   TBranch        *b_ElEta;   //!
   TBranch        *b_ElPhi;   //!
   TBranch        *b_ElCharge;   //!
   TBranch        *b_ElPFIso;   //!
   TBranch        *b_ElD0;   //!
   TBranch        *b_ElIsVeto;   //!
   TBranch        *b_ElIsLoose;   //!
   TBranch        *b_ElIsTight;   //!
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
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("qcdBigFile_START53_V20.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("qcdBigFile_START53_V20.root");
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
   MuIsGlobal = 0;
   MuIsPF = 0;
   MuChi2 = 0;
   MuChamberHits = 0;
   MuMatchedStations = 0;
   MuDz = 0;
   MuPixelHits = 0;
   MuNLayers = 0;
   MuIsVeto = 0;
   MuIsLoose = 0;
   MuIsTight = 0;
   ElPt = 0;
   ElEta = 0;
   ElPhi = 0;
   ElCharge = 0;
   ElPFIso = 0;
   ElD0 = 0;
   ElIsVeto = 0;
   ElIsLoose = 0;
   ElIsTight = 0;
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
   fChain->SetBranchAddress("HLT_MU8", &HLT_MU8, &b_HLT_MU8);
   fChain->SetBranchAddress("HLT_MU8_PS", &HLT_MU8_PS, &b_HLT_MU8_PS);
   fChain->SetBranchAddress("HLT_MU17", &HLT_MU17, &b_HLT_MU17);
   fChain->SetBranchAddress("HLT_MU17_PS", &HLT_MU17_PS, &b_HLT_MU17_PS);
   fChain->SetBranchAddress("HLT_MU40", &HLT_MU40, &b_HLT_MU40);
   fChain->SetBranchAddress("HLT_MU40_PS", &HLT_MU40_PS, &b_HLT_MU40_PS);
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
   fChain->SetBranchAddress("MuIsGlobal", &MuIsGlobal, &b_MuIsGlobal);
   fChain->SetBranchAddress("MuIsPF", &MuIsPF, &b_MuIsPF);
   fChain->SetBranchAddress("MuChi2", &MuChi2, &b_MuChi2);
   fChain->SetBranchAddress("MuChamberHits", &MuChamberHits, &b_MuChamberHits);
   fChain->SetBranchAddress("MuMatchedStations", &MuMatchedStations, &b_MuMatchedStations);
   fChain->SetBranchAddress("MuDz", &MuDz, &b_MuDz);
   fChain->SetBranchAddress("MuPixelHits", &MuPixelHits, &b_MuPixelHits);
   fChain->SetBranchAddress("MuNLayers", &MuNLayers, &b_MuNLayers);
   fChain->SetBranchAddress("MuIsVeto", &MuIsVeto, &b_MuIsVeto);
   fChain->SetBranchAddress("MuIsLoose", &MuIsLoose, &b_MuIsLoose);
   fChain->SetBranchAddress("MuIsTight", &MuIsTight, &b_MuIsTight);
   fChain->SetBranchAddress("ElPt", &ElPt, &b_ElPt);
   fChain->SetBranchAddress("ElEta", &ElEta, &b_ElEta);
   fChain->SetBranchAddress("ElPhi", &ElPhi, &b_ElPhi);
   fChain->SetBranchAddress("ElCharge", &ElCharge, &b_ElCharge);
   fChain->SetBranchAddress("ElPFIso", &ElPFIso, &b_ElPFIso);
   fChain->SetBranchAddress("ElD0", &ElD0, &b_ElD0);
   fChain->SetBranchAddress("ElIsVeto", &ElIsVeto, &b_ElIsVeto);
   fChain->SetBranchAddress("ElIsLoose", &ElIsLoose, &b_ElIsLoose);
   fChain->SetBranchAddress("ElIsTight", &ElIsTight, &b_ElIsTight);
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
