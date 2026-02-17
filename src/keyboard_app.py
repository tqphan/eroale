import sys
import json
from pathlib import Path
from PySide6.QtCore import QObject, Property, Slot, QAbstractListModel, Qt, QModelIndex
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement, QQmlApplicationEngine

QML_IMPORT_NAME = "KeyboardModel"
QML_IMPORT_MAJOR_VERSION = 1


class KeyboardItem:
    def __init__(self, data):
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.color = data.get("color", "#3498db")
        self.icon = data.get("icon", "")
        self.row = data.get("row", 0)
        self.column = data.get("column", 0)
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
        self._items = [KeyboardItem(item) for item in items]
        self.endResetModel()


@QmlElement
class KeyboardData(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._columns = 0
        self._rows = 0
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

    @Slot(str)
    def loadJson(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._columns = data.get("columns", 0)
                self._rows = data.get("rows", 0)
                self._itemsModel.setItems(data.get("items", []))
        except Exception as e:
            print(f"Error loading JSON: {e}")


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    # Create keyboard data object
    keyboard_data = KeyboardData()
    
    # Load the JSON file
    json_path = Path("./keyboard_95.json")
    keyboard_data.loadJson(str(json_path))
    
    # Set context property
    engine.rootContext().setContextProperty("keyboardData", keyboard_data)
    
    # Load QML
    qml_file = Path(__file__).parent / "main.qml"
    engine.load(qml_file)
    
    if not engine.rootObjects():
        sys.exit(-1)
    
    sys.exit(app.exec())
