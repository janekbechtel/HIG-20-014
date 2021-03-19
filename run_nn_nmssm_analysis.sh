#!/bin/bash
ERA=$1
CHANNEL=$2

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
    ERA_STRING="137.2 fb^{-1} (13 TeV)"
fi

for MASS in  240 280 320 360 400 450 500 550 600 700 800 900 1000 1200 1400 1600 1800 2000 2500 3000
do
    SELECT_JSON=""
    if [ "$MASS" -lt 1001 ]; then
        plotMSSMLimits.py limit_jsons/nmssm_${ERA}_${CHANNEL}_${MASS}_cmb.json --title-right "$ERA_STRING" --y-axis-min 0.0001 --y-axis-max 500.0  --show exp,obs  --output plots/limits/${ERA}/${CHANNEL}/nmssm_${ERA}_${CHANNEL}_${MASS} --logy --process "nmssm" --title-left ${CHANNEL}"   m_{H} = "${MASS}" GeV" --xmax 800.0  --logx 
    else
        plotMSSMLimits.py limit_jsons/nmssm_${ERA}_${CHANNEL}_${MASS}_cmb.json --title-right "$ERA_STRING"  --y-axis-min 0.0001 --y-axis-max 500.0  --show exp,obs  --output plots/limits/${ERA}/${CHANNEL}/nmssm_${ERA}_${CHANNEL}_${MASS} --logy --process "nmssm" --title-left ${CHANNEL}"   m_{H} = "${MASS}" GeV" --xmax 2800.0  --logx 
fi
done


