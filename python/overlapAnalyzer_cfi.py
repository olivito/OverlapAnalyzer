import FWCore.ParameterSet.Config as cms

overlapAnalyzer = cms.EDAnalyzer("OverlapAnalyzer",
    processName = cms.string("reHLT"),
    hltTriggerNames = cms.vstring(""),
    triggerResults = cms.InputTag("TriggerResults","","reHLT"),
    weight = cms.double(1.),
    minPU = cms.double(-1.),
    maxPU = cms.double(-1.),
    rejectHardPU = cms.bool(False),
    plotVsPU = cms.bool(False),
    useMCweights = cms.bool(False),
    normByXsec = cms.bool(False),
    normByWeight = cms.bool(False),
    verbose = cms.bool(False)
)
