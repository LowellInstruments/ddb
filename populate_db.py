import sqlite3


def table_create(db, t):
    conn = sqlite3.connect(db)
    conn.execute('''CREATE TABLE if not exists {}
    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    DAY     TEXT    NOT NULL,
    LAT     TEXT    NOT NULL,
    LON     TEXT    NOT NULL,
    VALUE   TEXT    NOT NULL);'''.format(t))
    conn.close()


def table_display(db, t):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM {}".format(t))
    rows = cur.fetchall()
    for row in rows:
        print(row)


def table_query(db, t, day, lat, lon):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = ''' SELECT * FROM {} WHERE DAY = ? AND LAT = ? AND LON = ?'''.format(t)
    cur.execute(sql, (day, lat, lon))
    rows = cur.fetchall()

    if len(rows) == 0:
        print('no value for this day and coordinates')
        return

    assert len(rows) == 1
    s = 'the value for day #{} at ({},{}) was {}'
    v = rows[0][4]
    print(s.format(day, lat, lon, v))
    return v


def table_delete(db, t):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('DROP TABLE if exists {}'.format(t))
    conn.commit()
    conn.close()


# ----------------------------------------------
# lat, lon grids are 221 x 201
# lat starts at +35, increases row by 0.05
# lon starts at -76, increases col by 0.05
# ----------------------------------------------

def put_data_file_to_table(db, t, s):
    # s: 'Bottom_Temperature/BT_197'
    # fv: file values handler
    # lv: list of lines w/ values
    print('processing', s)
    with open(s, 'r') as fv:
        lv = fv.read().splitlines()

    # opening database here accelerates the process :)
    day = s.split('.')[0]
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    sql = ''' INSERT INTO {}(DAY, LAT, LON, VALUE)
              VALUES(?,?,?,?) '''.format(t)

    # rw: row
    # i_r: index row
    # i_c: index column
    for i_r, rw in enumerate(lv):
        rw = rw.split(',')
        for i_c, v in enumerate(rw):
            if v == 'NaN':
                continue

            # calculate lat, lon statically
            lat = 35 + (i_r * .05)
            lon = -76 + (i_c * .05)
            day = s.split('.')[0].split('_')[2]

            # save to DB
            cursor.execute(sql, (day, lat, lon, v))

    # closing our stuff
    conn.commit()
    conn.close()
