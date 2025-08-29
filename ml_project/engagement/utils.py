"""
Engagement ML Feature Engineering Utilities
Week 5: Data preparation and feature extraction
"""
import pandas as pd
import numpy as np
from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from .models import (
    User, UserSlideRead, UserSlideReadSession, 
    RevisionQuestionAttempt, RevisionQuestionAttemptDetail,
    WritingInteraction, TextbookPage, TextbookSlide
)

def clean_nulls(df):
    """Clean null values in the dataset"""
    # Fill numeric nulls with 0
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    # Fill categorical nulls with 'unknown'
    categorical_columns = df.select_dtypes(include=['object']).columns
    df[categorical_columns] = df[categorical_columns].fillna('unknown')
    
    return df

def aggregate_student_features(student_id, days_back=30):
    """Aggregate engagement features for a specific student"""
    end_date = timezone.now()
    start_date = end_date - timedelta(days=days_back)
    
    # Get student
    try:
        student = User.objects.get(id=student_id)
    except User.DoesNotExist:
        return None
    
    # 1. Time spent per slide
    slide_sessions = UserSlideReadSession.objects.filter(
        slide_read__user=student,
        expanded__gte=start_date
    )
    
    total_time_seconds = 0
    unique_slides = set()
    for session in slide_sessions:
        total_time_seconds += session.read_duration()
        unique_slides.add(session.slide_read.slide_id)
    
    time_spent_per_slide = total_time_seconds / len(unique_slides) if unique_slides else 0
    
    # 2. Average accuracy per page
    question_attempts = RevisionQuestionAttemptDetail.objects.filter(
        attempt__user=student,
        timestamp__gte=start_date
    )
    
    total_questions = question_attempts.count()
    correct_questions = question_attempts.filter(is_correct=True).count()
    average_accuracy_per_page = (correct_questions / total_questions) if total_questions > 0 else 0
    
    # 3. Attempt count per question
    attempts = RevisionQuestionAttempt.objects.filter(
        user=student,
        viewed__gte=start_date
    )
    
    total_attempts = attempts.count()
    unique_questions = attempts.values('question').distinct().count()
    attempt_count_per_question = total_attempts / unique_questions if unique_questions > 0 else 0
    
    # 4. Revisits (slides marked as 'revise')
    revisits = UserSlideRead.objects.filter(
        user=student,
        slide_status='revise'
    ).count()
    
    return {
        'student_id': student_id,
        'time_spent_per_slide': time_spent_per_slide,
        'average_accuracy_per_page': average_accuracy_per_page,
        'attempt_count_per_question': attempt_count_per_question,
        'revisits': revisits
    }

def build_dataset_csv(days_back=30, output_path='dataset.csv'):
    """Build complete dataset CSV from engagement data"""
    print(f"Building dataset for the last {days_back} days...")
    
    # Get all users with engagement data
    users_with_data = User.objects.filter(
        Q(revision_attempts__isnull=False) |
        Q(userslideread__isnull=False) |
        Q(id__in=WritingInteraction.objects.values_list('user_id', flat=True))
    ).distinct()
    
    print(f"Found {users_with_data.count()} users with engagement data")
    
    # Extract features for each user
    features_list = []
    for user in users_with_data:
        features = aggregate_student_features(user.id, days_back)
        if features:
            features_list.append(features)
    
    if not features_list:
        print("No features extracted. Check if engagement data exists.")
        return None
    
    # Convert to DataFrame
    df = pd.DataFrame(features_list)
    
    # Clean nulls
    df = clean_nulls(df)
    
    # Set target variable (y) - use time spent as score (since writing grades may not exist)
    df['score'] = df['time_spent_per_slide']
    
    # Remove rows where score is missing or 0
    df = df[df['score'] > 0].copy()
    
    # Select features for ML (X)
    feature_columns = [
        'time_spent_per_slide', 'average_accuracy_per_page', 'attempt_count_per_question',
        'revisits'
    ]
    
    # Ensure all feature columns exist
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    
    # Create final dataset
    X = df[feature_columns]
    y = df['score']
    
    # Add features and target to main dataframe
    final_df = df[['student_id'] + feature_columns + ['score']]
    
    # Save to CSV
    final_df.to_csv(output_path, index=False)
    
    print(f"Dataset saved to {output_path}")
    print(f"Shape: {final_df.shape}")
    print(f"Features: {feature_columns}")
    print(f"Target range: {y.min():.1f} - {y.max():.1f}")
    
    return final_df

def get_feature_importance(model, feature_names):
    """Extract feature importance from trained model"""
    if hasattr(model, 'feature_importances_'):
        importance_dict = dict(zip(feature_names, model.feature_importances_))
        return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
    return {}


