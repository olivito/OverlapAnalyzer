/** \class OverlapAnalyzer
 *
 * See header file for documentation
 *
 *  $Date: 2012/01/30 09:40:35 $
 *  $Revision: 1.1 $
 *
 *  \author Dominick Olivito
 *
 */

#include "FWCore/Common/interface/TriggerNames.h"
#include "FWCore/Common/interface/TriggerResultsByName.h"
#include "TrigAnalyzer/OverlapAnalyzer/interface/OverlapAnalyzer.h"

#include <cassert>

using namespace reco;
using namespace edm;

//
// constructors and destructor
//
//____________________________________________________________________________
OverlapAnalyzer::OverlapAnalyzer(const edm::ParameterSet& ps) : 
  processName_(ps.getParameter<std::string>("processName")),
  hltTriggerNames_(ps.getParameter<std::vector<std::string>>("hltTriggerNames")),
  triggerResultsTag_(ps.getParameter<edm::InputTag>("triggerResults")),
  xsec_(ps.getParameter<double>("xsec")),
  lumi_(ps.getParameter<double>("lumi")),
  verbose_(ps.getParameter<bool>("verbose"))
{
  using namespace std;
  using namespace edm;

  ntrigs_ = hltTriggerNames_.size();
  nevents_ = 0;

  cout << "OverlapAnalyzer configuration: " << endl
       << "   ProcessName = " << processName_ << endl
       << "   hltTriggerNames = ";
  for (unsigned int itrig = 0; itrig < ntrigs_; ++itrig) {
    cout << hltTriggerNames_.at(itrig) << ", ";
  }
  cout << endl
       << "   TriggerResultsTag = " << triggerResultsTag_.encode() << endl
       << "   xsec = " << xsec_ << endl
       << "   lumi = " << lumi_ << endl
       << "   Verbose = " << verbose_ << endl;

  // histogram setup
  edm::Service<TFileService> fs;
  h_menurate_ = fs->make<TH1D>("h_menurate" , ";Total Menu; Rate [Hz]" , 2 , -0.5 , 1.5 );
  h_rates_ = fs->make<TH1D>("h_rates" , ";; Rate [Hz]" , ntrigs_ , 0. , ntrigs_ );
  h_excl_rates_ = fs->make<TH1D>("h_excl_rates" , ";; Exclusive Rate [Hz]" , ntrigs_ , 0. , ntrigs_ );
  h_overlaps_ = fs->make<TH2D>("h_overlaps" , ";;; Rate [Hz]" , ntrigs_ , 0. , ntrigs_ , ntrigs_ , 0. , ntrigs_ );

  // axis bin labels
  for (unsigned int itrig = 0; itrig < ntrigs_; ++itrig) {
    h_rates_->GetXaxis()->SetBinLabel(itrig+1,formatTriggerName(hltTriggerNames_.at(itrig)).c_str());
    h_excl_rates_->GetXaxis()->SetBinLabel(itrig+1,formatTriggerName(hltTriggerNames_.at(itrig)).c_str());
    h_overlaps_->GetXaxis()->SetBinLabel(itrig+1,formatTriggerName(hltTriggerNames_.at(itrig)).c_str());
    h_overlaps_->GetYaxis()->SetBinLabel(itrig+1,formatTriggerName(hltTriggerNames_.at(itrig)).c_str());
  }

}

//____________________________________________________________________________
OverlapAnalyzer::~OverlapAnalyzer()
{
}

//
// member functions
//
//____________________________________________________________________________
void
OverlapAnalyzer::beginRun(edm::Run const & iRun, edm::EventSetup const& iSetup)
{
  using namespace std;
  using namespace edm;

  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      const unsigned int n(hltConfig_.size());
      // check if trigger names in (new) config
      for (unsigned int itrig = 0; itrig < ntrigs_; ++itrig) {
	unsigned int triggerIndex(hltConfig_.triggerIndex(hltTriggerNames_.at(itrig)));
	if (triggerIndex>=n) {
	  cout << "OverlapAnalyzer::analyze:"
	       << " TriggerName " << hltTriggerNames_.at(itrig) 
	       << " not available in (new) config!" << endl;
	}
      } // loop over triggers
    } // if changed
  } else {
    cout << "OverlapAnalyzer::analyze:"
	 << " config extraction failure with process name "
	 << processName_ << endl;
  }

}

//____________________________________________________________________________
// ------------ method called to produce the data  ------------
void
OverlapAnalyzer::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace std;
  using namespace edm;

  if (verbose_) cout << endl;

  // get event products
  iEvent.getByLabel(triggerResultsTag_,triggerResultsHandle_);
  if (!triggerResultsHandle_.isValid()) {
    cout << "OverlapAnalyzer::analyze: Error in getting TriggerResults product from Event!" << endl;
    return;
  }
  assert(triggerResultsHandle_->size()==hltConfig_.size());

  // double loop over triggers to see overlaps
  bool pass_event = false;

  // to avoid retrieving the trigger results N^2 times, 
  //  loop once and fill a vector with results
  //  sanity check: vector size == trigger name vector size
  std::vector<int> trigResults;
  for (unsigned int itrig=0; itrig < ntrigs_; ++itrig) {
    trigResults.push_back((int)analyzeTrigger(iEvent,iSetup,hltTriggerNames_.at(itrig)));
  }

  if (trigResults.size() != ntrigs_) {
    std::cerr << "ERROR: mismatch in ntrigs.  nresults: " << trigResults.size()
	      << ", ntrigs: " << ntrigs_ << std::endl;
    return;
  }

  for (unsigned int itrig=0; itrig < ntrigs_; ++itrig) {
    bool pass1 = bool(trigResults.at(itrig));
    if (pass1) {
      h_rates_->Fill(itrig);
      pass_event = true;
    }
    bool pass_other = false;
    for (unsigned int jtrig=0; jtrig < ntrigs_; ++jtrig) {
      bool pass2 = bool(trigResults.at(jtrig));
      if (pass1 && pass2) h_overlaps_->Fill(itrig,jtrig);
      if (pass2 && (itrig != jtrig)) pass_other = true;
    }
    if (pass1 && !pass_other) h_excl_rates_->Fill(itrig);
  }

  // all events
  h_menurate_->Fill(0.);
  ++nevents_;
  // events passing menu
  if (pass_event) h_menurate_->Fill(1.);

  if (verbose_) cout << endl;

  return;
}

//____________________________________________________________________________
bool OverlapAnalyzer::analyzeTrigger(const edm::Event& iEvent, const edm::EventSetup& iSetup, const std::string& triggerName) {
  
  using namespace std;
  using namespace edm;
  using namespace reco;
  using namespace trigger;

  if (verbose_) cout << endl;

  const unsigned int ntrigs(hltConfig_.size());
  const unsigned int triggerIndex(hltConfig_.triggerIndex(triggerName));
  assert(triggerIndex==iEvent.triggerNames(*triggerResultsHandle_).triggerIndex(triggerName));

  // abort on invalid trigger name
  if (triggerIndex>=ntrigs) {
    cout << "OverlapAnalyzer::analyzeTrigger: path "
	 << triggerName << " - not found!" << endl;
    return false;
  }

  if (verbose_) {
    cout << "OverlapAnalyzer::analyzeTrigger: path "
	 << triggerName << " [" << triggerIndex << "]" << endl;
  }
  // modules on this trigger path
  const unsigned int m(hltConfig_.size(triggerIndex));
  const vector<string>& moduleLabels(hltConfig_.moduleLabels(triggerIndex));

  bool wasRun = triggerResultsHandle_->wasrun(triggerIndex);
  bool accept = triggerResultsHandle_->accept(triggerIndex);
  bool error = triggerResultsHandle_->error(triggerIndex);
  const unsigned int moduleIndex(triggerResultsHandle_->index(triggerIndex));
  // Results from TriggerResults product
  if (verbose_) {
    cout << " Trigger path status:"
	 << " WasRun=" << wasRun
	 << " Accept=" << accept
	 << " Error =" << error
	 << endl;
    cout << " Last active module - label/type: "
	 << moduleLabels[moduleIndex] << "/" << hltConfig_.moduleType(moduleLabels[moduleIndex])
	 << " [" << moduleIndex << " out of 0-" << (m-1) << " on this path]"
	 << endl;
  }
  assert (moduleIndex<m);

  if (!wasRun || !accept || error) return false;
  return true;
}

//____________________________________________________________________________
void OverlapAnalyzer::endJob() {

  //  double ilumi = 1.4e34;
  double xs = xsec_ * 1.e-36;
  double norm = lumi_ * xs / double(nevents_);
  h_menurate_->Scale(norm);
  h_rates_->Scale(norm);
  h_excl_rates_->Scale(norm);
  h_overlaps_->Scale(norm);

}

//____________________________________________________________________________
std::string OverlapAnalyzer::formatTriggerName(const std::string& triggerName) {

  std::string outname = triggerName;
  // names of the form "HLT_TRIGGER_v1"
  // remove HLT_ and _v1
  outname.replace(outname.begin(),outname.begin()+4,"");
  outname.replace(outname.end()-3,outname.end(),"");

  // also remove "_NoiseCleaned" from MET names..
  size_t pos = outname.find("_NoiseCleaned");
  if (pos != std::string::npos) {
    outname.replace(pos,13,"");
  }

  //  std::cout << "input string: " << triggerName << ", output string: " << outname << std::endl;

  return outname;

}
