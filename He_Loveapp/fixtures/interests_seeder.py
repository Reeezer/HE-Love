
f = open('data.txt', 'r')
lines = f.readlines()

file = open('interests.json', 'a')
file.write("[\n")

i = 1
for line in lines:
    description = line.strip()
    file.write("\t{\n")
    file.write('\t\t"model": "He_Loveapp.interest",\n')
    file.write(f'\t\t"pk": {i},\n')
    file.write('\t\t"fields": {\n')
    file.write(f'\t\t\t"description": "{description}"\n')
    file.write("\t\t}\n")
    file.write("\t},\n")
    i += 1
    
file.write("]")