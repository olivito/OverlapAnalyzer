#!/bin/bash

HADOOPDIR=/hadoop/cms/store/user/olivito/
#TAG=ECAL_Mf_JEC
#TAG=ECAL_Mf_HCALM2_JEC
TAG=oldreco
OUTPUTDIR=/nfs-7/userdata/olivito/HLT/had_recotest/v2/62X/PU40/${TAG}/
DATE=150306

function run () {
    /bin/ls ${HADOOPDIR}/QCD_Pt-${1}_Tune4C_13TeV_pythia8/*${TAG}*/${DATE}_*/*/*.root > list_${TAG}_qcd_pt$1.txt
    sed -i 's/\/hadoop/file:\/hadoop/g' list_${TAG}_qcd_pt$1.txt
    echo cmsRun copyPickMerge_cfg.py inputFiles_load=list_${TAG}_qcd_pt$1.txt outputFile=${OUTPUTDIR}/qcd_pt$1.root maxSize=5000000 
    nohup cmsRun copyPickMerge_cfg.py inputFiles_load=list_${TAG}_qcd_pt$1.txt outputFile=${OUTPUTDIR}/qcd_pt$1.root maxSize=5000000 >& log_merge_${TAG}_qcd_pt$1.txt &
}

mkdir -p $OUTPUTDIR

#declare -a Samples=(qcdem_20to30 qcdem_30to80 qcdem_80to170 wenu dyee)
declare -a Samples=(30to50 50to80 80to120 120to170 170to300 300to470 470to600 600to800 800to1000)

for SAMPLE in ${Samples[@]}
  do run $SAMPLE
done

