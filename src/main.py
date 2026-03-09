import sys
import json
from pathlib import Path
from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement, QQmlApplicationEngine

QML_IMPORT_NAME = "KeyboardModel"
QML_IMPORT_MAJOR_VERSION = 1


class KeyboardItem:
    def __init__(self, data, row=None, column=None):
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.color = data.get("color", "#3498db")
        self.icon = data.get("icon", "")
        # Use provided row/column if given, otherwise use from data, otherwise None (will be calculated)
        self.row = row if row is not None else data.get("row", None)
        self.column = column if column is not None else data.get("column", None)
        self.rowSpan = data.get("rowSpan", 1)
        self.columnSpan = data.get("columnSpan", 1)


class KeyboardItemsModel(QAbstractListModel):
    NameRole = Qt.UserRole + 1
    DescriptionRole = Qt.UserRole + 2
    ColorRole = Qt.UserRole + 3
    IconRole = Qt.UserRole + 4
    RowRole = Qt.UserRole + 5
    ColumnRole = Qt.UserRole + 6
    RowSpanRole = Qt.UserRole + 7
    ColumnSpanRole = Qt.UserRole + 8

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._items):
            return None

        item = self._items[index.row()]

        if role == self.NameRole:
            return item.name
        elif role == self.DescriptionRole:
            return item.description
        elif role == self.ColorRole:
            return item.color
        elif role == self.IconRole:
            return item.icon
        elif role == self.RowRole:
            return item.row
        elif role == self.ColumnRole:
            return item.column
        elif role == self.RowSpanRole:
            return item.rowSpan
        elif role == self.ColumnSpanRole:
            return item.columnSpan

        return None

    def roleNames(self):
        return {
            self.NameRole: b"name",
            self.DescriptionRole: b"description",
            self.ColorRole: b"color",
            self.IconRole: b"icon",
            self.RowRole: b"row",
            self.ColumnRole: b"column",
            self.RowSpanRole: b"rowSpan",
            self.ColumnSpanRole: b"columnSpan",
        }

    def setItems(self, items):
        self.beginResetModel()
        self._items = items
        self.endResetModel()


@QmlElement
class KeyboardData(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._columns = 0
        self._rows = 0
        self._width = 1.0
        self._height = 0.4
        self._dock = ""
        self._itemsModel = KeyboardItemsModel(self)

    def get_columns(self):
        return self._columns

    def get_rows(self):
        return self._rows

    def get_items_model(self):
        return self._itemsModel

    columns = Property(int, get_columns, constant=True)
    rows = Property(int, get_rows, constant=True)
    itemsModel = Property(QObject, get_items_model, constant=True)

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_dock(self):
        return self._dock

    width = Property(float, get_width, constant=True)
    height = Property(float, get_height, constant=True)
    dock = Property(str, get_dock, constant=True)

    def _calculate_positions(self, items_data, columns):
        """Calculate row/column positions for items that don't have explicit positions."""
        if not items_data:
            return [], 0
        
        # Determine grid dimensions
        if columns == 0:
            columns = 20  # Default column count if not specified
        
        # Create a grid to track occupied cells
        # We'll dynamically expand rows as needed
        grid = []
        processed_items = []
        
        for item_data in items_data:
            row_span = item_data.get("rowSpan", 1)
            col_span = item_data.get("columnSpan", 1)
            
            # Check if item has explicit position
            if "row" in item_data and "column" in item_data:
                row = item_data["row"]
                col = item_data["column"]
            else:
                # Find next available position in grid
                row, col = self._find_next_position(grid, columns, row_span, col_span)
            
            # Mark cells as occupied in grid
            self._mark_occupied(grid, row, col, row_span, col_span)
            
            # Create KeyboardItem with calculated position
            item = KeyboardItem(item_data, row, col)
            processed_items.append(item)
        
        # Calculate total rows
        max_row = 0
        for item in processed_items:
            max_row = max(max_row, item.row + item.rowSpan)
        
        return processed_items, max_row
    
    def _find_next_position(self, grid, columns, row_span, col_span):
        """Find the next available position in the grid for an item."""
        row = 0
        while True:
            for col in range(columns - col_span + 1):
                if self._can_place(grid, row, col, row_span, col_span):
                    return row, col
            row += 1
    
    def _can_place(self, grid, row, col, row_span, col_span):
        """Check if an item can be placed at the given position."""
        for r in range(row, row + row_span):
            for c in range(col, col + col_span):
                if r < len(grid) and c < len(grid[r]) and grid[r][c]:
                    return False
        return True
    
    def _mark_occupied(self, grid, row, col, row_span, col_span):
        """Mark cells as occupied in the grid."""
        # Expand grid if necessary
        while len(grid) <= row + row_span:
            grid.append([False] * 100)  # Use a large number for columns
        
        for r in range(row, row + row_span):
            for c in range(col, col + col_span):
                grid[r][c] = True

    @Slot(str)
    def loadJson(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                columns = data.get("columns", 0)
                items_data = data.get("items", [])
                # Read optional layout metadata
                self._width = float(data.get("width", self._width))
                self._height = float(data.get("height", self._height))
                self._dock = data.get("dock", self._dock)

                # Calculate positions for items
                processed_items, calculated_rows = self._calculate_positions(items_data, columns)

                # Set grid dimensions
                self._columns = columns if columns > 0 else 20
                self._rows = data.get("rows", calculated_rows)

                # Set processed items
                self._itemsModel.setItems(processed_items)
        except Exception as e:
            print(f"Error loading JSON: {e}")


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    # Create keyboard data object
    keyboard_data = KeyboardData()
    
    # Load the JSON file
    json_path = Path("./keyboard-alphabet-14x4-bottom.json")
    keyboard_data.loadJson(str(json_path))
    
    # Set context property
    engine.rootContext().setContextProperty("keyboardData", keyboard_data)
    
    # Load QML
    qml_file = Path(__file__).parent / "main.qml"
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec())
