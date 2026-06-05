# XYZC Language Documentation

## Overview

**XYZC is a systems programming language designed for developers who need explicit control over memory, execution, and resource allocation without compromise. It prioritizes predictability, auditability, and performance-critical semantics while remaining practical for large-scale systems development.**

## Table of Contents
1. [About](#about)
2. [Syntax](#syntax)
3. [Data Types](#data-types)
4. [Features](#features)
5. [Examples](#examples)

## About

XYZC is engineered for scenarios where C's simplicity and control meet modern systems demands. Unlike languages that enforce safety through restrictions, XYZC trusts the developer to make intentional trade-offs between safety guarantees and performance requirements. Every feature is designed to be auditable — what you write is what executes, with no hidden allocations, implicit behavior, or runtime overhead.

The language assumes you know what you're doing. It provides the tools for low-level manipulation, direct hardware access, and fine-grained resource management without apology or compromise. Safety mechanisms exist where they add value without performance cost; elsewhere, the responsibility lies with the programmer.

### Target Use Cases

- **Operating Systems & Low-Level Systems — Kernels, bootloaders, firmware where direct hardware control and memory manipulation are fundamental**
- **Performance-Critical Applications — Game engines, real-time systems, databases, compilers where predictability and zero-overhead execution are essential**
- **High-Assurance Software — Systems requiring complete auditability and explicit control flow, where implicit behavior is unacceptable**

### Design Principles
- **Explicit Over Implicit** — No hidden allocations, implicit conversions, or magical behavior. What you write is what executes.
- **Programmer Trust** — The language assumes competence and intent. Safety is the programmer's responsibility, not enforced by the compiler.
- **Complete Control** — Direct access to memory, hardware, and execution flow without abstraction layers or restrictions standing in the way.

## Syntax

### Basic Structure
```
as task(UNIQUE-ID) with address(TYPE-TASK-ADDRESS-HERE) {
  // code here...
}
```
Tasks are the fundamental execution units in XYZC. Each task has a unique identifier and an explicit memory address, giving the programmer full control over where code executes and how it's isolated.

### Function Declaration
```
// Type 1 - normal functions
callable STORAGE-LOCATION-HERE NAME(INT arg1, INT arg2) {
  return INT arg1 + INT arg2;
}

// Type 2 - family functions
callable STORAGE-LOCATION-HERE name(INT id) {
  let STORAGE-LOCATION-HERE num1 = INT getChildValue(INT id, childNum1); // get the value of childNum1
  let STORAGE-LOCATION-HERE num2 = INT getChildValue(INT id, childNum2); // same here for childNum2
}

let editable STORAGE-LOCATION-HERE childNum1(INT id) = INT 0; // use the same variable type and name as the parent (funtion)
let editable STORAGE-LOCATION-HERE childNum1(INT id) = int 0; //same
// ^^^^^^^^^^ this keyword allows files (or users) to edit the variable outside the file
```

Functions in XYZC are storage-explicit and support family hierarchies. The `editable` keyword allows external modification of child variables, giving precise control over scope and access patterns.

### Variables
```
let virtual a = INT 7; // stores a in memory
let register a = INT 7; // stores a in CPU
let stack a = INT 7; // stores a in a stack frame
let static a = INT 7; // stores a in a data segment
let heap a = INT 7; // stores a in a heap
// Flags
let STORAGE-LOCATION-HERE volatile a = INT 7; // forces the compiler to lookup the variable everytime (never cache)
let STORAGE-LOCATION-HERE a = INT 7 at ADDR(0x4000) // store a at a specific address
```

Variables in XYZC give explicit control over storage location — virtual, register, stack, static, or heap. Flags like `volatile` and address pinning (`at ADDR`) allow fine-grained optimization and hardware interaction.

### Control Flow
```
[FILL IN: If/else, loops, etc.]
```

## Data Types

| Type | Description | Example |
|------|-------------|---------|
| **[FILL IN]** | [FILL IN] | `[FILL IN]` |
| **[FILL IN]** | [FILL IN] | `[FILL IN]` |
| **[FILL IN]** | [FILL IN] | `[FILL IN]` |

## Features

### [FILL IN: Feature 1]
**[Description]**

```
[FILL IN: Code example]
```

### [FILL IN: Feature 2]
**[Description]**

```
[FILL IN: Code example]
```

### [FILL IN: Feature 3]
**[Description]**

```
[FILL IN: Code example]
```

## Examples

### Example 1: [FILL IN: Title]
```
[FILL IN: Full working example]
```

### Example 2: [FILL IN: Title]
```
[FILL IN: Full working example]
```

## Comparison with Other Languages

| Aspect | XYZC | C | Rust |
|--------|------|---|------|
| **[FILL IN]** | [FILL IN] | [FILL IN] | [FILL IN] |
| **[FILL IN]** | [FILL IN] | [FILL IN] | [FILL IN] |

---

*XYZC: [FILL IN: Tagline/motto]*
