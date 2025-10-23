# Devonika Architecture

This document describes the internal architecture of Devonika.

## Overview

Devonika is built as a multi-agent system where specialized components work together to autonomously build software projects. The architecture follows a modular design with clear separation of concerns.

## Core Components

### 1. DevonikaEngine (Core)

The main orchestrator that coordinates all subsystems.

**Location**: `devonika/core/engine.py`

**Responsibilities**:
- Project lifecycle management
- Component coordination
- Configuration management
- Progress tracking

**Key Methods**:
- `build_project()`: Main entry point for building projects
- `_iterative_development_loop()`: Manages the development cycle

### 2. ProjectPlanner

Analyzes requirements and creates comprehensive project plans.

**Location**: `devonika/planner/project_planner.py`

**Responsibilities**:
- Requirement analysis
- Component identification
- Task breakdown
- Technology stack suggestion

**Key Methods**:
- `create_comprehensive_plan()`: Creates detailed project plan
- `_expand_requirements()`: Expands vague descriptions
- `_generate_components()`: Identifies project components

### 3. SystemArchitect

Designs system architecture and structure.

**Location**: `devonika/architect/system_architect.py`

**Responsibilities**:
- Directory structure design
- Module architecture
- Data architecture
- API design
- Infrastructure planning

**Key Methods**:
- `design_architecture()`: Creates complete architecture
- `_design_directory_structure()`: Plans folder structure
- `_design_module_architecture()`: Designs component interactions

### 4. CodeGenerator

Generates actual source code files.

**Location**: `devonika/generator/code_generator.py`

**Responsibilities**:
- File generation
- Multi-language support
- Configuration file creation
- Documentation generation

**Key Methods**:
- `generate_project_structure()`: Creates all project files
- `_generate_component_files()`: Generates code for components
- `generate_documentation()`: Creates documentation

### 5. TaskExecutor

Executes individual development tasks.

**Location**: `devonika/executor/task_executor.py`

**Responsibilities**:
- Task execution
- File creation/modification
- Integration with existing code

**Key Methods**:
- `execute_task()`: Executes a single task
- `_execute_implementation_task()`: Implements code

### 6. TechResearcher

Researches technologies and gathers knowledge.

**Location**: `devonika/researcher/tech_researcher.py`

**Responsibilities**:
- Technology research
- Best practices gathering
- Framework knowledge

**Key Methods**:
- `research_technologies()`: Researches tech stack
- `_research_languages()`: Gathers language-specific knowledge

### 7. TestRunner

Runs tests and validates code.

**Location**: `devonika/tester/test_runner.py`

**Responsibilities**:
- Test execution
- Framework detection
- Result reporting

**Key Methods**:
- `run_tests()`: Executes test suite
- `_detect_test_framework()`: Identifies testing framework

### 8. AutoDebugger

Automatically debugs and fixes errors.

**Location**: `devonika/debugger/auto_debugger.py`

**Responsibilities**:
- Error analysis
- Fix generation
- Code repair

**Key Methods**:
- `debug_and_fix()`: Analyzes and fixes errors
- `_analyze_and_fix_error()`: Generates fixes for specific errors

### 9. PerformanceOptimizer

Optimizes code for performance.

**Location**: `devonika/optimizer/performance_optimizer.py`

**Responsibilities**:
- Performance analysis
- Optimization identification
- Code optimization

**Key Methods**:
- `optimize()`: Optimizes project
- `_identify_opportunities()`: Finds optimization opportunities

### 10. ProjectManager

Manages project state and progress.

**Location**: `devonika/manager/project_manager.py`

**Responsibilities**:
- Progress tracking
- Task prioritization
- State persistence

**Key Methods**:
- `get_next_task()`: Determines next task to work on
- `save_progress()`: Persists project state

## Supporting Components

### LLM Interface

Handles interactions with Large Language Models.

**Location**: `devonika/intelligence/llm_interface.py`

**Responsibilities**:
- LLM API calls
- Prompt engineering
- Response parsing
- Context management

### Tool Manager

Manages external tools and integrations.

**Location**: `devonika/tools/tool_manager.py`

**Responsibilities**:
- Git operations
- Package management
- Build operations
- Docker integration

### CLI

Command-line interface for user interaction.

**Location**: `devonika/cli/main.py`

**Responsibilities**:
- Argument parsing
- User interaction
- Progress display

## Data Flow

```
User Input (Description)
    ↓
DevonikaEngine
    ↓
ProjectPlanner → Plan
    ↓
SystemArchitect → Architecture
    ↓
TechResearcher → Knowledge
    ↓
CodeGenerator → Initial Codebase
    ↓
┌─────────────────────────────┐
│ Iterative Development Loop  │
│  ↓                          │
│  TaskExecutor → Code         │
│  ↓                          │
│  TestRunner → Results        │
│  ↓                          │
│  AutoDebugger → Fixes        │
│  ↓                          │
│  (repeat until complete)     │
└─────────────────────────────┘
    ↓
PerformanceOptimizer → Optimized Code
    ↓
CodeGenerator → Documentation
    ↓
Final Project
```

## Configuration

Configuration is managed through a hierarchical system:

1. Default configuration in `DevonikaEngine`
2. User-provided config file
3. Command-line arguments

Configuration schema:

```python
{
    "max_iterations": int,
    "auto_fix_errors": bool,
    "auto_test": bool,
    "auto_optimize": bool,
    "research_enabled": bool,
    "verbose": bool,
    "llm": {
        "provider": str,
        "model": str,
        "temperature": float
    }
}
```

## Project State

Project state is maintained in `.devonika/` directory:

```
.devonika/
├── plan.json           # Project plan
├── architecture.json   # Architecture design
└── progress.json       # Current progress
```

## Extension Points

The architecture is designed for extensibility:

1. **New Languages**: Extend `CodeGenerator` with language-specific generators
2. **New Test Frameworks**: Add methods to `TestRunner`
3. **New LLM Providers**: Implement in `LLMInterface`
4. **New Tools**: Add to `ToolManager`

## Design Principles

1. **Modularity**: Each component has a single, well-defined responsibility
2. **Async by Design**: All major operations are asynchronous
3. **Fail-Safe**: Errors are caught and handled gracefully
4. **Stateful**: Progress is saved regularly
5. **Extensible**: Easy to add new capabilities

## Performance Considerations

- LLM calls are the primary bottleneck
- Caching is used where possible
- File operations are batched
- Progress is saved incrementally

## Future Enhancements

- Parallel task execution
- Incremental code generation
- Learning from past projects
- Multi-agent collaboration
- Real-time progress streaming
