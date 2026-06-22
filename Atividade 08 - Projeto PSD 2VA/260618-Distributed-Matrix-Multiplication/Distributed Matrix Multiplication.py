from pathlib import Path
from common.matrixUtils import *
from common import simpleGUI as gui
from datetime import datetime
import multiprocessing
from multiprocessing import Manager
import os
import sys
import time
import socket
import pickle
import threading

# ====================
# CONSTANTS

DEFAULT_PORT = 5000

# ====================
# USABLE FUNCTIONS

def exitIfNone(object):
    if object is None or object == "":
        sys.exit(0)

# ====================
# P1-P5 FUNCTIONS

def workerProcess(matrixA, matrixB, start, end, queue):
    partial = multiplyRows(matrixA, matrixB, start, end)
    #print(partial)
    return queue.put((start, partial))

def runParallel(matrixA, matrixB, numberOfProcesses):
    manager = Manager()
    queue = manager.Queue()
    processes = []
    rows = getRowLength(matrixA)
    chunk = rows // numberOfProcesses  # How many times we be dividing the work of multiplying the matrices
    # --------------------
    startTime = time.time()         # TIME STARTED
    for workerIndex in range(numberOfProcesses):
        startRow = workerIndex * chunk
         # --------------------
        if workerIndex == numberOfProcesses - 1:
            endRow = getRowLength(matrixA)
        else:
            endRow = startRow + chunk
         # --------------------
        process = multiprocessing.Process(target=workerProcess, args=(matrixA, matrixB, startRow, endRow, queue))
        processes.append(process)
        process.start()

    for p in processes:
        p.join()
     # --------------------
    matrixResult = [None] * getRowLength(matrixA)
    for workerIndex in range(numberOfProcesses):
        startRow, partial = queue.get()

        for index, row in enumerate(partial):
            matrixResult[startRow + index] = row
     # --------------------
    endTime = time.time()         # TIME ENDED

    return {
        "matrix" : matrixResult,
        "startTime" : startTime,
        "endTime" : endTime,
        "processingTime" : endTime - startTime
    }

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

    matrix = runParallel(
        matrixA,
        matrixB,
        workers
    )

    return matrix



def sendJob(
    workerID,
    workerIP,
    workerPort,
    matrixPart,
    matrixB,
    responses
):
    try:

        client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        client.connect(
            (workerIP, workerPort)
        )

        #client.settimeout(0)

        payload = {
            "A": matrixPart,
            "B": matrixB
        }

        client.sendall(
            pickle.dumps(payload)
        )

        client.shutdown(
            socket.SHUT_WR
        )

        data = b""

        while True:

            packet = client.recv(4096)

            if not packet:
                break

            data += packet

        result = pickle.loads(data)

        responses[workerID] = result["rows"]

        client.close()

    except Exception as e:

        print(
            f"Worker {workerID} failed: {e}"
        )


def P5(matrixA, matrixB):
    # -----------------------------------
    # List of worker machines
    # -----------------------------------


    # REMEBER TO CHANGE THE IPs HERE TO THE ONE ON THE MASTER'S IP
    workers = [
        ("192.168.1.104", 5001),
        ("192.168.1.104", 5002),
        ("192.168.1.104", 5003)
        #("192.168.1.107", 5004),  # my laptop
        #("192.168.1.107", 5005)   # my laptop
    ]

    workerCount = len(workers)

    # -----------------------------------
    # Split Matrix A
    # -----------------------------------
    startTime = time.time()
    rowsPerWorker = len(matrixA) // workerCount

    matrixParts = []

    for i in range(workerCount):

        start = i * rowsPerWorker

        if i == workerCount - 1:
            end = len(matrixA)
        else:
            end = (i + 1) * rowsPerWorker

        matrixParts.append(
            matrixA[start:end]
        )

    # -----------------------------------
    # Send jobs
    # -----------------------------------

    responses = [None] * workerCount

    threads = []

    for i in range(workerCount):

        ip, port = workers[i]

        thread = threading.Thread(
            target=sendJob,
            args=(
                i,
                ip,
                port,
                matrixParts[i],
                matrixB,
                responses
            )
        )

        thread.start()

        threads.append(thread)

    # -----------------------------------
    # Wait all workers
    # -----------------------------------

    for thread in threads:
        thread.join()

    # -----------------------------------
    # Join results
    # -----------------------------------

    resultMatrix = []
    for part in responses:
        if part is not None:
            resultMatrix.extend(part)
    endTime = time.time()

    result = {
        "matrix": resultMatrix,
        "startTime": startTime,
        "endTime": endTime,
        "processingTime": endTime - startTime,
        "remoteComputers": len(workers)
    }
    #print(f"DEBUG: P5 Result: {result}")
    return result

# ========================================
# MAIN CODE
# ========================================
def main(variation=None, filename=None):
    inputDefaultPath = str(Path(__file__).resolve().parent) + "\\data\\input\\"
    outputDefaultPath = str(Path(__file__).resolve().parent) + "\\data\\output\\"
    
    if filename is None:
        matrixAName = gui.openFile(title="Selecione a Matriz A", fileTypes=[("Text Files", "*.txt")], initialPath=inputDefaultPath, ); exitIfNone(matrixAName)
        matrixBName = gui.openFile(title="Selecione a Matriz B", fileTypes=[("Text Files", "*.txt")]); exitIfNone(matrixBName)
    else:
        matrixAName = inputDefaultPath + filename
        matrixBName = inputDefaultPath + filename

    matrixA = readMatrix(matrixAName)
    matrixB = readMatrix(matrixBName)

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

    if variation is None:
        variation = gui.showSelectOptions(["P1", "P2", "P3", "P4", "P5"], title="Selecione", message="Selecione a Variação desejada:")

    cores = os.cpu_count()
    remoteComputers=0

    # ====================
    print("STARTING MULTIPLICATION...")
    # ----------
    if variation == "P1":
        matrixResult = P1(matrixA, matrixB)
    # ----------
    elif variation in "P2 P3 P4":
        workers = cores
        if variation == "P3": workers = cores * 2
        if variation == "P4": workers = max(1, cores // 2)
        
        matrixResult = runParallel(matrixA, matrixB, workers)
    elif variation == "P5":
        matrixResult = P5(matrixA, matrixB)
        remoteComputers = matrixResult["remoteComputers"]
    else:
        gui.showError(f"Variação Inválida! <{variation}>")
    # ----------
    

    print("MULTIPLICATION FINISHED!")

    # ====================

    filename = f"Matrix {datetime.now()} ({variation} {filename}).txt".replace(":", "-")  # datetime.now().strftime("Matrix_%Y-%m-%d_%H-%M-%S.txt")

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
        formatted=False
    )
    print("FILE SAVED!")

if __name__ == "__main__":
    multiprocessing.freeze_support()
    variations = ["P1", "P2", "P3", "P4", "P5"]
    filenames = [
        "4_int.txt", 
        "4_int1.txt",
        "4_int2.txt",
        "10_int.txt",
        "10_float.txt",
        "128.txt",
        "512.txt",
        "1024.txt",
        "2048.txt"
        ]
    
    for variation in variations[0:4]:
        for filename in filenames[0:8]:
            main(variation=variation, filename=filename)
    gui.showMessage("PROGRAM FINISHED")
    
    #main(variation=variations[4])
