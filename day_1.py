lines = open('input.txt').read().splitlines()
print(lines)

inventory = {}
elf_index = 0

for item in lines:
    if item == '':
        elf_index += 1
        continue
    if elf_index not in inventory:
        inventory[elf_index] = 0
    inventory[elf_index] = inventory[elf_index] + int(item)

print(inventory)

max_calory = max(list(inventory.values()))
sorted_inventory = sorted(list(inventory.values()), reverse=True)

print(sorted_inventory[0] + sorted_inventory[1] + sorted_inventory[2])