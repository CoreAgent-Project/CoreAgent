ProtoLang
=========

## What is `ProtoLang`? 
ProtoLang is based on AIML format, it defines a packet structure for CoreAgent to operate with. 

## `RESPOND` Format
`RESPOND` is used when the agent needs to respond to the peer. 
```
%$action=>_
RESPOND
%$_<
%$respond=>_
Some text or specific format. 
%$_<
$$EOF$$
```

## `TOOLCALL` Format
`TOOLCALL` is used when the agent needs to call a registered tool. 
```
%$action=>_
TOOLCALL
%$_<
%name=>_
toolname.method
%$_<
%$param:some_param=>_
param value here
%$_<
%$param:y=>_
123
%$_<
...
$$EOF$$
```

## GBNF Generation
CoreAgent utilizes smart GBNF generation to ensure correct packet structure generation by the LLM. 

Please check out `./coreagent/communication/gbnf_gen.py` for more details. 



