# CLIENT
# color 2 & cd C:\Users\norma\OneDrive\Documents\College Subjects\2026.1 Projeto de Sistemas Distribuidos (PSD)\Atividade 08 - Projeto PSD 2VA\260618-Distributed-Matrix-Multiplication & python "Distributed Matrix Multiplication - Client.py"

from datetime import datetime
import multiprocessing
from common.matrixUtils import *
from multiprocessing import Manager
from multiprocessing import Pool, cpu_count
import time

import socket
import pickle

# ==================================================
# Matrix multiplication function that was in the common.matrixUtils
# ==================================================
def multiplyRows(matrixA, matrixB, startRow, endRow):
    result = []

    for i in range(startRow, endRow):
        rowResult = []

        for j in range(getColumnLength(matrixB)):
            value = 0

            for k in range(len(matrixB)):
                value += matrixA[i][k] * matrixB[k][j]
                #print(value)

            rowResult.append(value)
        result.append(rowResult)
    return result

def workerProcess(matrixA, matrixB, start, end, queue):
    partial = multiplyRows(matrixA, matrixB, start, end)
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

# --------------------------------------------------
# Uses ALL local CPU cores
# --------------------------------------------------
def processMatrix(matrixA_part, matrixB):

    cores = cpu_count()

    # Prevent creating more processes than rows
    cores = min(cores, len(matrixA_part))

    if cores == 0:
        return []

    chunk_size = len(matrixA_part) // cores

    chunks = []

    start = 0

    for i in range(cores):

        if i == cores - 1:
            end = len(matrixA_part)
        else:
            end = start + chunk_size

        chunks.append(matrixA_part[start:end])

        start = end

    tasks = []

    for chunk in chunks:
        tasks.append((chunk, matrixB))

    with Pool(cores) as pool:

        partial_results = pool.map(
            multiplyRows,
            tasks
        )

    final_result = []

    for part in partial_results:
        final_result.extend(part)

    return final_result


# --------------------------------------------------
# Main Worker Server
# --------------------------------------------------
def startClient():
    cores = cpu_count()

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )
    
    server.bind((HOST, PORT))
    server.listen()

    print(f"[CLIENT] Listening on port {PORT}")

    while True:
        conn, addr = server.accept()
        #server.settimeout(0)
        print(f"[CLIENT] Connection from {addr}")
        data = b""

        while True:
            packet = conn.recv(4096)
            if not packet:
                break
            data += packet
        task = pickle.loads(data)

        matrixA_part = task["A"]
        matrixB = task["B"]

        print(f"[CLIENT] Received {len(matrixA_part)} rows")
        #print(f"[CLIENT] Matrix A {matrixA_part}")
        #print(f"[CLIENT] Received {matrixB}")

        #resultRows = processMatrix(matrixA_part, matrixB)

        resultRows = runParallel(matrixA_part, matrixB, cores)

        #print(f"[CLIENT] Result Row {resultRows}")

        response = {
            "rows": resultRows["matrix"]
        }

        #print(response)

        conn.sendall(
            pickle.dumps(response)
        )

        conn.close()

        print("[CLIENT] Result sent")


if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = int(input("Port (ex: 5001): "))
    startClient()
