#!/usr/bin/env python3
import io
import json
import os
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from tabnanny import verbose

import requests
from lxml import etree

GITHUB_REPO = "lucide-icons/lucide"
ROOT = Path(__file__).parents[1]
WORKSPACE = ROOT / ".tmp"
DESTINATION = ROOT / "custom_components/lucide_icons/data/icons"


@dataclass
class Version:
    version: str
    url: str


def setup_workspace() -> None:
    WORKSPACE.mkdir(parents=True, exist_ok=True)


def setup_version_workspace(version: Version) -> Path:
    folder = WORKSPACE / version.version
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_latest_valid_release() -> Version:
    print("Searching for latest release with valid assets...")
    url = f"https://api.github.com/repos/{GITHUB_REPO}/releases"

    try:
        resp = requests.get(url)
        resp.raise_for_status()
        releases = resp.json()
    except Exception as e:
        print(f"Error fetching releases: {e}")
        sys.exit(1)

    for release in releases:
        tag = release["tag_name"]
        version = tag.lstrip("v")
        assets = release.get("assets", [])

        target_asset = None
        for asset in assets:
            if asset["name"] == f"lucide-icons-{version}.zip":
                target_asset = asset
                break
            # Fallback: strict match failed, try loose match
            elif asset["name"].startswith("lucide-icons-") and asset["name"].endswith(
                ".zip"
            ):
                target_asset = asset
                break

        if target_asset:
            print(f"Found valid release: {tag}")
            return Version(version, target_asset["browser_download_url"])

    print(
        "Error: No release found with a valid 'lucide-icons-*.zip' asset in the last 30 releases."
    )
    sys.exit(1)


def download_and_extract(version: Version, workspace: Path) -> Path:
    zip_path = workspace / "lucide-icons.zip"
    raw_output = workspace / "raw"

    if not zip_path.exists():
        print(f"Downloading {version.url}...")
        r = requests.get(version.url)
        zip_path.write_bytes(r.content)

    if raw_output.exists():
        shutil.rmtree(raw_output)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(raw_output)

    return raw_output / "icons"


def run_inkscape(icon_dir: Path):
    print("Running Inkscape processing (this may take a while)...")

    cmd = 'inkscape --actions="select-all;selection-ungroup;select-all;selection-ungroup;select-all;object-stroke-to-path;object-set-attribute:stroke-width,0;path-union;object-set-attribute:stroke-width,0;" --export-plain-svg --export-type=svg --export-overwrite *.svg'

    try:
        subprocess.run(cmd, cwd=icon_dir, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Inkscape failed: {e}")
        sys.exit(1)


def process_svg(workspace: Path, icon_dir: Path):
    print("Processing XML and merging metadata...")
    output_dir = workspace / "output"

    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    files = [file for file in icon_dir.glob("*.svg")]

    for file in files:
        icon_name = file.stem
        metadata_json = icon_dir / f"{icon_name}.json"

        icon_destination = output_dir / file.name

        with open(metadata_json, "r") as j:
            metadata = json.load(j)

        parser = etree.XMLParser(remove_blank_text=True)
        try:
            tree = etree.parse(file, parser)
            root = tree.getroot()

            attribs_to_remove = [
                "version",
                "id",
                "stroke",
                "stroke-width",
                "stroke-linecap",
                "stroke-linejoin",
            ]
            for attr in attribs_to_remove:
                if attr in root.attrib:
                    del root.attrib[attr]

            root.set("fill", "currentColor")

            root.set("tags", ",".join(metadata.get("tags", [])))
            root.set("categories", ",".join(metadata.get("categories", [])))

            for defs in root.findall(".//{http://www.w3.org/2000/svg}defs"):
                root.remove(defs)

            for path in root.findall(".//{http://www.w3.org/2000/svg}path"):
                if "id" in path.attrib:
                    del path.attrib["id"]
                if "style" in path.attrib:
                    del path.attrib["style"]
                if "stroke-width" in path.attrib:
                    del path.attrib["stroke-width"]

            tree.write(
                icon_destination,
                pretty_print=True,
                xml_declaration=False,
                encoding="utf-8",
            )

        except Exception as e:
            print(f"Error processing {file}: {e}")

    return output_dir


def main():
    setup_workspace()

    version = get_latest_valid_release()
    workspace = setup_version_workspace(version)

    icon_dir = download_and_extract(version, workspace)
    run_inkscape(icon_dir)

    output_dir = process_svg(workspace, icon_dir)

    shutil.copytree(output_dir, DESTINATION, dirs_exist_ok=True)


if __name__ == "__main__":
    main()
