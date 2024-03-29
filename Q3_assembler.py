# To check other instructions not using floating registers
def decimal_to_binary(n):
    L = ""
    while(n>0):
        L += str(n%2)
        n = n//2
    
    return L[::-1]
def floater_to_binary(a):
    f = str(a)
    
    ans = f.split(".")
    x = int(ans[0])
    bin_ans = decimal_to_binary(x)
    y = ans[1]
    y_actual = "0." + y
    s = float(y_actual)
    ans_float = ''
    if(int(y_actual[2:]) == 0):
        ans_float += "00000"
    else:
        for i in range(5):
            if(s>=1):
                s -= 1
            x_new = str(float(s*2))
            
            # elif(int(x_new[2:]) == 0 and i!=0):
            #     ans_float += '1'
            #     ans_float += (5-i)*'0'
            #     break

            ans_float += x_new[0]
            
            s = s*2
    fin = bin_ans[:] + "." + ans_float
    fin_ans = ''
    fin_ans = str(float(fin))
    fin_ans += '00000'
    a = fin_ans.split(".")
    expo = 0
    mantissa = ''
    if(int(a[0])!=0):
        expo = fin_ans.index('.')-1
        count = 0
        i = 1
        while(count<5):
            if(fin_ans[i]!='.'):
                mantissa += fin_ans[i]
                count += 1
            i += 1
    expo_new = decimal_to_binary(expo)
    if(expo_new==""):
        expo_new = "0"
    if(mantissa==""):
        mantissa = "00000"
    return [expo_new, mantissa]

# print(floater_to_binary(5.25))
dict_opcode = {
    # Type A
    'add' : '1000000',
    'sub' : '1000100',
    'mul' : '1011000',
    'xor' : '1101000',
    'or' : '1101100',
    'and' : '1110000',
    'addf' : '0000000',
    'subf' : '0000100',

    # Type B
    'movB' : '10010',
    'movf' : '00010',
    'ls' : '11001',
    'rs' : '11000',
    # Type C
    'movC' : '1001100000',
    'div' : '1011100000',
    'not' : '1110100000',
    'cmp' : '1111000000',
    # Type D
    'ld' : '10100',
    'st' : '10101',
    # Type E
    'jmp' : '11111000',
    'jlt' : '01100000',
    'jgt' : '01101000',
    'je' : '01111000',
    # Type F
    'hlt' : '0101000000000000'
}



dict_registers={"R0" :"000" ,"R1":"001","R2":"010","R3":"011","R4":"100","R5":"101","R6":"110","FLAGS":"111"}
dict_labels={}
dict_var={}
instruction = []
floating_registers = []
counter = 0
counter_label = 0
counter_line = 1
counter_var = 0
counter_dono = 1
list_label = []
label_ahead = []
main = False
a = False
h = False
i_err = False
g_err = False
d_err = False
c_err = False
e_err = False
f_err = False
gen_err = False
# =========================================================================================================
def mov(L):
    flag = False
    for x in L:
        if '$' in x:
            flag = True
            break
    if(flag==True):
        print('10010', end="")
        print(dict_registers[L[1]], end = "")
        a = int(L[2][1:])
        if(a<0):
            print("00000000")
        elif(a>255):
            print("11111111")
        else:
            b = decimal_to_binary(a)
            print("0"*(8-len(b)), end = "")
            print(b)
    else:
        print('1001100000', end = "")
        print(dict_registers[L[1]], end = "")
        print(dict_registers[L[2]])
def TypeA(L):
    if(L[0]=='add'):
        print('1000000',end="")
    elif(L[0]=='sub'):
        print('1000100',end="")
    elif(L[0]=='mul'):
        print('1011000',end="")
    elif(L[0]=='xor'):
        print('1101000',end="")
    elif(L[0]=='or'):
        print('1101100',end="")
    elif(L[0]=='and'):
        print('1110000',end="")
    elif(L[0]=='addf'):
        print('0000000', end = "")
        # if(L[3] not in floating_registers):
        #     floating_registers.append(L[3])
    elif(L[0]=='subf'):
        print('0000100', end = "")
        # if(L[3] not in floating_registers):
        #     floating_registers.append(L[3])
    print(dict_registers[L[1]], end = "")
    print(dict_registers[L[2]], end="")
    print(dict_registers[L[3]])
    
def TypeB(L):
    if(L[0]=='ls'):
        print('11001',end="")
        print(dict_registers[L[1]], end = "")
        a = int(L[2][1:])
        b = decimal_to_binary(a)
        print("0"*(8-len(b)), end = "")
        print(b)
    elif(L[0]=='rs'):
        print('11000',end="")
        print(dict_registers[L[1]], end = "")
        a = int(L[2][1:])
        b = decimal_to_binary(a)
        print("0"*(8-len(b)), end = "")
        print(b)
    elif(L[0]=='movf'):
        print('00010',end="")
        
        print(dict_registers[L[1]], end = "")
        a = L[2][1:]
        #print(float(a))
        list = floater_to_binary(float(a))
        print((3-len(list[0]))*"0" + list[0], end = "")
        print(list[1])
def TypeC(L):
    if(L[0] == 'div'):
        print('1011100000',end = "")
    elif(L[0] == 'not'):
        print('1110100000',end= "")      #here
    elif(L[0] == 'cmp'):
        print('1111000000',end = "")
    print(dict_registers[L[1]], end = "")
    print(dict_registers[L[2]])
def TypeD(L):
    if(L[0] == 'ld'):
        print('10100', end="")
    elif(L[0] == 'st'):
        print('10101',end = "")   
    print(dict_registers[L[1]], end = "")
    print(dict_var[L[2]])
def TypeE(L):
    if(L[0] == 'jmp'):
        print('11111000', end="")
    elif(L[0] == 'jlt'):
        print('01100000', end="")
    elif(L[0] == 'jgt'):
        print('01101000', end="")
    elif(L[0] == 'je'):
        print('01111000', end="")
    print(dict_labels[L[1] + ":"])




# =========================================================================================================





while(1):
    try:
        line = input()
    except EOFError:
        break
    instruction.append(line)
# print(instruction)

try:

    if(len(instruction)>0):
        for i in instruction:
            words = i.split()
            if(len(words)>0):
                if words[0]!='var':
                    counter += 1
                elif(words[0]=='var'):
                    if len(words)==2 and words[1] not in dict_var.keys():
                        dict_var[words[1]] = ""
                    elif(len(words)!=2):
                        gen_err = True
                        main = True
                        print("GENERAL SYNTAX ERROR IN LINE", counter_dono)
                        break
                counter_dono += 1
        counter_label2 = 0
        for i in instruction:
            words = i.split()
            counter_label2+=1
            if(len(words)>0 and words[0][-1]==':' ):
                label_ahead.append(words[0][0:len(words[0])-1])
            if ( len(words)>0 and  words[0][-1] == ':'):
                b = decimal_to_binary(counter_label2-1)
                b = "0"*(8-len(b)) + b
                if words[0] not in dict_labels.keys():
                    dict_labels[words[0]] = b
                words = words[1:]
            
    for i in dict_var.keys():
        b = decimal_to_binary(counter)
        b = "0"*(8-len(b)) + b
        dict_var[i] = b
        counter += 1
    # =========================================================================================================




    if(len(instruction)>0 and not main):
        for i in instruction:
            if(len(i)==0):
                counter_line +=1
                continue
            words = i.split()
            
            if(words[0][-1]==":" and len(words)>0):
                if(words[0][0:len(words[0])-1] not in list_label and len(words)<=5 and words[0][0:len(words[0])-1] not in dict_registers.keys() and words[0][0:len(words[0])-1] not in dict_opcode.keys()):
                    list_label.append(words[0][0:len(words[0])-1])
                    words = words[1:]
                # print(list_label)
                # print(words)
                else:
                    gen_err = True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    main = True
                    break
            for again in words:
                #assert(':' != words[-1])
                if ':' ==again[-1]:
                    gen_err = True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    main = True
                    break
            for j in words:
                if j not in dict_opcode.keys() and j !='mov' and j not in dict_registers.keys() and j[-1] != ':' and j !='var' and j not in dict_var.keys() and j[0]!='$' and j not in list_label and j not in label_ahead:
                    a = True
                    break
                if j=='hlt':
                    h = True

                if(j=='hlt' and counter_line!=len(instruction)):
                    i_err = True
                    break
                if(j=='var' and counter_var!=0):
                    g_err = True
                    break
            if(words[0]=='add' or words[0]=='sub' or words[0]=='mul' or words[0]=='xor' or words[0]=='or' or words[0]=='and'):
                if(len(words)!=4 or words[1] not in dict_registers.keys() or words[2] not in dict_registers.keys() or words[3] not in dict_registers.keys()):
                    gen_err = True
                    main=True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
                # if(len(words)!=4 or words[1] in floating_registers or words[2] in floating_registers):
                #     gen_err = True
                #     main=True
                #     print("REGISTER CONTAINS FLOATING POINT NUMBER NOT SUPPORTED BY INSTRUCTION IN LINE ", counter_line)
                #     break
            if(words[0]=='add' or words[0]=='sub' or words[0]=='mul' or words[0]=='xor' or words[0]=='or' or words[0]=='and' or words[0]=='addf' or words[0]=='subf'):
                if(len(words)!=4 or words[1] not in dict_registers.keys() or words[2] not in dict_registers.keys() or words[3] not in dict_registers.keys()):
                    gen_err = True
                    main=True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
                if(words[0]=="addf" or words[0]=="subf"):
                    # if(words[1] not in floating_registers or words[2] not in floating_registers ):
                    #     print("USING REGISTERS WHICH DO NOT HOLD FLOATING VALUES IN LINE ", counter_line)
                    #     main = True
                    #     gen_err = True
                    #     break               #changed
                    if(words[3] not in floating_registers):
                        floating_registers.append(words[3])
            if(words[0]=="movf"):
                if(words[1] not in dict_registers or '$' not in words[2] or "." not in words[2]):
                    main = True
                    gen_err = True
                    print("GENERAL SYNTAX ERROR IN LINE ", counter_line)
                    break
                elif(words[1] not in floating_registers):
                    floating_registers.append(words[1])
            if(words[0]=="movf"):
                #if(words[1] not in dict_registers or )
                X = words[2][1:]
                Y = float(X)
                if(Y>252 or Y<1):
                    main = True
                    print("NUMBERS OUT OF RANGE IN FLOATING POINT ARITHMETICS IN LINE ", counter_line)
                    break
            list_helper = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            if(words[0]=='mov'):
                if(len(words)!=3 or words[1] not in dict_registers.keys()):
                    gen_err = True
                    main = True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
                if('$' in words[2]):
                    if('.' in words[2]):
                        main= True

                        print("TRYING TO USE FLOATING POINT NUMBER IN PLACE OF INTEGER IN LINE ", counter_line)
                        break
                    for k in words[2][1:]:
                        
                        if(k not in list_helper):
                            gen_err= True
                            main=True
                            print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                            break
                else:
                    
                    if(words[2] not in dict_registers.keys()):
                        gen_err = True
                        main = True
                        print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    if (words[1]  in floating_registers ):
                        floating_registers.append(words[2])

            if(gen_err):
                break
            if(words[0]=='ls' or words[0]=='rs'):
                if(len(words)!=3 or words[1] not in dict_registers.keys() or '$' not in words[2]):
                    gen_err = True
                    main = True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
                # if(len(words)!=3 or words[1] in floating_registers):
                #     gen_err = True
                #     main = True
                #     print("REGISTER CONTAINS FLOATING POINT NUMBER NOT SUPPORTED BY INSTRUCTION IN LINE", counter_line)
                #     break
                if('$' in words[2]):
                    for k in words[2][1:]:
                        if(k not in list_helper):
                            gen_err= True
                            main=True
                            print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                            break
            if(gen_err):
                break
            if(words[0]=='div' or words[0]=='not' or words[0]=='cmp'):
                if(len(words)!=3 or words[1] not in dict_registers.keys() or words[2] not in dict_registers.keys()):
                    gen_err = True
                    main=True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
                # if(len(words)!=3 or words[1] in floating_registers or words[2] in floating_registers):
                #     gen_err = True
                #     main=True
                #     print("REGISTER CONTAINS FLOATING POINT NUMBER NOT SUPPORTED BY INSTRUCTION IN LINE", counter_line)
                #     break
            # if(len(words)==3 and (words[0]=='ld' or words[0]=='st')):
            #     if(words[2] not in dict_var.keys()):
            #         print("TYPE B(USE OF UNDEFINED VARIABLES) ERROR IN LINE", counter_line)
            #         main = True
            #         break
            # if(words[0]=='ld' or words[0]=='st'):
            #     if(len(words)!=3 or words[1] not in dict_registers.keys() or words[2] not in dict_var.keys()):
            #         gen_err = True
            #         main=True
            #         print("GENERAL SYNTAX ERROR IN LINE", counter_line)
            #         break
            if((words[0]=='jmp' or words[0]=='jlt' or words[0]=='jgt' or words[0]=='je') and words[1] in dict_var.keys()):
                f_err = True
                main = True
                print("TYPE F(MISUSE OF LABELS AS VARIABLES OR VICE-VERSA) ERROR IN LINE", counter_line)
                break
            if((words[0]=='ld' or words[0]=='st') and words[2] in list_label):
                f_err = True
                main = True
                print("TYPE F(MISUSE OF LABELS AS VARIABLES OR VICE-VERSA) ERROR IN LINE", counter_line)
                break
            if(len(words)==3 and (words[0]=='ld' or words[0]=='st')):
                if(words[2] not in dict_var.keys()):
                    print("TYPE B(USE OF UNDEFINED VARIABLES) ERROR IN LINE", counter_line)
                    main = True
                    break
            if(words[0]=='ld' or words[0]=='st'):
                if(len(words)!=3 or words[1] not in dict_registers.keys() or words[2] not in dict_var.keys()):
                    gen_err = True
                    main=True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
            if((len(words)==2) and (words[0]=='jmp' or words[0]=='jlt' or words[0]=='jgt' or words[0]=='je') and words[1] not in list_label and words[1] not in label_ahead):
                c_err = True
                main = True
                print("TYPE C(USE OF UNDEFINED LABELS) ERROR IN LINE", counter_line)
                break
            if(words[0]=='jmp' or words[0]=='jlt' or words[0]=='je' or words[0]=='jgt'):
                if(len(words)!=2 or (words[1] not in list_label and words[1] not in label_ahead)):
                    gen_err = True
                    main=True
                    print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                    break
            if(words[0]=='hlt' and len(words)!=1):
                main = True
                gen_err = True
                print("GENERAL SYNTAX ERROR IN LINE", counter_line)
                break
            if(len(words)>2 and '$' in words[2]):
                if(words[0]!='movf' and (int(words[2][1:])>255 or int(words[2][1:])<0)):
                    e_err = True
                    main = True
                    print("TYPE E(ILLEGAL IMMEDIATE VALUES) ERROR IN LINE", counter_line)
                    break
            # if((words[0]=='ld' or words[0]=='st') and words[1] in list_label):
            #     f_err = True
            #     main = True
            #     print("TYPE F(MISUSE OF LABELS AS VARIABLES OR VICE-VERSA) ERROR IN LINE", counter_line)
            #     break
            # if((words[0]=='jmp' or words[0]=='jlt' or words[0]=='jgt' or words[0]=='je') and words[1] in dict_var.keys()):
            #     f_err = True
            #     main = True
            #     print("TYPE F(MISUSE OF LABELS AS VARIABLES OR VICE-VERSA) ERROR IN LINE", counter_line)
            #     break
            if(words[0]!='var'):
                counter_var += 1
            if('FLAGS' in words):
                #print('to')
                if(words[0]!='mov'):
                    d_err = True
                    main = True  
                if(words[1] not in dict_registers.keys() or words[1]=='FLAGS'):
                    d_err = True
                    main = True
                if(words[2]!='FLAGS'):
                    d_err = True
                    main = True
                if(d_err):
                    print('TYPE D(ILLEGAL USE OF FLAGS REGISTER) ERROR IN LINE', counter_line)
                    main = True
                    break
                
                
            if(a):
                if(words[0]=='jmp' or words[0]=='jlt' or words[0]=='jgt' or words[0]=='je'):
                    print("TYPE C(USE OF UNDEFINED LABELS) ERROR IN LINE", counter_line)
                    c_err = True
                else:
                    print('TYPE A(TYPOS IN INSTRUCTION NAME OR REGISTER NAME) ERROR IN LINE', counter_line)
                main = True
                break
            if(i_err):
                break
            if(g_err):
                print("TYPE G(VARIABLES NOT DECLARED AT THE BEGINNING) ERROR IN LINE", counter_line)
                main = True
                break
            
            
            counter_line += 1  
        if(not main):
            if not h:
                print('TYPE H(MISSING hlt INSTRUCTION) ERROR IN LINE', counter_line-1)
                main = True
            elif(i_err):
                print('TYPE I(hlt NOT BEING USED AS LAST INSTRUCTION) ERROR IN LINE', counter_line)
                main = True
except:
    gen_err = True
    main=True

    print("GENERAL SYNTAX ERROR IN LINE", counter_line)





# =========================================================================================================        




if(len(instruction)>0 and not main):
    for i in instruction:
        if(len(i)==0):
            continue
        words = i.split()
        counter_label += 1
        if words[0][-1] == ':':
            b = decimal_to_binary(counter_label-1)
            b = "0"*(8-len(b)) + b
            if words[0] not in dict_labels.keys():
                dict_labels[words[0]] = b
            words = words[1:]
        if(words[0]=='mov'):
            mov(words)
        elif(words[0]=='add' or words[0]=='sub' or words[0]=='mul' or words[0]=='xor'or words[0]=='or' or words[0]=='and' or words[0]=='addf' or words[0]=='subf'):
            TypeA(words)
        elif(words[0]=='ls' or words[0]=='rs' or words[0]=='movf'):
            TypeB(words)
        elif(words[0]=='div' or words[0]=='not' or words[0] == 'cmp'):
            TypeC(words)
        elif(words[0]=='ld' or words[0]=='st'):
            TypeD(words)
        elif(words[0]=='jmp' or words[0]=='jlt' or words[0] == 'jgt' or words[0] == 'je'):
            TypeE(words)
        elif(words[0]=='hlt'):
            print('0101000000000000')











# for i,j in dict_registers.items():
#     print(i,j)
# for i,j in dict_opcode.items():
#     print(i, j)
# print(floating_registers)