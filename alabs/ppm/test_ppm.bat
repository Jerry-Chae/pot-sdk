REM test ppm

set PPM=exe\dist\alabs-ppm.exe
echo "Test set using %PPM%"

GOTO :GOTO_HERE

echo test_0035_clear_all
%PPM% clear-all
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo test_0040_build
%PPM% --venv -v build
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo test_0055_submit_with_key
REM %PPM% submit --submit-key aL0PK2Rhs6ed0mgqLC42
REM if %ERRORLEVEL% NEQ 0 goto :errorscript

echo test_0060_upload
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv --venv upload
REM if %ERRORLEVEL% NEQ 0 goto :errorscript

REM :GOTO_HERE

echo "test_0120_get"
%PPM% get repository
%PPM% get trusted-host

echo "test_0150_list"
%PPM% -vv list
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0160_list_self_upgrade"
%PPM% --self-upgrade -vv list
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0300_search"
%PPM% -vv search argoslabs
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0310_list_repository"
%PPM% list-repository
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0390_plugin_versions"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin versions argoslabs.demo.helloworld
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0400_plugin_get_all_short_output"
%PPM% plugin get --short-output --official-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0405_plugin_get_all_short_output"
%PPM% plugin get --short-output --flush-cache
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0410_plugin_get_all"
%PPM% plugin get
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0420_plugin_versions"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin versions argoslabs.demo.helloworld
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0430_plugin_get_module"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin get argoslabs.demo.helloworld
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0440_plugin_get_module_with_version"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin get argoslabs.demo.helloworld==1.424.2255
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0470_plugin_get_all_only_official"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin get --official-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0475_plugin_get_all_only_official_with_dumpspec"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin get --official-only --with-dumpspec
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0480_plugin_get_all_only_official_last_only"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin get --official-only --last-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0490_plugin_dumpspec_all_only_official"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin get --official-only --last-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0500_plugin_dumpspec_all_only_official_with_last_only"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin dumpspec --official-only --last-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0510_plugin_dumpspec_all_only_private"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin dumpspec --private-only --last-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0550_plugin_dumpspec_user_official"
REM %PPM% plugin dumpspec --official-only --last-only --user mcchae@gmail.com --user-auth "Bearer 7484d5ea-4213-49fa-a35d-e31ea6bdf3a7"
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0560_plugin_dumpspec_user_official"
REM %PPM% --pr-user mcchae@gmail.com --pr-user-auth "Bearer 7484d5ea-4213-49fa-a35d-e31ea6bdf3a7" plugin dumpspec --official-only
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0570_get_with_private_repository"
REM %PPM% --pr-user mcchae@gmail.com --pr-user-auth "Bearer 7484d5ea-4213-49fa-a35d-e31ea6bdf3a7" get private
if %ERRORLEVEL% NEQ 0 goto :errorscript

REM :GOTO_HERE

echo "test_0600_plugin_venv_clear"
del /Q/S %USERPROFILE%\.argos-rpa.venv\2019*
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin versions argoslabs.data.fileconv
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0700_pip_install"
%PPM% pip install argoslabs.google.tts --index https://pypi-official.argos-labs.com/pypi --trusted-host pypi-official.argos-labs.com --extra-index-url https://pypi-test.argos-labs.com/simple --trusted-host pypi-test.argos-labs.com --extra-index-url https://pypi-demo.argos-labs.com/simple --trusted-host pypi-demo.argos-labs.com
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0605_plugin_venv_success"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin venv argoslabs.google.tts
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0610_plugin_venv_success"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin venv argoslabs.data.fileconv
if %ERRORLEVEL% NEQ 0 goto :errorscript

echo "test_0620_plugin_venv_success"
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin venv argoslabs.data.fileconv==1.515.1506
if %ERRORLEVEL% NEQ 0 goto :errorscript

:GOTO_HERE

echo "0680"
REM %PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin venv argoslabs.time.workalendar==1.830.2039
%PPM% --pr-user mcchae@gmail.com --pr-user-pass ghkd67vv plugin venv argoslabs.data.binaryop
if %ERRORLEVEL% NEQ 0 goto :errorscript


:endofscript
echo "Script complete"

:errorscript
echo "Error of Script"
