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
    Make sure it's installed for the correct python version. To do run the command `pip show ply` and check the Location field.

## Running the project

Make sure all the dependencies are properly installed. Then, try analysing one of the sample files:
```bash
cd src
./analyzer.py ../tests/sqli_02.php 2>/dev/null
```
`2>/dev/null` disables debug messages.

It should output something like:
```txt
> Tainted sink for SQL injection in line 3:
$hasil=mysql_query($q_sems,$koneksi);
```

Another example:
```bash

./analyzer.py ../tests/qli_02_sanitized.php 2>/dev/null
```

Should output something like:
```txt
> Sanitization function for SQL injection in line 2:
$nis=mysql_real_escape_string($nis);
```

## Data structures

The data structure used is `rule`. This structure has attributes `name` (name of the rule), `entry_point` ( a possible entry point of a vulnerability), `validation` (the validation function used for the vulnerability) and lastly a `sink` (the sink of the problem, where the vulnerability can be executed). All these attributes but the name one are lists which are all the attributes encontered in a config file which is read by the analyzer. This attributes if more than 1 are divided by commas (,). See more about config files on the examples at the [tests folder](https://github.com/Gisson/SS1617/tree/master/tests).

```
	list(struct:rule(string:name,list:entry_point,list:validation,list:sink))
```
