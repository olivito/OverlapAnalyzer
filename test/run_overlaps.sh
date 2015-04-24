#!/bin/bash

#TAG=ECAL_Mf_JEC
#TAG=ECAL_Mf_HCALM2_JEC
TAG=ECAL_Mf_HCALM3_JEC
#TAG=oldreco
BASEDIR=/nfs-7/userdata/olivito/HLT/had_ntuple_740/v1/62X/PU40/${TAG}/
LABEL=had_ntuple_740_${TAG}

declare -a Samples=(qcd_pt30to50 qcd_pt50to80 qcd_pt80to120 qcd_pt120to170 qcd_pt170to300 qcd_pt300to470 qcd_pt470to600 qcd_pt600to800 qcd_pt800to1000)

for SAMPLE in ${Samples[@]}
  do nohup cmsRun ana_overlaps.py sample=${SAMPLE} basedir=${BASEDIR} label=${LABEL} >& log_overlaps_${SAMPLE}_${LABEL}.txt &
done

