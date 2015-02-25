import sys
from PySide import QtGui
from forms.MainWizard import MainWizard
from Application import Application


if __name__ == '__main__':
    application = QtGui.QApplication(sys.argv)
    
    wizard = MainWizard()
    wizard.run()
    sys.exit(wizard.exec_())
