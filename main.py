import pyperclip
from squares import cords_black
import pyautogui as pg
import chess
import chess.engine
import chess.pgn
import time

pg.FAILSAFE = True


def black_cords():
    time.sleep(4)
    cords = cords_black
    try:
        a1 = pg.locateCenterOnScreen('images/wbR2.png')
    except TypeError:
        a1 = pg.locateCenterOnScreen('images/wbR.png')

    try:
        h8 = pg.locateCenterOnScreen('images/bbR2.png')
    except TypeError:
        h8 = pg.locateCenterOnScreen('images/bbR.png')

    perm_x = a1[0]
    perm_y = a1[1]
    x = perm_x
    y = perm_y

    x_increment = (perm_x - h8[0]) / 8
    y_increment = x_increment

    keys = list(cords)

    count = 0
    for key in keys:
        cords[key] = (x, y)
        y += 85
        count += 1
        if count >= 8:
            y = perm_y
            x -= y_increment + 9
            count = 0
    return cords


cords = black_cords()
values = cords.values()

for value in values:
    time.sleep(.2)
    pg.moveTo(x=value[0], y=value[1])

print(cords)



def get_fen():
    time.sleep(4)
    try:
        x, y = pg.locateCenterOnScreen(r'images/download3.png', confidence=.95)
    except TypeError:
        try:
            x, y = pg.locateCenterOnScreen(r'images/download2.png', confidence=.95)
        except TypeError:
            x, y = pg.locateCenterOnScreen(r'images/download.png', confidence=.95)


    pg.click(x=x, y=y)
    time.sleep(1)
    pg.click(895, 525)
    pg.hotkey('ctrl', 'c')
    time.sleep(1)
    try:
        x, y = pg.locateCenterOnScreen(r'images/x2.png', confidence=.9)
    except TypeError:
        x, y = pg.locateCenterOnScreen(r'images/x.png', confidence=.9)
    pg.click(x, y)
    return pyperclip.paste()


def move_piece(uni, coordinates):
    from_cord = coordinates[uni[:2].upper()]
    pg.click(x=from_cord[0], y=from_cord[1])
    time.sleep(1)
    to_cord = coordinates[uni[2:].upper()]
    pg.click(x=to_cord[0], y=to_cord[1])


def main():
    engine_path = input("Stockfish Path: ")
    engine = chess.engine.SimpleEngine.popen_uci(engine_path)

    board = chess.Board()

    color = ''
    while color != 'black' or color != 'white':
        color = input("Are You Black or White? ").lower()
        if color == 'white':
            break
        elif color == 'black':
            break

    if color == 'black':
        board = chess.Board(fen=chess.STARTING_FEN)
        prev_fen = chess.STARTING_FEN
        while not board.is_game_over():

            fen = get_fen()

            if fen != prev_fen:
                board = chess.Board(fen=fen)
                print(board)

                result = engine.play(board, chess.engine.Limit(time=0.1))
                move = result.move
                print(str(move))
                move_piece(str(move), cords)
                board.push(move)
                print(board)

                print(board.legal_moves)
            else:
                pass
            prev_fen = fen


    elif color == 'white':
        pass

main()
