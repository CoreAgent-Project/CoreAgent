AIML
====

## What is AIML? 
AIML in this project is not the old 1900s AIML.
AIML is a new protocol format for LLMs. 

## Why AIML?
Communicating with JSON is not very human friendly, thus LLM can be bad at generating JSON. 

Especially when generating JSON with a lot of nested objects or code. 

Thus, we hereby invented AIML, a protocol format for LLMs that can easily be handled and to be generated. 

## Format
```
%$key=>_
... value here ...
Anything can be put. 
%$_<
$$EOF$$
```
### About `%$namespace:key=>_`
This indicates a new field. 
### About `%$_<`
This indicates the end of the field. 
### About `$$EOF$$`
This indicates the end of the packet. 

## GBNF Format
AIML can be easily controlled by a GBNF format generation conditioner. 
```
text-line ::= "%$_<"{0} [^\\n]* "%$_<"{0} newline
```
Note here we used `{0}` smartly to prevent generating unwanted packet reserved strings. 
