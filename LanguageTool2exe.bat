@echo off
@color 0a

CD /D "%~dp0"

echo ==更新pip==
python.exe -m pip install --upgrade pip
echo ===========

echo ==安裝pyinstaller==
pip install pyinstaller
echo ===========

echo ==刪除打包暫存檔==
rd /Q /S __pycache__\
rd /Q /S build\
rd /Q /S dist\
del /F /Q /S *.spec
echo ===========

echo ==執行打包==
rem pyinstaller --clean -i 128.ico -F LanguageTool.py
pyinstaller --clean -i 128.ico -F -w LanguageTool.py
echo ===========

echo ==複製執行檔==
copy dist\LanguageTool.exe .\
echo ===========

echo ==刪除打包暫存檔==
rd /Q /S __pycache__\
rd /Q /S build\
rd /Q /S dist\
del /F /Q /S *.spec
echo ===========

echo ==執行壓縮==
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "語系小幫手.rar" ".\*.ico"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "語系小幫手.rar" ".\*.exe"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "語系小幫手.rar" ".\*.py"
"C:\Program Files\WinRAR\Rar.exe" a -ep1 "語系小幫手.rar" ".\*.bat"
timeout /t 3