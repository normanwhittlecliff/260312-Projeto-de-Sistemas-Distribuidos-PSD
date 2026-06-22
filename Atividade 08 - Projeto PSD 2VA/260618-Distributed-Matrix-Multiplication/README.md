# Distributed Matrix Multiplication

A Python implementation of sequential, parallel, and distributed matrix multiplication developed for the **Distributed Systems (Projeto de Sistemas Distribuidos)** course.

This project compares different execution strategies for matrix multiplication, ranging from a traditional single-process implementation to a distributed architecture capable of delegating computation across multiple machines.

## Information
- **Project ID**: 260614
- **Title**: Distributed Matrix Multiplication
- **Creator**: Norman Vinícius Pereira dos Santos (normanwhittlecliff)
- **Date of Creation**: June 16, 2026
- **Language**: Python
<!-- - **Change Log**: [CHANGELOG.md](https://github.com/normanwhittlecliff/260322-Markdown-TOC-Generator/blob/main/CHANGELOG.md) -->

---

## Requirements & Dependencies

### Python

Python 3.9 or newer

---

## Objectives

The main objective of this project is to analyze the impact of parallelism and distribution on the execution time of matrix multiplication.

The project implements five different approaches:

| Variation | Description                                                                     |
| --------- | ------------------------------------------------------------------------------- |
| P1        | Sequential execution using a single process                                     |
| P2        | Parallel execution using a number of processes equal to the number of CPU cores |
| P3        | Parallel execution using twice the number of CPU cores                          |
| P4        | Parallel execution using half the number of CPU cores                           |
| P5        | Distributed execution using a master-worker architecture with remote machines   |

The execution time of each variation can be compared to evaluate scalability and performance.

---

## Features

* Matrix multiplication from text files
* Sequential execution
* Multiprocessing-based parallel execution
* Distributed execution using a master-worker architecture
* Automatic workload partitioning
* Execution time measurement
* Result export to text files
* Simple graphical user interface (GUI)

---

## Technologies Used

* Python 3
* Multiprocessing
* Socket Programming
* Tkinter

---

## Project Structure

```text
Distributed-Matrix-Multiplication/
│
├── common/
│   ├── simpleGUI.py
│   └── matrixUtils.py
│
├── data/
│   ├── input/
│   │   ├── 4_int.txt
│   │   ├── 10_float.txt
│   │   ├── 10_int.txt
│   │   ├── 128.txt
│   │   ├── ...
│   │   └── 2048.txt
│   └── output/
│
├── Distributed Matrix Multiplication - Client.py
│
└── Distributed Matrix Multiplication.py
```

### Input File Format

The application expects matrices to be stored in text files, where the first line holds two numbers; The number of rows and the number of columns.

Example:

```text
3 3
1 2 3
4 5 6
7 8 9
```

### Format

```text
<rows> <columns>
<row 1 values>
<row 2 values>
...
<row n values>
```

Values can be integers or floating-point numbers.

### Output File Format

The generated result file follows the structure below:

```text
P2
8
0
3
3
0.003217

30 24 18
84 69 54
138 114 90
```

### Description

| Line | Content                        |
| ---- | ------------------------------ |
| 1    | Program variation (P1–P5)      |
| 2    | Number of processes/cores used |
| 3    | Number of remote computers     |
| 4    | Number of matrix rows          |
| 5    | Number of matrix columns       |
| 6    | Processing time (seconds)      |
| 7    | Blank line                     |
| 8+   | Result matrix                  |

---
<!-- 
## Execution Strategies

### P1 — Sequential

The entire matrix multiplication is performed by a single process.

### P2 — Parallel (CPU Cores)

The matrix rows are divided among a number of worker processes equal to the available CPU cores.

### P3 — Parallel (2× CPU Cores)

The matrix rows are divided among twice the number of available CPU cores.

### P4 — Parallel (½ CPU Cores)

The matrix rows are divided among half the available CPU cores.

### P5 — Distributed

A master process distributes portions of the matrix multiplication task to remote worker machines.

Each worker computes its assigned rows and returns the partial result to the master, which reconstructs the final matrix.

---

## Running the Project

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project folder:

```bash
cd Distributed-Matrix-Multiplication
```

Run the application:

```bash
python "Distributed Matrix Multiplication.py"
```

---

## Performance Evaluation

This project was designed to compare:

* Sequential execution
* Local multiprocessing
* Distributed execution

Execution times can be compared using different matrix sizes to evaluate:

* Speedup
* Scalability
* Resource utilization
* Communication overhead

---

## Future Improvements

* Shared memory implementation
* Dynamic load balancing
* NumPy optimization
* Distributed execution over heterogeneous networks
* Performance graphs and statistics
* Automatic worker discovery

---

## Author

**Norman**

Distributed Systems Project

---

## License

This project was developed for educational purposes.

-->
