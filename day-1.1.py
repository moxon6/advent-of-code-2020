def get_solution():
    with open("inputs/day1.txt") as f:
        numbers = list( map(lambda x: int(x), f.readlines() ) )
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                if numbers[i] + numbers[j] == 2020:
                    return numbers[i] * numbers[j]

if __name__ == "__main__":
    print(get_solution())
    