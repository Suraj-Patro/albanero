import csv

input_file = csv.DictReader(open("data.csv"))

for i in input_file:
    print( i )
    print( len(i) )


# with open('test.txt', 'r+') as f:
#     file = f.readlines()
    # for line in file:
    #     if 'Upwork' in line:
    #         pos = line.index('Upwork')
    #         file.insert(pos + 1, 'Freelancer.com\n')
    # f.seek(0)
    # f.writelines(file)
# f.close()


# with open('data.csv', 'r+') as f:
#     lines = f.readlines()
#     cl = len( next( iter( lines ) ).split(',') )

#     # print( cl )
#     ptr = 0

#     for line in lines:
#         sp = line.split(',')

#         if cl != len( sp ):
#             sp[4] = '"' + sp[4] + ", " + sp[5] + '"'
#             del sp[5]
#             f.seek(ptr)
#             f.write( ",".join( sp ) )
        
#         ptr += len(line)

#         # print( sp, len(sp) )

#     f.seek(0)
#     for line in lines:
#         print(line)
        