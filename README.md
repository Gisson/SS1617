# SS1617

A static analysis tool written in Python for identifying data flow integrity violations in PHP code.

## Dependencies

- [PLY](http://www.dabeaz.com/ply/) (Python Lex-Yacc):

  ```bash
  pip install ply
  ```
  Make sure it's installed for the correct python version.
  
- [phply](https://github.com/viraptor/phply) (Python PHP parser)

  ```bash
  git clone --depth 1 https://github.com/viraptor/phply.git
  export PYTHONPATH="$PYTHONPATH:$(pwd)/phply"
  ```

