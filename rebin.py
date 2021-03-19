import ROOT
import argparse
import numpy as np

def parse_arguments():
    parser = argparse.ArgumentParser(
        description=
        "")
    parser.add_argument("input", type=str, help="")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    print args.input
    file_ = ROOT.TFile(args.input,"UPDATE")
    for key in file_.GetListOfKeys():
        print key.GetName()
        hists = file_.Get(key.GetName()).GetListOfKeys()
        file_.cd(key.GetName())
        base_hist = file_.Get(key.GetName()+"/data_obs")
        oldbinning = [base_hist.GetBinLowEdge(i) for i in range(1,base_hist.GetNbinsX()+2)]
        newbinning = np.array([x if (x-0.2)>0.001 else 0.2 for x in oldbinning])
        print oldbinning
        print newbinning
        for histname in hists:

            base_hist = file_.Get(key.GetName()+"/"+histname.GetName())
            temp_hist = ROOT.TH1D(histname.GetName(),histname.GetName(),len(newbinning)-1,newbinning)
            for bin_ in range(1,temp_hist.GetNbinsX()+1):
                temp_hist.SetBinContent(bin_,base_hist.GetBinContent(bin_))
                temp_hist.SetBinError(bin_,base_hist.GetBinError(bin_))

            temp_hist.Write()


    file_.Write()
    file_.Close()
