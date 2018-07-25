
CHANNEL_DECAY='generic'    # "${2#*=}"

ConfigReleaseReco=CMSSW_9_4_0_patch1

echo "=================  Starting cmssw environment prepration ====================" >> job.log

#export SCRAM_ARCH=slc6_amd64_gcc630
#export VO_CMS_SW_DIR=/cvmfs/cms.cern.sh
#source $VO_CMS_SW_DIR/cmsset_default.sh

if [ -r ${ConfigReleaseReco}/src ] ; then
 echo release ${ConfigReleaseReco} already exists
else
scram p CMSSW ${ConfigReleaseReco}
fi
cd ${ConfigReleaseReco}/src
eval `scram runtime -sh`
scram b
cd ../../

echo "================= PB: Input Paramateres ========================================">> job.log
#echo $CHANNEL_DECAY
#echo $NEVENTS
#echo $NCORES

echo "================= PB: CMSRUN starting Step 0 ====================" >> job.log

cmsRun -j ${CHANNEL_DECAY}_step0.log -p PSet.py


echo "================= PB: CMSRUN starting Step 1 ====================" >> job.log

cmsRun -e -j ${CHANNEL_DECAY}_step1.log step1-DR-${CHANNEL_DECAY}_cfg.py
#cleaning
rm -rfv GS-${CHANNEL_DECAY}.root


echo "================= PB: CMSRUN starting step 2 ====================" >> job.log

cmsRun -e -j ${CHANNEL_DECAY}_step2.log  step2-DR-${CHANNEL_DECAY}_cfg.py
#cleaning
rm -rfv step1-DR-${CHANNEL_DECAY}.root


echo "================= PB: CMSRUN starting step 3 ====================" >> job.log

cmsRun -e -j ${CHANNEL_DECAY}_step3.log step3-MiniAOD-${CHANNEL_DECAY}_cfg.py
#cleaning
rm -rfv step2-DR-${CHANNEL_DECAY}.root


echo "================= PB:Set up for  Rootuple ====================" >> job.log

scram p -n CMSSW_947_Rootuples CMSSW_9_4_7
cp Ponia.tar.gz CMSSW_947_Rootuples/src/
#cp step3-MiniAOD-${CHANNEL_DECAY}.root CMSSW_947_Rootuples/src/
cd CMSSW_947_Rootuples/src/
tar -xvzf Ponia.tar.gz
eval `scram runtime -sh`
scram b
cd ../..

echo "================= PB: CMSRUN starting step 4 ====================" >> job.log
cmsRun -e -j ${CHANNEL_DECAY}_step4.log CMSSW_947_Rootuples/src/Ponia/Onia/XbMC2017/test/run-${CHANNEL_DECAY}-Rootuple_cfg.py


echo "================= PB: CMSRUN starting step 5 ====================" >> job.log

cmsRun -e -j FrameworkJobReport.xml  CMSSW_947_Rootuples/src/Ponia/Onia/XbMC2017/test/Rootuple-MiniAOD-2017-${CHANNEL_DECAY}_cfg.py


echo "================= PB: End ====================" >> job.log

