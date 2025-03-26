#!/bin/bash

#SBATCH --partition=all
#SBATCH --job-name=comsol_job
#SBATCH --time=10-40:00:00
#SBATCH --nodelist=node32
#SBATCH --output=/home/tlswpgus22/slurm_manager/log/test/%A.log


PYTHON_PATH="/home/tlswpgus22/.conda/envs/tera/bin/python"

# Python 스크립트 실행
$PYTHON_PATH -u /home/tlswpgus22/slurm_manager/task.py
