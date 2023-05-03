import face_recognition
import pickle
import cv2
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate('')
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://reconhecimentofacial-a9de4-default-rtdb.firebaseio.com/",
    'storageBucket': "reconhecimentofacial-a9de4.appspot.com"
})

pasta = ''
inf_rosto = os.listdir(pasta)
print(inf_rosto)
imgROSTO = []
RG = []

for path in inf_rosto:
    imgROSTO.append(cv2.imread(os.path.join(pasta, path)))
    RG.append(os.path.splitext(path)[0])

    arquivoNOME = f'{pasta}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(arquivoNOME)
    blob.upload_from_filename(arquivoNOME)



print (RG)

def buscador(imgROSTO):
    Banco = []
    for img in imgROSTO:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        x = face_recognition.face_encodings(img)[0]
        Banco.append(x)

    return Banco

print("Salvando...")
y = buscador(imgROSTO)
z = [y, RG]


arquivo = open ("dados.p", 'wb')
pickle.dump(z, arquivo)
arquivo.close()
print("Salvo!")
