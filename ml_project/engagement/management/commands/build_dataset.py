"""
Django management command to build ML dataset from engagement data
Week 5: Data preparation automation
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import os
from engagement.utils import build_dataset_csv

class Command(BaseCommand):
    help = 'Build ML dataset CSV from engagement data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days to look back for engagement data (default: 30)'
        )
        parser.add_argument(
            '--output',
            type=str,
            default='dataset.csv',
            help='Output CSV file path (default: dataset.csv)'
        )

    def handle(self, *args, **options):
        days_back = options['days']
        output_path = options['output']
        
        self.stdout.write(
            self.style.SUCCESS(f'Building dataset for the last {days_back} days...')
        )
        
        try:
            # Build dataset
            dataset = build_dataset_csv(days_back, output_path)
            
            if dataset is not None:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Dataset successfully created at {output_path}\n'
                        f'Shape: {dataset.shape}\n'
                        f'Features: {list(dataset.columns[:-2])}  # Excluding student_id and score\n'
                        f'Target range: {dataset["score"].min():.1f} - {dataset["score"].max():.1f}'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING('No dataset created. Check if engagement data exists.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error building dataset: {str(e)}')
            )
            raise
