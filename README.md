# mutate4c

Mutation testing for **C** projects.

```bash
python -m pip install git+https://github.com/lukasa1993/mutate4c.git
mutate4c --test-command "cmake --build build && ctest --test-dir build"
```

The tool checks the baseline test command, mutates one operator at a time, runs tests, and restores the source after each mutant. Exit status `2` means a mutant survived.
