# Devonika - AI Software Engineer

<div align="center">

**A full-fledged AI software engineer capable of building projects of any scale from scratch**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## Overview

Devonika is not just another programmer assistant AI tool - it's a complete, autonomous software engineering system equipped with all the tools necessary for anything and everything. From simple CLI tools to complex MMORPGs, Devonika can build it all.

### Key Features

- **Autonomous Development**: Builds complete projects from start to finish with minimal human intervention
- **Vague Input Handling**: Adapts and overcomes even the most ambiguous project descriptions
- **Multi-Language Support**: Works with Python, JavaScript/TypeScript, Rust, and more
- **Full Project Lifecycle**: Planning, architecture, implementation, testing, debugging, and optimization
- **Scalable**: Handles projects of any size - from simple scripts to enterprise applications
- **Self-Healing**: Automatically debugs and fixes errors during development
- **Adaptive Learning**: Researches technologies and best practices as needed

## Architecture

Devonika consists of several interconnected subsystems:

1. **Project Planner**: Analyzes requirements and creates comprehensive project plans
2. **System Architect**: Designs system architecture and module structure
3. **Code Generator**: Generates production-ready code in multiple languages
4. **Task Executor**: Executes individual development tasks autonomously
5. **Tech Researcher**: Researches technologies and gathers implementation knowledge
6. **Test Runner**: Runs tests and validates code quality
7. **Auto Debugger**: Identifies and fixes bugs automatically
8. **Performance Optimizer**: Optimizes code for performance and best practices
9. **Project Manager**: Tracks progress and manages task prioritization
10. **Tool Manager**: Integrates with Git, package managers, databases, and more

## Installation

### Prerequisites

- Python 3.8 or higher
- API key for an LLM provider (Anthropic Claude or OpenAI)

### Install from source

```bash
# Clone the repository
git clone https://github.com/fratua/devonika.git
cd devonika

# Install dependencies
pip install -r requirements.txt

# Install Devonika
pip install -e .
```

### Set up API key

```bash
# For Anthropic Claude (recommended)
export ANTHROPIC_API_KEY=your_api_key_here

# Or for OpenAI
export OPENAI_API_KEY=your_api_key_here
```

## Quick Start

### Build a project from a description

```bash
devonika build "Create a REST API for a blog with users, posts, and comments"
```

### Build with specific project name

```bash
devonika build "Create a real-time chat application" --name chat_app
```

### Check project status

```bash
devonika status my_project
```

### List all projects

```bash
devonika list
```

### Interactive mode

```bash
devonika interactive
```

## Usage Examples

### Example 1: Simple CLI Tool

```bash
devonika build "Create a command-line tool that converts markdown to HTML"
```

### Example 2: Web Application

```bash
devonika build "Build a task management web app with React frontend and Node.js backend. Users should be able to create, edit, delete, and organize tasks into projects."
```

### Example 3: Game (Complex Project)

```bash
devonika build "Create a multiplayer online chess game with user accounts, matchmaking, ELO ratings, and game history"
```

### Example 4: MMORPG (Very Complex Project)

Yes, Devonika can even attempt this:

```bash
devonika build "Create a 2D MMORPG with character classes, inventory system, combat, questing, player trading, guilds, and a persistent world"
```

Note: Extremely large projects may require multiple iterations and human oversight.

## Configuration

Create a `config.json` file to customize Devonika's behavior:

```json
{
  "max_iterations": 1000,
  "auto_fix_errors": true,
  "auto_test": true,
  "auto_optimize": true,
  "research_enabled": true,
  "verbose": true,
  "llm": {
    "provider": "anthropic",
    "model": "claude-3-5-sonnet-20241022",
    "temperature": 0.7
  }
}
```

Use it with:

```bash
devonika build "your project description" --config config.json
```

## How It Works

1. **Understanding**: Devonika analyzes your project description, even if vague, and expands it into detailed requirements
2. **Planning**: Creates a comprehensive project plan with components, tasks, and dependencies
3. **Architecture**: Designs the system architecture, directory structure, and data models
4. **Research**: Researches relevant technologies and best practices
5. **Implementation**: Generates code iteratively, component by component
6. **Testing**: Runs tests after each implementation phase
7. **Debugging**: Automatically fixes errors and failures
8. **Optimization**: Optimizes code for performance and maintainability
9. **Documentation**: Generates comprehensive documentation

## Project Structure

```
devonika/
├── devonika/
│   ├── core/           # Main engine and orchestration
│   ├── planner/        # Project planning and requirement analysis
│   ├── architect/      # System architecture design
│   ├── generator/      # Code generation
│   ├── executor/       # Task execution
│   ├── researcher/     # Technology research
│   ├── tester/         # Testing and validation
│   ├── debugger/       # Auto-debugging
│   ├── optimizer/      # Performance optimization
│   ├── manager/        # Project management
│   ├── intelligence/   # LLM interface
│   ├── tools/          # Tool integrations
│   └── cli/            # Command-line interface
├── tests/              # Test suite
├── docs/               # Documentation
└── examples/           # Example projects
```

## Limitations and Considerations

- **LLM Costs**: Building large projects requires many LLM API calls, which can be expensive
- **Time**: Complex projects may take considerable time to complete
- **Human Oversight**: While autonomous, some projects benefit from human review and guidance
- **Experimental**: This is an ambitious project and may not always produce perfect results
- **API Limits**: Respect rate limits of your LLM provider

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

MIT License - see LICENSE file for details

## Disclaimer

Devonika is an experimental project that pushes the boundaries of AI-assisted software development. While it can generate impressive results, always review generated code for security, correctness, and suitability for your use case.

## Roadmap

- [ ] Support for more programming languages (Go, Java, C++, etc.)
- [ ] Web UI interface
- [ ] Project templates and presets
- [ ] Integration with cloud deployment platforms
- [ ] Collaborative multi-agent architecture
- [ ] Learning from user feedback
- [ ] Plugin system for extensibility
- [ ] Support for modifying existing projects

## Contact

For questions, feedback, or support, please open an issue on GitHub.

---

Built with ❤️ by Fratua
