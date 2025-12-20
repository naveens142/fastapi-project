import joblib
import pandas as pd
import warnings
import logging
from app.core.config import settings
from app.cache.redis_cache import set_cached_prediction, get_cached_prediction

_model = None


def load_model():
    """Lazily load the model. If scikit-learn reports a version mismatch,
    log a warning but continue to load the model to keep runtime behaviour
    smooth for now.
    """
    global _model
    if _model is not None:
        return _model

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        _model = joblib.load(settings.MODEL_PATH)
        for w in caught:
            # Avoid importing sklearn-specific classes here; check by name.
            if getattr(w.category, "__name__", "").endswith("InconsistentVersionWarning"):
                logging.warning(
                    "Saved model was created with a different scikit-learn "
                    "version and may be incompatible. Retrain the model or "
                    "restore the original scikit-learn version. Warning: %s",
                    w.message,
                )

    return _model


def predict_car_price(data: dict):
    cache_key = " ".join([str(val) for val in data.values()])
    cached = get_cached_prediction(cache_key)
    if cached:
        return cached

    model = load_model()
    input_data = pd.DataFrame([data])
    prediction = model.predict(input_data)[0]
    set_cached_prediction(cache_key, prediction)
    return prediction