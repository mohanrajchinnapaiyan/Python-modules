import random
import curses
from curses import textpad


def print_score (stdscr, score):
    sh, sw = stdscr.getmaxyx()
    score_text = "Your score is: {}".format(score)
    stdscr.addstr(1, sw//2-len(score_text)//2, score_text)
    stdscr.refresh()


def create_food (snake, box):
    food = None
    while food is None:
        food = [random.randint(box[0][0]+1, box[1][0]-1),
        random.randint(box[0][1]+1, box[1][1]-1)]
        if food in snake:
            food = None
    return food


def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.nodelay(1)
    stdscr.timeout(150)
    
 

    # draw a rectangle
    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]
    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    stdscr.refresh()

    stdscr.getch()
    
    # draw snake
    snake = [[sh//2, sw//2+1], [sh//2, sw//2], [sh//2, sw//2-1]]
    direction = curses.KEY_RIGHT

    for y, x in snake:
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(y, x, '#')
        stdscr.attroff(curses.color_pair(1))

    stdscr.getch()

    # draw food
    food = create_food(snake, box)
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(food[0], food[1], '*')
    stdscr.attroff(curses.color_pair(2))

    # score
    score = 0
    print_score(stdscr, score)

    while True:
        key = stdscr.getch()
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
            direction = key            
        
        head = snake[0]        

        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]

        snake.insert(0, new_head)
        stdscr.attron(curses.color_pair(1))
        stdscr.addstr(new_head[0], new_head[1], '#')
        stdscr.attroff(curses.color_pair(1))

        if snake[0] == food:
            food = create_food(snake, box)
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(food[0], food[1], '*')
            stdscr.attroff(curses.color_pair(2))
            score += 100
            print_score(stdscr, score)
        else:
            stdscr.addstr(snake [-1] [0], snake[-1] [1], ' ')
            snake.pop()

        if (snake[0][0] in [box[0][0], box[1][0]] or
            snake[0][1] in [box[0][1], box[1][1]] or
            snake[0] in snake[1:]):
            msg = "Game Over !!!"
            stdscr.addstr(sh//2, sw//2-len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break

        stdscr.refresh()

curses.wrapper(main)
