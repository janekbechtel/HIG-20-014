#!/bin/bash
ERA=combined
CHANNEL=all

source utils/setup_cmssw.sh
mkdir plots/limits/${ERA}/${CHANNEL} -p
if [ "$ERA" -eq 2016 ]; then
    ERA_STRING="35.9 fb^{-1} (2016, 13 TeV)"
fi
if [ "$ERA" -eq 2017 ]; then
    ERA_STRING="41.5 fb^{-1} (2017, 13 TeV)"
fi
if [ "$ERA" -eq 2018 ]; then
    ERA_STRING="59.7 fb^{-1} (2018, 13 TeV)"
fi
if [ "$ERA" = "combined" ]; then
    ERA_STRING="137 fb^{-1} (13 TeV)"
fi
JSONFILES=""
for MASS in 240 280 320 360 400 450 500 550 600 700 800 900 1000 1200 1400 1600 1800 2000 2500 3000 
do

    SELECT_JSON=""
    if [ "$MASS" -lt 1001 ]; then
        JSONFILES="${JSONFILES} limit_jsons/nmssm_${ERA}_${CHANNEL}_${MASS}_cmb_scaled.json"
        
    else
        CHECK_JSON=/storage/gridka-nrg/jbechtel/gc_storage/nmssm_limits/2020_12_11/train_all/${ERA}/${CHANNEL}/1200_1/nmssm_${CHANNEL}_1200_1_1200_120_cmb.json
        [ -f "$CHECK_JSON" ] || continue
        SELECT_JSON=""
        JSONFILES="${JSONFILES} limit_jsons/nmssm_${ERA}_${CHANNEL}_${MASS}_cmb_scaled.json"

fi
done
echo $JSONFILES

python CMSSW_10_2_16_UL/src/CombineHarvester/MSSMvsSMRun2Legacy/scripts/plotMSSMLimits_scaled.py $JSONFILES --title-right "$ERA_STRING" --y-axis-min 0.001 --y-axis-max 900000000000000000000000  --show exp,obs  --output plots/limits/${ERA}/${CHANNEL}/nmssm_${ERA}_${CHANNEL} --logy --process "nmssm" --title-left ${CHANNEL} --xmax 9999.0 --mass $MASS  --logx  



