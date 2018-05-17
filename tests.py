#!/usr/bin/python

 
from pysnmp.proto import v2
from pysnmp.proto.api import generic
from pysnmp.mapping.udp import role
req = v2.GetRequest()
req.apiGetPdu().apiSetVarBind([('1.3.6.1.2.1.1.1.0', None)])
tr = role.manager(('router-1.glas.net', 161))
(answer, src) = tr.send_and_receive(req.encode())
rsp = v1.GetResponse()
rsp.decode(answer)
vars = rsp.apiGetPdu().apiGetVarBind()
print vars
