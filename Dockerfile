# use the Miniconda3 base image
FROM continuumio/miniconda3

# install git and curl
# (final line removes package lists which are no longer needed)
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# set the working directory in the Docker image
WORKDIR /sudoku_master

# copy the current directory contents into the container at /sudoku_master
COPY . /sudoku_master

# update the conda environment
RUN conda env update --file environment.yml --name base

# get data
RUN mkdir -p puzzles \
    && curl https://norvig.com/top95.txt --output puzzles/hard.txt \
    && curl https://norvig.com/hardest.txt --output puzzles/hardest.txt \
    && curl https://projecteuler.net/project/resources/p096_sudoku.txt --output puzzles/easy.txt

# run the data conversion script
RUN python convert_data.py
