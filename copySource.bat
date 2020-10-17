@echo off  
  
:: BatchGotAdmin  获取管理员权限
:-------------------------------------  
REM  --> Check for permissions  
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"  
  
REM --> If error flag set, we do not have admin.  
if '%errorlevel%' NEQ '0' (  
:echo Requesting administrative privileges...  
    goto UACPrompt  
) else ( goto gotAdmin )  
  
:UACPrompt  
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"  
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"  
  
    "%temp%\getadmin.vbs"  
    exit /B  
  
:gotAdmin  
    if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )  
    pushd "%CD%"  
    CD /D "%~dp0"  
:--------------------------------------
if not exist E:\MeeX\MeeX mkdir E:\MeeX\MeeX
echo ---------------COPY PROGRAM---------------
xcopy /E "C:\MeeX\Hub\MeeTouch\_x64_1.16.1" "E:\MeeX\MeeX\Hub\MeeTouch\_x64_1.16.1"

echo ---------------COPY DATA---------------
xcopy /E "G:\MeeX\红色公益平台\MeeTouch_Data" "E:\MeeX\MeeX\红色公益平台\MeeTouch_Data"

echo ---------------COPY ASSET---------------
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (1)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (1)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (100)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (100)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (101)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (101)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (109)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (109)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (1)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (1)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (100)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (100)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud功能\SourceFile\Assloud\bundle\tech.meex.culture.red\12_朱德 (1)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_朱德 (1)"


echo -------------------------------------
echo !                                   
echo !   安装完成，可以关闭此窗口          
echo !                                   
echo -------------------------------------
pause
