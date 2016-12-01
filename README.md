# SS1617

A static analysis tool written in Python for identifying data flow integrity violations in PHP code.

## Dependencies

- [phply](https://github.com/viraptor/phply) (Python PHP parser)

  ```bash
  git clone --depth 1 https://github.com/viraptor/phply.git
  export PYTHONPATH="$PYTHONPATH:$(pwd)/phply"
  ```


  - [PLY](http://www.dabeaz.com/ply/) (Python Lex-Yacc) (needed by `phply`):

    ```bash
    pip install ply
    ```
    Make sure it's installed for the correct python version.

## Data structures

The data structure used is rule. This class has attributes name (name of the rule), entry_point ( a possible entry point of a vulnerability), validation (the validation function used for the vulnerability) and lastly a sink (the sink of the problem, where the vulnerability can be executed). All these attributes but the name one are lists which are all the attributes encontered in a config file which is read by the analyzer. This attributes if more than 1 are divided by commas (,). See more about config files on the examples at the tests folder.

```
	list(struct:rule(string:name,list:entry_point,list:validation,list:sink))
```
