from runner import TerminalRunner

sch = TerminalRunner.from_database('terminal:PPM', 'database.db')

print('starting')
sch.spool()
