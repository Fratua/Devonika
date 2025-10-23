# DEVONIKA System Prompt Integration

## Overview

The DEVONIKA system prompt transforms the AI from a simple coding assistant into a complete software engineering system capable of building production-grade projects of any scale. This document explains how the system prompt is integrated into Devonika and how to use it effectively.

## Architecture

The DEVONIKA system prompt is implemented as a modular, composable system:

```
devonika/system_prompts/
├── __init__.py
├── system_prompt_manager.py    # Core manager for assembling prompts
├── components/                 # Modular prompt components
│   ├── core_identity.txt
│   ├── capabilities.txt
│   ├── operating_principles.txt
│   ├── context_management.txt
│   ├── communication_protocol.txt
│   ├── autonomous_mode.txt
│   ├── success_metrics.txt
│   └── final_directives.txt
└── workflows/                  # 5-phase workflow templates
    ├── phase1_discovery.txt
    ├── phase2_architecture.txt
    ├── phase3_implementation.txt
    ├── phase4_verification.txt
    └── phase5_deployment.txt
```

## Operational Modes

DEVONIKA supports multiple operational modes:

### 1. FULL Mode (Default)
Complete DEVONIKA system with all capabilities and workflows.

```python
from devonika.system_prompts import OperationalMode, get_devonika_prompt

prompt = get_devonika_prompt(mode=OperationalMode.FULL)
```

**Use when:** Building complete projects from scratch

### 2. AUTONOMOUS Mode
Maximum independence - DEVONIKA makes all decisions and executes without checkpoints.

```python
prompt = get_devonika_prompt(mode=OperationalMode.AUTONOMOUS)
```

**Use when:**
- You have a clear project vision
- You trust the AI to make architectural decisions
- You want minimal intervention

### 3. GUIDED Mode
Step-by-step with user approval at major checkpoints.

```python
prompt = get_devonika_prompt(mode=OperationalMode.GUIDED)
```

**Use when:**
- You want strategic oversight
- Important architectural decisions need review
- Learning how DEVONIKA works

### 4. DISCOVERY Mode
Focus on requirements gathering, research, and planning.

```python
prompt = get_devonika_prompt(mode=OperationalMode.DISCOVERY)
```

**Use when:**
- Exploring project feasibility
- Need comprehensive planning before coding
- Want to understand technical requirements

### 5. IMPLEMENTATION Mode
Focus on code implementation with quality assurance.

```python
prompt = get_devonika_prompt(mode=OperationalMode.IMPLEMENTATION)
```

**Use when:**
- Architecture is already defined
- Need to implement specific features
- Want focus on coding and testing

## Workflow Phases

DEVONIKA follows a structured 5-phase workflow:

### Phase 1: Discovery & Analysis
- Requirements gathering
- Technology research
- Risk assessment
- Output: PROJECT_SPECIFICATION.md

### Phase 2: Architecture & Design
- System design
- Technology selection
- Project structure planning
- Output: ARCHITECTURE.md

### Phase 3: Implementation
- Iterative development
- Test-driven development
- Continuous integration
- Code quality enforcement

### Phase 4: Verification & QA
- Functional testing
- Integration testing
- Performance testing
- Security validation
- Output: QA_REPORT.md

### Phase 5: Deployment & Delivery
- Deployment preparation
- Environment configuration
- Documentation
- Final delivery

## Using DEVONIKA in Your Code

### Basic Usage

```python
from devonika.intelligence.llm_interface import LLMInterface
from devonika.system_prompts import OperationalMode, WorkflowPhase

# Initialize with DEVONIKA
config = {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "operational_mode": "full",
    "use_devonika_prompt": True
}

llm = LLMInterface(config)

# Generate with DEVONIKA system prompt
response = await llm.generate_with_devonika(
    prompt="Build a REST API for a task management system"
)
```

### Phase-Specific Usage

```python
# Focus on a specific phase
llm.set_workflow_phase(WorkflowPhase.DISCOVERY)

response = await llm.generate_with_devonika(
    prompt="Analyze requirements for a social media platform"
)

# Clear phase to return to full workflow
llm.set_workflow_phase(None)
```

### Changing Operational Modes

```python
# Start in guided mode
llm.set_operational_mode(OperationalMode.GUIDED)

# Switch to autonomous for implementation
llm.set_operational_mode(OperationalMode.AUTONOMOUS)
```

### Custom Additions

```python
# Add custom instructions to the system prompt
custom_instructions = """
Additional requirements:
- Must use PostgreSQL database
- Must follow our company's coding standards
- Must include comprehensive error logging
"""

response = await llm.generate_with_devonika(
    prompt="Build a user authentication system",
    custom_system_additions=custom_instructions
)
```

## Configuration Files

DEVONIKA can be configured via JSON files. Example configurations are provided in `examples/`:

### Autonomous Configuration
```bash
devonika build "Create a todo app" --config examples/config_autonomous.json
```

### Guided Configuration
```bash
devonika build "Create a chat application" --config examples/config_guided.json
```

### Discovery Configuration
```bash
devonika build "Plan an MMORPG" --config examples/config_discovery.json
```

## Configuration Options

### LLM Configuration
```json
{
  "llm": {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.7,
    "operational_mode": "full",
    "use_devonika_prompt": true
  }
}
```

### Workflow Configuration
```json
{
  "workflows": {
    "skip_checkpoints": false,
    "auto_approve_architecture": false,
    "auto_approve_deployment": false,
    "require_user_approval": ["architecture", "deployment"],
    "focus_phase": null,
    "stop_after_phase": null
  }
}
```

## Best Practices

### 1. Start with Discovery for Complex Projects
For ambitious projects (games, enterprise systems, etc.), use Discovery mode first:

```bash
devonika build "Create an MMORPG" --config examples/config_discovery.json
```

Review the generated specifications, then proceed with implementation.

### 2. Use Guided Mode for Learning
If you're new to DEVONIKA or want to understand its decision-making:

```bash
devonika build "Build a web app" --config examples/config_guided.json
```

### 3. Use Autonomous Mode for Well-Defined Projects
For clear, straightforward projects:

```bash
devonika build "Create a CLI tool for JSON parsing" --config examples/config_autonomous.json
```

### 4. Provide Clear Project Descriptions
Even with vagueness resilience, clearer descriptions yield better results:

**Good:**
```
Build a task management web app with React frontend and Node.js backend.
Users should authenticate, create projects, add tasks with priorities,
and mark tasks complete. Include real-time updates.
```

**Better:**
```
Build a Trello-like task management web app.

Requirements:
- User authentication (email/password)
- Create/edit/delete projects and tasks
- Drag-and-drop task organization
- Priority levels and due dates
- Real-time collaboration
- Mobile-responsive design

Tech preferences:
- React + TypeScript frontend
- Node.js + Express backend
- PostgreSQL database
- WebSocket for real-time updates
```

## Advanced Features

### Modular Prompt Assembly

```python
from devonika.system_prompts import SystemPromptManager, WorkflowPhase

manager = SystemPromptManager()

# Get specific phase prompt
discovery_prompt = manager.get_phase_specific_prompt(WorkflowPhase.DISCOVERY)

# Get minimal prompt (just core identity and principles)
minimal_prompt = manager.get_minimal_prompt()

# Get full prompt with custom workflows
full_prompt = manager.get_system_prompt(
    mode=OperationalMode.FULL,
    include_workflows=[WorkflowPhase.DISCOVERY, WorkflowPhase.ARCHITECTURE]
)
```

### Inspecting Available Components

```python
manager = SystemPromptManager()

# See available components
components = manager.get_available_components()
print(components)
# ['core_identity', 'capabilities', 'operating_principles', ...]

# See available workflows
workflows = manager.get_available_workflows()
print(workflows)
# ['phase1_discovery', 'phase2_architecture', ...]
```

## Core Principles

DEVONIKA operates on these principles:

1. **Autonomous Intelligence**: Self-directed research and problem-solving
2. **Vagueness Resilience**: Handles incomplete requirements intelligently
3. **Scale-Appropriate Architecture**: Adapts to project complexity
4. **Quality First**: Every deliverable meets professional standards
5. **Transparency**: Clear communication of progress and decisions

## Success Metrics

DEVONIKA aims for:

- ✓ Technical Excellence: Clean, tested, performant code
- ✓ User Success: Usable, documented, reliable software
- ✓ Project Management: Transparent, efficient, complete delivery

## Troubleshooting

### Issue: System prompt not being applied
**Solution:** Ensure `use_devonika_prompt: true` in config

### Issue: Too autonomous or not autonomous enough
**Solution:** Adjust operational mode:
- More autonomy: Use `autonomous` mode
- More control: Use `guided` mode

### Issue: Project scope too large
**Solution:** Use `discovery` mode first to plan, then implement in phases

### Issue: Want to focus on specific phase
**Solution:** Use `set_workflow_phase()` to focus on one phase at a time

## Examples

### Example 1: Building a Simple API

```python
config = {"operational_mode": "autonomous"}
llm = LLMInterface(config)

result = await llm.generate_with_devonika(
    prompt="Create a REST API for a blog with posts and comments"
)
```

### Example 2: Planning a Complex Game

```python
llm.set_operational_mode(OperationalMode.DISCOVERY)

result = await llm.generate_with_devonika(
    prompt="Plan a 2D MMORPG with classes, combat, quests, and trading"
)
```

### Example 3: Guided Development

```python
llm.set_operational_mode(OperationalMode.GUIDED)

# Phase 1: Discovery
llm.set_workflow_phase(WorkflowPhase.DISCOVERY)
spec = await llm.generate_with_devonika(
    prompt="Build an e-commerce platform"
)

# Review spec, then proceed to architecture
llm.set_workflow_phase(WorkflowPhase.ARCHITECTURE)
architecture = await llm.generate_with_devonika(
    prompt="Design architecture based on the approved specification"
)

# Continue through phases...
```

## Contributing

To extend DEVONIKA system prompts:

1. Add new components in `devonika/system_prompts/components/`
2. Add new workflows in `devonika/system_prompts/workflows/`
3. Update `SystemPromptManager` to include new components
4. Add tests for new functionality
5. Update this documentation

## References

- [Main README](../README.md)
- [Architecture](ARCHITECTURE.md)
- [Getting Started](GETTING_STARTED.md)
- Example Configurations: `examples/config_*.json`
