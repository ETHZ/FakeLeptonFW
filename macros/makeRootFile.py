import ROOT, sys

args = sys.argv

n_sets = (len(args)-1)/2

run = [{} for i in range(n_sets)]
URL = [{} for i in range(n_sets)]
names = [{} for i in range(n_sets)]

fn = ['FR_2dmap_data.root', 'FR_2dmap_mc.root', 'FR_2dmap_data-ew_central1.root']
nn  = [{} for i in range(n_sets)]

for i in range(n_sets):
	run[i] = args[i*2+1]
	URL[i] = args[i*2+2]
	names[i] = URL[i].split('/')[-2]
	nn[i] = ['FR_data_' + str(run[i]) + '_pure', 'FR_mc_' + str(run[i]), 'FR_data_' + str(run[i])]

fl = []
fr = []
cv = []
hi = []

for i in range(n_sets):

	fl.append([])
	fr.append([])

	path = 'Plots/' + URL[i] + 'unweighted/fakerates_2d/'

	fl[i] = [path + f for f in fn]
	fr[i] = [ROOT.TFile(f, 'read') for f in fl[i]]


nf = ROOT.TFile('Plots/histos_' + ''.join(names) + '.root', 'recreate')

for i in range(n_sets):

	cv.append([])
	hi.append([])

	cv[i] = [f.Get('c2dFR') for f in fr[i]]
	hi[i] = [c.FindObject('h_FTight') for c in cv[i]]

	for j, hist in enumerate(hi[i]):
		hist.SetName(nn[i][j])
		hist.Write()

nf.Close()


