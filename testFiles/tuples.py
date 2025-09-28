import json
list_of_tuples = [("z","A", 1), ("x","B", 2), ("v","C", 3)]

for index,tupleItem in enumerate(list_of_tuples):
    list_of_tuples[index] = (tupleItem[1], tupleItem[2])
print(f"List of tuples edited\n{list_of_tuples}")


# Check if the tuple ("B", 2) is in the list
if ("B", 2) in list_of_tuples:
    print("The tuple ('B', 2) is in the list.")
else:
    print("The tuple ('B', 2) is not in the list.")


credentials = (input('Ingresa tu usuario: '), input('Ingresa tu contrasena: '))
print(credentials)
print(json.dumps(credentials))

asd = {'username':'mario', 'password':'pass'}
print(asd)
print(json.dumps(asd))

