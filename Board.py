import math
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPolygonF
from PyQt5.QtCore import Qt, QPointF

class Node:

    def __init__(self, x, y, r=30):

        self.name = ""

        self.x = x
        self.y = y
        self.r = r

        self.is_to_drag = False

        self.conns = []

        self.is_selected = False

    def get_x(self):
        return self.x + self.r / 2

    def get_y(self):
        return self.y + self.r / 2

class Board(QWidget):

    def __init__(self):

        super().__init__()

        self.nodes = []
        self.selected = None
        self.pre_selected = None

        self.start_node = None
        self.finals_nodes = []

        self.drag_node = None
        self.type_test = ""

        self.setWindowTitle("Trabalho de Automatos")
        self.resize(1300, 700)

        self.layout = QVBoxLayout()
        self.input = QLineEdit()

        self.input.setFixedHeight(40)
        self.input.setFixedWidth(100)

        self.set_value_button = QPushButton("Continuar")
        self.set_value_button.clicked.connect(self.set_value_to_connection)
        self.set_value_button.setFixedWidth(300)
        self.set_value_button.setFixedHeight(100)
        self.set_value_button.setStyleSheet(
          """
            QPushButton {
                background-color: gray;
                border: none;
                border-radius: 12px;   
            }
        """
        )

        self.afd_test_button = QPushButton("Testar Cadeia")
        self.afd_test_button.clicked.connect(self.test_afd)
        self.afd_test_button.setFixedWidth(300)
        self.afd_test_button.setFixedHeight(100)
        self.afd_test_button.setStyleSheet(
            """
            QPushButton {
                background-color: gray;
                border: none;
                border-radius: 12px;   
            }
        """
        )

        self.afdButton = QPushButton("ADF")
        self.afdButton.clicked.connect(self.afd)

        self.layout.addWidget(self.afdButton, alignment=Qt.AlignTop | Qt.AlignRight)
        self.layout.addWidget(self.input, alignment=Qt.AlignCenter)

        self.layout.addWidget(self.set_value_button, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.afd_test_button, alignment=Qt.AlignCenter)

        self.setLayout(self.layout)
        self.counter = 2

        self.warn_label = QLabel("", self)
        self.warn_label.setFixedWidth(400)

        self.warn_label.setStyleSheet("font-size: 20px;")

        self.warn_label.hide()

        self.set_value_button.hide()
        self.afd_test_button.hide()
        self.input.hide()

    def set_value_to_connection(self):

        if self.test_error(["has_text", "is_one_letter"]):
            return

        b1 = self.pre_selected
        b2 = self.selected

        label = QLabel(self.input.text(), self)
        label.show()

        self.input.setText("")

        b1.conns.append((b2, label))

        self.set_value_button.hide()
        self.input.hide()

        self.selected = None
        self.update()

        self.type_test = ""

    def afd(self):

        self.reset_labels()

        self.input.show()
        self.afd_test_button.show()
        self.type_test = "test_afd"

    def test_afd(self):

        if self.test_error(["has_text"]):
            return

        chain_test = self.input.text()
        current_node = self.start_node

        for c in chain_test:
            for n, l in current_node.conns:
                if l.text() == c:
                    current_node = n

        accept = current_node in self.finals_nodes
        text = "Cadeia"

        if accept:
            text += " Aceita"
        else:
            text += " Recusada"

        self.warn_label.setText(text)
        self.warn_label.setVisible(True)

        self.input.setText("")

    def reset_labels(self):
        self.input.setText("")

        self.input.hide()
        self.set_value_button.hide()
        self.afd_test_button.hide()

        self.warn_label.hide()

    def test_error(self, erros):

        has_error = False

        if "is_one_letter" in erros:

            is_one_letter = len(self.input.text()) == 1
            has_error = has_error and not is_one_letter

            if not is_one_letter:
                self.warn_label.setText("Valor só pode conter um caractere")

        if "has_text" in erros:

            has_text = self.input.text() != ""
            has_error = has_error and not has_text

            if not has_text:
                self.warn_label.setText("Você precisa digitar um valor")

        self.warn_label.setVisible(has_error)
        return has_error

    def mousePressEvent(self, event):

        ball = self.mouse_entered_ball(event.x(), event.y())

        if ball:
            self.drag_node = ball

    def mouseDoubleClickEvent(self, event):

        pre_ball = self.selected
        self.selected = self.mouse_entered_ball(event.x(), event.y())

        if self.selected:

            if pre_ball:
                self.try_connect_nodes(pre_ball, self.selected)
                return

            self.update()
            return

        else:
            self.drag_node = False

        node = Node(event.x(), event.y())
        node.name = len(self.nodes) + 1

        self.nodes.append(node)
        self.update()

        if not self.start_node:
            self.start_node = node

    def mouseMoveEvent(self, event):

        if not self.mouse_entered_ball(event.x(), event.y()):
            self.drag_node = None

        if self.drag_node:
            self.drag_node.x = event.x()
            self.drag_node.y = event.y()
            self.update()

    def keyPressEvent(self, a0):

        if a0.key() in (Qt.Key_Return, Qt.Key_Enter) and self.input.isVisible():
            match self.type_test:
                case "set_value":
                    self.set_value_to_connection()
                case "test_afd":
                    self.test_afd()

        if a0.key() == Qt.Key_Escape:
            self.reset_labels()

        if a0.key() == Qt.Key_F:
            if self.selected:
                if not self.selected in self.finals_nodes and self.type_test == "":
                    self.finals_nodes.append(self.selected)

                self.selected = None

    def paintEvent(self, event):

        painter = QPainter(self)

        for node in self.nodes:

            node: Node = node

            if self.start_node == node:

                p1 = QPointF(node.x, node.get_y())
                p2 = QPointF(p1.x(), p1.y())
                p3 = QPointF(p1.x(), p1.y())

                scala = 20

                p2.setX(p2.x() - scala)
                p2.setY(p2.y() - scala)

                p3.setX(p2.x())
                p3.setY(p3.y() + scala)

                point = [p1, p2, p3]
                painter.drawPolygon(QPolygonF(point))

            if node == self.selected:
                painter.setBrush(QColor(255, 0, 0))
            elif node in self.finals_nodes:
                painter.setBrush(QColor(0, 0, 0))
            else:
                painter.setBrush(QColor(255, 255, 255))

            painter.drawEllipse(node.x, node.y, node.r, node.r)

            self.draw_connections(node, painter)

    def draw_connections(self, node: Node, painter):

        arrow_size = 20

        for conn, label in node.conns:

            p1 = QPointF(node.get_x(), node.get_y())
            p2 = QPointF(conn.get_x(), conn.get_y())

            t = 0.2

            x_label = p1.x() + t * (p2.x() - p1.x())
            y_label = p1.y() + t * (p2.y() - p1.y())

            label.move(int(x_label), int(y_label))

            angle = math.atan2(p2.y() - p1.y(), p2.x() - p1.x())

            end_x = conn.get_x() - conn.r * math.cos(angle)
            end_y = conn.get_y() - conn.r * math.sin(angle)

            start_x = node.get_x() + node.r * math.cos(angle)
            start_y = node.get_y() + node.r * math.sin(angle)

            painter.drawLine(
                QPointF(start_x, start_y),
                QPointF(end_x, end_y)
            )

            p1 = QPointF(
                end_x - arrow_size * math.cos(angle - math.pi / 6),
                end_y - arrow_size * math.sin(angle - math.pi / 6)
            )
            p2 = QPointF(
                end_x - arrow_size * math.cos(angle + math.pi / 6),
                end_y - arrow_size * math.sin(angle + math.pi / 6)
            )

            arrow_head = QPolygonF([QPointF(end_x, end_y), p1, p2])

            painter.drawPolygon(arrow_head)

    def mouse_entered_ball(self, x, y):

        for ball in self.nodes:

            dy = (y - ball.y)
            dx = (x - ball.x)

            if dx * dx + dy * dy < (ball.r * 1.5) * (ball.r * 1.5):
                self.update()
                return ball

        return None

    def try_connect_nodes(self, b1: Node, b2: Node):

        self.reset_labels()

        self.set_value_button.show()
        self.input.show()
        self.type_test = "set_value"

        self.pre_selected = b1
        self.selected = b2

app = QApplication(sys.argv)
janela = Board()
janela.show()
sys.exit(app.exec_())
