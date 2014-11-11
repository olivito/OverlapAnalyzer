#ifndef OverlapAnalyzer_h
#define OverlapAnalyzer_h

/** \class OverlapAnalyzer
 *
 *  
 *  Makes 2D hist of overlaps of triggers
 *
 *  $Date: 2012/01/30 09:40:35 $
 *  $Revision: 1.1 $
 *
 *  \author Dominick Olivito
 *
 */

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "DataFormats/HLTReco/interface/TriggerEventWithRefs.h"

#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "TH1.h"
#include "TH2.h"

//
// class declaration
//
class OverlapAnalyzer : public edm::EDAnalyzer {
  
 public:
  explicit OverlapAnalyzer(const edm::ParameterSet&);
  ~OverlapAnalyzer();

  virtual void beginRun(edm::Run const &, edm::EventSetup const&);
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  bool analyzeTrigger(const edm::Event&, const edm::EventSetup&, const std::string&);

  std::string formatTriggerName(const std::string& triggerName);

 private:

  /// module config parameters
  std::string   processName_;
  std::vector<std::string> hltTriggerNames_;
  edm::InputTag triggerResultsTag_;
  double xsec_;
  bool verbose_;

  /// additional class data memebers
  edm::Handle<edm::TriggerResults>           triggerResultsHandle_;
  HLTConfigProvider hltConfig_;
  TH1D* h_menurate_;
  TH1D* h_rates_;
  TH2D* h_overlaps_;
  unsigned int ntrigs_;
  unsigned int nevents_;

};
#endif
