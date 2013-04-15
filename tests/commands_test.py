from ado.commands import abbrev
from ado.commands import const_key
from ado.commands import db_filepath
from ado.commands import setting
from ado.portfolio import Portfolio
import os

def test_abbrev():
    assert abbrev("f") == Portfolio

    try:
        abbrev("x")
        assert False, "should raise error"
    except SystemExit:
        pass

def test_const_key():
    assert const_key("foo-bar") == "FOO_BAR"

def test_setting():
    assert setting("default-command") == "projects"
    os.environ['DEFAULT_COMMAND'] = 'foo'
    assert setting("default-command") == "foo"

def test_db_filepath():
    assert "/ado.sqlite3" in db_filepath
