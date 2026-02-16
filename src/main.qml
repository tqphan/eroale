import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

ApplicationWindow {
    id: root
    visible: true
    width: 1400
    height: 600
    title: "Keyboard Layout - 95% Keyboard"
    
    color: "#1e1e1e"
    
    GridLayout {
        id: gridLayout
        anchors.fill: parent
        anchors.margins: 10
        
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
