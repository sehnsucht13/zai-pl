from zai.env import Scope, EnvironmentStack


# Test a symbol which does not exist
def test_sym_retrieval_DNE():
    f = Scope(None)

    # look up a non-existant symbol
    sym = f.get_variable("does_not_exist")
    assert sym is None


def test_scope_overwrite_sym():
    f = Scope(None)

    # look up an existing symbol
    f.initialize_variable("sym", 4)
    sym = f.get_variable("sym")
    assert sym == 4

    f.replace_variable("sym", 13)
    sym = f.get_variable("sym")
    assert sym == 13


def test_scope_nesting():
    e = EnvironmentStack()
    e.peek().initialize_variable("sym_outer", 13)
    sym = e.peek().get_variable("sym_outer")
    assert sym == 13

    e.enter_scope(e.peek())
    e.peek().initialize_variable("sym_inner", 2)

    sym_inner = e.peek().get_variable("sym_inner")
    assert sym_inner == 2
    sym_outer = e.peek().get_variable("sym_outer")
    assert sym_outer == 13


def test_scope_shadowing():
    e = EnvironmentStack()

    e.peek().initialize_variable("sym", 13)

    e.enter_scope(e.peek())
    e.peek().initialize_variable("sym", 2)

    sym = e.peek().get_variable("sym")
    assert sym == 2
    e.exit_scope()
    sym = e.peek().get_variable("sym")
    assert sym == 13
