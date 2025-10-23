"""
Example: Building a simple project with Devonika

This example shows how to use Devonika programmatically to build a simple project.
"""

import asyncio
from devonika.core.engine import DevonikaEngine


async def main():
    """Build a simple calculator application"""

    # Initialize the engine
    engine = DevonikaEngine(
        workspace="./example_workspace",
        config={
            "max_iterations": 50,  # Limit iterations for demo
            "auto_test": True,
            "auto_fix_errors": True,
            "verbose": True
        }
    )

    # Define the project
    description = """
    Create a command-line calculator application that:
    - Supports basic operations (add, subtract, multiply, divide)
    - Has a clean, user-friendly interface
    - Handles errors gracefully
    - Includes unit tests
    """

    print("Building calculator application...")
    print(f"Description: {description}")
    print()

    # Build the project
    result = await engine.build_project(description, project_name="calculator")

    # Check results
    if result["status"] == "success":
        print("\n✓ Project built successfully!")
        print(f"Location: {result['path']}")
    else:
        print("\n✗ Build failed")
        print(f"Error: {result.get('error')}")


if __name__ == "__main__":
    asyncio.run(main())
