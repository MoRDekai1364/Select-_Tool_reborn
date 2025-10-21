@echo off
setlocal

:: Set the title for the command window
title GitHub Update Script for Select+

:: --- Main Script ---
echo =======================================================
echo  GitHub Quick Update for Select+
echo =======================================================
echo.

:: Check if the current directory is a Git repository
if not exist ".git" (
    echo [ERROR] This is not a Git repository.
    echo Please run this script from the root of your project folder.
    echo.
    pause
    exit /b 1
)

:: Prompt the user for a commit message
echo Please enter a short description of the changes you made.
set /p commit_message="Commit Message: "

:: Check if the commit message is empty
if "%commit_message%"=="" (
    echo.
    echo [WARNING] Commit message cannot be empty.
    echo Using default message: "Update project files"
    set "commit_message=Update project files"
)

echo.
echo =======================================================
echo.

:: Step 1: Stage all changes (new, modified, and deleted files)
echo [1/3] Staging all changes...
git add .
echo [SUCCESS] All files staged.
echo.

:: Step 2: Commit the changes with the user's message
echo [2/3] Committing changes with message: "%commit_message%"
git commit -m "%commit_message%"
if %errorlevel% neq 0 (
    echo.
    echo [INFO] It seems there were no new changes to commit.
    echo Nothing to push. Exiting.
    echo.
    pause
    exit /b 0
)
echo [SUCCESS] Changes committed locally.
echo.

:: Step 3: Push the commit to the remote repository on GitHub
echo [3/3] Pushing changes to GitHub...
git push origin HEAD
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to push changes to GitHub.
    echo Please check your internet connection, credentials, and repository URL.
    echo.
    pause
    exit /b 1
)
echo [SUCCESS] Your repository on GitHub has been updated!
echo.

echo =======================================================
echo  Update Complete.
echo =======================================================
echo.
pause
