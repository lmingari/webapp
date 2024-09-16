#!/bin/bash
#SBATCH --job-name=FALL3D
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=20
#SBATCH --time=00:10:00
#SBATCH --qos=training
#SBATCH --reservation=Computational24

#module purge
#module load intel/2017.4
#module load impi/2017.4
#module load netcdf

RUNDIR={{path}}
EXEDIR=/home/lmingari/fall3d/fall3d/build3/Fall3d.r8.x
INPFILE="config.inp"
TASK="all"

{% for field in form if field.widget.input_type != 'hidden' -%}
{{field.label.text}}={{field.data}}
{% endfor %}
NP=$((NX*NY*NZ*NENS))

cd $RUNDIR
mpirun -np ${NP} ${EXEDIR} ${TASK} ${INPFILE} ${NX} ${NY} ${NZ} -nens ${NENS}
