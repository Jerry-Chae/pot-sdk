REM @echo off

REM 1) pip install
pip install PyYAML


REM 2) move shell folder
PUSHD %~dp0
set WDIR=%CD%
echo "working directory for build_all is \"%WDIR%\""

REM 3) first do alabs.ppm
set dirname=%WDIR%\alabs\ppm
set bf=%dirname%\build.bat
python.exe %WDIR%\change_version.py -n %dirname%\setup.yaml
pushd %dirname%
	CALL build.bat
popd
echo "Build %dirname% is done!"

REM 4) next do alabs.common
set dirname=%WDIR%\alabs\common
set bf=%dirname%\build.bat
python.exe %WDIR%\change_version.py -n %dirname%\setup.yaml
pushd %dirname%
	CALL build.bat
popd
echo "Build %dirname% is done!"

REM 5) bf has each build.bat and do
for /f "tokens=*" %%a in ('dir /s/b build.bat') do call :processline %%a

goto :eof

REM 6) %bf% has the build.sh path
:processline
	set bf=%*
	echo %bf%
	for %%F in (%bf%) do set dirname=%%~dpF
	echo ">>> dirname=<%dirname%>"
	echo ">>> WDIR=<%WDIR%>"
	set "IS_BUILD="
	if "%dirname%"=="%WDIR%\alabs\ppm\" set IS_BUILD=1
	if "%dirname%"=="%WDIR%\alabs\common\" set IS_BUILD=1
	if defined IS_BUILD (
		echo "Already built, skip Building %dirname% is done!"
	) else (
		echo "building %dirname% ..."
		python.exe %WDIR%\change_version.py -n %dirname%\setup.yaml
		pushd %dirname%
			CALL build.bat
		popd
		echo "Build %dirname% is done!"
	)
	goto :eof
:eof
POPD
