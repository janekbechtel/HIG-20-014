for CHANNEL in tt mt et
for T_MASS in 500
do
for T_BATCH in 3 
do
LM=`python ml/get_typical_point.py ${T_MASS} ${T_BATCH}`


# RUN THESE COMMANDS ONLY TO RECREATE THE ERA-COMBINED ROOT FILES FROM POSTFITSHAPE ROOT FILES : 

# for ERA in 2016 2017 2018
# do
# python add_hists.py output_${ERA}_${CHANNEL}_500_3_nmssm_500_110/${ERA}/cmb/postfitshape.root --input-hist ggH125 ttH125 VH125  --output-hist HTT
# python rebin.py output_${ERA}_${CHANNEL}_500_3_nmssm_500_110/${ERA}/cmb/postfitshape.root
# done




for CAT in 1 2 3 4 5 
do

# python merge_prefit.py $CHANNEL $CAT $T_MASS $T_BATCH $LM


# PLOTTING PART STARTS HERE


if [ "$CAT" -eq 1 ]; then
NAME="#tau#tau"
process="emb"
color="0 #FFCC66"
linewidth="0"
marker="HIST"
nmssm_signal="false"
siglabel=""
sigcolor="0"
fi
if [ "$CAT" -eq 2 ]; then
NAME="t#bar{t}"
process="ttl"
color="0 #9999CC"
linewidth="0"
marker="HIST"
nmssm_signal="false"
siglabel=""
sigcolor="0"
fi
if [ "$CAT" -eq 3 ]; then
NAME="misc."
process="zll vvl htt"
color="0 #6F2D35"
linewidth="0"
marker="HIST"
nmssm_signal="false"
siglabel=""
sigcolor="0"
fi
if [ "$CAT" -eq 4 ]; then
NAME="Jet#rightarrow#tau_{h}"
color="0 #FFCCFF"
process="fakes"
linewidth="0"
marker="HIST"
nmssm_signal="false"
siglabel=""
sigcolor="0"
fi
if [ "$CAT" -eq 5 ]; then
NAME="Signal"
process="nmssm_${T_MASS}_125_${LM}"
linewidth="3"
marker="HIST"
color="0 #CF5E61"
nmssm_signal="true"
if [ "$CHANNEL" = "tt" ]; then
siglabel="#scale[0.85]{H(${T_MASS})#rightarrowh(125)h_{S}(${LM}) (50 fb)}" 
else
siglabel="#scale[0.85]{H(${T_MASS})#rightarrowh(125)h_{S}(${LM}) (200 fb)}" 
fi
sigcolor="#CF5E61"

fi
echo $NAME
echo $process

if [ "$CAT" -eq 3 ]; then
cp combine_${CHANNEL}_base_cat3.json combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
fi
else
cp combine_${CHANNEL}_base.json combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
fi


sed -i "s#CAT#"${CAT}"#g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s#+TM+#"${T_MASS}"#g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s#+LM+#"${LM}"#g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+NAME+%${NAME}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+PROCESS+%${process}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+COLOR+%${color}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+MARKER+%${marker}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+LINEWIDTH+%${linewidth}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+NMSSM_SIGNAL+%${nmssm_signal}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+SIGCOLOR+%${sigcolor}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json
sed -i "s%+SIGLABEL+%${siglabel}%g" plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json

higgsplot.py -j plots/prefit/combine_${CHANNEL}_${CAT}_${T_MASS}_${T_BATCH}_${LM}.json

done
done
done
done

