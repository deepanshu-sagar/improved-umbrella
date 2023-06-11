# Improved Umbrella

## Description

This Python script is designed to split a large Python file into separate files based on its classes and functions. After splitting, it executes a specific command on each of these files. Then, it recombines these into a new Python file while maintaining the original order of functions.

## Usage

The script uses the following constants:

- `BIG_FILE_PATH`: The path to the large Python file that needs to be split.
- `NEW_DIR`: The directory where the new split files will be stored.
- `CMD`: The command to be executed on each split file.
- `OUTFILE`: The output file where the results of the command execution are stored.

## How it Works

1. The script first checks if the input file exists. If not, it raises a `FileNotFoundError`.
2. It then creates the directory where the new files will be stored.
3. The script parses the big Python file and maintains an ordered list of new file paths.
4. It separates classes and functions, and writes them to individual files.
5. The script then runs the command on the new Python file.
6. Finally, it combines all the small Python files into a new Python file.

## Requirements

- Python 3.6+
- `ast` and `subprocess` Python libraries

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
