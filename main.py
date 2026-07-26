from src.pipeline.training_pipeline import TrainPipeline

if __name__ == "__main__":
    print("==================================================")
    print("      House Price Prediction Training Pipeline    ")
    print("==================================================")
    
    pipeline = TrainPipeline()
    metrics = pipeline.run_pipeline()
    
    print("\n==================================================")
    print("Training & Evaluation Pipeline Finished Successfully")
    print("Metrics:", metrics)
    print("==================================================")