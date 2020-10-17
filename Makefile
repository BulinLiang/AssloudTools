.PHONY: build
build:
	$(PYTHONHOME)/Scripts/pyuic5.exe ./code/ui/launcher.ui -o ./code/src/ui/launcher.py
	$(PYTHONHOME)/Scripts/pyuic5.exe ./code/ui/app.ui -o ./code/src/ui/app.py

.PHONY: run
run:
	python -B ./code/src/main.py

.PHONY: dist
dist:
	IF EXIST .\dist RMDIR /S/Q .\dist
	IF EXIST .\build RMDIR /S/Q .\build
	pyinstaller -i code/assloud.ico -D -w ./code/src/main.py -n assloud
	MOVE /Y .\\dist\\assloud .\\dist\\application
	XCOPY /Y/E .\\template .\\dist\\template\\
	XCOPY /Y/E .\\ART .\\dist\\ART\\
	XCOPY /Y/E .\\xpinyin .\\dist\\application\\xpinyin\\
	
	IF EXIST .\installer\_package RMDIR /S/Q .\installer\_package
	MOVE /Y .\\dist .\\installer\\_package
	