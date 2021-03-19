ERA=$1
CHANNEL=$2
VARIABLE=$3
MODE=$4



for ERA in 2018 #2017 2018
do
for CHANNEL in mt #et tt
do
for VARIABLE in mbb_highCSV_bReg kinfit_mH m_vis m_sv_puppi m_ttvisbb_highCSV_bReg  kinfit_mh2
do
python add_hists.py output/${VARIABLE}_2018_mt_500_3_nmssm_500_110/2018/cmb/prefitshape.root --input-hist ggH125 ttH125 VH125 qqH125 --output-hist HTT --mode prefit &&  python plot_nmssm_var.py -v ${VARIABLE} --era Run2018 -c mt --emb --ff --output-dir plots/prefit --shapes output/${VARIABLE}_2018_mt_500_3_nmssm_500_110/2018/cmb/prefitshape.root &
done
done
done
wait


exit


# for STAT only plot:

for ERA in 2018 #2016 2017 2018 #2016 2017
do
for CHANNEL in tt et mt #et mt #et mt tt #tt mt #et
do

for VARIABLE in m_sv_puppi mbb_highCSV_bReg kinfit_mH #pt_1 #kinfit_mH kinfit_chi2 m_sv_puppi mbb_highCSV_bReg #kinfit_chi2 #pt_ttvisbb_highCSV_bReg # kinfit_mH mbb_highCSV_bReg m_sv_puppi #mjj pt_1 pt_2 m_vis ptvis m_sv_puppi jpt_1 njets jdeta mjj dijetpt bpt_bReg_1 bpt_bReg_2 jpt_2 mbb_highCSV_bReg pt_bb_highCSV_bReg m_ttvisbb_highCSV_bReg kinfit_mH kinfit_mh2 kinfit_chi2 nbtag  bm_bReg_1 bm_bReg_2 bcsv_1 bcsv_2 highCSVjetUsedFordiBJetSystemCSV
do
./shapes/produce_shapes_variables_nominal.sh $ERA $CHANNEL $VARIABLE && python add_hists.py output/shapes/${ERA}_${CHANNEL}_${VARIABLE}/${ERA}-${ERA}_${CHANNEL}_${VARIABLE}-${CHANNEL}-shapes.root --input-hist ggH125 ttH125 qqH125 VH125 --output-hist HTT  --mode control & 


done 
done
done

wait


for ERA in 2018 #2016 2017 2018
do
for CHANNEL in et mt tt #tt mt #et
do


for VARIABLE in m_sv_puppi mbb_highCSV_bReg kinfit_mH #pt_ttvisbb_highCSV_bReg #kinfit_mH mbb_highCSV_bReg m_sv_puppi #  mjj pt_1 pt_2 m_vis ptvis m_sv_puppi jpt_1 njets jdeta mjj dijetpt bpt_bReg_1 bpt_bReg_2 jpt_2 mbb_highCSV_bReg pt_bb_highCSV_bReg m_ttvisbb_highCSV_bReg kinfit_mH kinfit_mh2 kinfit_chi2 nbtag  bm_bReg_1 bm_bReg_2 bcsv_1 bcsv_2 highCSVjetUsedFordiBJetSystemCSV

do


python plot_nmssm_nominal.py  -v ${VARIABLE} --era Run${ERA}  --shapes output/shapes/${ERA}_${CHANNEL}_${VARIABLE}/${ERA}-${ERA}_${CHANNEL}_${VARIABLE}-${CHANNEL}-shapes.root -c $CHANNEL --emb   --output-dir plots/control/ --ff  &

done
done
done

wait






