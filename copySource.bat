@echo off  
  
:: BatchGotAdmin  ��ȡ����ԱȨ��
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
xcopy /E "G:\MeeX\��ɫ����ƽ̨\MeeTouch_Data" "E:\MeeX\MeeX\��ɫ����ƽ̨\MeeTouch_Data"

echo ---------------COPY ASSET---------------
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (1)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (1)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (100)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (100)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (101)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (101)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (109)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (109)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (1)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (1)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (100)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (100)"
xcopy /E "C:\Users\Administrator\Desktop\Assloud����\SourceFile\Assloud\bundle\tech.meex.culture.red\12_��� (1)" "E:\MeeX\Assloud\MeeX\bundle\tech.meex.culture.red\12_��� (1)"


echo -------------------------------------
echo !                                   
echo !   ��װ��ɣ����Թرմ˴���          
echo !                                   
echo -------------------------------------
pause
