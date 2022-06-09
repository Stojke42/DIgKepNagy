import math
import os
import cv2
import numpy as np

try:
    os.mkdir("megoldas")
    print("CREATED FOLDER")
except:
    print("FOLDER IS EXIST")

def rotate(pic,row, col, ang):
    M = cv2.getRotationMatrix2D((row / 2, col / 2), ang, 1)
    dst = cv2.warpAffine(pic, M, (row, col))
    # dst = cv2.warpAffine(pic, M, (col, row), cv2.BORDER_CONSTANT, 0)
    cv2.imshow('Rotated image', dst)
    cv2.imwrite("rotated.png", dst)
    cv2.waitKey(0)


def crop(ang):
    img=cv2.imread("rotated.png")

    y, x = img.shape[:2]
    print(ang,y,x)

    tanalfa = math.tan(abs(ang) * math.pi / 180)
    print(tanalfa)
    xblack = tanalfa * (y / 2)
    yblack = tanalfa * (x / 2)
    pointone = [xblack, yblack]
    pointtwo = [x - xblack, yblack]
    pointthree = [xblack, y - yblack]
    pointfour = [x - xblack, y - yblack]
    print(pointone, pointtwo, pointthree, pointfour)
    x1 = int(xblack)
    y1 = int(yblack)
    x2 = int(x - xblack)
    y2 = int(y - yblack)
    cropped_copy = img[y1: y2, x1: x2]
    cv2.imshow("x", cropped_copy)
    cv2.imwrite(f"megoldas/AleksandarStoisavljevic_V1KQIM{filename.split('/')[1].split('.')[0]}rotated.png", cropped_copy)
    cv2.waitKey(0)


try:
    filename = "Kep_kiegyenesitese/jail.png"
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    src = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    # src = cv2.GaussianBlur(src, (5, 5), 2.0)
    dst = cv2.Canny(src, 50, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstlong = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cdstangle = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    lines = cv2.HoughLines(dst, 1, np.pi / 180, 300, None, 0, 0)

    sizemax = math.sqrt(cdst.shape[0] ** 2 + cdst.shape[1] ** 2)

    cv2.imshow("Original",img)
    cv2.waitKey(0)
    cv2.imshow("Gray",src)
    cv2.waitKey(0)
    cv2.imshow("cdst",cdst)
    cv2.waitKey(0)

    sumang = 0
    bigangelpt1 = 0
    bigangelpt2 = 0
    bigangel = 0

    maxd=0
    maxdpt1=0
    maxdpt2=0
    if lines is not None:

        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho

            pt1 = (int(x0 + sizemax * (-b)), int(y0 + sizemax * a))
            pt2 = (int(x0 - sizemax * (-b)), int(y0 - sizemax * a))
            angle = math.atan2(pt1[1] - pt2[1], pt1[0] - pt2[0]) * 180 / math.pi

            if i == 0:
                bigangel = 180 - abs(angle)
                bigangelpt1 = pt1
                bigangelpt2 = pt2
                # print("angl first")
            elif bigangel < (180 - abs(angle)):
                bigangel = 180 - abs(angle)
                bigangelpt1 = pt1
                bigangelpt2 = pt2
                # print("angl new first")
            d=math.sqrt((pt1[1] - pt2[1])** 2 + (pt1[0] - pt2[0]) ** 2)
            if i == 0:
                maxd = d
                maxdpt1 = pt1
                maxdpt2 = pt2

            elif maxd<d:
                maxd = d
                maxdpt1 = pt1
                maxdpt2 = pt2

            sumang = +angle
            cv2.line(cdst, pt1, pt2, (0, 0, 255), 3, cv2.LINE_AA)
            cv2.imshow("cdst", cdst)
            cv2.waitKey(0)

            line = math.sqrt((pt2[0] - pt1[0]) ** 2 + (pt2[1] - pt1[1]) ** 2)



    cv2.line(cdstlong, maxdpt1, maxdpt2, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.imshow("Legerosebb vonal",cdstlong)
    cv2.waitKey(0)
    cv2.line(cdstangle, bigangelpt1, bigangelpt2, (0, 0, 255), 3, cv2.LINE_AA)
    cv2.imshow("Legerosebb szog",cdstangle)
    cv2.waitKey(0)
    rows, cols = cdstangle.shape[:2]
    print(bigangel)
    #bigangel=sumang/len(lines)
    if bigangel <= 45:
        print("horizontal")
        print("-",bigangel)
        rotate(img, cols, rows, bigangel*(-1))
        crop(bigangel*(-1))
    else:
        print("vertical")
        print("-",bigangel)
        rotate(img, cols, rows, 90-bigangel)
        crop(90-bigangel)
        cv2.destroyAllWindows()
except:
    print("Szet halt a program :( Valoszinulegnem talalt vonalt.")

