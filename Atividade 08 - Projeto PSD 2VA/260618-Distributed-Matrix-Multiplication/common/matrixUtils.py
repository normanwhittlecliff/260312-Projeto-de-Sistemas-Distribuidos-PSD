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
