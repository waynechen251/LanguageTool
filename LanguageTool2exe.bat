@echo off
@color 0a

CD /D "%~dp0"

echo ==��spip==
python.exe -m pip install --upgrade pip
echo ===========

echo ==�w��pyinstaller==
pip install pyinstaller
echo ===========

echo ==�R�����]�Ȧs��==
rd /Q /S __pycache__\
rd /Q /S build\
rd /Q /S dist\
del /F /Q /S *.spec
echo ===========

echo ==���楴�]==
rem pyinstaller --clean -i 128.ico -F LanguageTool.py
pyinstaller --clean -i 128.ico -F -w LanguageTool.py
echo ===========

echo ==�ƻs������==
copy dist\LanguageTool.exe .\
echo ===========

echo ==�R�����]�Ȧs��==
rd /Q /S __pycache__\
rd /Q /S build\
rd /Q /S dist\
del /F /Q /S *.spec
echo ===========

echo ==�������Y==
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "�y�t�p����.rar" ".\*.ico"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "�y�t�p����.rar" ".\*.exe"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "�y�t�p����.rar" ".\*.py"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "�y�t�p����.rar" ".\*.bat"
timeout /t 3