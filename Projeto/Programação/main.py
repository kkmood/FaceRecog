import face_recognition
import pickle
import cvzone
import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
import numpy as np
import numpy

cred = credentials.Certificate("") #Onde o DATABASE SE LOCALIZA, EX: C:/Users/BOB/Desktop/facerecog/Database.json
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://reconhecimentofacial-a9de4-default-rtdb.firebaseio.com/",
    'storageBucket': "reconhecimentofacial-a9de4.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)

imgFundo = cv2.imread('') # EX: C:/Users/BOB/Desktop/facerecog/Projeto/HUD/Fundo/background.png

pasta = '' #Pasta HUD, EX: C:/Users/BOB/Desktop/facerecog/Projeto/HUD
inf_pasta = os.listdir(pasta)
imgHUD = []
for path in inf_pasta:
    imgHUD.append(cv2.imread(os.path.join(pasta, path)))


arquivo = open('dados.p','rb')
z = pickle.load(arquivo)
arquivo.close()
y, RG = z

modeType = 0
counter = 0
id = -1
#imgPAIS = []

while True:
    success, img = cap.read()

    imgP = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgP = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    recog_rosto = face_recognition.face_locations(imgP)
    comparando = face_recognition.face_encodings(imgP, recog_rosto)


    imgFundo[162:162 + 480, 55:55 + 640] = img
    imgFundo[44:44 + 633, 808:808 + 414] = imgHUD[modeType]

    for rosto, local_rosto in zip(comparando, recog_rosto):
        rsim = face_recognition.compare_faces(y, rosto)
        rnao = face_recognition.face_distance(y, rosto)

        rINDEX = np.argmin(rnao)

        if rsim[rINDEX]:
            #y1, x2, y2, x1 = local_rosto
            #y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            #bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
            #imgFundo = cvzone.cornerRect(imgFundo, bbox, rt=0)
            id = RG[rINDEX]

            if counter == 0:
                counter = 1
                modeType = 1

        if counter != 0:

            if counter == 1:
                leituraInfo = db.reference(f'Responsáveis/{id}').get()
                print(leituraInfo)

                ref = db.reference(f'Responsáveis/{id}')

                #blob = bucket.get_blob(f'/C:/Users/Gabriel Castro/Desktop/facerecog/Projeto/Rostos/{RGindex}.jpg')
                #array = np.frombuffer(blob.download_as_string(),np.uint8)
                #imgPAIS = cv2.imdecode(array, cv2.IMREAD_COLOR)

            if 10<counter>20:
                modeType = 1

            imgFundo[44:44 + 633, 808:808 + 414] = imgHUD[modeType]


            if counter<=10:
                cv2.putText(imgFundo, str(leituraInfo['responsável pelo']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgFundo, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1),

                (w, h), _ = cv2.getTextSize(leituraInfo['nome'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2
                cv2.putText(imgFundo, str(leituraInfo['nome']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

            #imgFundo[175:175 + 216, 909:909 + 216] = imgPAIS
            counter+=1

            if counter>=20:
                counter = 0
                modeType = 0
                leituraInfo = []

                imgFundo[44:44 + 633, 808:808 + 414] = imgHUD[modeType]

    cv2.imshow("App", imgFundo)
    cv2.waitKey(1)
