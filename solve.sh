#!/bin/bash

# Get the prefix from the command line argument
prefix="$1"

# Find all files in the ./models directory that start with the prefix
find ./models -name "${prefix}*.mod" -print0 | while IFS= read -r -d '' file; do
  # Extract the base filename without extension
  basename=$(basename "$file")
  filename="${basename%.*}"

  # Construct the glpsol command
  glpsol_command="glpsol -m ./models/${filename}.mod -d ./models/${filename}.dat --cuts"

  # Execute the glpsol command
  echo "Executing: $glpsol_command"
  $glpsol_command
done
