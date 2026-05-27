#!/usr/bin/env python3
"""
A simple Hello World Python script with some additional features.
This script demonstrates basic Python functionality.
"""

def greet(name="World"):
    """
    Greet a person by name.
    
    Args:
        name (str): The name to greet (default: "World")
    
    Returns:
        str: A greeting message
    """
    return f"Hello, {name}!"

def main():
    """Main function to demonstrate the script's functionality."""
    print("=" * 50)
    print("Hello World Python Script")
    print("=" * 50)
    
    # Basic greeting
    print(greet())
    
    # Greet with a custom name
    print(greet("Python Developer"))
    
    # Interactive greeting
    try:
        user_name = input("\nWhat's your name? ").strip()
        if user_name:
            print(greet(user_name))
        else:
            print("No name provided, using default.")
            print(greet())
    except EOFError:
        print("\nNo input provided, using default.")
        print(greet())
    
    # Demonstrate some Python features
    print("\n" + "=" * 50)
    print("Python Version Information:")
    import sys
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    
    # Simple calculation example
    print("\n" + "=" * 50)
    print("Simple Calculation Example:")
    numbers = [1, 2, 3, 4, 5]
    total = sum(numbers)
    average = total / len(numbers)
    print(f"Numbers: {numbers}")
    print(f"Sum: {total}")
    print(f"Average: {average:.2f}")
    
    print("\n" + "=" * 50)
    print("Script execution completed successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()