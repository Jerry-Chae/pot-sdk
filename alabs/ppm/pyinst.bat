REM PYTHON installer for PPM

REM XCOPY argos-pbtail\argos-pbtail\bin\Release pyinst\Release /O /X /E /H /K
REM ..\..\..\src-vault\sign\sign.bat pyinst\Release\argos-pbtail.exe


REM    --add-data README.md;README.md ^
REM    --add-data LICENSE.txt;LICENSE.txt ^
REM    --add-data requirements.txt;requirements.txt ^
REM    --add-data setup.yaml;setup.yaml ^

DEL /Q/S exe
DEL /Q/S build
DEL /Q/S dist

REM sign.bat

COPY __main__.py alabs-ppm.py

REM     --onefile ^
REM    __main__.py
rem    --uac-admin ^

pyinstaller ^
    --add-data pyinst;. ^
    --add-data setup.yaml;. ^
    --onefile ^
    alabs-ppm.py

if %ERRORLEVEL% == 0 goto :next2
    echo "Errors encountered during pyinstaller.  Exited with status: %errorlevel%"
    goto :endofscript
:next2

mkdir exe
REM move __pycache__ exe
REM move build exe
REM move dist exe
MOVE dist\alabs-ppm exe

..\..\..\src-vault\sign\sign.bat dist\alabs-ppm.exe

REM for test
REM COPY exe\dist\alabs-ppm.exe C:\work\ppm\ppm.exe

DEL /Q/S build
DEL /Q/S dist

:endofscript
echo "Script complete"
