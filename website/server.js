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
		var myobj = { board: "Gossiping", 
					  aid : "M123A", 
					  title: "QQ", 
                      ts: 1, 
                      author: "JAQQ", 
                      content: "", 
                      push_content: "", 
                      ip: "111"};
		
        dbo.collection("PTTArticle").insertOne(myobj, function(err, res) {
			if(err) {
				throw err;
			}
		});  		
        
        dbo.listCollections().toArray(function(err, collInfos) {
            console.log(collInfos)     
        });

        dbo.collection("PTTArticle").findOne({}, function(err, result) {
              if (err) throw err;
                  console.log(result);
                        });

		var cursor = dbo.collection('PTTArticle').find();

		// Execute the each command, triggers for each document
		cursor.each(function(err, item) {
			// If the item is null then the cursor is exhausted/empty and closed
			console.log(item)			
            // otherwise, do something with the item
		});
            
        db.close();
	});

	res.send("OK")
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
