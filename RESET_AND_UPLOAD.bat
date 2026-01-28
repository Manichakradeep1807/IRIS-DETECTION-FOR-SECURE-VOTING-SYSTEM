@echo off
echo Cleaning old git history...
rmdir /s /q .git

echo Initializing new repository...
git init

echo Ignoring large files...
echo *.h5 >> .gitignore
echo *.weights.h5 >> .gitignore

echo Adding files...
git add .

echo Committing...
git commit -m "Final Release"

echo Linking remote...
git branch -M main
git remote add origin https://github.com/Manichakradeep1807/IRIS-DETECTION-FOR-SECURE-VOTING-SYSTEM.git

echo Uploading (Force Push)...
git push -u -f origin main
pause
