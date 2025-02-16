#!/usr/bin/env python3
"""
Author : Amy M. Liu <liu.amy05@gmail.com>
Date   : 2025-02-09
Purpose: Simplify version control for CIS-7000 assets
"""

import argparse, sys, logging, json
from pathlib import Path
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict

logging.basicConfig(stream=sys.stdout, format="%(message)s", level=10)
logger = logging.getLogger(__name__)


# --------------------------------------------------
# CLASSES & ENUMS
class Mode(Enum):
    PUBLISH = 0
    UPGRADE = 1
    PATCH = 2

    def __str__(self):
        return self.name


@dataclass
class Args:
    assetDir: Path
    note: str
    author: str
    mode: "Mode" = Mode.PATCH
    dryRun: bool = False
    verbosity: bool = True


# --------------------------------------------------
# MAIN
def main():
    args = get_args()
    _setup_logger(args.verbosity)

    logger.info(f"Beginning {args.mode} operation...")

    metadata_path: Path = args.assetDir.joinpath("metadata.json")

    if not metadata_path.is_file():
        raise FileNotFoundError(f"Metadata file does not exist at expected path")

    with open(metadata_path, "r+") as file:
        metadata = json.load(file)

        """Handle version incrementing"""

        currVer: str = metadata["assetStructureVersion"]  # add `id` value.
        newVer: str = _increment_version(currVer, args.mode)

        """Handle new commit"""
        commitList: List = metadata["commitHistory"]
        newTimestamp: str = _get_current_timestamp()

        newCommit: Dict = {
            "author": args.author,
            "version": newVer,
            "timestamp": newTimestamp,
            "note": args.note,
        }

        commitList.insert(0, newCommit)

        metadata["assetStructureVersion"] = newVer
        metadata["commitHistory"] = commitList

        logger.info(f"  New asset version is: {newVer}")
        logger.info(f"  New last-modified timestamp is: {newTimestamp}")
        logger.info(f"  New commit is: {json.dumps(newCommit, indent=4)}")

        logger.info("\n\n`metadata.json` CONTENTS:\n")
        logger.info(json.dumps(metadata, indent=4))

        if not args.dryRun:
            file.seek(0)  # reset file pointer to beginning.
            json.dump(metadata, file, indent=4)
            file.truncate()  # remove excess bytes if necessary

    msg_helper: str = "" if not args.dryRun else "Dry run of "
    logger.info(f"{msg_helper}{args.mode} operation complete!")


# --------------------------------------------------
# ARGPARSE
def get_args() -> "Args":
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Simplify version control for CIS-7000 assets",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "assetDir",
        type=_is_valid_directory,
        help="Path to asset directory in platform-specific syntax. Can be relative, absolute, cannonical, etc.",
    )

    parser.add_argument(
        "--note",
        required=True,
        metavar="STR",
        type=_check_note_length,
        help="Note to attach to commit. Max 100 characters",
    )

    parser.add_argument(
        "--author",
        required=True,
        metavar="STR",
        type=str,
        help="Author of commit",
    )

    parser.add_argument(
        "--mode",
        metavar="STR",
        type=_Mode_from_str,
        default=Mode.PATCH,
        help=f"Choices are {list(Mode.__members__)}",
    )

    parser.add_argument(
        "-D",
        "--dryRun",
        help="Run program in dry-run mode",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-V",
        "--verbosity",
        help="Run program with verbosity",
        action="store_true",
        default=True,
    )

    return Args(**vars(parser.parse_args()))


# --------------------------------------------------
# INTERNAL USE FUNCTIONS
def _Mode_from_str(s: str) -> Mode:
    """Handles typing of `Mode` enum for argparse

    Arguments:
        s -- string representation of a `Mode`
    """
    try:
        return Mode[s]
    except KeyError:
        raise argparse.ArgumentTypeError(f"{s} is not a valid mode.")


def _setup_logger(verbose: bool):
    """Sets logging level of our global logger"""
    if verbose:
        logger.setLevel(10)  # 10 maps to DEBUG level
    else:
        logger.setLevel(30)  # 30 maps to WARNING level


def _check_note_length(note: str) -> str:
    """Checks if commit note is less than 100 characters"""
    if len(note) <= 100:
        return note
    else:
        raise argparse.ArgumentTypeError("Commit note is longer than 100 characters.")


def _is_valid_directory(path: str) -> Path:
    """Handles typing of `assetDir` argument for argparse"""
    canonical_path: Path = Path(path).resolve()
    if canonical_path.is_dir():
        return canonical_path
    else:
        raise argparse.ArgumentTypeError(f'"{path}" is not a valid local directory.')


def _increment_version(currVer: str, mode: "Mode") -> str:
    """Increments `currVer` (extracted from ASSET_JSON["version"]) based on given `Mode`"""
    parts = list(map(int, currVer.split(".")))  # Convert version parts to integers

    parts[mode.value] += 1

    for i in range(mode.value + 1, 3):
        parts[i] = 0

    return ".".join(f"{part:02d}" for part in parts)


def _get_current_timestamp() -> str:
    """Updates ASSET_JSON["lastModified"]

    Returns:
        a formatted timestamp (e.g. 2024-12-03T14:55:13-05)
    """
    dt: datetime = datetime.now()
    dt = dt.astimezone()  # Modify `datetime` obj to include timezone

    timestamp: str = dt.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2]  # Format the timestamp
    return timestamp


# --------------------------------------------------
if __name__ == "__main__":
    main()
