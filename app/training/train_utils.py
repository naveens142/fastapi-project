import os

# Data file lives under app/notebooks in this repository
DATA_FILE_NAME = 'car-details.csv'
DATA_FILE_PATH = os.path.abspath(
	os.path.join(os.path.dirname(__file__), '..', 'notebooks', DATA_FILE_NAME)
)

APP_DIR = 'app'
MODEL_DIR_NAME = 'models'
MODEL_NAME = 'model.joblib'
MODEL_DIR = os.path.join(APP_DIR, MODEL_DIR_NAME)
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_NAME)