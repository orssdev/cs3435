# Data Collection & Visualization

cs3435 Fall 2025

## Setting up an environment with conda
Creating a conda environment:  
run: `conda create -n cs3435 python=3.12`  

Install the following packages:  
run: `conda install beautifulsoup4 seaborn requests jupyter ipython`  

run: `conda install -c conda-forge selenium scrapy protego scikit-learn`

run: `conda install -c conda-forge python-dotenv`

## HW3
To export data to jsonl file in /hw3   
run: `scrapy crawl hw3 -O plot_explained.jsonl`