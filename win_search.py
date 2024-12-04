
def find_completable_lines(x, y) -> list[list]:
    lines = list()
    lines.append([(x,i) for i in range(7)])
    lines.append([(i,y) for i in range(6)])
    lines.append([(i,abs(i-(x-y))) for i in range((x-y if x-y > 0 else 0), 6) if i-(x-y) < 7])
    lines.append([(i,abs(i-(x+y))) for i in range((x+y if x+y < 6 else 5), -1, -1) if abs(i-(x+y)) < 7])

    return lines


def find_winner_segment(array:list[list[int]], line:list[tuple]) -> list:
    segment = list()
    player = 0
    counter = 0

    for x,y in line:
        segment.append((x,y))

        if player != array[x][y].player:
            player = array[x][y].player
            counter = 1
            segment = [(x,y)]
        elif player != 0:
            counter += 1

        if counter == 4:
            return segment
        
    return []


def find_winner(array:list[list[int]], row:int, col:int) -> list:
    lines = find_completable_lines(row, col)

    for line in lines:
        if segment := find_winner_segment(array, line):
            return segment
        
    return []