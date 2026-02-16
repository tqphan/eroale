# PySide6 Keyboard Layout Viewer

A QML-based keyboard layout viewer that displays a 95% keyboard layout from JSON data.

## Features

- **Grid Layout**: Displays keyboard keys in a proper grid with row/column spanning
- **Responsive**: Grid fills the entire window and resizes with the window
- **Proper Sizing**: Each key has preferred width/height based on its columnSpan and rowSpan
- **Color-coded Keys**: Different key types have different colors (function keys, letters, modifiers, etc.)
- **Interactive**: Hover effects and tooltips on each key
- **Icons**: Displays special character icons where available

## Requirements

- Python 3.8+
- PySide6

## Installation

Install PySide6:

```bash
pip install PySide6 --break-system-packages
```

## Running the Application

```bash
python keyboard_app.py
```

## Files

- `keyboard_app.py` - Main Python application with data models
- `main.qml` - QML UI definition with GridLayout
- `keyboard_95.json` - Keyboard layout data (38 columns × 6 rows)

## How It Works

1. **Data Model**: The Python side loads the JSON and creates a QAbstractListModel
2. **Grid Layout**: QML GridLayout with columns and rows from JSON
3. **Repeater**: Creates rectangles for each key item
4. **Sizing**: Each key's preferredWidth/Height is calculated based on:
   - Cell width = window width / total columns
   - Cell height = window height / total rows
   - Item width = cell width × columnSpan
   - Item height = cell height × rowSpan

5. **Layout Properties**:
   - `Layout.row` and `Layout.column` position each key
   - `Layout.rowSpan` and `Layout.columnSpan` make keys span multiple cells
   - `Layout.preferredWidth` and `Layout.preferredHeight` set the exact size
   - `Layout.fillWidth` and `Layout.fillHeight` enable resizing

## Grid Details

- **38 columns**: Allows for precise key positioning
- **6 rows**: Standard keyboard row count
- **Column/Row Spanning**: Keys like Spacebar span 14 columns, Backspace spans 4, etc.
- **Spacing**: 2px gaps between keys

## Customization

You can modify colors, spacing, font sizes, or add animations in `main.qml`.
