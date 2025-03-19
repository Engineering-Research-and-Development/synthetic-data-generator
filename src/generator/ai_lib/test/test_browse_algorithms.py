from ai_lib.browse_algorithms import browse_algorithms

def test_browse_algorithms():
    base_package = "ai_lib.data_generator.models."
    for desc in browse_algorithms(model_package=base_package):
        assert desc is not None

def test_browse_algorithms_wrong():
    base_package = "ai_lib.data_generator.does_not_exist."
    for not_found in browse_algorithms(model_package=base_package):
        assert not_found is None