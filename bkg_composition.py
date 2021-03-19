import ROOT
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt 
import squarify
import numpy as np
# plt.style.use('ggplot')
eras = ["2016","2017","2018"]
channels = ["et","mt","tt"]

processes = {
    "TTT": {
        "histos": ["TTT"],
        "color": "#d876d8",
        "label": r"$t\bar{t} \ (\tau\tau)$"
    },
    "TTL": {
        "histos": ["TTL"],
        "color": "#9999CC",
        "label": r"$t\bar{t} \ (\ell\tau)$"
    },
    "TTJ": {
        "histos": ["TTJ"],
        "color": "#2b172b",
        "label": r"$t\bar{t} \ (\rm{jet})$"
    },
    "Z": {
        "histos": ["ZTT","ZJ"],
        "color": "#FFCC66",
        "label": r"$Z \ (\tau\tau)$"
        },
    "ZL": {
        "histos": ["ZL"],
        "color": "#4496C8",
        "label": r"$Z \ (\ell\ell)$"
        },
    "W": {
        "histos": ["W"],
        "color": "#DE5A6A",
        "label": r"W+jets"
        },
    "VVT": {
        "histos": ["VVT"],
        "color": "#39171b",
        "label": r"Diboson $(\tau\tau)$"
        },
    "VVL": {
        "histos": ["VVL","VVJ"],
        "color": "#6F2D35",
        "label": r"Diboson $(\ell\tau)$"
        },
    "QCD": {
        "histos": ["QCD"],
        "color": "#FFCCFF",
        "label": r"QCD"
        },
    "Higgs": {
        "histos": ["ggH125","qqH125","ttH125"],
        "color": "#043927",
        "label": r"Single h"
        }
}


channel_dict = {
    "tt": "$\\tau_h\\tau_h$",
    "et": "$e\\tau_h$",
    "mt": "$\mu\\tau_h$"
}

yields = {}
signalyield = [0.,0.,0.]
for c,channel in enumerate(channels):
    for era in eras:
        filename = "output/shapes/{era}_{channel}_eventWeight/{era}-{era}_{channel}_eventWeight-{channel}-shapes.root".format(era=era,channel=channel)
        file_ = ROOT.TFile(filename) 
        histname = "#{channel}#{channel}_eventWeight#{p}#smhtt#Run{era}#eventWeight#125#".format(era=era,channel=channel,p="NMSSM_500_125_100")
        hist = file_.Get(histname)
        signalyield[c] += 0.11729400*hist.Integral()
        print signalyield[c]
for channel in channels:
    yields[channel] = {}
    for era in eras:
        yields[channel][era] = {}
        filename = "output/shapes/{era}_{channel}_eventWeight/{era}-{era}_{channel}_eventWeight-{channel}-shapes.root".format(era=era,channel=channel)
        file_ = ROOT.TFile(filename)
        labels = []
        colors = []
        sizes = []
        for process in processes.keys():
            labels.append(processes[process]["label"])
            colors.append(processes[process]["color"])
            yield_ = 0.0
            for p in processes[process]["histos"]:
                histname = "#{channel}#{channel}_eventWeight#{p}#smhtt#Run{era}#eventWeight#125#".format(era=era,channel=channel,p=p)
                hist = file_.Get(histname)
                yield_ += hist.Integral()
            yields[channel][era][process] = yield_
            sizes.append(yield_)
        fig = plt.figure(figsize=(8,6))
        colors = [x for _,x in sorted(zip(sizes,colors))]
        labels = [x for _,x in sorted(zip(sizes,labels))]
        sum_ = sum(sizes)
        sizes = [x/sum_ for x in sizes]
        sizes = sorted(sizes)

        # ax = fig.add_subplot(111, aspect="equal")
        plt.barh(y=range(len(sizes)),width=sizes,height=0.8,color=colors,tick_label=labels)
        plt.title(r"{}".format(channel_dict[channel]),loc="left")
        for i in range(len(labels)):
            label = labels[i] 
            if "ell" in label:
                text = r"Simulation"
            elif "QCD" in label or "W" in label or "jet" in label:
                text = r"$F_{\rm{F}}$-method"
            else:
                text = r"$\tau$-embedding"
            plt.text(0.301,i-0.1,text,alpha=0.5)
        plt.xticks([0.1,0.2,0.3,0.4,0.5],["10%","20%","30%","40%","50%"])
        # squarify.plot(sizes=[yields[channel][era][p] for p in yields[channel][era].keys()], label=[processes[p]["label"] for p in processes.keys()], color=[processes[p]["color"] for p in processes.keys()] , alpha=0.8, ax=ax, pad=False)
        # plt.axis('off') 
        # ax.set_xticks([])
        # ax.set_yticks([])
        # plt.title(channel)
        plt.savefig("{era}_{channel}.png".format(era=era,channel=channel))
        plt.savefig("{era}_{channel}.pdf".format(era=era,channel=channel))
        plt.clf()

totalevents = []
sizes_mt_et = [0.]*len(processes.keys())

for channel in channels:
        yields[channel]["cmb"] = {}
        labels = []
        colors = []
        sizes = []
        for process in processes.keys():
            labels.append(processes[process]["label"])
            colors.append(processes[process]["color"])
            yields[channel]["cmb"][process] = 0.0
            for era in eras:
                yields[channel]["cmb"][process] += yields[channel][era][process]
            sizes.append(yields[channel]["cmb"][process])
        # squarify.plot(sizes=[yields[channel]["cmb"][p] for p in yields[channel]["cmb"].keys()], label=[processes[p]["label"] for p in processes.keys()], color=[processes[p]["color"] for p in processes.keys()] , alpha=0.8)
        # plt.axis('off')
        # plt.title(channel)
        fig = plt.figure(figsize=(8,6))
        colors = [x for _,x in sorted(zip(sizes,colors))]
        labels = [x for _,x in sorted(zip(sizes,labels))]
        sizes = sorted(sizes)
        if channel in ["mt","et"]:
            for s in range(len(sizes_mt_et)):
                sizes_mt_et[s] += sizes[s]
                labels_mt_et = labels
                colors_mt_et = colors

        sum_ = sum(sizes)
        totalevents.append(sum_)
        sizes = [x/sum_ for x in sizes]

	print sizes
	print labels
        # ax = fig.add_subplot(111, aspect="equal")
        plt.barh(y=range(len(sizes)),width=sizes,height=0.8,color=colors,tick_label=labels)
        plt.title(r"{}".format(channel_dict[channel]),loc="left")
        sim,ff,emb = 0.0,0.0,0.0
        for i in range(len(labels)):
            label = labels[i] 
            if "ell" in label or "Single" in label:
                text = r"Simulation"
                sim += sizes[i]
            elif "QCD" in label or "W" in label or "jet" in label:
                text = r"$F_{\rm{F}}$-method"
                ff += sizes[i]
            else:
                text = r"$\tau$-embedding"
                emb += sizes[i]
        
            plt.text(0.301,i-0.1,text,alpha=0.5)
        print channel
        print sim,emb,ff
        plt.xticks([0.1,0.2,0.3,0.4,0.5],["10%","20%","30%","40%","50%"])
        plt.xlim(0.0,0.57)
        plt.subplots_adjust(left=0.15, bottom=0.1, right=0.95, top=0.9)
        plt.savefig("{era}_{channel}.png".format(era="cmb",channel=channel))
        plt.savefig("{era}_{channel}.pdf".format(era="cmb",channel=channel))
        plt.clf()

sizes_mt_et = [x/(totalevents[0]+totalevents[1]) for x in sizes_mt_et]
plt.barh(y=range(len(sizes_mt_et)),width=sizes_mt_et,height=0.8,color=colors_mt_et,tick_label=labels_mt_et)
for i in range(len(labels_mt_et)):
    label = labels_mt_et[i] 
    if "ell" in label or "Single" in label:
        text = r"Simulation"
        sim += sizes[i]
    elif "QCD" in label or "W" in label or "jet" in label:
        text = r"$F_{\rm{F}}$-method"
        ff += sizes[i]
    else:
        text = r"$\tau$-embedding"
        emb += sizes[i]

    plt.text(0.301,i-0.1,text,alpha=0.5)

plt.xticks([0.1,0.2,0.3,0.4,0.5],["10%","20%","30%","40%","50%"])
plt.xlim(0.0,0.57)
plt.title(r"$e\tau_h$ + $\mu\tau_h$",loc="left")
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.95, top=0.9)
plt.savefig("cmb_et_mt.png".format(era="cmb",channel=channel))
plt.savefig("cmb_et_mt.pdf".format(era="cmb",channel=channel))
print "here"
plt.clf()

soverb = np.array(signalyield)/np.sqrt( np.array(signalyield)+np.array(totalevents))
print signalyield
print totalevents

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

print soverb 
ax1.bar([1,2,3],height=[n/1000. for n in totalevents],color="#708090")
ax1.tick_params(axis='y', labelcolor="#708090")
ax2.scatter(x=[1,2,3],y=soverb,color="#E89B68",marker="X",s=200)
ax2.tick_params(axis='y', labelcolor="#E89B68")


ax1.set_ylabel("Total number of expected bkg. events / 1000")
ax2.set_ylabel(r"Max. allowed $S/\sqrt{S+B}$ (example mass point)")
ax1.set_xticks([1,2,3])
ax1.set_xticklabels([r"$e\tau_h$",r"$\mu\tau_h$",r"$\tau_h\tau_h$"])

fig.tight_layout()
fig.savefig("eventyield.png")
fig.savefig("eventyield.pdf")