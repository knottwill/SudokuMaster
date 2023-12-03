# use the Miniconda3 base image
FROM continuumio/miniconda3

# Install git and curl
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the Docker image
WORKDIR /sudoku_master

# Copy the current directory contents into the container at /sudoku_master
COPY . /sudoku_master

# # update the conda environment
RUN conda env update --file environment.yml --name base
# RUN conda env create -f environment.yml -n sudoku
# SHELL ["conda", "run", "-n", "sudoku", "/bin/bash", "-c"]
# # RUN conda install numpy black flake8 line_profiler pytest pre-commit

# Get data
RUN mkdir -p puzzles \
    && curl https://norvig.com/top95.txt --output puzzles/hard.txt \
    && curl https://norvig.com/hardest.txt --output puzzles/hardest.txt \
    && curl https://projecteuler.net/project/resources/p096_sudoku.txt --output puzzles/easy.txt

# Run the data conversion script
RUN python convert_data.py
