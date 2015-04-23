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
    schema[0] = schema[0] + " INTEGER"
    for i in range(1, len(schema)):
        schema[i] = schema[i] + " TEXT"
    createCommand = 'CREATE TABLE {0} ({1})'.format(tableName, ','.join(schema))
    print createCommand
    try:
        c.execute(createCommand)
    except sqlite3.OperationalError:
        c.execute('DROP TABLE {0}'.format(tableName))
        c.execute(createCommand)
    for i in range(1, len(lines)):
        values = lines[i].split("\t")
        values[-1] = values[-1].replace("\r", "").replace("\n", "")
        for j in range(1, len(values)):
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