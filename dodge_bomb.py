import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1100, 650
DELTA = {
        pg.K_UP:(0, -5),
        pg.K_DOWN:(0, 5),
        pg.K_LEFT:(-5, 0),
        pg.K_RIGHT:(5, 0),
        }
#accs = [a for a in range(1, 11)]
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果，縦方向判定結果）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right: # 横方向判定
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom: # 縦方向判定
        tate = False
    return yoko, tate


def game_over(screen:pg.display):
    """
    引数：最初に作ったディスプレイ
    戻り値：なし
    画面をブラックアウトし, 泣いているこうかとんと文字列を時間分表示
    """
    go_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0, 0, WIDTH, HEIGHT))
    go_img.set_alpha(200)
    screen.blit(go_img, [0, 0])
    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rect = txt.get_rect()
    txt_rect.center = (WIDTH//2, HEIGHT//2)
    screen.blit(txt, txt_rect)
    gokk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    gokk1_rect = gokk_img.get_rect()
    gokk1_rect.center = (300, HEIGHT//2)
    gokk2_rect = gokk_img.get_rect()
    gokk2_rect.center = (800, HEIGHT//2)
    screen.blit(gokk_img, gokk1_rect)
    screen.blit(gokk_img, gokk2_rect)
    pg.display.update()
    time.sleep(5)


#def kasoku()


def return_dic(mv:tuple, dic:dict) -> tuple:
    """
    引数：移動量と画像辞書
    戻り値：画像
    """
    mv = tuple(mv)
    return dic[mv]

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    kks_img = []
    mvs_lis = [(-5, -5), (-5, 0), (-5, 5), (0, 5),
               (5, 5), (5, 0), (5, -5), (0, -5), ]
    for k in range(8):
        if k==3:
            kks_img.append(pg.transform.flip((pg.transform.rotozoom(kk_img, 45, 1.0)), True, False))
            continue
        if k==4:
           kks_img.append(pg.transform.flip(kks_img[2], True, False)) 
           continue
        if k==5:
            kks_img.append(pg.transform.flip(kks_img[1], True, False))
            continue
        if k==6:
            kks_img.append(pg.transform.flip(kks_img[0], True, False))
            continue
        if k==7:
            kks_img.append(pg.transform.flip(kks_img[3], True, True))
            continue
        kks_img.append(pg.transform.rotozoom(kk_img, 45*k-45, 1.0))
    kks_img = dict(zip(mvs_lis, kks_img))
    bb_img = pg.Surface((20, 20))
    bb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT) 
    bb_imgs = []
    #for r in range(1, 11):
        #bb_img = pg.Surface((20*r, 20*r))
        #pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    vx = 5
    vy = 5
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            game_over(screen)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=tpl[0]
                sum_mv[1]+=tpl[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        if sum_mv != [0, 0]:
            kk_img = return_dic(sum_mv, kks_img)
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
