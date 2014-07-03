import ROOT, sys

args = sys.argv

n_sets = (len(args)-1)/2

run = [{} for i in range(n_sets)]
URL = [{} for i in range(n_sets)]
names = [{} for i in range(n_sets)]
fn  = [{} for i in range(n_sets)]
nn  = [{} for i in range(n_sets)]

for i in range(n_sets):
	run[i] = args[i*2+1]
	URL[i] = args[i*2+2]
	names[i] = URL[i].split('/')[-2]

	fn[i] = ['FR_2dmap_data.root', 'FR_2dmap_mc.root', 'PR_2dmap_mc.root', 'FR_2dmap_datamcsub_central1.root', 'FR_2dmap_qcd.root', 'FR_2dmap_' + str(run[i]) + '_ttbar0.root', 'FR_2dmap_' + str(run[i]) + '_ttbar1.root', 'FR_2dmap_' + str(run[i]) + '_ttbar2.root', 'FR_2dmap_' + str(run[i]) + '_ttbar3.root', 'FR_2dmap_' + str(run[i]) + '_qcd0.root', 'FR_2dmap_' + str(run[i]) + '_qcd1.root', 'FR_2dmap_' + str(run[i]) + '_qcd2.root', 'FR_2dmap_' + str(run[i]) + '_qcd3.root']
	nn[i] = ['FR_data_pure_' + str(run[i]), 'FR_mc_' + str(run[i]), 'PR_mc_' + str(run[i]), 'FR_data_' + str(run[i]), 'FR_qcd_' + str(run[i]), 'FR_ttbar_all_' + str(run[i]), 'FR_ttbar_b_' + str(run[i]), 'FR_ttbar_c_' + str(run[i]), 'FR_ttbar_light_' + str(run[i]), 'FR_qcd_all_' + str(run[i]), 'FR_qcd_b_' + str(run[i]), 'FR_qcd_c_' + str(run[i]), 'FR_qcd_light_' + str(run[i])]


fl = []
fr = []
cv = []
hi = []

for i in range(n_sets):

	fl.append([])
	fr.append([])

	path = 'Plots/' + URL[i] + 'unweighted/fakerates_2dct/'

	fl[i] = [path + f for f in fn[i]]
	fr[i] = [ROOT.TFile(f, 'read') for f in fl[i]]


nf = ROOT.TFile('Closure/histos_' + ''.join(names) + '.root', 'recreate')

for i in range(n_sets):

	cv.append([])
	hi.append([])

	cv[i] = [f.Get('c2dFR') for f in fr[i]]
	hi[i] = [c.FindObject('h_FTight') for c in cv[i]]

	for j, hist in enumerate(hi[i]):
		hist.SetName(nn[i][j])
		hist.Write()

nf.Close()


nf1 = ROOT.TFile('Closure/histos_closuretest.root', 'recreate')

for i in range(n_sets):

	cv.append([])
	hi.append([])

	cv[i] = [f.Get('c2dFR') for f in fr[i]]
	hi[i] = [c.FindObject('h_FTight') for c in cv[i]]

	hi[i][3].SetName(nn[i][3])
	hi[i][3].Write()

nf1.Close()

