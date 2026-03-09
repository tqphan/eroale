"""
XAML Geometry to QML Path Dictionary Converter

Reads a XAML ResourceDictionary and writes a QML file containing
a QtObject with all paths as string properties, usable from other QML files.

Usage:
    python xaml_to_qml.py input.xaml [output.qml]

    input.xaml    - Path to the XAML ResourceDictionary file
    output.qml    - Output QML file (default: IconPaths.qml)

Example:
    python xaml_to_qml.py icons.xaml
    python xaml_to_qml.py icons.xaml MyIcons.qml

Usage in another QML file:
    import "."

    Image {
        source: IconPaths.tabKeyIcon
    }

    // or with Shape/PathSvg:
    Shape {
        ShapePath {
            PathSvg { path: IconPaths.tabKeyIcon }
        }
    }
"""

import re
import os
import sys
from datetime import datetime


def to_camel_case(name: str) -> str:
    """Lower-camel-case for QML property names: TabKeyIcon -> tabKeyIcon"""
    if not name:
        return name
    return name[0].lower() + name[1:]


def convert(input_path: str, output_path: str) -> None:
    with open(input_path, encoding="utf-8") as f:
        xaml = f.read()

    geometries = {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r'<Geometry\s+x:Key="([^"]+)"\s*>(.*?)</Geometry>', xaml, re.DOTALL)
    }

    if not geometries:
        print("No <Geometry> nodes found.")
        return

    component_name = os.path.splitext(os.path.basename(output_path))[0]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        f"// Generated from {os.path.basename(input_path)} on {timestamp}",
        f"// Usage: import this file, then reference {component_name}.<propertyName>",
        "",
        "pragma Singleton",
        "import QtQuick",
        "",
        "QtObject {",
    ]

    for name, path in geometries.items():
        prop = to_camel_case(name)
        # Escape any backslashes or quotes in the path data (rare but safe)
        safe_path = path.replace("\\", "\\\\").replace('"', '\\"')
        lines.append(f'    readonly property string {prop}: "{safe_path}"')

    lines += ["}", ""]

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  ✓  {output_path}  ({len(geometries)} path(s))")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    input_path = args[0]
    output_path = args[1] if len(args) > 1 else "IconPaths.qml"

    if not os.path.isfile(input_path):
        print(f"Error: '{input_path}' not found.")
        sys.exit(1)

    convert(input_path, output_path)


if __name__ == "__main__":
    main()