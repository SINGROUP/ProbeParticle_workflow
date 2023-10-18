from runner import SlurmRunner

sch = SlurmRunner.from_database('slurm:PPM', 'database.db')

print('starting')
sch.spool()