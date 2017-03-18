#! /usr/bin/python
"""
	script for plotting smeared histogrammed ORCA event rates (9m configuration)
	based on results also used in the
	"Letter of Intent for KM3NeT 2.0"
	Journal of Physics G: Nuclear and Particle Physics, Volume 43, Number 8
	https://arxiv.org/abs/1601.07459
"""
__author__ = "Steffen Hallmann"
__copyright__ = "2016-10-12"
__email__ = "steffen.hallmann@fau.de"

import ROOT
from math import sqrt 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--input_file", help="non-smeared input file name", required=True)
args = parser.parse_args()

def binSignificance(s,b):
	if s+b == 0:
		return 0
	else:
		return s/sqrt(s+b)

def binWiseSignificance(hSignal, hBgr):
	hSignificance = hSignal.Clone('hSignificance')
	hSignificance.Reset()
	for xbin in range(1, hSignificance.GetNbinsX()+1):
		for ybin in range(1, hSignificance.GetNbinsY()+1):
			theSignal = hSignal.GetBinContent(xbin,ybin)
			theBackground = hBgr.GetBinContent(xbin,ybin)
			hSignificance.SetBinContent(xbin, ybin, binSignificance(theSignal, theBackground))
	return hSignificance

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetNumberContours(100)
f = ROOT.TFile(args.input_file)
hBackground = f.hBackground
hTau = f.hTau

hBackground.SetTitle("other events per month classified as 'shower';log_{10}(E_{reco}[GeV]);cos(zenith_{reco})")
hBackground.Draw('colz')
ROOT.gPad.Print('numberOthersPerMonth_smeared.pdf')

hTau.SetTitle("#nu_{#tau} CC events per month classified as 'shower';log_{10}(E_{reco}[GeV]);cos(zenith_{reco})")
hTau.Draw('colz')
ROOT.gPad.Print('numberTausPerMonth_smeared.pdf')

hSignificance = binWiseSignificance(hTau, hBackground)
hSignificance.SetTitle("1 month, shower-like, N(#nu_{#tau} CC) / N(all #nu)^{0.5}")
hSignificance.Draw('colz')
ROOT.gPad.Print('perBinSignificance_oneMonth_smeared.pdf')



