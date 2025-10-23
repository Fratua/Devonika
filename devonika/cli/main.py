"""
Devonika CLI - Command-line interface for the AI Software Engineer
"""

import asyncio
import argparse
import sys
import os
from pathlib import Path
import logging

from devonika.core.engine import DevonikaEngine


class DevonikaCLI:
    """Command-line interface for Devonika"""

    def __init__(self):
        self.parser = self._create_parser()

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog="devonika",
            description="Devonika - Full-Fledged AI Software Engineer",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Build a project from a description
  devonika build "Create a REST API for a blog with users and posts"

  # Build with a specific name
  devonika build "Create a chess game" --name chess_game

  # Build using a specific workspace
  devonika build "Create a TODO app" --workspace ./my_projects

  # Check status of a project
  devonika status my_project

  # List all projects
  devonika list

For more information, visit: https://github.com/fratua/devonika
            """
        )

        subparsers = parser.add_subparsers(dest="command", help="Command to execute")

        # Build command
        build_parser = subparsers.add_parser("build", help="Build a project from description")
        build_parser.add_argument("description", help="Project description (can be vague)")
        build_parser.add_argument("--name", "-n", help="Project name (auto-generated if not provided)")
        build_parser.add_argument("--workspace", "-w", default="./workspace", help="Workspace directory")
        build_parser.add_argument("--config", "-c", help="Path to config file")
        build_parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

        # Status command
        status_parser = subparsers.add_parser("status", help="Check project status")
        status_parser.add_argument("project", help="Project name")
        status_parser.add_argument("--workspace", "-w", default="./workspace", help="Workspace directory")

        # List command
        list_parser = subparsers.add_parser("list", help="List all projects")
        list_parser.add_argument("--workspace", "-w", default="./workspace", help="Workspace directory")

        # Interactive mode
        interactive_parser = subparsers.add_parser("interactive", help="Start interactive mode")
        interactive_parser.add_argument("--workspace", "-w", default="./workspace", help="Workspace directory")

        return parser

    async def run(self, args=None) -> int:
        """Run the CLI"""
        args = self.parser.parse_args(args)

        if not args.command:
            self.parser.print_help()
            return 1

        try:
            if args.command == "build":
                return await self._cmd_build(args)
            elif args.command == "status":
                return await self._cmd_status(args)
            elif args.command == "list":
                return await self._cmd_list(args)
            elif args.command == "interactive":
                return await self._cmd_interactive(args)
            else:
                print(f"Unknown command: {args.command}")
                return 1

        except KeyboardInterrupt:
            print("\n\nInterrupted by user")
            return 130
        except Exception as e:
            print(f"Error: {e}")
            if args.verbose if hasattr(args, 'verbose') else False:
                import traceback
                traceback.print_exc()
            return 1

    async def _cmd_build(self, args) -> int:
        """Execute build command"""
        print("=" * 60)
        print("Devonika AI Software Engineer")
        print("=" * 60)
        print(f"\nProject: {args.description}")
        print(f"Workspace: {args.workspace}")
        print()

        # Check for API key
        if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
            print("ERROR: No API key found!")
            print("Please set ANTHROPIC_API_KEY or OPENAI_API_KEY environment variable")
            print("\nExample:")
            print("  export ANTHROPIC_API_KEY=your_api_key_here")
            return 1

        # Create config
        config = {}
        if args.config:
            import json
            config = json.loads(Path(args.config).read_text())

        if args.verbose:
            config["verbose"] = True

        # Initialize engine
        print("Initializing Devonika engine...")
        engine = DevonikaEngine(workspace=args.workspace, config=config)

        # Build project
        print("\nStarting project build...\n")
        result = await engine.build_project(args.description, args.name)

        # Print results
        print("\n" + "=" * 60)
        if result["status"] == "success":
            print("✓ Project build completed successfully!")
            print(f"\nProject location: {result['path']}")
            print("\nNext steps:")
            print(f"  cd {result['path']}")
            print("  # Review the generated code")
            print("  # Install dependencies if needed")
            print("  # Run tests")
            print("  # Start the application")
            return 0
        else:
            print("✗ Project build failed")
            print(f"\nError: {result.get('error', 'Unknown error')}")
            return 1

    async def _cmd_status(self, args) -> int:
        """Execute status command"""
        workspace = Path(args.workspace)
        project_path = workspace / args.project

        if not project_path.exists():
            print(f"Project not found: {args.project}")
            return 1

        engine = DevonikaEngine(workspace=args.workspace)
        status = engine.get_project_status()

        print(f"Project: {args.project}")
        print(f"Status: {status.get('status', 'unknown')}")
        print(f"Completion: {status.get('completion_percentage', 0):.1f}%")
        print(f"Iteration: {status.get('iteration', 0)}")
        print(f"Last updated: {status.get('last_updated', 'never')}")

        return 0

    async def _cmd_list(self, args) -> int:
        """Execute list command"""
        engine = DevonikaEngine(workspace=args.workspace)
        projects = engine.list_projects()

        if not projects:
            print("No projects found in workspace")
            return 0

        print(f"Projects in {args.workspace}:")
        for project in projects:
            print(f"  - {project}")

        return 0

    async def _cmd_interactive(self, args) -> int:
        """Execute interactive mode"""
        print("=" * 60)
        print("Devonika Interactive Mode")
        print("=" * 60)
        print("\nType 'help' for commands, 'exit' to quit\n")

        engine = DevonikaEngine(workspace=args.workspace)

        while True:
            try:
                user_input = input("devonika> ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "q"]:
                    print("Goodbye!")
                    return 0

                if user_input.lower() == "help":
                    self._print_interactive_help()
                    continue

                if user_input.lower() == "list":
                    projects = engine.list_projects()
                    if projects:
                        print("Projects:")
                        for p in projects:
                            print(f"  - {p}")
                    else:
                        print("No projects found")
                    continue

                if user_input.lower().startswith("build "):
                    description = user_input[6:].strip()
                    if description:
                        print(f"\nBuilding: {description}\n")
                        result = await engine.build_project(description)
                        if result["status"] == "success":
                            print(f"\n✓ Project built: {result['path']}")
                        else:
                            print(f"\n✗ Build failed: {result.get('error')}")
                    continue

                print("Unknown command. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit")
                continue

    def _print_interactive_help(self):
        """Print interactive mode help"""
        print("""
Available commands:
  build <description>  - Build a new project
  list                 - List all projects
  help                 - Show this help message
  exit                 - Exit interactive mode
        """)


def main():
    """Main entry point"""
    cli = DevonikaCLI()
    exit_code = asyncio.run(cli.run())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
