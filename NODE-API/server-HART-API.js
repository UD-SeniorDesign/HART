//Pull in required packages
var http = require('http');
var md5 = require('js-md5');
var fs = require('fs');

//Create the server
http.createServer(function (req, res) {
    var endpoint = req.url;
    //handle endpoints
    switch(endpoint){
        case "/createtarget":
            res.write("<h1>target created</h1>");
            createTarget();
            break;
        case "/gettargetdata":
            break;
    }// switch | endpoint handling

    res.end();

}).listen(9090); // the server object listens on port 8080

//for logging purposes
console.log('listening...');


function createTarget(){
    currentDatetime = new Date();
    hashedDatetime = md5(currentDatetime.toString());
    console.log("Pulling target data from file\n" + currentDatetime + "\n" + hashedDatetime);
}// createTarget | 

function getTargerData(){
    file = "madisonTest.json";
    console.log("info retreived: ");
    var contentsArr = []
    fs.readFile(file,'utf8',function(err,contents){
        JSON.parse(contents)
        returnData(contents);
        console.log(contents);
    })
    
}// pullTargetDataFromFile | 

function returnData(data){
    return data;
}//returnData