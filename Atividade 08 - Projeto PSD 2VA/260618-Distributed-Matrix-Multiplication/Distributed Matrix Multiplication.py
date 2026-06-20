from pathlib import Path
from common.matrixUtils import *
from common import simpleGUI as gui
from datetime import datetime
import multiprocessing
import os
import sys
import time

# ==========
# CONSTANTS

DEFAULT_PORT = 5000

# ==========
# USABLE FUNCTIONS

def exitIfNone(object):
    if object is None or object == "":
        sys.exit(0)

# ==========
# P1-P5 FUNCTIONS

def workerProcess(matrixA, matrixB, start, end, queue):
    partial = multiplyRows(matrixA, matrixB, start, end)
    return queue.put((start, partial))

def runParallel(matrixA, matrixB, numberOfProcesses):
    queue = multiprocessing.Queue()
    processes = []
    rows = getRowLength(matrixA)
    chunk = rows // numberOfProcesses  # How many times we be dividing the work of multiplying the matrices
    queue = multiprocessing.Queue()
    # ----------
    for workerIndex in range(numberOfProcesses):
        startRow = workerIndex * chunk
         # ----------
        if workerIndex == numberOfProcesses - 1:
            endRow = getRowLength(matrixA)
        else:
            endRow = startRow + chunk
         # ----------
        process = multiprocessing.Process(target=workerProcess, args=(matrixA, matrixB, startRow, endRow, queue))
        processes.append(process)
        process.start()

        for p in processes:
            p.join()
     # ----------
    matrixResult = [None] * getRowLength(matrixA)
    for workerIndex in range(numberOfProcesses):
        startRow, partial = queue.get()

        for index, row in enumerate(partial):
            matrixResult[startRow + index] = row
     # ----------
    return matrixResult

def P1(matrixA, matrixB):
    startTime = time.time()         # TIME STARTED
    matrix = multiplyRows(matrixA, matrixB, 0, len(matrixA))
    endTime = time.time()           # TIME FINISHED
    result = {
        "matrix" : matrix,
        "startTime" : startTime,
        "endTime" : endTime,
        "processingTime" : endTime - startTime
    }
    return result

def P2(matrixA, matrixB):
    workers = os.cpu_count()
    startTime = time.time()         # TIME STARTED

    matrix = runParallel(
        matrixA,
        matrixB,
        workers
    )

    endTime = time.time()         # TIME ENDED

    return {
        "matrix" : matrix,
        "startTime" : startTime,
        "endTime" : endTime,
        "processingTime" : endTime - startTime
    }

# ==========

def main():

    #inputDefaultPath = os.path.expanduser("~")
    inputDefaultPath = str(Path(__file__).resolve().parent) + "\\data\\input\\"
    outputDefaultPath = str(Path(__file__).resolve().parent) + "\\data\\output\\"

    askMatrix = True

    if askMatrix:
        #matrixA = gui.openFile(title="Selecione a Matriz A", fileTypes=[("Text Files", "*.txt")], initialPath=inputDefaultPath, ); exitIfNone(matrixA)
        #matrixB = gui.openFile(title="Selecione a Matriz B", fileTypes=[("Text Files", "*.txt")]); exitIfNone(matrixA)

        #matrixA = inputDefaultPath + "4_int.txt"
        matrixA = inputDefaultPath + "10_int.txt"
        #matrixA = inputDefaultPath + "10_float.txt"

    matrixA = readMatrix(matrixA)
    matrixB = matrixA

    if (getColumnLength(matrixA)) != (getRowLength(matrixB)):
        gui.showError("O número de colunas da 'matriz A' deve ser o mesmo que o número de linhas da 'matriz B'")
        sys.exit(0)

    # DELETE THIS IF STATEMENT LATER
    if getRowLength(matrixA) <= 10:
        print("-" * 50)
        print("MATRIX A:")
        printMatrix(matrixA)
        print("-" * 50)
        print("MATRIX B:")
        printMatrix(matrixB)
        print("-" * 50)

    #variation = gui.showSelectOptions(["P1", "P2", "P3", "P4", "P5"], title="Selecione", message="Selecione a Variação desejada:")
    variation = "P2" # =================================

    cores = os.cpu_count()
    remoteComputers=0

    # ==========
    print("STARTING MULTIPLICATION...")
    # ----------
    if variation == "P1":
        matrixResult = P1(matrixA, matrixB)
    # ----------
    elif  variation == "P2":
        matrixResult = P2(matrixA, matrixB)
    elif variation in "P2P3P4" and False:
        workers = cores
        if variation == "P3": workers = cores * 2
        if variation == "P4": workers = max(1, cores // 2)
        
        
        endTime = time.time()           # TIME FINISHED
    # ----------
            

    # ----------

    print("MULTIPLICATION FINISHED!")

    # ==========

    filename = f"Matrix {datetime.now()}.txt".replace(":", "-")  # datetime.now().strftime("Matrix_%Y-%m-%d_%H-%M-%S.txt")

    print(f"SAVING FILE: {filename}")
    writeMatrixResult(
        filename=outputDefaultPath + filename,  
        variation=variation,
        cores=cores,
        remoteComputers=remoteComputers,
        rows=getRowLength(matrixResult["matrix"]),
        cols=getColumnLength(matrixResult["matrix"]),
        processingTime=matrixResult["processingTime"],
        matrix=matrixResult["matrix"],
        formatted=True
    )
    print("FILE SAVED!")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
