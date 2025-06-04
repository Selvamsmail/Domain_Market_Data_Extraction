
wrl = [0,5293,10586]

l = []
for i in range(1,4):
    with open('dom_comp_'+str(i)+'.txt', 'r') as file:
        st_rng = int(file.read())
        l.append(abs(st_rng-wrl[i-1]))

print(sum(l),'-',15879)