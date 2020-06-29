from yapl.env import RunTime_Stack, Frame


# Test a symbol which does not exist
def test_sym_retrieval_DNE():
    f = Frame()

    # look up a non-existant symbol
    sym = f.resolve_sym("does_not_exist")
    assert sym == None


def test_sym_retrieval_exists():
    f = Frame()

    # look up an existing symbol
    f.add_symbol("sym", 4)
    sym = f.resolve_sym("sym")
    assert sym == 4

    # Test nested scope resolution
    f.enter_scope()
    sym = f.resolve_sym("sym")
    assert sym == 4

    # Test variable name shadowing
    f.add_symbol("sym", 13)
    sym = f.resolve_sym("sym")
    assert sym == 13


def test_scope_nesting():
    f = Frame()

    f.add_symbol("sym_a", 1)

    f.enter_scope()
    f.add_symbol("sym_b", 2)

    f.enter_scope()
    f.add_symbol("sym_c", 3)

    sym = f.resolve_sym("sym_c")
    assert sym == 3
    sym = f.resolve_sym("sym_b")
    assert sym == 2
    sym = f.resolve_sym("sym_a")
    assert sym == 1

    f.exit_scope()
    sym = f.resolve_sym("sym_c")
    assert sym == None
    sym = f.resolve_sym("sym_b")
    assert sym == 2
    sym = f.resolve_sym("sym_a")
    assert sym == 1

    f.exit_scope()
    sym = f.resolve_sym("sym_c")
    assert sym == None
    sym = f.resolve_sym("sym_b")
    assert sym == None
    sym = f.resolve_sym("sym_a")
    assert sym == 1

    f.exit_scope()
    sym = f.resolve_sym("sym_c")
    assert sym == None
    sym = f.resolve_sym("sym_b")
    assert sym == None
    sym = f.resolve_sym("sym_a")
    assert sym == None
