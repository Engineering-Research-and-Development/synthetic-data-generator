from ai_lib.browse_algorithms import browse_algorithms


def test_browse_algorithms():
    for desc in browse_algorithms():
        assert desc is not None