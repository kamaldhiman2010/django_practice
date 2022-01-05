def gen_prime(x):
    multiples = []
    results = []
    print(x)
    for i in range(2, x+1):
        if i not in multiples:
            results.append(i)
            for j in range(i*i, x+1, i):
                multiples.append(j)
            print(x)
    return results
