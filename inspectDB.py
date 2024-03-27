import psycopg2
import os

print('Checking environment ...')
environGood = True
if 'DB' not in os.environ:
  environGood = False
  print(' Remember to set DB environment variable: $env:db=\'\'')

if 'DB_UN' not in os.environ:
  environGood = False
  print(' Remember to set DB_UN environment variable: $env:DB_UN=\'\'')

if 'DB_PW' not in os.environ:
  environGood = False
  print(' Remember to set DB_PW environment variable: $env:DB_PW=\'\'')

if not environGood:
  print('Set up the environment and try again.')
  exit()

print('Setting up database connection ...')
conn = psycopg2.connect(database=os.environ['DB'], user=os.environ['DB_UN'], password=os.environ['DB_PW'], host='sc2-cit-b112', port='5432')
c1 = conn.cursor()
c2 = conn.cursor()
c3 = conn.cursor()

print('Database connection setup complete!')
print('Building query of public tables ...')
#c1 gets the list of tables
c1.execute('SELECT table_schema, table_name FROM information_schema.tables WHERE table_schema =%s',('public',))
print (str(c1.rowcount) + ' public tables found')

#iterate over the tables
for d1 in c1:
    #c2 gets the columns for the table for this loop pass
    c2.execute('SELECT table_name, column_name, data_type from information_schema.columns where table_name = %s order by table_name, ordinal_position',(d1[1],))
    #c3 gets data for this table
    c3.execute('select * from '+d1[1])
    cols = c2.rowcount
    print(' ')
    print ('Table ' + d1[0] + '.' + d1[1] + ' has ' + str(cols) + ' columns and ' + str(c3.rowcount) + ' row' + ('' if c3.rowcount==1 else 's'))

    #iterate over columns printing info
    for d2 in c2:
        print(' ' + str(d2[1]).ljust(20,' ') + ' | ' + d2[2])
    print(' ')
    if c3.rowcount > 0:
        print('Here '+('is' if c3.rowcount==1 else 'are')+' the first ' + (str(5) if c3.rowcount >= 5 else str(c3.rowcount)) + ' row' + ('' if c3.rowcount == 1 else 's') + ':')

    #iterate over table data printing first 5 records
    for d3 in c3:
        row = ''
        for i in range (cols):
            row = row + ' '+ str(d3[i]) + ' '
        print (row)
        if c3.rownumber == 5:
            break

print('Done!')

c3.close()
c2.close()
c1.close()
conn.close()
