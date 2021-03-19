import ROOT
from copy import deepcopy
import numpy as np
import sys

category = sys.argv[2]
channel = sys.argv[1]
training_mass = sys.argv[3]
training_batch = sys.argv[4]
lm = sys.argv[5]

basehists = []

print channel
hists = {}

for process in ["data_obs","EMB","ZL","VVL","jetFakes","NMSSM_{training_mass}_125_{lm}".format(training_mass=training_mass,lm=lm),"TTL","HTT","TotalBkg","TotalSig", "Other"]:
        
        
    binning = []
    hists[process] = []
    first = True
    i_hist=0

    for era in ["2016","2017","2018"]:
        for channel in [channel]: #,"et","tt"]:
            basepath = "output_{era}_{channel}_{training_mass}_{training_batch}_nmssm_{training_mass}_{lm}/{era}/cmb/postfitshape.root".format(era=era,channel=channel,training_mass=training_mass,training_batch=training_batch,lm=lm)
            dir_ = "htt_{channel}_{cat}_{era}_postfit".format(era=era,cat=category,channel=channel)
            rfile = ROOT.TFile(basepath,"READ")
            dir_test = rfile.Get("{}".format(dir_))
            if (process in [x.GetName() for x in dir_test.GetListOfKeys()]):
                hists[process].append(deepcopy(rfile.Get("{}/{}".format(dir_,process))))
            else:
                hists[process].append(deepcopy(rfile.Get("{}/{}".format(dir_,"data_obs"))))
                hists[process][-1].Scale(0.0)
                hists[process][-1].SetName(process)
                hists[process][-1].SetTitle(process)

            if process == "data_obs":
                if first:
                    best_binning =  set([round(hists[process][-1].GetBinLowEdge(i),4) for i in range(1,hists[process][-1].GetNbinsX()+2)])
                    first = False
                else:
                    best_binning = set([round(hists[process][-1].GetBinLowEdge(i),4) for i in range(1,hists[process][-1].GetNbinsX()+2)]).intersection(best_binning)
            i_hist+=1

    rfile.Close()
del rfile
newfile = ROOT.TFile("newfile_{training_mass}_{lm}_postfit_{channel}_{cat}.root".format(channel=channel,cat=category,training_mass=training_mass,lm=lm),"RECREATE")
newfile.cd()
binning  = np.array(sorted(list(best_binning)))

for process in ["data_obs","EMB","ZL","VVL","jetFakes","NMSSM_{training_mass}_125_{lm}".format(training_mass=training_mass,lm=lm),"TTL","HTT","TotalBkg","TotalSig", "Other"]:

    hists_rebinned = []
    for x in hists[process]:
        print "before: ",[x.GetBinLowEdge(b) for b in range(1,x.GetNbinsX()+2)]
        print "after : ",sorted(list(best_binning))
        tmp_hist = x.Rebin(len(binning)-1,x.GetName(),binning)
        hists_rebinned.append(deepcopy(tmp_hist))
        del tmp_hist
    basehists.append(hists_rebinned[0].Clone(process))
    basehists[-1].Add(hists_rebinned[0],-1)
    for hist in hists_rebinned:
        basehists[-1].Add(hist)
        del hist
    del hists_rebinned

    basehists[-1].Write()

newfile.Write()

newfile.Close()
