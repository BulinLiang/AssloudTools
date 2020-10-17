@echo off

if exist _output RD /Q/S _output
MD _output

set make_dir=%CD%

cd _package

%make_dir%\7z\7z.exe a %make_dir%\_output\app.7z .\*
cd %make_dir%\data\skin
%make_dir%\7z\7z.exe a %make_dir%\_output\skin.zip .\*
cd %make_dir%
%make_dir%\nsis\makensis.exe %make_dir%\data\app.nsi

DEL /Q "%make_dir%\_output\app.7z"
DEL /Q "%make_dir%\_output\skin.zip"
