# CIS7000 EZ Version Control

- [Contents](#contents)
- [Getting Started](#getting-started)
- [`cis7000_version_control.py`](#cis7000_version_controlpy)
- [Makefile](#makefile)
    - [Example formats](#example-formats)
  - [Command-line Usage](#command-line-usage)
- [Version History](#version-history)
- [Authors](#authors)
- [Tags](#tags)

## Contents

`cis7000_version_control.py` Main python script

`Makefile`
Template makefile to run script with customized flags.

## Getting Started
1. Clone the repo
```bash
git clone https://github.com/mialana/CIS7000-EZ-Version-Control.git
```
2. Make the `cis7000_version_control.py` file executable
```bash
# MacOS and Linux
chmod 755
```
3. Start using program (or Makefile)!


## `cis7000_version_control.py`
```bash
usage: cis7000_version_control.py [-h] [-D] [-V] [--mode STR] assetDir

Simplify version control for CIS-7000 assets

positional arguments:
  assetDir    Path to asset directory in platform-specific syntax. Can be relative, absolute, cannonical, etc.

optional arguments:
  -h, --help  show this help message and exit
  -D          Run program in dry-run mode (default: False)
  -V          Run program with verbosity (default: True)
  --mode STR  Choices are ['PUBLISH', 'UPGRADE', 'PATCH'] (default: PATCH)
```
---
***Example usage**: Outputs dry-run result of updating `lastModified` field and PATCH part of `version` field in `metadata.json`.*
```make
`./cis7000_version_control.py` "./yugiohClockArc/" -D --patch
```

## Makefile

Vim into file, replace `ASSET_DIR_PATH` with path to the root directory of your CIS7000 asset. Path format can be relative, absolute, or cannonical -- just match the syntax of your machine!

#### Example formats
```make
# MacOS
ASSET_DIR_PATH = "/Users/liu.amy05/Documents/cis7000/yugiohClockArc"
# Linux
ASSET_DIR_PATH = "/opt/cis7000/yugiohClockArc"
# Windows
ASSET_DIR_PATH = "C:\liu.amy05\Documents\cis7000\yugiohClockArc"
```

### Command-line Usage

```bash
make publish # run script in `PUBLISH` mode
```

```bash
make upgrade # run script in `UPGRADE` mode
```

```bash
make patch # run script in `PATCH` mode
```

## Version History

* 1.0.0 (Initial Release)
  * Automate updating of `lastModified` field in `metadata.json`
  * Program modes:
    1. `PUBLISH` mode:
       * Increment `xx.00.00` of `version` field in `metadata.json`
       * Reset `00.xx.00` and `00.00.xx`
    2. `UPGRADE` mode:
       * Increment `00.xx.00` of `version` field in `metadata.json`
       * Reset `00.00.xx`
    3. `PATCH` mode:
       * Increment `00.00.xx` of `version` field in `metadata.json`
  * Include flags for verbose `-V` and dry-run `-D`

## Authors

* [**Amy M. Liu**](liu.amy05@gmail.com) - *Original author*

## Tags

*@Personal*
*@v1.0.0*