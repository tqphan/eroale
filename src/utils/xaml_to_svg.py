"""
XAML Geometry to SVG Converter

Usage:
    python xaml_to_svg.py input.xaml [output_dir]

    input.xaml    - Path to the XAML ResourceDictionary file
    output_dir    - Output directory (default: svg_output)

Examples:
    python xaml_to_svg.py icons.xaml
    python xaml_to_svg.py icons.xaml ./out
"""

import re
import os
import sys


def to_snake_case(name: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return s.lower()


def convert(input_path: str, output_dir: str) -> None:
    os.makedirs(output_dir, exist_ok=True)

    with open(input_path, encoding="utf-8") as f:
        xaml = f.read()

    geometries = {
        m.group(1): m.group(2).strip()
        for m in re.finditer(r'<Geometry\s+x:Key="([^"]+)"\s*>(.*?)</Geometry>', xaml, re.DOTALL)
    }

    if not geometries:
        print("No <Geometry> nodes found.")
        return

    for name, path in geometries.items():
        svg = f'<svg xmlns="http://www.w3.org/2000/svg">\n  <path d="{path}"/>\n</svg>\n'
        filename = to_snake_case(name) + ".svg"
        out = os.path.join(output_dir, filename)
        with open(out, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  ✓  {filename}")

    print(f"\nDone — {len(geometries)} file(s) written to '{output_dir}/'")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    input_path = args[0]
    output_dir = args[1] if len(args) > 1 else "svg_output"

    if not os.path.isfile(input_path):
        print(f"Error: '{input_path}' not found.")
        sys.exit(1)

    convert(input_path, output_dir)


if __name__ == "__main__":
    main()