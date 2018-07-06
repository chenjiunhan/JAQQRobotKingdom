var express = require('express');
var app = express();
 
var fs = require('fs');

app.get('/', function (req, res) {
    res.send('Hello');
})

app.get('/create', function(req, res) {
    var MongoClient = require('mongodb').MongoClient;
	var url = "mongodb://localhost:27017/";
	 
	MongoClient.connect(url, {useNewUrlParser: true }, function(err, db) {
	  	if (err) {
			throw err;
		}
		var dbo = db.db("JAQQ");
		dbo.createCollection("PTTArticle", function(err, res) {
            if (err) throw err;
            console.log("Collection created!");
        });
            
        db.close();
	});

	res.send("OK")
})

app.get('/drop', function(req, res) {
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://localhost:27017/";

    MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("JAQQ");
        dbo.collection("PTTArticle").drop(function(err, res) {
            if (err) throw err;
            if (res) console.log("Collection deleted");
        });

        db.close();
    });

	res.send("OK")
})

app.get('/find', function(req, res) {
    var MongoClient = require('mongodb').MongoClient;
	var url = "mongodb://localhost:27017/";
	MongoClient.connect(url, {useNewUrlParser: true }, function(err, db) {
	  	if (err) {
			throw err;
		}
		var dbo = db.db("JAQQ");
        
        var cursor = dbo.collection('PTTArticle').find();

	    var result = ""
        // Execute the each command, triggers for each document
        cursor.each(function(err, item) {
            // If the item is null then the cursor is exhausted/empty and closed
            if(typeof item == 'undefined') {
                send(err, result)   
            } else {
                console.log("????????????????")
                //console.log(JSON.stringify(item))
                result += JSON.stringify(item)
                //console.log(result)
                console.log("!!!!!!!!!!!!!!")
            }            
            // otherwise, do something with the item
        });

        function send(err, result) {
            res.send(result)
        }

        db.close();
    });
})


app.get('*', function (req, res) {
    //console.log(req, res)
    filePath = __dirname + "/" + req.url
    if (fs.existsSync(filePath)) {
        res.sendFile(filePath);
    } else {
        res.sendStatus(404);
    }
})

var server = app.listen(8080, function () {
     
    var host = server.address().address
    var port = server.address().port

    console.log("%s %s", host, port)
               
})
