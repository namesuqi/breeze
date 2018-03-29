'use strict';

var spawnSync = require('child_process').spawnSync;
var spawn = require('child_process').spawn;

exports.execute = function(command, args, callback) {
	var cmd = spawnSync(command, args);
	var stdout = cmd['stdout'];
	var stderr = cmd['stderr'];
	var status = cmd['status'];

	console.log(args);

	// console.log(String(stdout), String(stderr), status);
	if (stderr.length === 0) {
		callback([stdout, status]);
	} else {
		callback([stderr, status]);
	}
};

exports.execute_2 = function(command, args, callback) {
	var options = {
		// stdio: 'inherit' //feed all child process logging into parent process
		stdio: 'pipe'
	}
	var cmd = spawn(command, args, options);

	try{
		cmd.stdout.on('data', function(data) {
			// console.log('stdout: ' + data.toString());
			callback(data.toString());
		});

		cmd.stderr.on('data', function(data) {
			console.log('stderr: ' + data.toString());
		});

		cmd.on('exit', function(code) {
			console.log('child process exited with code ' + code.toString());
		});
	}catch (err){
		console.log(err);
	}
	
};