import ROOT, math


def divWithErr(a, ae, b, be):
	central = a/b
	relerr_a = ae/a
	relerr_b = be/b
	relerr_tot = relerr_a + relerr_b
	return central, central*relerr_tot

class cat:
	def __init__(self, name):
		self.name = name
	nttc , ntlc , nltc , nllc = 0  , 0  , 0  , 0
	ntt  , ntl  , nlt  , nll  = 0. , 0. , 0. , 0.
	npp  , npf  , nfp  , nff  = 0  , 0  , 0  , 0
	ntt2 , ntl2 , nlt2 , nll2 = 0. , 0. , 0. , 0.
	npp2 , npf2 , nfp2 , nff2 = 0  , 0  , 0  , 0
	def __add__(self, other):
		self.nttc = self.nttc + other.nttc ; self.ntlc = self.ntlc + other.ntlc ; self.nltc = self.nltc + other.nltc ; self.nllc = self.nllc + other.nllc
		self.ntt  = self.ntt  + other.ntt  ; self.ntl  = self.ntl  + other.ntl  ; self.nlt  = self.nlt  + other.nlt  ; self.nll  = self.nll  + other.nll 
		self.npp  = self.npp  + other.npp  ; self.npf  = self.npf  + other.npf  ; self.nfp  = self.nfp  + other.nfp  ; self.nff  = self.nff  + other.nff 
		self.ntt2 = self.ntt2 + other.ntt2 ; self.ntl2 = self.ntl2 + other.ntl2 ; self.nlt2 = self.nlt2 + other.nlt2 ; self.nll2 = self.nll2 + other.nll2
		self.npp2 = self.npp2 + other.npp2 ; self.npf2 = self.npf2 + other.npf2 ; self.nfp2 = self.nfp2 + other.nfp2 ; self.nff2 = self.nff2 + other.nff2
		return self
	def __iadd__(self, other):
		self.nttc = self.nttc + other.nttc ; self.ntlc = self.ntlc + other.ntlc ; self.nltc = self.nltc + other.nltc ; self.nllc = self.nllc + other.nllc
		self.ntt  = self.ntt  + other.ntt  ; self.ntl  = self.ntl  + other.ntl  ; self.nlt  = self.nlt  + other.nlt  ; self.nll  = self.nll  + other.nll 
		self.npp  = self.npp  + other.npp  ; self.npf  = self.npf  + other.npf  ; self.nfp  = self.nfp  + other.nfp  ; self.nff  = self.nff  + other.nff 
		self.ntt2 = self.ntt2 + other.ntt2 ; self.ntl2 = self.ntl2 + other.ntl2 ; self.nlt2 = self.nlt2 + other.nlt2 ; self.nll2 = self.nll2 + other.nll2
		self.npp2 = self.npp2 + other.npp2 ; self.npf2 = self.npf2 + other.npf2 ; self.nfp2 = self.nfp2 + other.nfp2 ; self.nff2 = self.nff2 + other.nff2
		return self

class sample:
	def __init__(self, name, file):
		self.name = name
		self.file = ROOT.TFile(file)
		#self.tree = ROOT.TFile(file).Get('closureTree')
		self.tree = self.file.Get('closureTree')
		self.mm = cat('MUON-MUON')
		self.em = cat('MUON-ELECTRON')
		self.ee = cat('ELECTRON-ELECTRON')
		self.cats = [self.mm, self.em, self.ee]
		self.number = 0
	def __iadd__(self, other):
		self.mm = self.mm + other.mm
		self.em = self.em + other.em
		self.ee = self.ee + other.ee
		return self
	def __add__(self, other):
		self.mm = self.mm + other.mm
		self.em = self.em + other.em
		self.ee = self.ee + other.ee
		return self
