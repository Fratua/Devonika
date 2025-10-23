# Getting Started with Devonika

This guide will help you get started with Devonika, the AI Software Engineer.

## Prerequisites

Before using Devonika, ensure you have:

1. **Python 3.8+** installed
2. **API Key** for either:
   - Anthropic Claude (recommended)
   - OpenAI GPT

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/fratua/devonika.git
cd devonika
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Install Devonika

```bash
pip install -e .
```

### Step 4: Set Up API Key

```bash
# For Anthropic Claude
export ANTHROPIC_API_KEY=your_api_key_here

# Or for OpenAI
export OPENAI_API_KEY=your_api_key_here
```

To make the API key permanent, add it to your `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export ANTHROPIC_API_KEY=your_api_key_here' >> ~/.bashrc
source ~/.bashrc
```

## Your First Project

Let's build a simple project to test Devonika:

```bash
devonika build "Create a command-line tool that generates random passwords"
```

Devonika will:
1. Analyze the description
2. Plan the project
3. Design the architecture
4. Generate code
5. Test and debug
6. Create documentation

The process may take several minutes depending on project complexity.

## Understanding the Output

After completion, you'll find your project in the workspace directory:

```
workspace/
└── password_generator/
    ├── .devonika/           # Devonika metadata
    │   ├── plan.json        # Project plan
    │   ├── architecture.json # Architecture design
    │   └── progress.json    # Build progress
    ├── src/                 # Source code
    ├── tests/               # Test files
    ├── docs/                # Documentation
    ├── requirements.txt     # Dependencies
    ├── README.md           # Project README
    └── ...
```

## Using Your Generated Project

```bash
# Navigate to the project
cd workspace/password_generator

# Install dependencies (if any)
pip install -r requirements.txt

# Run the application
python src/main.py

# Run tests
pytest tests/
```

## Building More Complex Projects

### Web Application

```bash
devonika build "Create a REST API for a library management system with books, authors, and borrowing records"
```

### With Specific Requirements

```bash
devonika build "Build a real-time chat application with:
- User authentication
- Multiple chat rooms
- Message history
- WebSocket support
- React frontend
- Node.js backend"
```

## Configuration

Create a `config.json` file for custom settings:

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
devonika build "your description" --config config.json
```

## Tips for Best Results

1. **Be Descriptive**: While Devonika handles vague descriptions, more detail leads to better results
2. **Specify Technologies**: If you have preferences, mention them (e.g., "using React and Express")
3. **Define Features Clearly**: List the main features you want
4. **Start Small**: For complex projects, consider building components incrementally
5. **Review Output**: Always review generated code for your specific needs

## Interactive Mode

For an interactive experience:

```bash
devonika interactive
```

Commands in interactive mode:
- `build <description>` - Build a project
- `list` - List all projects
- `help` - Show help
- `exit` - Exit interactive mode

## Next Steps

- Read the [Architecture Guide](ARCHITECTURE.md) to understand how Devonika works
- Check out [Examples](../examples/) for sample projects
- Explore the [API Documentation](API.md) for programmatic usage

## Troubleshooting

### "No API key found"

Make sure your API key is properly set:

```bash
echo $ANTHROPIC_API_KEY
```

If empty, set it again.

### "Module not found"

Reinstall dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

### Build Takes Too Long

Large projects can take time. You can:
- Reduce `max_iterations` in config
- Start with a simpler version
- Use `--verbose` to see progress

## Getting Help

- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

Happy building with Devonika!
