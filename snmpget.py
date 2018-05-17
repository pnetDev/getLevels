#!/usr/bin/python

## CM Testing SNMP code

import netsnmp,sys,time

## System ARG is the IP address of the modem.
cmIP = sys.argv[1]
#cmts = sys.argv[2]
print ""

def getOid(oid):
	session = netsnmp.Session( DestHost=cmIP, Version=2, Community='private' )
	vars = netsnmp.VarList( netsnmp.Varbind(oid) )
	#print( session.get(vars) )
	value  = ( session.get(vars) )
	value =str(value)
	value = value.replace("(","") ; value = value.replace(")","") ; value = value.replace("'","") ; value = value.replace(",","") ## Clean up the string
	return  value


def convert(MAC):
	## This function carries out string manipulation on the variable mac
	MAC = MAC.replace("x","") ; MAC = MAC.replace('\\',":")  ## Have to use 2 \\ to escape the first \
	return MAC

def getUpstreamErrors(MAC,cmts):
	## This function will:
	## Convert the MAC into dotted decimal
	## Get the CM index by polling the CMTS
	## Get the Upstream Error counter by polling the CMTS
	## Oids
	cmIndex = ".1.3.6.1.2.1.10.127.1.3.7.1.2"   ## Append the dotted decimal mac to the string.
	upHec = ".1.3.6.1.2.1.10.127.1.3.3.1.12."   ## Append the cmIndex to the string
	print "Converting", MAC ,"to decimal"    ## Easy to convert hex in Python result = int("0xff", 16)
	MAC = MAC.replace('.',"")
	MAC = MAC.split(':')
	print MAC

	## Until I find a faster way need to convert each hextet to decimal and then build the dotted decimal result
	macH1 = MAC[1]
	macH2 = MAC[2]
	macH3 = MAC[3]
	macH4 = MAC[4]
	macH5 = MAC[5]
	macH5 = MAC[6]

	dec1 = int(macH1, 16)
	dec2 = int(macH2, 16)
	dec3 = int(macH3, 16)
	dec4 = int(macH4, 16)
	dec5 = int(macH5, 16)
	dec6 = int(macH6, 16)

	print dec1, dec2, dec3, dec4, dec5, dec6		

## CM Lets make a Python version of get levels.
## Here are the oids we use for getLevels.

mac=".1.3.6.1.2.1.2.2.1.6.2"
dfq=".1.3.6.1.2.1.10.127.1.1.1.1.2.3"
ufq=".1.3.6.1.2.1.10.127.1.1.2.1.2.4"
dsp=".1.3.6.1.2.1.10.127.1.1.1.1.6.3"
snr=".1.3.6.1.2.1.10.127.1.1.4.1.5.3"
txp=".1.3.6.1.2.1.10.127.1.2.2.1.3.2"
unr=".1.3.6.1.2.1.10.127.1.1.4.1.2.3"
cor=".1.3.6.1.2.1.10.127.1.1.4.1.3.3"
unc=".1.3.6.1.2.1.10.127.1.1.4.1.4.3"

## Call the function getOid
MAC = getOid(mac)
hexMac = MAC
MAC = convert(MAC)
dsFreq = getOid(dfq) 	
usFreq = getOid(ufq) 	
DSP = getOid(dsp)	
SNR = getOid(snr)	
TXP = getOid(txp)	 
UNR = getOid(unr)	
COR = getOid(cor)	
UNC = getOid(unc)	

print "MAC",MAC, cmIP, "DSFREQ:", dsFreq, "USFREQ:", usFreq, "PWR:", DSP, "SNR:", SNR, "TX PWR:", TXP, "Packets:",UNR, "Corrected", COR, "Uncorrected", UNC

#time.sleep(3)

MAC = getOid(mac)
MAC = convert(MAC)
dsFreq = getOid(dfq)
usFreq = getOid(ufq)
DSP = getOid(dsp)
SNR = getOid(snr)
TXP = getOid(txp)
UNR = getOid(unr)
COR = getOid(cor)
UNC = getOid(unc)

print "MAC",MAC, cmIP, "DSFREQ:", dsFreq, "USFREQ:", usFreq, "PWR:", DSP, "SNR:", SNR, "TX PWR:", TXP, "Packets:",UNR, "Corrected", COR, "Uncorrected", UNC
print ""

getUpstreamErrors(MAC,"knock13")
