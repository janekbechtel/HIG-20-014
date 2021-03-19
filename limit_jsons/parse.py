import json,sys

mass = sys.argv[1]

with open("nmssm_combined_all_{}_cmb.json".format(mass),"r") as jsonfile:
    dict_ = json.load(jsonfile)

minimum_exp = 1000.
exp_mass = 0.
minimum_obs = 1000.
obs_mass = 0.
for key in dict_:
    if dict_[key]["exp0"] < minimum_exp:
        minimum_exp = dict_[key]["exp0"]
        exp_mass = key
    if dict_[key]["obs"] < minimum_obs:
        minimum_obs = dict_[key]["obs"]
        obs_mass = key
print exp_mass
print minimum_exp
print obs_mass
print minimum_obs



    
	


