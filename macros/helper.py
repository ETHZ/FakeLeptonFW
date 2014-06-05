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
	nttc, ntlc, nltc, nllc = 0 , 0 , 0 , 0
	ntt, ntl, nlt, nll     = 0., 0., 0., 0.
	npp, npf, nfp, nff     = 0 , 0 , 0 , 0
	ntt2, ntl2, nlt2, nll2     = 0., 0., 0., 0.
	npp2, npf2, nfp2, nff2     = 0 , 0 , 0 , 0

class sample:
	def __init__(self, name, file):
		self.name = name
		self.file = file
		self.tree = ROOT.TFile(file).Get('closureTree')
	mm = cat('MUON-MUON')
	em = cat('MUON-ELECTRON')
	ee = cat('ELECTRON-ELECTRON')
	cats = [mm, em, ee]
