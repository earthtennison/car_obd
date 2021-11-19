

def hex_to_int(h, is_low_to_high=True):
    HEX_PER_BYTE = 2
    if len(h)>2 and h[:2] == "0x":
        if is_low_to_high == True:
            h = h[:2] + "".join(reversed([h[i:i + 2] for i in range(2, len(h), 2)]))
        return int(h, 0)
    else:
        if is_low_to_high == True:
            h = "".join(reversed([h[i:i + 2] for i in range(0, len(h), 2)]))
        return int(h, 16)

def decode_dtc_flag(f):
    f = hex_to_int(f)
    if f == 0:
        return 'stored trouble code'
    else:
        return 'pending trouble code' 

def decode_dtc_count(c):
    c = hex_to_int(c)
    if c==0:
        return 'no filed'
    else:
        return c

def decode_dtc_array(d, is_low_to_high=True):
    HEX_PER_BYTE = 2
    if len(d)>2 and d[:2] == "0x":
        if is_low_to_high == True:
            d = d[:2] + "".join(reversed([d[i:i + 2] for i in range(2, len(d), 2)]))
    else:
        if is_low_to_high == True:
            d = "".join(reversed([d[i:i + 2] for i in range(0, len(d), 2)]))
    
    x=bin(int(d, 16))[2:].zfill(16)
    y=''
    if x[1:3] == '00':
        y = 'P'
    if x[1:3] == '01':
        y = 'C'
    if x[1:3] == '10':
        y = 'B'
    if x[1:3] == '11':
        y = 'U'

    return y+d





def decode_dtc_pass_data(data):
    #if len(data) != 20*2:
        #print(len(data))
        #return False
    dtc_data_pass = {
        "dtc_flag": None,
        "dtc_count": None,
        "dtc_array": None,

    }
    
    dtc_flag = data[:1*2]
    dtc_count = data[1*2:2*2]
    dtc_data_pass["dtc_flag"]=decode_dtc_flag(dtc_flag)
    dtc_data_pass["dtc_count"]=decode_dtc_count(dtc_count)

    i = dtc_data_pass["dtc_count"]

    if type(i) != int:
        dtc_data_pass["dtc_array"]= 'no dtc'
    else:
        dtc_array = data[2*2:]
        dtc_data_pass["dtc_array"] = ''
        for a in range(1,i+1):
            dtc_data_pass["dtc_array"]= dtc_data_pass["dtc_array"] + ' ' + decode_dtc_array(dtc_array[4*(a-1):4*a])

        
    return dtc_data_pass

if __name__ == "__main__":
    #input_data = "0000"
    #input_data = "00015113"
    input_data = "000251135123"
    dtc_pass_data = decode_dtc_pass_data(input_data)
    print(dtc_pass_data)
