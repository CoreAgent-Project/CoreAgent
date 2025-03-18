protolang_specs = """PROTOLANG RESPOND packet: 
```aiml
%$summary=>_
... Textual explanation about your current action...  
%$_<
%$action=>_
RESPOND
%$_<
%$respond=>_
Some text...
%$_<
$$EOF$$ 
```
or
```aiml
%$summary=>_
I need to ... 
%$_<
%$action=>_
RESPOND
%$_<
%$respond=>_
Some long text...
with multiple lines... 
%$_< 
$$EOF$$
```

Example PROTOLANG TOOLCALL (must have `name` param) packet: 
```aiml
%$summary=>_
I need to ... 
%$_<
%$action=>_
TOOLCALL
%$_<
%$name=>_
tool_name
%$_<
%$param:param_name=>_
param value
%$_<
%$param:example_string_block=>_
(multi-line string)
... Parameter is just a string block, can contain anything. 
%$_<
%$param:2=>_
123
%$_<
%$param:good=>_
true
%$_<
$$EOF$$
```
(note: function parameters in "param" namespace. )
(note: if no parameters required, you don't have to specify any. )
(note: make sure NO "%$" exists in a string! )
"""
