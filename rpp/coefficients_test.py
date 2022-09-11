from coefficients import pos_coef

# test
test_counter = 0
for pos, value in pos_coef.items():
    c = 0
    for stat in value.values():
        c += stat
    test_counter += c
    if c != 1:
        print(f"{pos} is bad")
if len(pos_coef) == test_counter:
    print('Test success!')
