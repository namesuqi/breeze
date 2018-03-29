'use strict';

var execute = require('./lib/executeCMD.js');
var path = require('path');

console.log(path.join(__dirname, '..', 'test.py'), 'start');

// execute.execute('python', [path.join(__dirname, '..', 'test.py'), 'starttest'], function(data) {
// 	console.log(String(data[0]), data[1]);
// });


// execute.execute('python', [path.join(__dirname, '..', 'test.py'), 'stoptest'], function(data) {
// 	console.log('************');
// 	console.log(String(data[0]), data[1]);
// });

// execute.execute_2('python', [path.join(__dirname, '..', 'test.py'), 'stoptest'], function(data) {
// 	console.log('callback: ' + data);
// });

// execute.execute_2('ping', ['8.8.8.8', '-c', '4'], function(data) {
// 	console.log('callback: ' + data);
// });

execute.execute('ping', ['8.8.8.8', '-c', '4'], function(data) {
	console.log(String(data[0]), data[1]);
});

// var spawn = require('child_process').spawn;


// var options = {
// 	stdio: 'inherit' //feed all child process logging into parent process
// }

// var childProcess = spawn('python', [path.join(__dirname, '..', 'test.py'), 'stoptest'], options);

// try{
// 	childProcess.stdout.on('data', function(data) {
// 	    process.stdout.write(data.toString());
// 	});
// }catch (err){
// }