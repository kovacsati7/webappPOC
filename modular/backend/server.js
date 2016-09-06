var express = require('express');
var app =express();

var userData = [
  {'id':1, 'fname':'Mark', 'lname':'Otto', 'username':'@mda'},
  {'id':2, 'fname':'Jacob', 'lname':'Thornton', 'username':'@fat'},
  {'id':3, 'fname':'Larry', 'lname':'the Bird', 'username':'@twitter'}
];

app.use(function(req,res,next){
  res.header('Acces-Control-Allow-Origin','*');
  res.header('Acces-Control-Allow-Headers', 'Origin, X-Request-With, Content-Type, Accept');
})

app.get('/', function (req,res) {
  res.send('Hello World Backend!');
});

app.get('/users', function(request, response){
  response.setHeader('Content-Type', 'application/json');
  response.send(JSON.stringify(userData));
});

app.listen(3001, function (){
  console.log('Server started on port 3001!');
});