#!/usr/local/bin/zsh

cd /Users/tnt/dev/new_conda
conda activate dj
conda env export >  dj.yml
conda deactivate
conda activate ipy
conda env export >  ipy.yml
conda deactivate
conda activate lvim
conda env export >  lvim.yml
conda deactivate
conda activate pogo_ocr
conda env export >  pogo_ocr.yml
conda deactivate
conda activate py311
conda env export >  py311.yml
conda deactivate
conda activate py312
conda env export >  py312.yml
conda deactivate
conda activate py313
conda env export >  py313.yml
conda deactivate
conda activate py39
conda env export >  py39.yml
conda deactivate
conda activate qt
conda env export >  qt.yml
conda deactivate
conda activate scraping
conda env export >  scraping.yml
conda deactivate
conda activate tools
conda env export >  tools.yml
conda deactivate