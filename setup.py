import os
import termcolor

required_directories = ["finished", "lower_finished", "assets", "meta"]

print("\n\ncreating required directories...\n")
for dir in required_directories:
    path = os.path.join(".", dir)

    try:
        os.mkdir(path)
        print(termcolor.colored(f"✔ Created Directory {dir}"))
    except:
        print(termcolor.colored(f"❌ Directory already exists {dir}", "red"))

print("\nfinished setting up project")