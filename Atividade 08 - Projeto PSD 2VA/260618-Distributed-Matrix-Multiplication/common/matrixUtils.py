def printMatrix(matrix):
    """
    This function takes a matrix and prints it nicely on the terminal.
    """
    for row in matrix:
        print(" ".join(f"{item:4}" for item in row))


def readMatrix(fileName):
    with open(fileName, "r") as file:
        rows, columns = map(int, file.readline().split())
        matrix = []
        for _ in range(rows):
            row = list(map(float, file.readline().replace(" \n", "").split(" ")))
            matrix.append(row)

    return matrix


def writeMatrixResult(
    filename,
    variation,
    cores,
    remoteComputers,
    rows,
    cols,
    processingTime,
    matrix,
    formatted=False
):
    with open(filename, "w") as file:

        if formatted:
            # Header information FORMATTED
            file.write(f"Variação do programa: {variation}\n")
            file.write(f"Número de Cores: {cores}\n")
            file.write(f"Número de computadores Remotos: {remoteComputers}\n")
            file.write(f"Número de linhas da Matriz: {rows}\n")
            file.write(f"Número de colunas da matriz: {cols}\n")
            file.write(f"Tempo de processamento (em segundos): {processingTime:.6f}\n")
        else:
            # Header information NOT FORMATTED
            file.write(f"{variation}\n")
            file.write(f"{cores}\n")
            file.write(f"{remoteComputers}\n")
            file.write(f"{rows}\n")
            file.write(f"{cols}\n")
            file.write(f"{processingTime:.6f}\n")

        file.write("\n")

        # Matrix
        for row in matrix:
            line = " ".join(map(str, row))
            file.write(line + "\n")


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


def getRowLength(matrix):
    return len(matrix)


def getColumnLength(matrix):
    return len(matrix[0])
