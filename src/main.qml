import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Window

ApplicationWindow {
    id: root
    visible: true
    flags: Qt.Window | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus
    // Determine window width/height: treat values <= 1 as fraction of Screen,
    // values > 1 as absolute pixels, otherwise fall back to fixed values.
    property real winWidth: (keyboardData.width > 0 && keyboardData.width <= 1) ? keyboardData.width * Screen.width : (keyboardData.width > 1 ? keyboardData.width : 1400)
    property real winHeight: (keyboardData.height > 0 && keyboardData.height <= 1) ? keyboardData.height * Screen.height : (keyboardData.height > 1 ? keyboardData.height : 600)

    width: winWidth
    height: winHeight
    title: "Keyboard Layout - 95% Keyboard"
    
    color: "#1e1e1e"

    // Positioning: support dock values: "top", "bottom", "left", "right".
    x: keyboardData.dock === "left" ? 0 : (keyboardData.dock === "right" ? (Screen.width - width) : (Screen.width - width) / 2)
    y: keyboardData.dock === "top" ? 0 : (keyboardData.dock === "bottom" ? (Screen.height - height) : (Screen.height - height) / 2)
    
    GridLayout {
        id: gridLayout
        anchors.fill: parent
        anchors.margins: 2
        
        columns: keyboardData.columns
        rows: keyboardData.rows
        
        // Calculate cell sizes based on window size
        property real cellWidth: (parent.width - anchors.margins * 2) / columns
        property real cellHeight: (parent.height - anchors.margins * 2) / rows
        
        columnSpacing: 2
        rowSpacing: 2
        
        Repeater {
            model: keyboardData.itemsModel
            
            Rectangle {
                id: keyRect
                
                // Position and span
                Layout.row: model.row
                Layout.column: model.column
                Layout.rowSpan: model.rowSpan
                Layout.columnSpan: model.columnSpan
                
                // Size calculation - critical for proper grid fitting
                Layout.preferredWidth: model.columnSpan
                Layout.preferredHeight: model.rowSpan
                
                Layout.fillWidth: true
                Layout.fillHeight: true
                
                color: model.color
                radius: 4
                border.color: Qt.lighter(model.color, 1.2)
                border.width: 1
                
                
                MouseArea {
                    id: mouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    
                    onClicked: {
                        console.log("Clicked:", model.name, "-", model.description)
                    }
                }
            }
        }
    }
}
