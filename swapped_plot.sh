#!/bin/bash

source utils/setup_cmssw.sh
mkdir plots/limits/${ERA}/${CHANNEL} -p

       
python CMSSW_10_2_16_UL/src/CombineHarvester/MSSMvsSMRun2Legacy/scripts/plotMSSMLimits_swapped.py limit_jsons/swapped_nmssm_combined_all_120.json --title-right "137 fb^{-1} (13 TeV)" --y-axis-min 0.0001 --y-axis-max 500.0  --show exp,obs  --output plots/limits/swapped_120 --logy --process "nmssm" --title-left "all   m^{}_{h_{S}}=120 GeV" --xmax 3001.0 --mass -1  --logx  
