import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate("C:/Users/Gabriel Castro/Desktop/facerecog/Database.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':"https://reconhecimentofacial-a9de4-default-rtdb.firebaseio.com/"
})

ref = db.reference('Responsáveis')

data = {
    "2222":
        {
            "nome": "Barack Hussein Obama II",
            "responsável pelo": "Ex Presidente",
        },
    "3333":
        {
            "nome": "Thomas Stanley Holland",
            "responsável pelo": "Ator",
        }

}


for key,value in data.items():
    ref.child(key).set(value)

