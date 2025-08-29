"""
Enhanced ML Training Script
Week 6: Train RandomForest model with comprehensive features
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib, json
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def train_model(dataset_path="dataset.csv", output_dir="."):
    """Train RandomForest model with comprehensive evaluation"""
    
    # Check if dataset exists
    if not os.path.exists(dataset_path):
        print(f"Error: Dataset file '{dataset_path}' not found!")
        print("Run 'python manage.py build_dataset' first to create the dataset.")
        return None
    
    print("Loading dataset...")
    df = pd.read_csv(dataset_path)
    
    # Validate dataset
    required_columns = ["score"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        print(f"Error: Missing required columns: {missing_columns}")
        return None
    
    print(f"Dataset loaded: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Prepare features (exclude student_id and score)
    feature_columns = [col for col in df.columns if col not in ['student_id', 'score']]
    X = df[feature_columns]
    y = df["score"]
    
    print(f"Features: {feature_columns}")
    print(f"Target range: {y.min():.1f} - {y.max():.1f}")
    
    # Handle missing values
    X = X.fillna(0)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=pd.cut(y, bins=5, labels=False)
    )
    
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set: {X_test.shape[0]} samples")
    
    # Initialize and train model
    model_params = {
        'n_estimators': 100,
        'max_depth': 10,
        'min_samples_split': 5,
        'min_samples_leaf': 2,
        'random_state': 42
    }
    
    print("Training RandomForest model...")
    model = RandomForestRegressor(**model_params)
    
    # Train on full training set
    model.fit(X_train, y_train)
    
    # Predictions
    y_pred = model.predict(X_test)
    
    # Calculate metrics
    metrics = {
        "mse": float(mean_squared_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred)),
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test))
    }
    
    # Feature importance
    feature_importance = dict(zip(feature_columns, model.feature_importances_))
    feature_importance = dict(sorted(feature_importance.items(), key=lambda x: x[1], reverse=True))
    
    # Print results
    print("\n" + "="*50)
    print("MODEL TRAINING RESULTS")
    print("="*50)
    print(f"Mean Squared Error: {metrics['mse']:.2f}")
    print(f"R² Score: {metrics['r2']:.3f}")
    
    print("\nFEATURE IMPORTANCE:")
    for feature, importance in feature_importance.items():
        print(f"  {feature}: {importance:.4f}")
    
    # Save model and metrics
    model_path = os.path.join(output_dir, "model.pkl")
    metrics_path = os.path.join(output_dir, "metrics.json")
    
    joblib.dump(model, model_path)
    print(f"\nModel saved to: {model_path}")
    
    with open(metrics_path, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"Metrics saved to: {metrics_path}")
    
    return model, metrics, feature_importance

if __name__ == "__main__":
    # Train model
    result = train_model()
    
    if result:
        print("\n" + "="*50)
        print("TRAINING COMPLETED SUCCESSFULLY!")
        print("="*50)
        print("Next steps:")
        print("1. Copy model.pkl to your Django project root")
        print("2. Restart your Django server")
        print("3. Test predictions at /engagement/predict/{student_id}/")
    else:
        print("\nTraining failed. Check the error messages above.")
        sys.exit(1)
