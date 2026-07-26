from src.pipeline.prediction_pipeline import CustomData, PredictPipeline

if __name__ == "__main__":
    print("Testing Prediction Pipeline...")

    sample_house = CustomData(
        bedrooms=3,
        bathrooms=2.25,
        sqft_living=2000,
        sqft_lot=7500,
        floors=2.0,
        waterfront=0,
        view=0,
        condition=4,
        sqft_above=1600,
        sqft_basement=400,
        yr_built=1985,
        yr_renovated=2010,
        city="Bellevue",
        zipcode="98008",
    )

    df = sample_house.get_data_as_data_frame()
    pipeline = PredictPipeline()
    price = pipeline.predict(df)

    print("\n==============================================")
    print(f"Sample Property Location : Bellevue, WA 98008")
    print(f"Predicted House Price   : ${price:,.2f}")
    print("==============================================")