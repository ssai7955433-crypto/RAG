from core.model_selector import detect_ollama_models, get_model_recommendation, select_model


def test_detect_ollama_models_handles_missing_service():
    status, state, models = detect_ollama_models()
    assert state in {"not_connected", "ok"}
    assert isinstance(models, list)


def test_get_model_recommendation_returns_tuple():
    model_name, family = get_model_recommendation()
    assert isinstance(model_name, str)
    assert isinstance(family, str)


def test_select_model_returns_tuple():
    model_name, family, message = select_model()
    assert model_name is None or isinstance(model_name, str)
    assert family is None or isinstance(family, str)
    assert message is None or isinstance(message, str)
