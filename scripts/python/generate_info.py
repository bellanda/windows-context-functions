#!/usr/bin/env python3
"""
Script to generate detailed information about selected files/folders.
Creates an info file with the same name as the selected item plus "_info.txt".
"""

import datetime
import os
import sys
from pathlib import Path


def format_size(size_bytes):
    """Convert bytes to human readable format."""
    if size_bytes == 0:
        return "0 B"

    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1

    return f"{size_bytes:.2f} {size_names[i]}"


def get_file_info(file_path):
    """Get detailed file information."""
    try:
        stat = file_path.stat()
        return {
            "size": stat.st_size,
            "size_formatted": format_size(stat.st_size),
            "created": datetime.datetime.fromtimestamp(stat.st_ctime),
            "modified": datetime.datetime.fromtimestamp(stat.st_mtime),
            "accessed": datetime.datetime.fromtimestamp(stat.st_atime),
        }
    except (OSError, PermissionError):
        return None


def get_directory_info(dir_path):
    """Get detailed directory information."""
    try:
        items = list(dir_path.iterdir())
        files = [item for item in items if item.is_file()]
        dirs = [item for item in items if item.is_dir()]

        total_size = 0
        for file in files:
            try:
                total_size += file.stat().st_size
            except (OSError, PermissionError):
                continue

        return {
            "total_items": len(items),
            "files_count": len(files),
            "dirs_count": len(dirs),
            "total_size": total_size,
            "total_size_formatted": format_size(total_size),
        }
    except (OSError, PermissionError):
        return None


def main():
    if len(sys.argv) < 2:
        print("❌ Error: No file path provided")
        return 1

    # Get absolute path
    selected_path = Path(sys.argv[1]).resolve()

    # Create info file name
    if selected_path.is_file():
        info_file_name = f"{selected_path.stem}_info.txt"
    else:
        info_file_name = f"{selected_path.name}_info.txt"

    info_file_path = selected_path.parent / info_file_name

    # Generate timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Collect all information
    info_content = []
    info_content.append("=" * 60)
    info_content.append("📋 DETAILED FILE/FOLDER INFORMATION")
    info_content.append("=" * 60)
    info_content.append(f"Generated: {timestamp}")
    info_content.append(f"Script executed from: {os.getcwd()}")
    info_content.append("")

    # Basic information
    info_content.append("📁 BASIC INFORMATION")
    info_content.append("-" * 30)
    info_content.append(f"Name: {selected_path.name}")
    info_content.append(f"Type: {'File' if selected_path.is_file() else 'Directory' if selected_path.is_dir() else 'Other'}")
    info_content.append(f"Exists: {'Yes' if selected_path.exists() else 'No'}")

    if selected_path.is_file():
        info_content.append(f"Extension: {selected_path.suffix}")
        info_content.append(f"Stem (name without extension): {selected_path.stem}")

    info_content.append("")

    # Path information in different formats
    info_content.append("🛤️  PATH FORMATS (for easy copying)")
    info_content.append("-" * 30)

    # Original argument
    info_content.append(f"Original argument: {sys.argv[1]}")

    # Different path formats
    abs_path = str(selected_path.absolute())
    info_content.append(f"Absolute path (native): {abs_path}")
    info_content.append(f"Forward slashes (/): {abs_path.replace(os.sep, '/')}")
    info_content.append(f"Backslashes (\\): {abs_path.replace('/', os.sep)}")
    info_content.append(f"Escaped backslashes (\\\\): {abs_path.replace(os.sep, os.sep + os.sep)}")

    # Parent directory
    info_content.append(f"Parent directory: {selected_path.parent}")
    info_content.append(f"Parent (forward slashes): {str(selected_path.parent).replace(os.sep, '/')}")
    info_content.append(f"Parent (escaped backslashes): {str(selected_path.parent).replace(os.sep, os.sep + os.sep)}")

    info_content.append("")

    # Detailed information based on type
    if selected_path.is_file():
        info_content.append("📄 FILE DETAILS")
        info_content.append("-" * 30)

        file_info = get_file_info(selected_path)
        if file_info:
            info_content.append(f"Size: {file_info['size_formatted']} ({file_info['size']:,} bytes)")
            info_content.append(f"Created: {file_info['created'].strftime('%Y-%m-%d %H:%M:%S')}")
            info_content.append(f"Modified: {file_info['modified'].strftime('%Y-%m-%d %H:%M:%S')}")
            info_content.append(f"Last accessed: {file_info['accessed'].strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            info_content.append("Could not retrieve file details (permission denied)")

    elif selected_path.is_dir():
        info_content.append("📁 DIRECTORY DETAILS")
        info_content.append("-" * 30)

        dir_info = get_directory_info(selected_path)
        if dir_info:
            info_content.append(f"Total items: {dir_info['total_items']}")
            info_content.append(f"Files: {dir_info['files_count']}")
            info_content.append(f"Subdirectories: {dir_info['dirs_count']}")
            info_content.append(f"Total size: {dir_info['total_size_formatted']} ({dir_info['total_size']:,} bytes)")
        else:
            info_content.append("Could not retrieve directory details (permission denied)")

    info_content.append("")

    # System information
    info_content.append("💻 SYSTEM INFORMATION")
    info_content.append("-" * 30)
    info_content.append(f"Operating system: {os.name}")
    info_content.append(f"Path separator: '{os.sep}'")
    info_content.append(f"Current working directory: {os.getcwd()}")
    info_content.append(f"Python executable: {sys.executable}")
    info_content.append(f"Python version: {sys.version}")

    info_content.append("")
    info_content.append("=" * 60)
    info_content.append("End of information")
    info_content.append("=" * 60)

    # Write to info file
    try:
        with open(info_file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(info_content))

        print("🎯 Script executed successfully!")
        print(f"📄 Info file created: {info_file_path}")
        print(f"📁 Selected item: {selected_path}")
        print(f"🔍 Item exists: {'✅ Yes' if selected_path.exists() else '❌ No'}")

        return 0

    except (OSError, PermissionError) as e:
        print(f"❌ Error creating info file: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
