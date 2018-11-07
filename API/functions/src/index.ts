import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'
admin.initializeApp()

export const currentLocations = functions.https.onRequest((request,response) => {
    admin.firestore().doc('locations/locOne').get().then(snapshot =>{
        const data = snapshot.data()
        response.send(data)
    }).catch(error=>{
        response.status(500).send(error)
    })

});

export const locks = functions.https.onRequest((request,response) => {
    admin.firestore().collection('locations').get().then(snapshot => {
        const data = snapshot.docs.entries
        response.send(data)
    }).catch(error=>{
        response.status(500).send(error)
    })
});

export const hellowWorld = functions.https.onRequest((request, response)=>{
    response.send("Hello,world");
});