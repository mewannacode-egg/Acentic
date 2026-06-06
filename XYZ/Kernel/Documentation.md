# XYZ Kernel Documentation

## Overview

**The XYZ Kernel is a systems kernel built entirely in XYZC, designed for explicit hardware control, predictable execution, and transparent resource management. It runs on XYZ company's hardware and software, all built in XYZC, with three distro variants offering different levels of system access.**

The kernel prioritizes auditability and performance — every system operation maps directly to XYZC code with no hidden abstractions.

---

## Table of Contents
1. [Architecture](#architecture)
2. [Boot Process](#boot-process)
3. [Task Management](#task-management)
4. [Memory Management](#memory-management)
5. [Hardware Abstraction Layer](#hardware-abstraction-layer)
6. [Distro Freedom Levels](#distro-freedom-levels)

---

## Architecture

### Core Components

The XYZ Kernel consists of four primary subsystems:

| Component | Role |
|-----------|------|
| **Boot Manager** | Hardware initialization, bootloader handoff, early task setup |
| **Task Scheduler** | Process/task execution, context switching, priority management |
| **Memory Manager** | Virtual/physical memory mapping, storage allocation, address management |
| **Hardware Abstraction Layer (HAL)** | Device drivers, interrupt handling, direct hardware access |

All components are built in XYZC with no machine-code fallback.

### Execution Model

The kernel is built on XYZC's **task-based execution model**. Every process, daemon, and interrupt handler is a first-class task with:
- Unique task identifier
- Explicit memory address space (kernel-space or user-space)
- Direct storage control (register, stack, heap, pinned addresses)

Tasks are the fundamental unit of execution — not threads, not processes, but XYZC tasks with transparent scheduling.

---

## Boot Process

### Stage 1: Hardware Detection
The bootloader transfers control to the kernel entry point. The kernel:
1. Reads XYZ hardware specification (CPU count, RAM size, device list)
2. Initializes minimal CPU features (interrupt table, memory paging)
3. Sets up kernel-space memory range

### Stage 2: Task System Initialization
1. Create KERNEL-MAIN task in kernel-space
2. Initialize task scheduler (for single or multi-core execution)
3. Load interrupt handlers and exception handlers as tasks

### Stage 3: Distro Boot Selection
The kernel presents three boot paths based on XYZC language freedom:
- **Unrestricted**: Full XYZC language access for user tasks
- **Moderate**: Selected XYZC features enabled; some restrictions apply
- **Restricted**: Core XYZC only; heavy sandboxing

### Stage 4: User-Space Initialization
1. Load selected distro's init system into user-space
2. Create user-space address isolation boundaries
3. Spawn first user-space task
4. Transfer execution to the distro

---

## Task Management

### Task Structure

Each task in the XYZ Kernel has:
- **Task ID**: Unique identifier (e.g., USER-APP-1, DRIVER-USB, KERNEL-SCHEDULER)
- **Memory Space**: Kernel-space (unrestricted) or user-space (isolated)
- **Storage Locations**: Variables explicitly placed in registers, stack, heap, or pinned memory addresses
- **Isolation Level**: Kernel tasks bypass protection; user-space tasks are restricted by MMU

### Task Lifecycle

| State | Meaning |
|-------|---------|
| **NEW** | Task created, not yet scheduled |
| **READY** | Task waiting for CPU time |
| **RUNNING** | Task currently executing on CPU |
| **BLOCKED** | Task waiting for I/O or resource |
| **TERMINATED** | Task finished; resources freed |

### Context Switching

When the scheduler switches from one task to another, it saves:
- CPU registers
- Stack pointer and program counter
- Memory protection settings (page table base)
- Task state (priority, flags, timeout)

The scheduler restores all state from the previous task. Context switches are deterministic and fully auditable in XYZC.

### Scheduling

Tasks are scheduled based on:
- **Priority**: User-space tasks may have lower priority than kernel tasks
- **Time slice**: Each task gets CPU time; scheduler preempts on timeout
- **Blocking**: If a task waits for I/O, scheduler immediately switches to next ready task
- **Multi-core**: On multi-core XYZ hardware, multiple tasks run simultaneously; the scheduler balances load

---

## Memory Management

### Storage Locations (XYZC-Native)

XYZC provides four storage locations; the kernel uses all of them:

| Location | Speed | Size | Scope | Use |
|----------|-------|------|-------|-----|
| **Register** | Fastest | Very small (CPU register count) | CPU-local | Hot variables, function parameters |
| **Stack** | Fast | Limited (per-task stack) | Task-local | Local variables, function frames |
| **Heap** | Medium | Large (system RAM) | Task-local or shared | Dynamic allocation, data structures |
| **Pinned Address** | Medium | Specific address | Kernel or device | Hardware registers, kernel data structures |

### Virtual Memory

User-space tasks operate in virtual address space. The kernel maintains page tables that map:
- Virtual address (what task sees)
- Physical address (actual RAM location)
- Permissions (read, write, execute)

The MMU (Memory Management Unit) enforces these mappings. Attempts to access unmapped or restricted pages trigger a page fault, which the kernel handles as an exception.

### Kernel-Space vs User-Space

| Aspect | Kernel-Space | User-Space |
|--------|--------------|-----------|
| **Memory Access** | Unrestricted; direct physical memory | Restricted to allocated virtual ranges |
| **I/O Access** | Full hardware I/O capability | Via system calls to kernel tasks |
| **Storage Control** | All XYZC storage types allowed | Register/stack/heap only (NO pinned addresses) |
| **Address Pinning** | Allowed; direct hardware mapping | Not allowed; kernel manages all addresses |

### Memory Protection

The kernel enforces isolation using the MMU. User-space tasks cannot:
- Access kernel memory
- Access other tasks' memory
- Directly access hardware (must use system calls)
- Modify page tables

Violations trigger page faults, which the kernel treats as task termination or exception handling.

---

## Hardware Abstraction Layer (HAL)

### Device Driver Model

Drivers are kernel-space tasks with unrestricted hardware access. Each driver:
- Manages a specific device (UART, timer, network, storage)
- Exposes system calls for user-space tasks to interact with the device
- Handles interrupts from the device
- Manages device state and resources

### Interrupt Handling

When hardware triggers an interrupt (IRQ), the CPU:
1. Pauses the current task (saves context)
2. Looks up the interrupt handler (kernel task) in the interrupt table
3. Switches to kernel-space and runs the handler
4. Handler processes the interrupt (e.g., read data from device)
5. Context switches back to the interrupted task

Interrupt handlers are kernel-space tasks with highest priority. They must be fast and deterministic.

### Exception Handling

Exceptions (faults, traps) are similar to interrupts but triggered by the CPU itself:
- **Page fault**: Task accessed invalid memory
- **Division by zero**: Invalid arithmetic operation
- **Invalid opcode**: Task executed forbidden instruction (security violation)

The kernel handles exceptions by terminating the task or raising an exception handler.

### Supported Hardware

The XYZ Kernel abstracts:
- **CPU**: Single-core or multi-core via task scheduling
- **Memory**: Physical RAM, memory controllers, page tables
- **Interrupts**: Programmable interrupt controller (APIC, GIC, or custom)
- **I/O**: UART (serial), timers, block devices, network interfaces
- **Storage**: Disk controllers, mapped as readable/writable memory regions

All hardware access goes through the HAL. User-space code cannot directly touch hardware.

---

## Distro Freedom Levels

### Level X: Unrestricted (Full System Access)

**User tasks can:**
- Direct hardware access via pinned addresses
- Access all system calls with no restrictions
- Full kernel memory access for privileged operations
- Bypass memory protection when needed

**Capability:** Maximum performance and flexibility. Full system access.

**Risk:** Applications can crash the system, corrupt kernel memory, or access other tasks' data.

---

### Level Y: Moderate (Selective System Access)

**User tasks cannot:**
- Direct hardware access via pinned addresses
- Access kernel memory or other tasks' memory

**BIG type limits:**
- BIG INT: 320 digits maximum
- BIG FLOAT: 320 digits maximum
- BIG STR: 8,060 characters maximum

**Capability:** Good balance of flexibility and safety.

**Trade-off:** Cannot directly manipulate hardware or access privileged kernel data. Slightly slower due to MMU checks.

---

### Level Z: Restricted (Minimal System Access)

**User tasks cannot:**
- Use BIG INT, BIG FLOAT, or BIG STR (fixed-size types only)
- Direct hardware access via pinned addresses
- Access kernel memory or other tasks' memory

**Capability:** Maximum safety and auditability. Suitable for untrusted or critical code.

**Trade-off:** Limited to fixed-size data types. All system calls validated by kernel before execution.

---

## System Calls

User-space tasks request kernel services via system calls. The kernel validates each call and executes the operation in kernel-space, giving user-space tasks indirect access to hardware and system resources they cannot reach directly.

System calls are the only bridge between user-space and kernel-space. Examples include memory allocation, device I/O, task creation, and timing operations — but the exact system call interface depends on the distro's freedom level and specific implementation.

---

## Summary

The XYZ Kernel is a **transparent, auditable systems kernel** built entirely in XYZC. It provides:

✓ **Explicit control** over task execution and memory layout  
✓ **Three freedom levels** enabling different safety/performance trade-offs  
✓ **Hardware abstraction** for device independence  
✓ **Task-based parallelism** leveraging XYZC's native task model  
✓ **Zero hidden overhead** — what executes in XYZC is what you get  

Developers select a distro freedom level matching their security and performance requirements. The kernel ensures isolation, resource accountability, and predictable execution.

---

*XYZ Kernel: Built for explicit control. Choose your freedom level.*
