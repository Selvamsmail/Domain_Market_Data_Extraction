wrl = [0,5293,10586]

for i in range(1,4):
    with open('dom_comp_'+str(i)+'.txt', 'w') as file:
        file.write(str(wrl[i-1]))
