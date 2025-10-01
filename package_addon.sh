#!/usr/bin/env bash
set -euo pipefail

# Small packaging script for the Blender add-on located in the io_mesh_3mf folder.
# Usage:
#   bash package_addon.sh           -> creates dist/io_mesh_3mf.zip
#   bash package_addon.sh --out foo.zip

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
ADDON_DIR_NAME="io_mesh_3mf"
ADDON_DIR="$ROOT_DIR/$ADDON_DIR_NAME"
DIST_DIR="$ROOT_DIR/dist"
OUT_NAME="${ADDON_DIR_NAME}.zip"

while [[ $# -gt 0 ]]; do
  case "$1" in
    -o|--out)
      shift
      OUT_NAME="$1"
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [-o|--out <filename.zip>]"
      exit 0
      ;;
    *)
      echo "Unknown arg: $1"
      echo "Usage: $0 [-o|--out <filename.zip>]"
      exit 1
      ;;
  esac
done

if [[ ! -d "$ADDON_DIR" ]]; then
  echo "Error: Add-on folder not found: $ADDON_DIR" >&2
  exit 2
fi

if [[ ! -f "$ADDON_DIR/__init__.py" ]]; then
  echo "Error: $ADDON_DIR/__init__.py not found. The add-on must include an __init__.py with bl_info." >&2
  exit 3
fi

# Quick sanity check: look for bl_info in __init__.py
if ! grep -q "bl_info" "$ADDON_DIR/__init__.py"; then
  echo "Warning: bl_info not found in $ADDON_DIR/__init__.py. Blender may not recognise the add-on metadata." >&2
  echo "Proceeding anyway..."
fi

mkdir -p "$DIST_DIR"

OUT_PATH="$DIST_DIR/$OUT_NAME"

echo "Packaging add-on '$ADDON_DIR_NAME' -> $OUT_PATH"

# Create zip. Exclude common unwanted files and folders.
cd "$ROOT_DIR"
zip -r "$OUT_PATH" "$ADDON_DIR_NAME" \
  -x "*/__pycache__/*" \
  -x ".git/*" \
  -x ".github/*" \
  -x "test/*" -x "tests/*" \
  -x "*.DS_Store" 1>/dev/null

echo "Created: $OUT_PATH"
echo "To install: Preferences → Add-ons → Install... → select $OUT_PATH"
