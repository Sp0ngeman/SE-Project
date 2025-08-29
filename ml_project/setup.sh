#!/bin/bash

echo "Setting up Django ML Engagement Project..."

# Check if virtual environment exists
if [ ! -d "../venv" ]; then
    echo "Creating virtual environment..."
    cd ..
    python3 -m venv venv
    cd ml_project
fi

# Activate virtual environment
echo "Activating virtual environment..."
source ../venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r ../requirements.txt

# Make migrations
echo "Creating database migrations..."
python manage.py makemigrations

# Apply migrations
echo "Applying migrations..."
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser (admin/admin)..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

# Train ML model
echo "Training ML model..."
cd ../ml_model
python train.py
cd ../ml_project

# Copy model to project directory
echo "Setting up ML model..."
cp ../ml_model/model.pkl .

echo ""
echo "Setup complete! 🎉"
echo ""
echo "To start the server:"
echo "  source ../venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  - http://127.0.0.1:8000/engagement/ (main app)"
echo "  - http://127.0.0.1:8000/admin/ (admin interface, login: admin/admin)"
echo ""
