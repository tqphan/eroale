import QtQuick.Shapes
import QtQuick.Window
import "."

Window {
    width: 600
    height: 400
    visible: true
    title: "Border Collapse"
    color: "#999ac6"

    Rectangle {
        anchors.centerIn: parent
        anchors.fill: parent
        color: "transparent"

        Shape {
            id: icon
            anchors.fill: parent

            transform: [
                Scale {
                    xScale: Math.min(icon.width / 24, icon.height / 24)
                    yScale: Math.min(icon.width / 24, icon.height / 24)
                },
                Translate {
                    x: (icon.width - 24 * Math.min(icon.width / 24, icon.height / 24)) / 2
                    y: (icon.height - 24 * Math.min(icon.width / 24, icon.height / 24)) / 2
                }
            ]

            ShapePath {
                fillColor: "black"
                strokeColor: "transparent"
                PathSvg { path: Icons.altKeyIcon }
            }
        }

        Rectangle {
            id: border
            anchors.fill: parent
            color: "transparent"
            border.color: "#00e5ff"
            border.width: 2
            transformOrigin: Item.Center
            scale: 1
            visible: false  // hidden at rest

            Behavior on scale {
                NumberAnimation {
                    id: scaleAnim
                    duration: 400
                    easing.type: Easing.InOutCubic
                }
            }

            // Show only while the animation is running
            states: State {
                when: scaleAnim.running
                PropertyChanges { target: border; visible: true }
            }
        }

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            onEntered: border.scale = 0
            onExited:  border.scale = 1
        }
    }
}
