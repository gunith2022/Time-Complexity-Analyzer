# Time Complexity Analyzer

Time Complexity Analyzer is a project designed to analyze the Big O time complexity of source code using static code analysis through Abstract Syntax Trees (ASTs). The initial version is developed for Python and focuses on evaluating `for` loops under the assumption that the loop variable is not modified within the loop body. After refining the Python implementation, the project will be extended to support other programming languages and more complex constructs.

## Overview

- **Purpose:**  
  Analyze the time complexity (Big O) of source code by leveraging AST-based static analysis.

- **Primary Focus:**  
  - Currently developed for Python.
  - Analyzes `for` loops where the loop variable remains unchanged within the loop body.

- **Future Scope:**  
  Extend support to other programming languages and handle additional control structures and recursive functions.

## Features

- **AST-Based Static Analysis:**  
  Utilizes Python's `ast` module to parse code and understand its abstract structure.

- **Loop Complexity Evaluation:**  
  Focuses on analyzing the time complexity of `for` loops along with upcoming support for `while` loops and recursive functions.

- **Extensible and Modular Architecture:**  
  Designed to accommodate extensions such as handling non-linear loop variable modifications and solving recurrence relations.

## Key Challenges

As part of the initial phase, this project aims to address the following challenges:

1. **Tracking non-linear change of loop variable:**  
   Accurately tracking cases where the loop variable changes in a non-linear pattern.

2. **Handling loop variable in `while` loops:**  
   Analyzing the behavior of loop variables in `while` loops, which can have more unpredictable iteration counts.

3. **Generating recursive relations for recursive functions:**  
   Creating models to represent the recursive structure of functions and characterizing their time complexity.

4. **Solving recurrence relations:**  
   Automatically solving the recurrence relations derived from recursive functions to provide a Big O estimation.

## Contribution & Community Involvement

We welcome contributions from everyone:

- **Have a solution but can't code?**  
  If you have a solid solution or idea—even if you're not comfortable coding—you can send your contribution to **gunithyadav4@gmail.com** with the subject line `TIME-COMPLEXITY-ANALYZER`.

- **Skilled in Python?**  
  You're invited to contribute your skills to improve the code, fix bugs, or add new features. Open an issue or submit a pull request to share your enhancements.

If you're interested in tackling any of the challenges listed above or have ideas for new features, please join the conversation and help shape this project.

## Future Directions

- **Enhanced Structural Analysis:**  
  Expand the tool to analyze additional control structures such as complex `while` loops and conditional statements.

- **Multi-Language Support:**  
  Extend the analyzer to incorporate other programming languages post the stable Python implementation.

- **Advanced Recurrence Analysis:**  
  Improve the generation and solving of recurrence relations for more accurate time complexity predictions in recursive functions.

- **Real-Time Integration:**  
  Explore the possibility of integrating the analyzer into popular IDEs for real-time code analysis.

