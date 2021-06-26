echo "git pull"
REM @ECHO OFF
PUSHD integration

echo "git pull is not applied because of naswork samba directory build"
echo " build automatically without git check"

EXIT 0

SET IS_DIRTY=n

CALL git reset --hard origin/master
CALL git pull | findstr /C:"Already up to date"
IF %ERRORLEVEL%==0 (
        SET RSTR="Git-Pull:Up-To-Date"
) ELSE (
        SET RSTR="Git-Pull:Something-Changed"
	SET IS_DIRTY=y
)
POPD
REM Git Update End
ECHO %RSTR%
IF %IS_DIRTY%==y (
	ECHO "Dirty Source"
	ECHO "Dirty Source" > dirty.txt
	EXIT 0
) ELSE (
	ECHO "Nothing to Build"
	EXIT 0
)
