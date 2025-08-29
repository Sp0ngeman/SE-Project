# Django ML Engagement Project

This is a Django-based application that imports student engagement data, trains an ML model to predict performance, and provides a dashboard for analysis.

## Features

- **Data Import**: Import engagement data from textbook API
- **Data Models**: Comprehensive models for sections, pages, slides, questions, and user interactions
- **ML Pipeline**: Random Forest model for predicting student scores
- **Admin Interface**: Django admin for data management
- **API Endpoints**: RESTful endpoints for predictions and data access
- **Dashboard**: Web interface for data visualization

## Quick Start

### 1. Setup Environment
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application
```bash
# Make migrations and apply them
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

### 3. Access the Application
- **Main App**: http://127.0.0.1:8000/engagement/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Prediction API**: http://127.0.0.1:8000/engagement/predict/{student_id}/

## Project Structure

```
ml_project/
├── engagement/          # Main Django app
│   ├── models.py       # Data models
│   ├── views.py        # Business logic
│   ├── admin.py        # Admin interface
│   ├── urls.py         # URL routing
│   └── templates/      # HTML templates
├── ml_model/           # ML training scripts
│   ├── train.py        # Model training
│   └── dataset.csv     # Sample data
├── tests/              # Test files
└── docs/               # Documentation
```

## Data Models

- **TextbookSection**: Textbook sections
- **TextbookPage**: Pages within sections
- **TextbookSlide**: Slides within pages
- **RevisionQuestion**: Questions on pages
- **RevisionQuestionAttempt**: User attempts at questions
- **WritingInteraction**: User writing interactions
- **UserSlideRead**: User reading progress
- **UserSlideReadSession**: Reading session details

## ML Model

The system uses a Random Forest Regressor to predict student scores based on:
- Time spent on content
- Accuracy of answers
- Number of attempts
- Number of revisits

### Training the Model
```bash
cd ml_model
python train.py
```

This will:
1. Load data from `dataset.csv`
2. Train a Random Forest model
3. Save the model as `model.pkl`
4. Generate performance metrics

## API Endpoints

### Prediction Endpoint
```
GET /engagement/predict/{student_id}/
```
Returns predicted score for a student.

### Import Endpoint
```
POST /engagement/manual-import/
```
Imports engagement data from external API.

## Testing

Run the test suite:
```bash
cd ml_project
python -m pytest ../tests/ -v
```

## Configuration

Key settings in `ml_project/settings.py`:
- `INSTALLED_APPS`: Includes 'engagement' app
- `ALLOWED_HOSTS`: Set to ['127.0.0.1', 'localhost']

## Dependencies

- Django 4.2+
- scikit-learn 1.5+
- pandas 2.2+
- requests 2.31+
- pytest 8.0+

## Troubleshooting

1. **Server won't start**: Ensure virtual environment is activated
2. **Import errors**: Check that all dependencies are installed
3. **Database errors**: Run migrations with `python manage.py migrate`
4. **ML model errors**: Ensure `model.pkl` exists in project root

## Development

To extend the project:
1. Add new models in `engagement/models.py`
2. Create views in `engagement/views.py`
3. Update admin interface in `engagement/admin.py`
4. Add URL patterns in `engagement/urls.py`
5. Create templates in `engagement/templates/`

## License

This project is for educational purposes as part of the Term 3 Software Engineering course.
