import os
import subprocess


class EnvivarSettings:
    def __init__(self, envivarName):
        self.envivarName = envivarName

    def setEnvVar(self, val):
        # Linux OS
        # if os.name == 'posix':
        # exportLX = f'export {self.envariableName}="{value}"'
        # subprocess.Popen(exportLX, shell=False).wait()
        # Windows OS
        # After set a user environment variable restart the os to accept the changes
        try:
            if os.name == 'nt':
                exportNT = f'setx {self.envivarName} "{val}"'
                subprocess.Popen(exportNT, shell=False).wait()
                return True
            else:
                return False
        except OSError as e:
            print(e)

    def getEnvVar(self):
        if os.environ.get(self.envivarName) is not None:
            return True, os.environ.get(self.envivarName)
        else:
            return False, os.environ.get(self.envivarName)
