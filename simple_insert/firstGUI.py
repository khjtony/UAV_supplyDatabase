__author__ = 'khjtony'

# Allow access to command-line arguments
import sys

# Import the core and GUI elements of Qt
from PySide.QtCore import *
from PySide.QtGui import *

# Every Qt application must have one and only one QApplication object;
# it receives the command line arguments passed to the script, as they
# can be used to customize the application's appearance and behavior
qt_app = QApplication(sys.argv)

# Create a label widget with our text
label = QLabel('Hello, world!')

# Show it as a standalone widget
label.show()

# Run the application's event loop
qt_app.exec_()