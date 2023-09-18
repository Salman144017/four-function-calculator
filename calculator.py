"""pyQT Four Functiton Calculator"""
import sys
from functools import partial
from PySide6.QtCore import Qt, QProcess, Signal, Slot, QObject
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QGridLayout,
    QLineEdit,
)


class CalculatorModel(QObject):
    """Calculator Model Class"""

    messageReceived = Signal(str)

    def __init__(self):
        super().__init__()
        self.result = 0
        self.queue = []

        self.process1 = QProcess()
        self.process2 = QProcess()

    def start_processes(self):
        """start processes"""
        self.process1.start("python3", ["process1.py"])
        self.process2.start("python3", ["process2.py"])

        self.process1.readyReadStandardOutput.connect(self.handle_output1)
        self.process2.readyReadStandardOutput.connect(self.handle_output2)

    @Slot()
    def handle_output1(self):
        """Handle message from process 1"""
        message = self.process1.readAllStandardOutput().data().decode()
        self.queue.append(message)
        self.messageReceived.emit(message)

    @Slot()
    def handle_output2(self):
        """Handle message from process 2"""
        message = self.process2.readAllStandardOutput().data().decode()
        self.queue.append(message)
        self.messageReceived.emit(message)

    def add(self, num1, num2):
        """Function to perform addition"""
        self.result = num1 + num2

    def subtract(self, num1, num2):
        """Function to perform subtraction"""
        self.result = num1 - num2

    def multiply(self, num1, num2):
        """Function to perform multiplication"""
        self.result = num1 * num2

    def divide(self, num1, num2):
        """Function to perform division"""
        if num2 == 0:
            self.result = "Error"
        else:
            self.result = num1 / num2


class CalculatorView(QMainWindow):
    """Calculator View Class"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        horizontal_layout = QHBoxLayout()
        self.layout.addLayout(horizontal_layout)

        self.result_display = QLineEdit("0")
        self.result_display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.result_display.setMinimumHeight(40)
        self.result_display.setMaximumWidth(255)
        horizontal_layout.addWidget(self.result_display)

        self.create_button_grid()
        self.create_clear_button()

        self.central_widget.setLayout(self.layout)
        self.controller = None

    def create_clear_button(self):
        """create clear button"""
        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.handle_clear_click)
        clear_button.setMinimumHeight(40)
        clear_button.setMaximumWidth(255)
        horizontal_layout = QHBoxLayout()
        self.layout.addLayout(horizontal_layout)
        horizontal_layout.addWidget(clear_button)

    def create_button_grid(self):
        """create button grid"""
        button_grid = QWidget()
        button_layout = QGridLayout()
        button_grid.setLayout(button_layout)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "=", "+"],
        ]

        for row, button_row in enumerate(buttons):
            for col, button_text in enumerate(button_row):
                button = QPushButton(button_text)
                button.clicked.connect(partial(self.handle_button_click, button_text))
                button.setMinimumSize(50, 70)
                button_layout.addWidget(button, row, col)

        self.layout.addWidget(button_grid)
        self.result_display.setReadOnly(True)

    def handle_clear_click(self):
        """handle clear button controller"""
        self.controller.clear_input()

    def handle_button_click(self, button_text):
        """handle button controller"""
        if button_text == "=":
            self.controller.calculate()
        else:
            self.controller.update_input(button_text)

    def set_controller(self, controller_init):
        """set the controller"""
        self.controller = controller_init

    def update_display(self, text):
        """updte the display"""
        current_text = self.result_display.text()
        if current_text in ("0", "Error"):
            self.result_display.setText(text)
        else:
            self.result_display.setText(current_text + text)


class CalculatorController(QObject):
    """Calculator Controller Class"""

    def __init__(self, model_init, view_init):
        super().__init__()
        self.model = model_init
        self.view = view_init
        self.view.set_controller(self)
        self.model.start_processes()
        self.model.messageReceived.connect(self.print_message)

        self.operand1 = ""
        self.operand2 = ""
        self.operator = ""
        self.is_first_operand = True
        self.last_result = None

    def update_input(self, text):
        """updte the input"""
        if text.isdigit() or text == ".":
            # if text is digit or dot
            if self.is_first_operand or not self.operator:
                # if its first operand or its not operator
                # append to the operand1
                self.operand1 += text
                self.view.update_display(text)
            else:
                # append to the operand2
                self.operand2 += text
                self.view.update_display(text)
        elif text == "=":
            self.calculate()
        else:
            # Check if the previous input was an operator
            if self.operator and not self.is_first_operand:
                # Replace the previous operator with the new one
                self.operator = text
            else:
                self.operator = text
                self.is_first_operand = False
                self.view.update_display(text)

    def calculate(self):
        """calcuate the result"""
        if self.operand1 and self.operand2 and self.operator:
            num1 = float(self.operand1)
            num2 = float(self.operand2)

            if self.operator == "+":
                model.add(num1, num2)
            elif self.operator == "-":
                model.subtract(num1, num2)
            elif self.operator == "*":
                model.multiply(num1, num2)
            elif self.operator == "/":
                model.divide(num1, num2)

            # Check if the result is an integer
            if model.result != "Error":
                if model.result.is_integer():
                    model.result = int(
                        model.result
                    )  # Convert to an integer if it's an integer
                else:
                    # Format the result to two decimal places
                    model.result = f"{float(model.result):.2f}"

            self.view.result_display.setText(
                str(model.result)
            )  # Update the result as a string

            # Clear the input and operator after each operation
            self.operand2 = ""
            self.operator = ""

            # Store the result as the last result for future operations
            if model.result != "Error":
                self.operand1 = str(model.result)
                self.last_result = str(model.result)
            else:
                self.operand1 = "0"
                self.last_result = "0"

    def clear_input(self):
        """clear variables and display"""
        self.operand1 = ""
        self.operand2 = ""
        self.operator = ""
        self.is_first_operand = True
        self.view.result_display.setText("0")

    def print_message(self, message):
        """print message"""
        print(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = CalculatorModel()
    view = CalculatorView()
    controller = CalculatorController(model, view)
    view.show()
    sys.exit(app.exec())
