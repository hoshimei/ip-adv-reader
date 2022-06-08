## ip_adv_reader

A project to read IDOLY PRIDE script files.

### Dependencies

* Python 3
* GNU Make
  * You can also run the scripts in the `Makefile` manually
* [ANTLR4](https://github.com/antlr/antlr4) and its Python binding 
  * Arch Linux: `pacman -S antlr4 python-antlr4`

### Usage

``` sh
make python
# If you don't have GNU Make:
# antlr4 -Dlanguage=Python3 *.g4
cat adv_group_tri_01_01.txt | python main.py | python target_to_object.py > object.json
```

### Limitations
* Cannot handle spaces within KV values.

### Tests

Put adv scripts to `./adv` and run `test_all.sh`.


### License

AGPLv3