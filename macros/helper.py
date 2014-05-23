import ROOT, math


def divWithErr(a, ae, b, be):
	central = a/b
	relerr_a = ae/a
	relerr_b = be/b
	relerr_tot = relerr_a + relerr_b
	return central, central*relerr_tot
