from PyQt5 import QtWidgets, uic
from home_page.navigate_pages import ButtonActions
from home_page.add_pages import AddPage
from home_page.launch_page import Launch
from home_page.icons import Icons
import subprocess

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load the .ui file
        uic.loadUi('../ui/mainwindow.ui', self)

        add_page = AddPage(self)
        add_page.add_widgets()

        button_handler = ButtonActions(self)
        button_handler.connect_buttons()
        
        icons = Icons(self)
        icons.setIcons()
        
        self.stacked_widget.setCurrentIndex(0)  # Set the initial page to index 0
        
        self.start_robot.clicked.connect(self.run_startup_script)
        
        launch_page = Launch(self)
    
    def run_startup_script(self):
        try:
            # Specify the path to the Python file you want to run
            subprocess.run(["python", "../../launch/startup.py"])
        except Exception as e:
            print("Error:", e)

    def closeEvent(self, event):
        # Define the path to the bash script
        bash_script_path = "../scripts/cleanup_scripts.sh"

        # Run the bash script using subprocess
        subprocess.Popen(["bash", bash_script_path])
        event.accept()