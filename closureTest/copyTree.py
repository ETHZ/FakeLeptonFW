import ROOT, os


ld = os.listdir('./')
fl = []


for f in ld:
	if not '_closureOutput.root' in f: continue

	print f

	oldfile = ROOT.TFile(f)
	oldtree = oldfile.Get('closureTree')
	
	
	newname = f.split('.')[0]+'_SS.root'
	
	newfile = ROOT.TFile(newname, 'RECREATE')
	
	newtree = oldtree.CopyTree('type < 3')
	
	newfile.cd()
	newtree.Write()
	newfile.Close()
