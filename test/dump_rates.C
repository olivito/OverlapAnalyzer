#include "TFile.h"
#include "TH1.h"
#include "TString.h"
#include <iostream>

void dump_rates ( const TString& infile = "histos_overlap_all_had_80x_nominalPU_hlt_susy_menu_test_v6.root" ) {

  std::cout << "-- dumping rates from file: " << infile << std::endl;
  TFile* f = new TFile(infile);
  TH1D* h_rates = (TH1D*) f->Get("overlapAnalyzer/h_rates");

  for (int i = 1; i <= h_rates->GetNbinsX(); ++i) {
    TString trigname = h_rates->GetXaxis()->GetBinLabel(i);
    float rate = h_rates->GetBinContent(i);
    float err = h_rates->GetBinError(i);
    std::cout << trigname << ": " << rate << " +/- " << err << " Hz" << std::endl;
  }

  f->Close();

  return;
}
