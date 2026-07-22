from src.components.data_ingestion import DataIngestion

if __name__ == "__main__":
    obj = DataIngestion()
    train_path, test_path = obj.initiate_data_ingestion()

    print("Train File:", train_path)
    print("Test File:", test_path)