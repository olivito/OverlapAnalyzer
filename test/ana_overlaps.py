# Auto generated configuration file
# using: 
# Revision: 1.20 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: RelVal --step=HLT:GRun --conditions=auto:hltonline_GRun --filein=file:/tas/olivito/data/RAW/Run2012D/DoubleMu/16951828-0D32-E211-A4C9-5404A63886B1.root --custom_conditions= --fileout=RelVal_HLT_GRun_DATA_doublemu_v2.root --number=100 --data --no_exec --datatier SIM-DIGI-RAW-HLTDEBUG --eventcontent=HLTDEBUG --customise=HLTrigger/Configuration/CustomConfigs.L1THLT --scenario=pp --python_filename=RelVal_HLT_GRun_DATA_test2.py --processName=HLT1
import FWCore.ParameterSet.Config as cms

process = cms.Process('HLTANALYZER')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load('TrigAnalyzer.OverlapAnalyzer.overlapAnalyzer_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
#   fileNames = cms.untracked.vstring('file:/hadoop/cms/store/user/olivito/HLT/TkMu/WToMuNu_Tune4C_13TeV-pythia8_Fall13dr-tsg_PU40bx50_POSTLS162_V2-v1_savel1/output_6_1_qCm.root'),
   fileNames = cms.untracked.vstring(),
   secondaryFileNames = cms.untracked.vstring()
)

basedir = '/nfs-7/userdata/olivito/HLT/allhadronic/v4/'

#sample,xsec = 'dy', 1586.  

#sample,xsec = 'wmunu', 16100.
#sample,xsec = 'qcd_30to50', 161500000. 
#sample,xsec = 'qcd_50to80', 22110000. 
#sample,xsec = 'qcd_80to120', 3000114. 
#sample,xsec = 'qcd_120to170', 493200. 
#sample,xsec = 'qcd_170to300', 120300. 
sample,xsec = 'qcd_300to470', 7475. 
#sample,xsec = 'qcd_470to600', 587.1 
#sample,xsec = 'qcd_600to800', 167. 
#sample,xsec = 'qcd_800to1000', 28.25 
#sample,xsec = 'qcd_1000to1400', 8.195 


#inputs = glob(basedir + '/qcd_50to80*.root')
#inputs = glob(basedir + '/qcd_80to120*.root')
#inputs = glob(basedir + '/qcd_120to170*.root')
#inputs = glob(basedir + '/qcd_170to300*.root')
#inputs = glob(basedir + '/qcd_300to470*.root')
#inputs = glob(basedir + '/qcd_470to600*.root')
#inputs = glob(basedir + '/qcd_600to800*.root')
#inputs = glob(basedir + '/qcd_800to1000*.root')
#inputs = glob(basedir + '/qcd_1000to1400*.root')
#inputs = glob(basedir + '/wmunu*.root')

from glob import glob
inputs = glob(basedir + '/' + sample + '*.root')
for i in inputs:
    process.source.fileNames.append('file:' + i)

print process.source.fileNames



process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    version = cms.untracked.string('$Revision: 1.20 $'),
    annotation = cms.untracked.string('RelVal nevts:100'),
    name = cms.untracked.string('Applications')
)

# Output definition

process.TFileService = cms.Service("TFileService",
                                       fileName = cms.string('histos_overlap_'+sample+'_allhadronic_v4_noalphat.root')
                                   )

process.overlapAnalyzer.processName = cms.string('reHLT')
process.overlapAnalyzer.triggerResults = cms.InputTag("TriggerResults","","reHLT")
#process.overlapAnalyzer.hltTriggerNames = cms.vstring('HLT_PFHT900_v1', 'HLT_PFHT650_4Jet_v1')
process.overlapAnalyzer.xsec = cms.double(xsec)
process.overlapAnalyzer.verbose = cms.bool(False)

process.overlapAnalyzer.hltTriggerNames = cms.vstring(
  'HLT_PFHT900_v1',
  'HLT_PFHT650_4Jet_v1',
  'HLT_PFHT350_PFMET120_NoiseCleaned_v1',
  'HLT_DiCentralPFJet70_PFMET120_NoiseCleaned_v1',
  'HLT_HT200_DiJet90_AlphaT0p57_v1',
  'HLT_HT250_DiJet90_AlphaT0p55_v1',
  'HLT_HT300_DiJet90_AlphaT0p53_v1',
  'HLT_HT350_DiJet90_AlphaT0p52_v1',
  'HLT_HT400_DiJet90_AlphaT0p51_v1',
  'HLT_PFJet450_v1',
  'HLT_CaloJet500_NoJetID_v1',
  'HLT_AK8PFJet360TrimMod_Mass30_v1',
  'HLT_AK8PFHT850_TrimR0p1PT0p03Mass50_v1',
  'HLT_AK8DiPFJet280_200_TrimMass30_BTagCSV0p3_v1',
  'HLT_PFHT650_WideJetMJJ900DEtaJJ1p5_v1',
  'HLT_DiPFJet40_DEta3p5_MJJ600_PFMETNoMu140_v1',
  'HLT_PFMET170_NoiseCleaned_v1',
  'HLT_PFMET120_NoiseCleaned_BTagCSV07_v1',
  'HLT_PFMET120_NoiseCleaned_Mu5_v1',
  'HLT_Mu3er_PFHT140_PFMET125_NoiseCleaned_v1',
  'HLT_Mu6_PFHT200_PFMET100_NoiseCleaned_BTagCSV07_v1',
  'HLT_Mu6_PFHT200_PFMET125_NoiseCleaned_v1',
  'HLT_Mu14er_PFMET120_NoiseCleaned_v1',
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:hltonline_GRun', '')

process.MessageLogger.cerr.FwkReport.reportEvery = 100000
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.cerr.HLTrigReport = cms.untracked.PSet(
    optionalPSet = cms.untracked.bool(True),
    limit = cms.untracked.int32(10000000), # 0 means turn this off!!!!!!!!
)

# Path and EndPath definitions
process.HLTanalyzers = cms.Path(process.overlapAnalyzer)
