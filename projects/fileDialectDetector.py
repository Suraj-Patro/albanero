import clevercsv


files = [
    'zz_abdul_inspect-multiline.csv',
    'zz_keshab_ItemMaster_MMS001.csv',
    'zz_shan_icsp_sample_2.csv',
    'zz_shan_peoplec.csv',
    'zz_shan_sample_csv_with_multiline_records.csv',
    'zz_shan_wayne_item_master.csv',
]


for file in files:
    print(f"Working on {file}.")

    try:
        dialect = clevercsv.wrappers.detect_dialect( file )
        print( dialect )
        print( dialect.to_dict() )
        print( dialect.to_csv_dialect() )
        
    except Exception as e:
        print(e)
    
    input()
