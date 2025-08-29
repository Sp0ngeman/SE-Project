"""
Django management command to retrain ML model weekly
Week 8: Automation and model maintenance
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os
import sys
from pathlib import Path

class Command(BaseCommand):
    help = 'Retrain ML model with latest engagement data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force retraining even if no new data'
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to look back for engagement data (default: 30)'
        )

    def handle(self, *args, **options):
        force = options['force']
        days_back = options['days']
        
        self.stdout.write(
            self.style.SUCCESS(f'Starting weekly model retraining (last {days_back} days)...')
        )
        
        try:
            # Build new dataset
            from engagement.utils import build_dataset_csv
            dataset = build_dataset_csv(days_back, 'dataset_retrain.csv')
            
            if dataset is None:
                self.stdout.write(
                    self.style.WARNING('No new data available for retraining.')
                )
                if not force:
                    return
                else:
                    self.stdout.write('Force flag set, continuing with existing data...')
            
            # Train new model
            project_root = Path(settings.BASE_DIR).parent
            ml_model_dir = project_root / 'ml_model'
            
            if not ml_model_dir.exists():
                self.stdout.write(
                    self.style.ERROR('ML model directory not found. Please check project structure.')
                )
                return
            
            # Change to ml_model directory and run training
            os.chdir(ml_model_dir)
            
            # Import and run training
            sys.path.append(str(ml_model_dir))
            from train import train_model
            
            self.stdout.write('Training new model...')
            result = train_model('dataset_retrain.csv', '.')
            
            if result:
                model, metrics, feature_importance = result
                
                # Copy new model to Django project root
                import shutil
                django_root = Path(settings.BASE_DIR)
                new_model_path = django_root / 'model.pkl'
                new_metrics_path = django_root / 'metrics.json'
                
                shutil.copy('model.pkl', new_model_path)
                shutil.copy('metrics.json', new_metrics_path)
                
                # Clean up temp files
                os.remove('dataset_retrain.csv')
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Model retraining completed successfully!\n'
                        f'New model saved to: {new_model_path}\n'
                        f'R² Score: {metrics["r2"]:.3f}\n'
                        f'RMSE: {metrics["rmse"]:.2f}'
                    )
                )
                

                
            else:
                self.stdout.write(
                    self.style.ERROR('Model retraining failed.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error during retraining: {str(e)}')
            )
            raise
