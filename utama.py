import cv2
from jarak import disCalt
import copy
from PIL import Image
from yolox.models import Yolox
from yolox.data.datasets import COCO_CLASSES

def distanceCalculation(results,img,pembanding,toleranjarak):
    imga = img.copy()
    boxes = results[0]['bboxes']
    labels = results[0]['labels']
    scores = results[0]['scores']

    jarakJarak = []
    jarakJarakY = []

    jarakTerdekat = 0
    jarakTerdekaty = 0

    b,g,r = cv2.split(pembanding)
    for box,label,conf in zip(boxes,labels,scores):
        x, y, w, h, = box#Coordinate

        name = COCO_CLASSES[label]#Ambil Nama Class/Label
        conf = round(conf,2)
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)
        if r[y][x] == 255 and b[y][x] == 255:
            if name == "car" or name == "truck":
                if y > jarakTerdekaty:
                    jarakTerdekaty = copy.deepcopy(y)
                    jarakTerdekat = copy.deepcopy(w)

    for box,label,conf in zip(boxes,labels,scores):
        x, y, w, h, = box

        name = COCO_CLASSES[label]
        conf = round(conf,2)
        x = int(x)
        y = int(y)
        w = int(w)
        h = int(h)

        if r[y][x] == 255 and b[y][x] == 255:
            if name == "car" or name == "truck":
                jarak = str(int(disCalt(w-x,imga,jarakTerdekat)))
                jarakJarak.append(int(jarak))
                jarakJarakY.append(int(y))

                cv2.rectangle(imga, (x, y), (w,h), (255, 0, 0), 1)
                cv2.putText(imga, jarak, (x,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                cv2.putText(imga, name, (w,y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)

    #Rata-rata jarak dari n jarak terjauh (n = toleran jarak)
    if len(jarakJarak) >= toleranjarak:
        jarakTerjauh = jarakJarak[-toleranjarak:]
        jarakTerjauh = sum(jarakTerjauh)/len(jarakTerjauh)
    elif len(jarakJarak) < toleranjarak and len(jarakJarak) != 0:
        jarakTerjauh = sum(jarakJarak)/len(jarakJarak)
    elif len(jarakJarak) == 0:
        jarakTerjauh = 0

    return jarakTerjauh,imga

#DrawLine
def drawLine():
    global ix,iy
    global lw1,lh1,lh2,lw2,lineThicc
    cv2.namedWindow(winname = "Buat Garis") 
    cv2.setMouseCallback("Buat Garis", drawLineDrag) 

    while True: 
        cv2.imshow("Buat Garis", ogCitra) 
        cv2.setWindowProperty("Buat Garis", cv2.WND_PROP_TOPMOST, 1)
        if cv2.waitKey(10) == 27:
            ix = iy = -1
            cv2.destroyAllWindows()
            print(lw1,lh1,lh2,lw2,lineThicc)
            break

def drawLineDrag(event, x, y, param, a):
    global og, ix, iy, ogCitra
    global lw1,lh1,lh2,lw2,lineThicc
    #Draw dengan left click mouse
    if event == cv2.EVENT_LBUTTONDOWN:
        ix = x
        iy = y
    elif event == cv2.EVENT_LBUTTONUP:
        cv2.line(ogCitra, (ix, iy),(x, y),(255, 0, 255),lineThicc)
        lw1 = copy.deepcopy(ix)
        lh1 = copy.deepcopy(iy)
        lw2 = copy.deepcopy(x)
        lh2 = copy.deepcopy(y)
    #Reset dengan right click mouse
    if event == cv2.EVENT_RBUTTONUP:
        lw1 = 0
        lh1 = 0
        lw2 = 0
        lh2 = 0
        ogCitra = og.copy()

#Set up
model = Yolox.from_pretrained("yolox_s")

citra = cv2.imread('Citra4.png')
og = citra
ogCitra = citra.copy()

#Draw Line
lw1 = 0
lh1 = 0
lw2 = 0
lh2 = 0
ix = 0
iy = 0
lineThicc = 80
drawLine()

#Ubah Opencv to PIl 
citraPil = Image.fromarray(citra)
#Operasi Yolox
result = model([citraPil],0.05)

#Bounding box dan penghitungan jarak
jarakTerjauh,hasilCitra = distanceCalculation(result,citra,ogCitra,toleranjarak=3)

print("Jarak Terjauh",jarakTerjauh)

cv2.imshow("Hasil citra",hasilCitra)
cv2.waitKey(0)
cv2.destroyAllWindows()