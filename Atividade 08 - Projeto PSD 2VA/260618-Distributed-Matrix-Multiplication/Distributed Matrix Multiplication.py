from common import simpleGUI as gui
from common.matrixUtils import *
import os
import sys
from pathlib import Path


def exitIfNone(object):
    if object is None or object == "":
        sys.exit(0)

#inputDefaultPath = os.path.expanduser("~")
inputDefaultPath = str(Path(__file__).resolve().parent) + "\\data"

#gui.showMessage("Attention", "Application is starting")
#print(gui.showConfirm("Mhmm?"))

askMatrix = True

if askMatrix:
    matrixA = gui.openFile(title="Selecione a Matriz A", fileTypes=[("Text Files", "*.txt")], initialPath=inputDefaultPath, ); exitIfNone(matrixA)
    #matrixB = gui.openFile(title="Selecione a Matriz B", fileTypes=[("Text Files", "*.txt")]); exitIfNone(matrixA)

#variation = gui.showSelectOptions(["P1", "P2", "P3", "P4", "P5"], title="Selecione", message="Selecione a Variação desejada:")

variation = "P1"

printMatrix(readMatrix(matrixA))
