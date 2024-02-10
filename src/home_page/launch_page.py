from PyQt5.QtWidgets import QCheckBox, QTextEdit
from PyQt5.QtCore import QObject
import re
import subprocess

class Launch(QObject):
    def __init__(self, main):
        self.main = main

        self.connect_checkbox(self.main.PID_Controller, self.main.nodes_selected)
        self.connect_checkbox(self.main.pids, self.main.nodes_selected)
        self.connect_checkbox(self.main.cameras, self.main.nodes_selected)
        self.connect_checkbox(self.main.motors, self.main.nodes_selected)
        
    def connect_checkbox(self, checkbox, text_edit):
        checkbox.toggled.connect(lambda state, te=text_edit, cb=checkbox: self.on_checkbox_toggled(state, te, cb))
            
    def on_checkbox_toggled(self, state, text_edit, checkbox):
        if state:
            text_edit.append(checkbox.objectName())  # Append the checkbox's object name to the text edit
            operation = "add"
        else:
            text = text_edit.toPlainText()
        
            # Construct the regular expression pattern to match the checkbox's object name
            pattern = r'\n?' + re.escape(checkbox.objectName())

            # Use re.sub() to remove the checkbox's object name along with the preceding newline character
            updated_text = re.sub(pattern, '', text)

            # Update the text content of the QTextEdit
            text_edit.setPlainText(updated_text)

            operation = "delete"
        
        subprocess.Popen(["bash", "../scripts/edit_startup_config.sh", operation, checkbox.objectName() + ".py"])        
