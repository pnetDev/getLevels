#!/usr/bin/python

from __future__ import division
import sys,time,subprocess
from easysnmp import snmp_get, snmp_set, snmp_walk

# Variables:
## Levels Oids

cmts = sys.argv[1]
usIF = sys.argv[2]

firstStats = []
secondStats = []

mac=".1.3.6.1.2.1.2.2.1.6.2"
dfq=".1.3.6.1.2.1.10.127.1.1.1.1.2.3"
ufq=".1.3.6.1.2.1.10.127.1.1.2.1.2.4"
dsp=".1.3.6.1.2.1.10.127.1.1.1.1.6.3"
snr=".1.3.6.1.2.1.10.127.1.1.4.1.5.3"
txp=".1.3.6.1.2.1.10.127.1.2.2.1.3.2"
unr=".1.3.6.1.2.1.10.127.1.1.4.1.2.3"
cor=".1.3.6.1.2.1.10.127.1.1.4.1.3.3"
unc=".1.3.6.1.2.1.10.127.1.1.4.1.4.3"

## Bonded Channel Oids



#Functions
def getOid(oid):
	try:
        	snmpData = snmp_get(oid, hostname=cmIP, community='private', version=2)
        	return snmpData.value
	except:
		return "1000" ## If there is a data read error

def mac2decimal(mac):
	mac = mac.split(':')
	## Need to convert each hextet to decimal and then build the dotted decimal result. Might be a better way to do this, can't find a function.
        ## Break up the MAC address into hextets H stands for Hextet
        macH0 = mac[0]
        macH1 = mac[1]
        macH2 = mac[2]
        macH3 = mac[3]
        macH4 = mac[4]
        macH5 = mac[5]
	## Convert each hextet to decimal
        dec0 = int(macH0, 16)
        dec1 = int(macH1, 16)
        dec2 = int(macH2, 16)
        dec3 = int(macH3, 16)
        dec4 = int(macH4, 16)
        dec5 = int(macH5, 16)
	macDottedDecimal = "." + str(dec0) + "." + str(dec1) + "." + str(dec2) + "." + str(dec3) + "." + str(dec4) + "." + str(dec5)
	return macDottedDecimal

def getCmIndex(macDottedDecimal,cmts):
	cmIndex = ".1.3.6.1.2.1.10.127.1.3.7.1.2" + macDottedDecimal
        cmIndexData = snmp_get(cmIndex,hostname=cmts, community='private', version=2)
        cmIndexData = cmIndexData.value
	return cmIndexData	

def getUpstreamErrors(cmts,cmIndex):
        cmUsErrors = ".1.3.6.1.2.1.10.127.1.3.3.1.12." + str(cmIndex)
        cmUsErrorsData = snmp_get(cmUsErrors,hostname=cmts, community='private', version=2)
	return cmUsErrorsData.value
	
def getCmIfIndex(cmts,cmIndex):
	getCmIfIndex = ".1.3.6.1.2.1.10.127.1.3.3.1.5." + str(cmIndex)
	getCmIfIndexData  = snmp_get(getCmIfIndex,hostname=cmts, community='private', version=2)
	return getCmIfIndexData.value

## MAIN
print "Script still under development"
print "-------------------------------------------------------------------------------"
print "Generating list of online modems on" , cmts, "upstream interface", usIF,"please wait....."
print "-------------------------------------------------------------------------------"
modems = subprocess.check_output(['bash','get_cmtsstatustable.sh',cmts,usIF])
modems=modems.split(',')
#print "DEBUG: Modem List",modems

print "First Check"
for cmIP in modems:
	#print "processing", cmIP
	try:
		mac = snmp_get('.1.3.6.1.2.1.2.2.1.6.2.', hostname=cmIP, community='private', version=2)
		mac = ':'.join('{:02x}'.format(ord(x)) for x in mac.value)  ## This nifty code presents the MAC in readable format
	except:
		#print "MAC Unable to contact", cmIP
		continue  # Skip this iteration.
	macDecimal = mac2decimal(mac)
        cmIndex = getCmIndex(macDecimal,cmts)
	cmIfIndex = getCmIfIndex(cmts,cmIndex)
	## Skip if its not the index the user entered
	if cmIfIndex <> usIF:
		continue ## Skip this iteration
        UsErrors = getUpstreamErrors(cmts,cmIndex)
	dsFreq = getOid(dfq)
	usFreq = getOid(ufq)
	DSP = getOid(dsp)
	SNR = getOid(snr)
	TXP = getOid(txp)
	UNR = getOid(unr)
	COR = getOid(cor)
	UNC = getOid(unc)
	macDecimal = mac2decimal(mac)
	cmIndex = getCmIndex(macDecimal,cmts)
	UsErrors = getUpstreamErrors(cmts,cmIndex)
	cmIfIndex = getCmIfIndex(cmts,cmIndex)
	#print mac, cmIP, "DSFREQ:", dsFreq, "USFREQ:", usFreq, "PWR:", DSP, "SNR:", SNR, "TX PWR:", TXP, "Packets:",UNR, "Corrected:", COR, "Down Uncorrected:", UNC, "Up Uncorrected:", UsErrors
	print "1st Check",cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,"ifIndex:",cmIfIndex
	firstStats.append([cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,cmIfIndex])

print firstStats

print ""

for data in firstStats:
	print data[0], data[1]
#print ("\n".join(firstStats))

print "Second Check"
for cmIP in modems:
        #print "processing", cmIP
        try:
                mac = snmp_get('.1.3.6.1.2.1.2.2.1.6.2.', hostname=cmIP, community='private', version=2)
                mac = ':'.join('{:02x}'.format(ord(x)) for x in mac.value)  ## This nifty code presents the MAC in readable format
        except:
                #print "MAC Unable to contact", cmIP
                continue  # Skip this iteration
	macDecimal = mac2decimal(mac)
        cmIndex = getCmIndex(macDecimal,cmts)
        cmIfIndex = getCmIfIndex(cmts,cmIndex)
        ## Skip if its not the index the user entered
        if cmIfIndex <> usIF:
                continue ## Skip this iteration
        dsFreq = getOid(dfq)
        usFreq = getOid(ufq)
        DSP = getOid(dsp)
        SNR = getOid(snr)
        TXP = getOid(txp)
        UNR = getOid(unr)
        COR = getOid(cor)
	UNC = getOid(unc)
        UsErrors = getUpstreamErrors(cmts,cmIndex)
	#print mac, cmIP, "DSFREQ:", dsFreq, "USFREQ:", usFreq, "PWR:", DSP, "SNR:", SNR, "TX PWR:", TXP, "Packets:",UNR, "Corrected:", COR, "Down Uncorrected:", UNC, "Up Uncorrected:", UsErrors
        print "2nd Check",cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,"ifIndex",cmIfIndex
        secondStats.append([cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors,cmIfIndex])



print ""

modemCount = len(secondStats)
#print firstStats
print "-------------------------------------------------------------------------------------------"
#print secondStats

print "********* REPORT ***********"
print ""
## Calculate results
## Header cmts,mac,cmIP,dsFreq,usFreq,DSP,SNR,TXP,UNR,COR,UNC,UsErrors
for data in range(modemCount):
	cmts1 = firstStats[data][0] 
	mac1 = firstStats[data][1] 
	cmIP1 = firstStats[data][2] 
	dsFreq1 = firstStats[data][3] 
	usFreq1 = firstStats[data][4] 
	DSP1 = firstStats[data][5] 
	SNR1 = firstStats[data][6] 
	TXP1 = firstStats[data][7] 
	UNR1 = firstStats[data][8] 
	COR1 = firstStats[data][9] 
	UNC1 = firstStats[data][10] 
	UsErrors1 = firstStats[data][11] 
	cmIfIndex1 = firstStats[data][12]

	cmts2 = secondStats[data][0]
        mac2 = secondStats[data][1]
        cmIP2 = secondStats[data][2]
        dsFreq2 = secondStats[data][3]
        usFreq2 = secondStats[data][4]
        DSP2 = secondStats[data][5]
        SNR2 = secondStats[data][6]
        TXP2 = secondStats[data][7]
        UNR2 = secondStats[data][8]
        COR2 = secondStats[data][9]
        UNC2 = secondStats[data][10]
        UsErrors2 = secondStats[data][11]
	cmIfIndex2 = secondStats[data][12]
	
	# Sanity print
	#print  cmts1,mac1,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1 + "\t" +  cmts2,mac2,cmIP2,dsFreq2,usFreq2,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2
		
	# Calculate DS errors
	goodWordsDelta = int(UNR2) - int(UNR1)
	downHecWordsDelta = int(UNC2) - int(UNC1)
	downHecPercent = (downHecWordsDelta / goodWordsDelta) * 100
	downHecPercent = round(downHecPercent,4)

	# Calculate US errors delta
	upHecWordsDelta = int(UsErrors2) - int(UsErrors1)

	#print "Counter Delta"
	print cmts1,mac1,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2,"goodWordsDelta:", goodWordsDelta, "downHecWordsDelta:" , downHecWordsDelta, "downHecPercent:", downHecPercent, "upHecWordsDelta:", upHecWordsDelta,"IfIndex:",cmIfIndex1
	 
	#print  cmts1,mac1,mac2,cmIP1,dsFreq1,usFreq1,DSP1,SNR1,TXP1,UNR1,COR1,UNC1,UsErrors1 + "\t" +  mac2,dsFreq2,DSP2,SNR2,TXP2,UNR2,COR2,UNC2,UsErrors2








