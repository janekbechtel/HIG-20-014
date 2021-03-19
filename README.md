
# HIG-20-014: Plot reproduction

### Limit plots (including this "scaled by 1eX" plot with all 420 points), Contour plot, Background composition
```bash
# Tested on portal1 (CentOS7)
git clone git@github.com:janekbechtel/HIG-20-014.git
cd HIG-20-014/
source utils/init_cmssw.sh
cd ../..
# for continous limits:
cp plotting_skips.py CMSSW_10_2_16_UL/src/CombineHarvester/CombineTools/python/plotting.py 
# for limits with whitespaces between batches (style as in thesis and paper):
cp plotting_skips.py CMSSW_10_2_16_UL/src/CombineHarvester/CombineTools/python/plotting.py 

# Plot with all limits
sh plot_scaled_limits.sh

# 1D limits
sh run_nn_nmssm_analysis.sh combined all 

# 2D contour plot
python plot_contour.py 

# for limit plot in dependence of mH:
cp plotting.py CMSSW_10_2_16_UL/src/CombineHarvester/CombineTools/python/plotting.py 
sh swapped_plot.sh

# Bar plot of expected background composition
source /cvmfs/sft.cern.ch/lcg/views/LCG_95/x86_64-centos7-gcc8-opt/setup.sh
python bkg_composition.py
```
### Grid plots and Fake factor plot:
They done per hand in Adobe Illustrator, I have uploaded the *.ai files in this repo which can be opened with Inkscape.

### Combined eras postfit plots of NN score:
```bash
# --> Tested and might only work on bms2 (SLC6) <--
source /cvmfs/cms.cern.ch/cmsset_default.sh
cp -r /ceph/htautau/nmssm_plotting/CMSSW_7_4_7/ .
cd CMSSW_7_4_7/src
cmsenv
git clone git@github.com:janekbechtel/HIG-20-014.git
cd HIG-20-014/
mkdir plots	
sh merge_and_plot.sh


# Prefit plot of input variable (2018 mt as in supplementary material)
cd ../Artus
git checkout nmssm_plotting_default
cd ../
scramv1 b ProjectRename; cmsenv
cd HIG-20-014
sh plot_nmssm_nominal.sh
```
