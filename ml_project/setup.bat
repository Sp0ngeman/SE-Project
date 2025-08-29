@echo off
echo Setting up Django ML Engagement Project...

REM Check if virtual environment exists
if not exist "..\venv" (
    echo Creating virtual environment...
    cd ..
    python -m venv venv
    cd ml_project
)

REM Activate virtual environment
echo Activating virtual environment...
call ..\venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r ..\requirements.txt

REM Make migrations
echo Creating database migrations...
python manage.py makemigrations

REM Apply migrations
echo Applying migrations...
python manage.py migrate

REM Create superuser if it doesn't exist
echo Creating superuser (admin/admin)...
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin') if not User.objects.filter(username='admin').exists() else None | python manage.py shell

REM Train ML model
echo Training ML model...
cd ..\ml_model
python train.py
cd ..\ml_project

REM Copy model to project directory
echo Setting up ML model...
copy ..\ml_model\model.pkl .

echo.
echo Setup complete! 🎉
echo.
echo To start the server:
echo   ..\venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then visit:
echo   - http://127.0.0.1:8000/engagement/ (main app)
echo   - http://127.0.0.1:8000/admin/ (admin interface, login: admin/admin)
echo.
pause
