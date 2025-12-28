#!/bin/bash

echo "🚀 Resetting Django environment..."

# 1. Remove old virtual environment
rm -rf venv
echo "✅ Removed old venv"

# 2. Remove old database (SQLite)
rm -f db.sqlite3
echo "✅ Removed old database"

# 3. Remove all migration files except __init__.py
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
echo "✅ Cleared old migrations"

# 4. Remove all __pycache__ directories
find . -type d -name "__pycache__" -exec rm -rf {} +
echo "✅ Cleared __pycache__"

# 5. Create new virtual environment
python3 -m venv venv
echo "✅ Created new virtual environment"

# 6. Activate venv
source venv/bin/activate

# 7. Upgrade pip
pip install --upgrade pip

# 8. Install Django and dependencies
pip install Django==4.2.27 pillow python-dotenv celery
echo "✅ Installed Django and dependencies"

# 9. Make new migrations
python manage.py makemigrations
echo "✅ Made new migrations"

# 10. Apply migrations
python manage.py migrate
echo "✅ Applied migrations"

# 11. Create superuser
echo "🛑 Now create a superuser manually: python manage.py createsuperuser"

echo "🎉 Environment reset complete!"
