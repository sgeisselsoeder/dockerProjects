#! /usr/bin/python
"""
	script for simplistic evaluation of ORCA sensitivity for tau flux normalisation
    no systematics, everything is assumed to be exactly known (fluxes, oscillation params)
"""
__author__ = "Steffen Hallmann"
__copyright__ = "2016-10-12"
__credits__ = ["KM3NeT Collaboration"]
__email__ = "steffen.hallmann@fau.de"


import ROOT
import numpy as np
from math import log
import argparse
import pandas as pd

def getNsigmas_ML(htau, hbgr, sigmas = [1, 2, 3, 4, 5, 7, 10]):
    stopwatch = ROOT.TStopwatch()
    stopwatch.Start()

    htauAssumed = htau.Clone('htauAssumed')
    hbgrAssumed = hbgr.Clone('hbgrAssumed')

    nX = htau.GetNbinsX()
    nY = htau.GetNbinsY()

    ### normalisation of tau flux
    testNormTau = np.arange(0., 2.005, 0.01)
    # print testNormsTau

    # number of pseudo experiments
    n_pseudo = 1000
    print '... generating', n_pseudo, 'pseudo measurements'
    sigmaArray = {}
    for sigma in sigmas:
        sigmaArray[sigma] = []
        sigmaArray[-sigma] = []

    minLLHvals = []
    for j in range(n_pseudo):
        #print j
        mlValue = np.zeros(len(testNormTau))
        # evaluate value over all bins
        for xbin in range(1, nX + 1):
            for ybin in range(1, nY + 1):
                nTauMeasured = htau.GetBinContent(xbin, ybin)
                nBgrMeasured = hbgr.GetBinContent(xbin, ybin)
                nTauUnitaryTrue = htauAssumed.GetBinContent(xbin, ybin)
                nTauTrueArray = nTauUnitaryTrue * testNormTau
                nBgrTrue = hbgrAssumed.GetBinContent(xbin, ybin)

                k = np.random.poisson(nTauMeasured + nBgrMeasured)
                #bgr==0 causes problems: add small number
                if nBgrTrue==0:
                    nBgrTrue += 0.000001
                if k>0:
                    mlValue = mlValue + 2*(k*log(k) - k)
                mlValue = mlValue -2*(k*np.log((nTauTrueArray + nBgrTrue)) - nTauTrueArray - nBgrTrue)

        gLeft = ROOT.TGraph()
        gRight = ROOT.TGraph()
        minimum = np.amin(mlValue)
        #print minimum
        index_minimum = np.argmin(mlValue)
        # subtract minimum value to have DeltaChi2
        mlValue = mlValue - minimum
        minLLHvals.append(minimum)
        for i in range(index_minimum):
            gLeft.SetPoint(gLeft.GetN(), mlValue[i], testNormTau[i])
        for i in range(index_minimum, len(testNormTau)):
            gRight.SetPoint(gRight.GetN(), mlValue[i], testNormTau[i])

        for sigma in sigmas:
            #print sigma**2, gRight.Eval(sigma**2), gLeft.Eval(sigma**2)
            sigmaArray[sigma].append(min(gRight.Eval(sigma**2),3))
            sigmaArray[-sigma].append(max(gLeft.Eval(sigma**2),-1))

        gLeft.Delete()
        gRight.Delete()

    # now get the median of each distribution
    boundLower = np.zeros(len(sigmas))
    boundUpper = np.zeros(len(sigmas))
    for item, sigma in enumerate(sigmas):
        sigmaArray[sigma].sort()
        sigmaArray[-sigma].sort()
        #h = ROOT.TH1F('h','h',100,-1,3)
        #for it in sigmaArray[sigma]:
        #    h.Fill(it)
        #h.Draw()
        #import time
        #time.sleep(2)
        #print sigma
        boundLower[item] = sigmaArray[-sigma][len(sigmaArray[-sigma])/2]
        boundUpper[item] = sigmaArray[sigma][len(sigmaArray[sigma])/2]


    stopwatch.Stop()
    stopwatch.Print()


    datatable = pd.DataFrame({'nSigmas': sigmas, 'upperBounds': boundUpper, 'lowerBounds': boundLower})
    #print datatable
    return datatable

def timeSeriesNutauFlux_ML(hTau, hBgr, nMonthsFirst=1, nMonthsLast=12, stepSize=1):
    tables = []
    for nMonths in range(nMonthsFirst, nMonthsLast+1, stepSize):
        print "livetime [months]:",nMonths
        hTauNow = hTau.Clone('hTauNow')
        hTauNow.Scale(nMonths)
        hBgrNow = hBgr.Clone('hBgrNow')
        hBgrNow.Scale(nMonths)

        sigs = getNsigmas_ML(hTauNow, hBgrNow, sigmas=[1,2,3,4,5])
        sigs['nMonths'] = nMonths
        tables.append(sigs)
    table = pd.concat(tables)
    return table

def drawTimeSeriesNutauFlux_ML(inputfile):
    f = ROOT.TFile(inputfile, 'READ')
    hsig = f.Get('hTau').Clone('hsig')
    hbgr = f.Get('hBackground').Clone('hbgr')
    table = timeSeriesNutauFlux_ML(hsig,hbgr)
    sigmas = [1,2,3,4,5]
    g = {}
    for i in sigmas:
        g[i] = ROOT.TGraph()
        g[-i] = ROOT.TGraph()
        g[i].SetLineColor(201+4*i)
        g[-i].SetLineColor(201+4*i)
        g[i].SetLineWidth(2)
        g[-i].SetLineWidth(2)
    for index, row in table.iterrows():
        g[row['nSigmas']].SetPoint(g[row['nSigmas']].GetN(), row['nMonths'], row['upperBounds'])
        g[-row['nSigmas']].SetPoint(g[-row['nSigmas']].GetN(), row['nMonths'], row['lowerBounds'])
    first=True
    for i in sigmas:
        if first:
            g[i].SetTitle(";livetime [months]; #nu_{#tau} CC flux normalisation")
            g[i].Draw('al')
            first=False
            g[i].GetHistogram().SetMaximum(2)
            g[i].GetHistogram().SetMinimum(0)
            g[i].SetTitle(";livetime [months]; #nu_{#tau} CC flux normalisation")
            g[i].GetXaxis().SetLimits(1,12)
            g[-i].Draw('l')
        else:
            g[i].Draw('l')
            g[-i].Draw('l')
    txt = ROOT.TText()
    txt.DrawTextNDC(0.5,0.85, 'KM3NeT Preliminary')
    tlatex = ROOT.TLatex()
    for i in sigmas:
        tlatex.SetTextColor(201+4*i)
        tlatex.DrawLatexNDC(0.25+i*0.1,0.15,"%i #sigma" %i)		
    ROOT.gPad.SetGrid()
    ROOT.gPad.Print('tau_sensitivity_ORCA_timeevol.pdf')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--input_file", help="non-smeared input file name", required=True)
    args = parser.parse_args()

    drawTimeSeriesNutauFlux_ML(args.input_file)

