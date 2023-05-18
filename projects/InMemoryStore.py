def solution(queries):
    output = []
    db = {}
    restore_point = []

    for q in queries:
        if q[0] == "SET":
            if db.get( q[1] ):
                db[ q[1] ][ q[2] ] = q[3]
            else:
                db[ q[1] ] = { q[2] : q[3] }
            output.append("")


        elif q[0] == "COMPARE_AND_SET":
            if db.get( q[1], {} ).get( q[2], "" ) == q[3]:
                if q[4]:
                    db[ q[1] ][ q[2] ] = q[4]
                else:
                    del( db[ q[1] ][ q[2] ] )
                output.append("true")
            else:
                output.append("false")


        elif q[0] == "GET":
            output.append( db.get( q[1], {} ).get( q[2], "" ) )


        elif q[0] == "SCAN":
            s = ""
            for k, v in iter( sorted( db.get( q[1], {} ).items() ) ):
                if k.startswith( q[2] ):
                    if s:
                        s += (", " + k + "(" + v + ")")
                    else:
                        s = k + "(" + v + ")"
            output.append(s)


        elif q[0] == "SET_AT":
            if db.get( q[1] ):
                db[ q[1] ][ q[2] ] = ( q[3], int( q[4] ), int( q[5] ) )
            else:
                db[ q[1] ] = { q[2] : ( q[3], int( q[4] ), int( q[5] ) ) }
            output.append("")


        elif q[0] == "COMPARE_AND_SET_AT":
            if db.get( q[1], {} ).get( q[2], ("",) )[ 0 ] == q[3]:
                if q[4]:
                    db[ q[1] ][ q[2] ] = ( q[4], int( q[5] ), int( q[6] ) )
                else:
                    del( db[ q[1] ][ q[2] ] )
                output.append("true")
            else:
                output.append("false")


        elif q[0] == "GET_AT":
            if db.get( q[1], {} ).get( q[2] ) and db[ q[1] ][ q[2] ][1] <= int( q[3] ):
                if db[ q[1] ][ q[2] ][2] == 0:
                    output.append( db[ q[1] ][ q[2] ][0] )
                elif int( q[3] ) <= db[ q[1] ][ q[2] ][1] + db[ q[1] ][ q[2] ][2]:
                    output.append( db[ q[1] ][ q[2] ][0] )
                else:
                    output.append( "" )
            else:
                output.append("")


        elif q[0] == "SCAN_AT":
            s = ""
            for k, v in iter( sorted( db.get( q[1], {} ).items() ) ):
                if v[1] <= int( q[3] ):
                    if v[2] == 0:
                        if k.startswith( q[2] ):
                            if s:
                                s += (", " + k + "(" + v[0] + ")")
                            else:
                                s = k + "(" + v[0] + ")"
                    elif int( q[3] ) <= v[1] + v[2]:
                        if k.startswith( q[2] ):
                            if s:
                                s += (", " + k + "(" + v[0] + ")")
                            else:
                                s = k + "(" + v[0] + ")"
            output.append(s)


        elif q[0] == "BACKUP":
            bkp_db = {}
            count = 0
            for k1, v1 in db.items():
                r = {}
                for k2, v2 in db[ k1 ].items():
                    a = db[ k1 ][ k2 ][ 0 ]
                    b = db[ k1 ][ k2 ][ 1 ]
                    c = db[ k1 ][ k2 ][ 2 ]
                    if b <= int( q[1] ):
                        if c == 0:
                            r[ k2 ] = ( a, 0, 0 )
                        elif int( q[1] ) < b + c:
                            r[ k2 ] = ( a, 0,  b + c - int( q[1] ) )
                if r:
                    count += 1
                    bkp_db[ k1 ] = r
            if bkp_db:
                restore_point.append( ( int( q[1]), bkp_db) )
            output.append( str( count ) )


        elif q[0] == "RESTORE":
            for point in reversed( restore_point ):
                if point[ 0 ] < int( q[2] ):
                    db = point[ 1 ]
                    break
            for k1, v1 in db.items():
                for k2, v2 in db[ k1 ].items():
                    a = db[ k1 ][ k2 ][ 0 ]
                    c = db[ k1 ][ k2 ][ 2 ]
                    db[ k1 ][ k2 ] = ( a, int( q[2] ), c )
            output.append("")


    return output




print(
    solution(
        [
            ["SET", "A", "B", "4"],
            ["SET", "A", "C", "6"],
            ["COMPARE_AND_SET", "A", "B", "4", "9"],
            ["COMPARE_AND_SET", "A", "C", "4", "9"],
            ["COMPARE_AND_SET", "A", "C", "6", ""],
            ["GET", "A", "C"],
            ["GET", "A", "B"],
        ]
    )
)


print(
    solution(
        [
            ["SET", "A", "BC", "4"],
            ["SET", "A", "BD", "5"],
            ["SET", "A", "C", "6"],
            ["SCAN", "A", "B"],
            ["SCAN", "A", ""],
            ["SCAN", "B", "B"],
        ]
    )
)


print(
    solution(
        [
            ["SET_AT", "A", "B", "4", "1", "0"],
            ["SET_AT", "X", "Y", "5", "2", "15"],
            ["SET_AT", "A", "D", "3", "4", "6"],
            ["COMPARE_AND_SET_AT", "A", "D", "3", "5", "6", "10"],
            ["GET_AT", "A", "D", "6"],
            ["SCAN_AT", "A", "", "15"],
            ["SCAN_AT", "A", "", "17"],
        ]
    )
)


print(
    solution(
        [
            ["SET_AT", "A", "B", "C", "1", "10"],
            ["BACKUP", "3"],
            ["SET_AT", "A", "D", "E", "4", "0"],
            
            ["SCAN_AT", "A", "", "5"],
            ["BACKUP", "5"],
            
            # ["DELETE_AT", "A", "B", "8"],
            ["COMPARE_AND_SET_AT", "A", "B", "C", "", "8", "0"],
            
            ["BACKUP", "9"],
            ["RESTORE", "10", "7"],
            ["BACKUP", "11"],
            ["SCAN_AT", "A", "", "15"],
            ["SCAN_AT", "A", "", "16"],
        ]
    )
)
