#! /usr/bin/python
"""
	script to apply smearing for histogrammed ORCA event rates (9m configuration)
	based on results also used in the
	"Letter of Intent for KM3NeT 2.0"
	Journal of Physics G: Nuclear and Particle Physics, Volume 43, Number 8
	https://arxiv.org/abs/1601.07459
"""
__author__ = "Steffen Hallmann"
__copyright__ = "2016-10-12"
__credits__ = ["Martijn Jongen", "KM3NeT Collaboration"]
__email__ = "steffen.hallmann@fau.de"

import ROOT
import argparse
import os



# use only shower-channel

histogramNames = ["nue_cc_shower-like",
                  "nbe_cc_shower-like",
                  "num_cc_shower-like",
                  "nbm_cc_shower-like",
                  "nut_cc_shower-like",
                  "nbt_cc_shower-like",
                  "nu_nc_shower-like",
                  "nb_nc_shower-like",
                  "atmomu_shower-like"]

### smearing file
smearingFileNames = {
			"nue_cc_shower-like":	"nue_cascade",
			"nbe_cc_shower-like":	"nbe_cascade",
			"num_cc_shower-like":	"num_cascade",
			"nbm_cc_shower-like":	"nbm_cascade",
			"nut_cc_shower-like":	"nut_cascade",
			"nbt_cc_shower-like":	"nbt_cascade",
			"nu_nc_shower-like" :	"nu_nc_cascade",
			"nb_nc_shower-like" :	"nb_nc_cascade"
	}

### function for the zenith angle smearing
def smearZenith(hSmeared,h,hAngleSmearing):
	for etruebin in range(h.GetNbinsX()+2):
		for zsmearedbin in range(h.GetNbinsY()+2):
			for ztruebin in range(h.GetNbinsY()+2):
				### find histogram bins in th3:
				bincenterE = h.GetXaxis().GetBinCenter(etruebin)
				bincenterZtrue = h.GetYaxis().GetBinCenter(ztruebin)
				bincenterZsmeared = h.GetYaxis().GetBinCenter(zsmearedbin)
				responsebin = hAngleSmearing.FindBin(bincenterE,bincenterZtrue,bincenterZsmeared)

				hSmeared.SetBinContent(etruebin,zsmearedbin,hSmeared.GetBinContent(etruebin,zsmearedbin)+h.GetBinContent(etruebin,ztruebin)*hAngleSmearing.GetBinContent(responsebin))

### function for the energy smearing
def smearEnergy(hSmeared, h, hEnergySmearing):
	for zbin in range(h.GetNbinsY()+2):
		for etruebin in range(h.GetNbinsX()+2):
			for erecobin in range(h.GetNbinsY()+2):
				bincenterE = h.GetXaxis().GetBinCenter(etruebin)
				bincenterEsmeared = h.GetXaxis().GetBinCenter(erecobin)
				responsebin = hEnergySmearing.FindBin(bincenterE,bincenterEsmeared)

				hSmeared.SetBinContent(erecobin,zbin,hSmeared.GetBinContent(erecobin,zbin)+h.GetBinContent(etruebin,zbin)*hEnergySmearing.GetBinContent(responsebin))


def produceHistogramsFromTables(infileName, smearingDir="", outfileName="histogramsTauappearanceSmeared.root"):
	rootfile = ROOT.TFile(infileName,'READONLY')
	rootfile.cd('Classified events')

	hUnsmeared = {}
	hAngleSmeared = {}
	hSmeared = {}

	for name in histogramNames:
		### get unsmeared histograms from file
		hUnsmeared[name] = ROOT.TH2D()
		hUnsmeared[name] = ROOT.gDirectory.Get('hClassifiedEvents_'+name+'_yx').Clone(name+'_unsmeared')
		#print hUnsmeared[name].GetNbinsX(), hUnsmeared[name].GetNbinsY()
		### histograms to be filled with smeared values
		hAngleSmeared[name] = ROOT.TH2D()
		hAngleSmeared[name] = hUnsmeared[name].Clone(name+'_anglesmeared')
		hAngleSmeared[name].Reset()

		hSmeared[name] = ROOT.TH2D()
		hSmeared[name] = hUnsmeared[name].Clone(name+'_smeared')
		hSmeared[name].Reset()

	hTauPlusBackground = hUnsmeared["atmomu_shower-like"].Clone('hTauPlusBackground')
	hBackground = hUnsmeared["atmomu_shower-like"].Clone('hBackground')

	# smear histograms
	for sn in smearingFileNames:
		rootfileSmearing = ROOT.TFile(smearingDir+'/spacing_904m_NtupleSmearing_'+smearingFileNames[sn]+'.root','READONLY')
		hAngleSmearing = rootfileSmearing.Get('hAngleResp')
		print '... smearing', sn
		#print hAngleSmearing.GetXaxis().GetTitle()
		#print hAngleSmearing.GetYaxis().GetTitle()
		#print hAngleSmearing.GetZaxis().GetTitle()
		#print 'angle smearing:', hAngleSmeared[sn].GetNbinsX(), hUnsmeared[sn].GetNbinsX(), hAngleSmearing.GetNbinsX()
		smearZenith(hAngleSmeared[sn],hUnsmeared[sn],hAngleSmearing)
		hEnergySmearing = rootfileSmearing.Get('hEnergyResp')
		#print 'energy smearing', hSmeared[sn].GetNbinsX(),hAngleSmeared[sn].GetNbinsX(),hEnergySmearing.GetNbinsX()
		smearEnergy(hSmeared[sn],hAngleSmeared[sn],hEnergySmearing)
		print 'N (unsmeared, angle smeared, angle+energy smeared):', hUnsmeared[sn].Integral(), hAngleSmeared[sn].Integral(), hSmeared[sn].Integral()
		hTauPlusBackground.Add(hSmeared[sn])
	hTauPlusBackground.Draw('colz')
	hTau = hTauPlusBackground.Clone('hTau')
	hTau.Reset()
	hTau.Add(hSmeared["nut_cc_shower-like"])
	hTau.Add(hSmeared["nbt_cc_shower-like"])

	for name in ["nue_cc_shower-like", "nbe_cc_shower-like", "num_cc_shower-like", "nbm_cc_shower-like", "nu_nc_shower-like", "nb_nc_shower-like"]:
		hBackground.Add(hSmeared[name])

	### now fill only the up-going half to new histogram. Scale to 1 month
	print "storing only 'up-going' part of histograms..."
	thenx = hTau.GetNbinsX()
	xlow = hTau.GetXaxis().GetBinLowEdge(1)
	xup = hTau.GetXaxis().GetBinUpEdge(thenx)
	theny = hTau.GetNbinsY() / 2
	ylow = hTau.GetYaxis().GetBinLowEdge(1)
	yup = hTau.GetYaxis().GetBinUpEdge(theny)
	print thenx, xlow,xup, theny, ylow, yup

	hTauUpgoing = ROOT.TH2D('hTauUpgoing', "#nu_{#tau}_cc events per month classified as shower;log10(E_{rec} [GeV]);cos(zenith_{rec})", thenx, xlow,xup, theny, ylow, yup)
	hBackgroundUpgoing = ROOT.TH2D('hBackgroundUpgoing', "background events per month classified as shower;log10(E_{rec} [GeV]);cos(zenith_{rec})", thenx, xlow,xup, theny, ylow, yup)
	hTauPlusBackgroundUpgoing = ROOT.TH2D('hTauPlusBackgroundUpgoing', "#nu_{#tau}_cc + background events per month classified as shower;log10(E_{rec} [GeV]);cos(zenith_{rec})", thenx, xlow,xup, theny, ylow, yup)


	for xbin in range(1,hTauUpgoing.GetNbinsX()+1):
		for ybin in range(1,hTauUpgoing.GetNbinsY()+1):
			hTauUpgoing.SetBinContent(xbin, ybin, hTau.GetBinContent(xbin, ybin) / 3. / 12.)
			hBackgroundUpgoing.SetBinContent(xbin, ybin, hBackground.GetBinContent(xbin, ybin) / 3. / 12.)
			hTauPlusBackgroundUpgoing.SetBinContent(xbin, ybin, hTauPlusBackground.GetBinContent(xbin, ybin) / 3. / 12.)

	### save the histograms to the output file
	outfile = ROOT.TFile(outfileName,'RECREATE')
	hTauUpgoing.Write('hTau')
	hBackgroundUpgoing.Write('hBackground')
	hTauPlusBackgroundUpgoing.Write('hTauPlusBackground')
	outfile.Close()
	print 'TOTAL NUMBER OF UPGOING EVENTS (tau, bgr, tau+bgr):'
	print '  ', hTauUpgoing.Integral(), hBackgroundUpgoing.Integral(), hTauPlusBackgroundUpgoing.Integral()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--input_file", help="non-smeared input file name", required=True)
	parser.add_argument("-d", "--smearing_file_dir", default="", help="directory of smearing files")
	parser.add_argument("-o", "--output_file", default="", help="smeared output file name")
	args = parser.parse_args()

	if args.output_file == "":
		args.output_file = "smeared_"+os.path.basename(args.input_file)

	produceHistogramsFromTables(args.input_file, args.smearing_file_dir, args.output_file)

#produceHistogramsFromTables("data/spacing_904m_NH.root","data","histogramsTauappearanceSmearedNH.root")
#produceHistogramsFromTables("data/spacing_904m_IH.root","data","histogramsTauappearanceSmearedIH.root")

