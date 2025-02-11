ASSET_DIR_PATH = "../DRIVE_SUBMISSION/yugiohClockArc"

patch:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=PATCH

upgrade:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=UPGRADE

publish:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=PUBLISH

test:
	python3 -m pytest -xvs test.py