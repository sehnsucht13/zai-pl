from yapl.env import Scope, Environment


# Test a symbol which does not exist
def test_sym_retrieval_DNE():
    f = Scope(None)

    # look up a non-existant symbol
    sym = f.lookup_symbol("does_not_exist")
    assert sym == None


def test_scope_overwrite_sym():
    f = Scope(None)

    # look up an existing symbol
    f.add_symbol("sym", 4)
    sym = f.lookup_symbol("sym")
    assert sym == 4

    f.add_symbol("sym", 13)
    sym = f.lookup_symbol("sym")
    assert sym == 13


def test_scope_nesting():
    e = Environment()
    e.peek().add_symbol("sym_outer", 13)
    sym = e.peek().lookup_symbol("sym_outer")
    assert sym == 13

    e.enter_scope(e.peek())
    e.peek().add_symbol("sym_inner", 2)

    sym_inner = e.peek().lookup_symbol("sym_inner")
    assert sym_inner == 2
    sym_outer = e.peek().lookup_symbol("sym_outer")
    assert sym_outer == 13


def test_scope_shadowing():
    e = Environment()

    e.peek().add_symbol("sym", 13)

    e.enter_scope(e.peek())
    e.peek().add_symbol("sym", 2)

    sym = e.peek().lookup_symbol("sym")
    assert sym == 2
    e.exit_scope()
    sym = e.peek().lookup_symbol("sym")
    assert sym == 13
