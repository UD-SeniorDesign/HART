import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'
admin.initializeApp()

const db = admin.firestore();

export const currentLocations = functions.https.onRequest((request,response) => {
    db.doc('locations/locOne').get().then(snapshot =>{
        const data = snapshot.data()
        response.send(data)
    }).catch(error=>{
        response.status(500).send(error)
    })
});

export const hellowWorld = functions.https.onRequest((request, response)=>{
    response.send("Hello,world");
});
