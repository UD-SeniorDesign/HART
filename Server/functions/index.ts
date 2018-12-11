import * as functions from 'firebase-functions'
import * as admin from 'firebase-admin'
admin.initializeApp()

export const currentLocations = functions.https.onRequest((request,response) => {
    const promise = admin.firestore().doc('locOne').get()
    const p2 = promise.then(snapshot => {
        const data = snapshot.data()
        response.send(data)
    })

    p2.catch(error => {
        console.log(error)
        response.status(500).send(error) 
    })

})