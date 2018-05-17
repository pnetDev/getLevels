#!/usr/bin/python

## Need a way to convert a MAC address to dotted decimal.

## get the mac for 10.4.0.133
import netsnmp,sys,time
cmIP = "10.4.0.133"


def getOid(oid):
        session = netsnmp.Session( DestHost=cmIP, Version=2, Community='private' )
        vars = netsnmp.VarList( netsnmp.Varbind(oid) )
        #print( session.get(vars) )
        value  = ( session.get(vars) )
        #value = value.replace("(","") ; value = value.replace(")","") ; value = value.replace("'","") ; value = value.replace(",","") ## Clean up the string
        return  value


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
print MAC
