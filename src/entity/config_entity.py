from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    input_data_path: Path
    raw_data_path: Path
    train_data_path: Path
    test_data_path: Path


@dataclass(frozen=True)
class DataValidationConfig:
    root_dir: Path
    STATUS_FILE: Path
    unzip_data_dir: Path
    all_schema: Path

@dataclass(frozen=True)
class DataTransformationConfig:
    root_dir: Path
    preprocessor_obj_file_path: Path

@dataclass(frozen=True)
class ModelTrainerConfig:
    root_dir: Path
    trained_model_file_path: Path

@dataclass(frozen=True)
class ModelEvaluationConfig:
    root_dir: Path
    metric_file_name: Path