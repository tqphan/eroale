import sys
import time
import math
import random
from PySide6.QtCore import QObject, Signal, Slot, QThread, Property
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, qmlRegisterType


class Point2DBroadcaster(QObject):
    dataReady = Signal(float, float, float)  # x, y, time

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._paused = False
        self._thread = QThread()
        self.moveToThread(self._thread)
        self._thread.started.connect(self._run)

    def _run(self):
        t0 = time.time()
        while self._running:
            if not self._paused:
                t = time.time() - t0
                x = math.sin(t * 2)
                y = math.cos(t * 2)
                self.dataReady.emit(x, y, t)
            time.sleep(1 / 30)

    @Slot()
    def start(self):
        self._running = True
        self._paused = False
        if not self._thread.isRunning():
            self._thread.start()

    @Slot()
    def stop(self):
        self._running = False
        self._thread.quit()
        self._thread.wait()

    @Slot()
    def pause(self):
        self._paused = not self._paused


class DataBroadcaster(QObject):
    dataReady = Signal(list, list)  # probabilities (50,), matrix (4x4 flat)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._running = False
        self._paused = False
        self._thread = QThread()
        self.moveToThread(self._thread)
        self._thread.started.connect(self._run)

    def _run(self):
        while self._running:
            if not self._paused:
                probs = [random.random() for _ in range(50)]
                # 4x4 transformation matrix (row-major flat)
                matrix = [random.uniform(-1, 1) for _ in range(16)]
                self.dataReady.emit(probs, matrix)
            time.sleep(1 / 30)

    @Slot()
    def start(self):
        self._running = True
        self._paused = False
        if not self._thread.isRunning():
            self._thread.start()

    @Slot()
    def stop(self):
        self._running = False
        self._thread.quit()
        self._thread.wait()

    @Slot()
    def pause(self):
        self._paused = not self._paused


class Bridge(QObject):
    point2DUpdated = Signal(float, float, float)
    dataUpdated = Signal(list, list)

    def __init__(self):
        super().__init__()
        self.pt = Point2DBroadcaster()
        self.db = DataBroadcaster()
        self.pt.dataReady.connect(self.point2DUpdated)
        self.db.dataReady.connect(self.dataUpdated)

    @Slot()
    def startPoint2D(self): self.pt.start()
    @Slot()
    def stopPoint2D(self): self.pt.stop()
    @Slot()
    def pausePoint2D(self): self.pt.pause()

    @Slot()
    def startData(self): self.db.start()
    @Slot()
    def stopData(self): self.db.stop()
    @Slot()
    def pauseData(self): self.db.pause()


QML = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "Broadcaster GUI"

    property real ptX: 0
    property real ptY: 0
    property real ptT: 0
    property var probs: []
    property var matrix: []

    Connections {
        target: bridge
        function onPoint2DUpdated(x, y, t) {
            ptX = x.toFixed(4)
            ptY = y.toFixed(4)
            ptT = t.toFixed(3)
        }
        function onDataUpdated(p, m) {
            probs = p
            matrix = m
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        GroupBox {
            title: "Point2D Broadcaster"
            Layout.fillWidth: true
            ColumnLayout {
                Label { text: "x: " + ptX + "  y: " + ptY + "  t: " + ptT }
                RowLayout {
                    Button { text: "Start";  onClicked: bridge.startPoint2D() }
                    Button { text: "Stop";   onClicked: bridge.stopPoint2D() }
                    Button { text: "Pause";  onClicked: bridge.pausePoint2D() }
                }
            }
        }

        GroupBox {
            title: "Data Broadcaster (50 probs + 4×4 matrix)"
            Layout.fillWidth: true
            ColumnLayout {
                Label {
                    text: probs.length ? "probs[0..4]: " + probs.slice(0,5).map(v => v.toFixed(3)).join(", ") : "—"
                }
                Label {
                    text: matrix.length ? "matrix[0..3]: " + matrix.slice(0,4).map(v => v.toFixed(3)).join(", ") : "—"
                }
                RowLayout {
                    Button { text: "Start";  onClicked: bridge.startData() }
                    Button { text: "Stop";   onClicked: bridge.stopData() }
                    Button { text: "Pause";  onClicked: bridge.pauseData() }
                }
            }
        }
    }
}
"""

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    bridge = Bridge()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("bridge", bridge)
    engine.loadData(QML.encode())

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())