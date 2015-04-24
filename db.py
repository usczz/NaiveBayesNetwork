import sqlite3


def getInsertCommand(tableName, attributes, values):
    atts = ','.join(attributes)
    vals = ','.join(values)
    command = 'INSERT INTO {0} ({1}) VALUES ({2})'.format(tableName, atts, vals)
    return command


def initDB(inputFile, dbFile):
    fin = open(inputFile, "r")
    lines = fin.readlines()
    line = lines[0]
    assert isinstance(line, str)
    attributes = line.split("\t")
    attributes[-1] = attributes[-1].replace("\r", "").replace("\n", "")
    schema = attributes[:]
    conn = sqlite3.connect(dbFile)
    tableName = 'risks'
    c = conn.cursor()
    incomeIndex = 0
    for i in range(0, len(schema)):
        if schema[i] == 'income':
            incomeIndex = i
        schema[i] = schema[i] + " TEXT"
    createCommand = 'CREATE TABLE {0} ({1})'.format(tableName, ','.join(schema))
    try:
        c.execute(createCommand)
    except sqlite3.OperationalError:
        c.execute('DROP TABLE {0}'.format(tableName))
        c.execute(createCommand)
    for i in range(1, len(lines)):
        values = lines[i].split("\t")
        values[-1] = values[-1].replace("\r", "").replace("\n", "")
        values[incomeIndex] = (int)(values[incomeIndex])
        if values[incomeIndex] <= 25000:
            values[incomeIndex] = '25000'
        elif values[incomeIndex] > 25000 and values[incomeIndex] <= 50000:
            values[incomeIndex] = '25001-50000'
        elif values[incomeIndex] > 50000 and values[incomeIndex] <= 75000:
            values[incomeIndex] = '50001-75000'
        elif values[incomeIndex] > 75000:
            values[incomeIndex] = '75000'
        for j in range(0, len(values)):
            values[j] = '\'{0}\''.format(values[j])
        command = getInsertCommand(tableName, attributes, values)
        c.execute(command)
    conn.commit()
    conn.close()
    fin.close()

def getConnection(dbFile):
    conn = sqlite3.connect(dbFile)
    return conn

def getCursor(conn):
    assert isinstance(conn,sqlite3.Connection)
    return conn.cursor()

def endConnection(conn):
    conn.commit()
    conn.close()

