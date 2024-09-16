import matplotlib.pyplot as plt


filename1 = "doba_polievania"
filename2 = "vlhkost"
list1str = []
list1 = []
list2str = []
list2 = []
length = []


with open("{0}.txt".format(filename1), "r") as file:
    for line in file:
        #print(line)
        line = line.replace("\n","")
        list1str.append(line)
    list1str.pop(0)
    list1str.pop(0)
    
    for line in list1str:
        list1.append(float(line))

    print(list1)
    print(len(list1))

    print()

with open("{0}.txt".format(filename2), "r") as file2:
    for line in file2:
        #print(line)
        line = line.replace("\n","")
        list2str.append(line)
    list2str.pop(0)
    list2str.pop(0)
    
    for line in list2str:
        list2.append(float(line))

    print(list2)
    print(len(list2))

    print()

    for i in range(len(list1)):
        length.append(i)
    
    print(length)


x1 = length
y1 = list1
plt.subplot(2, 1, 2)
plt.plot(x1, y1, marker = 'o', ms = 2, color = 'r')
plt.xlabel('počet pokusov')
plt.ylabel('doba polievania')

x2 = length
y2 = list2
plt.subplot(2, 1, 1)
plt.plot(x2, y2, marker = 'o', ms = 2)
#plt.xlabel('počet pokusov')
plt.ylabel('vlhkosť pôdy')


plt.title('Graf závislosti počtu pokusov od vlhkosti pôdy\n a doby polievania')
plt.show()
