import FWCore.ParameterSet.Config as cms

overlapAnalyzer = cms.EDAnalyzer("OverlapAnalyzer",
    processName = cms.string("reHLT"),
    hltTriggerNames = cms.vstring(""),
    triggerResults = cms.InputTag("TriggerResults","","reHLT"),
    weight = cms.double(1.),
    verboase = cms.bool(False)
)
