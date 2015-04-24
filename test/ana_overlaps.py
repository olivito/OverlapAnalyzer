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

# Get command line options
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')

options.register(
    'sample',
    'qcd_30to50',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'sample to run')

options.register(
    'basedir',
    '/nfs-7/userdata/olivito/HLT/had_ntuple_740/v1/62X/PU40/ECAL_Mf_HCALM3_JEC/',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'input dir')

options.register(
    'label',
    'had_recotest_v2_ECAL_Mf_JEC',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    'label for output')

options.parseArguments()

# Input source
process.source = cms.Source("PoolSource",
#   fileNames = cms.untracked.vstring('file:/hadoop/cms/store/user/olivito/HLT/TkMu/WToMuNu_Tune4C_13TeV-pythia8_Fall13dr-tsg_PU40bx50_POSTLS162_V2-v1_savel1/output_6_1_qCm.root'),
   fileNames = cms.untracked.vstring(),
   secondaryFileNames = cms.untracked.vstring()
)

xsecs = {
    # 'dyee' : 6960. ,
    # 'wenu' : 16000.,
    # 'qcdem_20to30' : 677300000. * 0.01029 ,
    # 'qcdem_30to80' : 185900000. * 0.06071 ,
    # 'qcdem_80to170' : 3529000. * 0.15443 ,
    'qcd_pt30to50' : 161500000. ,
    'qcd_pt50to80' : 22110000. ,
    'qcd_pt80to120' : 3000114. ,
    'qcd_pt120to170' : 493200. ,
    'qcd_pt170to300' : 120300., 
    'qcd_pt300to470' : 7475. ,
    'qcd_pt470to600' : 587.1 ,
    'qcd_pt600to800' : 167. ,
    'qcd_pt800to1000' : 28.25 ,
    # 'qcd_1000to1400' : 8.195
}

if not options.sample in xsecs:
    print 'ERROR: unknown sample: ' + options.sample
    exit(1)

print 'sample is: ',options.sample,', xsec: ',xsecs[options.sample]

from glob import glob
inputs = glob(options.basedir + '/ntuple_' + options.sample + '*.root')
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
                                       fileName = cms.string('histos_overlap_'+options.sample+'_'+options.label+'.root')
                                   )

process.overlapAnalyzer.processName = cms.string('reHLT')
process.overlapAnalyzer.triggerResults = cms.InputTag("TriggerResults","","reHLT")
process.overlapAnalyzer.xsec = cms.double(xsecs[options.sample])
process.overlapAnalyzer.lumi = cms.double(1.4e34)
#process.overlapAnalyzer.lumi = cms.double(7.0e33)
process.overlapAnalyzer.verbose = cms.bool(False)

process.overlapAnalyzer.hltTriggerNames = cms.vstring(
	"HLT_PFHT350_PFMET120_NoiseCleaned_v1",
	"HLT_PFHT900_v1",
	"HLT_PFJet40_v1",
	"HLT_PFJet60_v1",
	"HLT_PFJet80_v1",
	"HLT_PFJet140_v1",
	"HLT_PFJet200_v1",
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:hltonline', '')

process.MessageLogger.cerr.FwkReport.reportEvery = 100000
process.MessageLogger.categories.append('HLTrigReport')
process.MessageLogger.cerr.HLTrigReport = cms.untracked.PSet(
    optionalPSet = cms.untracked.bool(True),
    limit = cms.untracked.int32(10000000), # 0 means turn this off!!!!!!!!
)

# Path and EndPath definitions
process.HLTanalyzers = cms.Path(process.overlapAnalyzer)
