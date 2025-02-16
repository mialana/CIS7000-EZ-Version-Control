ASSET_DIR_PATH = "./Users/liu.amy05/Documents/cis-7000/hw4/DRIVE_SUBMISSION/yugiohClockArc"

patch:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=PATCH

upgrade:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=UPGRADE

publish:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=PUBLISH

ASSET_DIR_PATH = "/Users/liu.amy05/Documents/cis-7000/hw4/DRIVE_SUBMISSION/parkBench"

commit:
	./cis7000_version_control.py $(ASSET_DIR_PATH) --mode=PUBLISH --author="liuamy05" --note="Converted LODs to a variant set"

test:
	python3 -m pytest -xvs test.py