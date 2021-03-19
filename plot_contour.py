import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import ROOT 
import copy
from scipy import interpolate
import CombineHarvester.CombineTools.plotting as plot 

col_store = []
def CreateTransparentColor(color, alpha):
  adapt   = ROOT.gROOT.GetColor(color)
  new_idx = ROOT.gROOT.GetListOfColors().GetSize() + 1
  trans = ROOT.TColor(new_idx, adapt.GetRed(), adapt.GetGreen(), adapt.GetBlue(), '', alpha)
  col_store.append(trans)
  trans.SetName('userColor%i' % new_idx)
  return new_idx


theory_file=ROOT.TFile("HXSG_NMSSM_recommendations_00.root","READ")
theory_graph = theory_file.Get("g_bbtautau")

era = "combined"
channel = "all"
mass_dict = {
    "heavy_mass": [400, 450, 500, 550, 600, 700, 800, 900, 1000], #, 1200, 1400, 1600, 1800, 2000, 2500, 3000],
    "light_mass_coarse": [60, 70, 80, 90, 100, 120, 150, 170, 190, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1600, 1800, 2000, 2200, 2400, 2600, 2800],
    "light_mass_fine": [60, 70, 75, 80, 85, 90, 95, 100, 110, 120, 130, 150, 170, 190, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850],
}

json_file = "limit_jsons/nmssm_combined_all_1000_cmb.json"
exp_dict = {}
obs_dict = {}
up_dict = {}
down_dict = {}
up2_dict = {}
down2_dict = {}
for mass in mass_dict["heavy_mass"]:
    theory_diff_value = theory_graph.Eval(mass)
    json_file = "limit_jsons/nmssm_{}_{}_{}_cmb.json".format(era,channel,mass)
    with open(json_file,"r") as read_file:
        temp_dict = json.load(read_file)
    exp_dict[mass] = {}
    obs_dict[mass] = {}
    up_dict[mass] = {}
    down_dict[mass] = {}
    up2_dict[mass] = {}
    down2_dict[mass] = {}

    for key in temp_dict:
        exp_dict[mass][key] = temp_dict[key]["exp0"]/theory_diff_value
        obs_dict[mass][key] = temp_dict[key]["obs"]/theory_diff_value
        down_dict[mass][key] = temp_dict[key]["exp-1"]/theory_diff_value
        up_dict[mass][key] = temp_dict[key]["exp+1"]/theory_diff_value
        down2_dict[mass][key] = temp_dict[key]["exp-2"]/theory_diff_value
        up2_dict[mass][key] = temp_dict[key]["exp+2"]/theory_diff_value


x = mass_dict["heavy_mass"]
y = [-10] * len(x)
y_obs = [-500] * len(x)
y_up = [-10] * len(x)
y_down = [-10] * len(x)
y_up2 = [-10] * len(x)
y_down2 = [-10] * len(x)
y_probed = [-10] * len(x)

y_obs2 = [-10] * len(x)
y_obs5 = [-10] * len(x)
y_obs10 = [-10] * len(x)


for i,mass in enumerate(x):
    light_masses = [float(lm) for lm in exp_dict[mass]]
    y_probed[i] = np.max(light_masses)
    light_masses.sort()

    for lm in light_masses:
        if exp_dict[mass][str(lm)] < 1.0:
            y[i] = lm
        if obs_dict[mass][str(lm)] < 1.0:
            y_obs[i] = lm
        if obs_dict[mass][str(lm)] < 2.0:
            y_obs2[i] = lm
        if exp_dict[mass][str(lm)] < 2.95742382575:
            y_obs5[i] = lm
        if obs_dict[mass][str(lm)] < 10.0:
            y_obs10[i] = lm
        if up_dict[mass][str(lm)] < 1.0:
            y_up[i] = lm
        if down_dict[mass][str(lm)] < 1.0:
            y_down[i] = lm
        if up2_dict[mass][str(lm)] < 1.0:
            y_up2[i] = lm
        if down2_dict[mass][str(lm)] < 1.0:
            y_down2[i] = lm
# unphysical (too small) uncertainies for low masses due to coarse granularity, reset to next mass value
y_down2[1] = 250.
y_down[1] = 210.
y_down2[0] = 190.
x_new = np.linspace(np.min(x)-1, np.max(x), 1000)
a_BSpline = interpolate.make_interp_spline(x, y)
y_new = a_BSpline(x_new)
a_BSpline_obs = interpolate.make_interp_spline(x, y_obs)
y_new_obs = a_BSpline_obs(x_new)
a_BSpline_obs2 = interpolate.make_interp_spline(x, y_obs2)
y_new_obs2 = a_BSpline_obs2(x_new)
a_BSpline_obs5 = interpolate.make_interp_spline(x, y_obs5)
y_new_obs5 = a_BSpline_obs5(x_new)
a_BSpline_obs10 = interpolate.make_interp_spline(x, y_obs10)
y_new_obs10 = a_BSpline_obs10(x_new)
a_BSpline_up = interpolate.make_interp_spline(x, y_up)
y_new_up = a_BSpline_up(x_new)
a_BSpline_down = interpolate.make_interp_spline(x, y_down)
y_new_down = a_BSpline_down(x_new)
a_BSpline_up2 = interpolate.make_interp_spline(x, y_up2)
y_new_up2 = a_BSpline_up2(x_new)
a_BSpline_down2 = interpolate.make_interp_spline(x, y_down2)
y_new_down2 = a_BSpline_down2(x_new)
a_BSpline_probed = interpolate.make_interp_spline(x, y_probed)
y_new_probed = a_BSpline_probed(x_new)


y_probed2 = np.array([entry-125 for entry in x_new])

for i in range(len(y_new_probed)):
    if x_new[i]<500:
        if abs(y_new_obs10[i]-y_new_probed[i])<20.:
            y_new_obs10[i] = y_new_probed[i]
        if abs(y_new_obs5[i]-y_new_probed[i])<20.:
            y_new_obs5[i] = y_new_probed[i]



zeros=False
for i in range(len(x_new)):
    if y_new[i] < 0.0 or zeros:
        y_new[i] = -0.1
        zeros = True
zeros=False
for i in range(len(x_new)):
    if y_new_up2[i] < 0.0 or zeros:
        y_new_up2[i] = -0.1
        zeros = True
zeros=False
for i in range(len(x_new)):
    if y_new_up[i] < 0.0 or zeros:
        y_new_up[i] = -0.1
        zeros = True
zeros=False
for i in range(len(x_new)):
    if y_new_down[i] < 0.0 or zeros:
        y_new_down[i] = -0.1
        zeros = True
zeros=False
for i in range(len(x_new)):
    if y_new_down2[i] < 0.0 or zeros:
        y_new_down2[i] = -0.1
        zeros = True
zeros=False
for i in range(len(x_new)):
    if y_new_obs[i] < 0.0 or zeros:
        y_new_obs[i] = -0.1
        zeros = True
    # if x_new[i]>600 and y_new_obs[i]>0.0:
    #     print 1-(x_new[i]-600.)*(1./100.)
    #     y_new_obs[i] *= 1-(x_new[i]-600.)*(1./100.)
y_new_up2[0] = 0
y_new_up2[-1] = 0
y_new_up[0] = 0
y_new_up[-1] = 0
y_new[0] = 0.
y_new[-1] = 0.
y_new_obs[0] = 0.
y_new_obs[-1] = 0.

y_new_down2[0] = 0.
y_new_down2[-1] = 0.
y_new_down[0] = 0.
y_new_down[-1] = 0.

excluded = np.array([400.]*len(x_new))
excluded[0] = 0.
excluded[-1] = 0.
y_probed2[0] = 0.
y_probed2[-1] = 0.
graph_excluded = ROOT.TGraph(len(x_new),x_new,excluded)
graph_excluded2 = ROOT.TGraph(len(x_new),x_new,y_probed2)

graph_obs = ROOT.TGraph(len(x_new),x_new,y_new_obs)
graph_exp = ROOT.TGraph(len(x_new),x_new,y_new)
graph_p2 = ROOT.TGraph(len(x_new),x_new,y_new_up2)
graph_p1 = ROOT.TGraph(len(x_new),x_new,y_new_up)
graph_m2 = ROOT.TGraph(len(x_new),x_new,y_new_down2)
graph_m1 = ROOT.TGraph(len(x_new),x_new,y_new_down)

c1=ROOT.TCanvas("c","c",800,600)
# c1.SetLogy()
# c1.SetLogx()
x_axis = graph_excluded.GetXaxis()
x_axis.SetLimits(400.,700.)
graph_excluded.GetHistogram().SetMaximum(399.)
graph_excluded.GetHistogram().SetMinimum(60.)
graph_excluded.GetXaxis().SetTitle("#scale[1.4]{Heavy mass m_{H} (GeV)}")
graph_excluded.GetYaxis().SetTitle("#scale[1.4]{Light mass m_{h_{S}} (GeV)}")
graph_excluded.GetXaxis().SetTitleOffset(1.2)
graph_excluded.GetYaxis().SetTitleOffset(1.2)
graph_excluded.SetTitle("")

graph_obs.SetFillColor(CreateTransparentColor(ROOT.kAzure+6,0.5))
graph_p2.SetFillColor(ROOT.kWhite)
graph_p1.SetFillColor(ROOT.kGray+1)
graph_m2.SetFillColor(ROOT.kGray+1)
graph_m1.SetFillColor(ROOT.kGray+2)
graph_exp.SetFillColor(100)
graph_obs.SetFillStyle(1001)
graph_p2.SetFillStyle(1001)
graph_p1.SetFillStyle(1001)
graph_m2.SetFillStyle(1001)
graph_m1.SetFillStyle(1001)
graph_p2.SetLineColor(0)
graph_p1.SetLineColor(0)
graph_m2.SetLineColor(0)
graph_m1.SetLineColor(0)

graph_exp.SetLineColor(ROOT.kBlack)
graph_exp.SetLineWidth(2)
graph_exp.SetLineStyle(2)
graph_obs.SetLineColor(ROOT.kBlack)
graph_obs.SetLineWidth(2)
graph_obs.SetMarkerStyle(20)
graph_obs.SetMarkerSize(1.0)
graph_obs.SetMarkerColor(ROOT.kBlack)

graph_excluded.SetFillStyle(3354)
graph_excluded.SetFillColor(46)
graph_excluded.SetLineColor(46)
graph_excluded.SetLineWidth(2)
graph_excluded2.SetLineColor(46)
graph_excluded2.SetLineWidth(2)

graph_excluded2.SetFillColor(ROOT.kWhite)

graph_excluded.Draw("AF")
graph_excluded2.Draw("FL SAME")

graph_m2.Draw(" F SAME ")
graph_m1.Draw(" F SAME ")
graph_p1.Draw(" F SAME ")
graph_p2.Draw(" F SAME  ")

graph_exp.Draw(" L SAME ")
graph_obs.Draw(" FL SAME ")

legend = ROOT.TLegend(0.6,0.5,0.85,0.725)
legend.SetBorderSize(0)
legend.AddEntry(graph_obs,"Observed","F")
legend.AddEntry(graph_exp,"Expected","L")
legend.AddEntry(graph_m1,"68% expected","F")
legend.AddEntry(graph_m2,"95% expected","F")
legend.AddEntry(graph_excluded,"m_{h}+m_{h_{S}} > m_{H}","F")
legend.Draw("SAME")
plot.DrawCMSLogo(c1, 'CMS', "Preliminary", 3, 0.045, 0.035, 1.2, '', 0.6)
# plot.DrawTitle(c1,"               #splitline{95% CL exclusion on maximally allowed}{cross section times branching fractions in NMSSM}",1,0.3,0.35)
plot.DrawTitle(c1, "#scale[0.8]{137 fb^{-1} (13 TeV)}", 3)

text = ROOT.TText(0.35,0.8,"95% CL exclusion on maximally allowed")
text2 = ROOT.TText(0.35,0.755,"cross section times branching fractions in NMSSM")
text.SetNDC()
text.SetTextFont(42)
# text.SetFillColor(0)
text.SetTextSize(0.036)
text.Draw("SAME")
text2.SetNDC()
text2.SetTextFont(42)
text2.SetTextSize(0.036)

text2.Draw("SAME")
c1.RedrawAxis()
c1.SaveAs("plots/contour_cms.pdf")
c1.SaveAs("plots/contour_cms.png")



# file_ = ROOT.TFile("contour.root","RECREATE")
# file_.cd()
# graph_obs.SetName("obs")
# graph_exp.SetName("exp0")
# graph_p2.SetName("exp+2")
# graph_p1.SetName("exp+1")
# graph_m2.SetName("exp-2")
# graph_m1.SetName("exp-1")
# graph_obs.Write()
# graph_exp.Write()
# graph_p2.Write()
# graph_p1.Write()
# graph_m2.Write()
# graph_m1.Write()

# file_.Write()

"""

fig, ax = plt.subplots(1,1,figsize=(9,6),sharex=True, sharey=True)
ax.fill_between(x_new,[0.]*len(x_new),y_new_obs,color="#5B84B1",edgecolor="#4d4d4d",label="Observed",alpha=0.5)
# ax.fill_between(x_new,y_new_obs,y_new_obs2,color="#EDA62B",label="Observed within factor 2 of NMSSM",alpha=0.5)
# ax.fill_between(x_new,y_new_obs,y_new_obs5,color="#EDA62B",label="Expected for Run-III",alpha=0.5)
# ax.fill_between(x_new,y_new_obs5,y_new_obs10,color="#91B051",label="Observed within factor 10 of NMSSM",alpha=0.5)

# ax.fill_between(x_new,y_new_probed,[850.]*len(x_new),color="#CF5E61",label="Not part of analysis",alpha=0.5)

ax.fill_between(x_new,y_new_up,y_new_down,color="#A9A9A9",label="68% expected",alpha=0.45)
# ax.plot(x_new,y_new_down,color="#4d4d4d",linestyle="dashdot",label="68% expected")
# ax.plot(x_new,y_new_up,color="#4d4d4d",linestyle="dashdot")

ax.fill_between(x_new,y_new_up2,y_new_down2,color="#DCDCDC",label="95% expected",alpha=0.45)
# ax.plot(x_new,y_new_down2,color="#4d4d4d",linestyle="dotted",label="95% expected")
# ax.plot(x_new,y_new_up2,color="#4d4d4d",linestyle="dotted")
ax.plot(x_new,y_new,color="#4d4d4d",label="Expected",linestyle="dashed")
# ax.plot(x_new,y_new_obs,color="#4d4d4d")
# ax.plot(x_new,y_probed2,color="#CF5E61",label=r"$\rm{m}(\rm{h}_{\rm{S}})+\rm{m}(\rm{h}_{\rm{SM}})>\rm{m}(\rm{H})$")
ax.fill_between(x_new,y_new_probed,[790.]*len(x_new),facecolor="none", hatch="/", edgecolor="#CF5E61",linewidth=0.0)
ax.plot(x_new,y_new_probed,color="#CF5E61",label=r"$\rm{m}(\rm{h}_{\rm{S}})+\rm{m}(\rm{h}_{\rm{SM}})>\rm{m}(\rm{H})$")

# ax.text(720,400,"95% CL exclusion on maximally")
# ax.text(720,358,"allowed cross section times")
# ax.text(720,320,"branching fractions in NMSSM")
# ax.plot(x,y,"+")
ax.text(410.,990.,"95% CL exclusion on maximally allowed cross section times branching fractions in NMSSM")
# ax.text(720,358,"")
# ax.text(720,320,"")
ax.set_ylim(60.,790.)
ax.set_xlim(400,690.)
ax.set_xscale('log')
ax.set_yscale('log')
ax.legend(loc="upper left")#,bbox_to_anchor=(0.311, 0.311))
handles, labels = plt.gca().get_legend_handles_labels()
order = [0,3,4,2,1]
ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc="upper left",framealpha=1.0)
ax.set_ylabel(r'Light mass $\rm{m}(\rm{h}_{\rm{S}})$ (GeV)')
ax.set_xlabel(r'Heavy mass $\rm{m}(\rm{H})$ (GeV)')
ax.yaxis.set_label_coords(-0.09,0.8)
ax.xaxis.set_label_coords(0.88,-0.09)
ax.set_xticks([],[])
ax.set_xticklabels([])
ax.set_xticks([400,500,600,700])
ax.set_xticklabels(["400","500","600","700"])
plt.tick_params(
    axis='x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom=True,      # ticks along the bottom edge are off
    top=False,         # ticks along the top edge are off
    labelbottom=False) # labels along the bottom edge are off
# ax.set_xticks([], []) 
ax.text(396.,53.,"400")
ax.text(494.,53.,"500")
ax.text(592.,53.,"600")
ax.text(690.,53.,"700")
ax.set_yticks([],[])

ax.set_yticks([60,100,200,300])
ax.set_yticklabels([60,100,200,300])

ax.set_title(r'$e\tau_{h}+\mu\tau_{h}+\tau_{h}\tau_{h}$',loc="left")
ax.set_title(r'$\bf{CMS}$ data, 137.2 $\rm{fb}^{-1}$ (13 TeV)',loc="right")

fig.savefig("plots/contour.pdf")
fig.savefig("plots/contour.png")
"""
