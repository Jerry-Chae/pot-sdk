
pyinstaller ^
    --onefile ^
    mvenv.py

if %ERRORLEVEL% == 0 goto :next2
    echo "Errors encountered during pyinstaller.  Exited with status: %errorlevel%"
    goto :endofscript
:next2

:endofscript
echo "Script complete"
