'use strict';


var executeCMD = require('../lib/executeCMD.js');
var path = require('path');

var executePath = path.join(__dirname, '..', '..');

exports.renderControl = function(req, res, next) {
	res.render('control', {
		msg: null
	});
};

exports.controlStopPeer = function(req, res, next) {
	executeCMD.execute('python', [path.join(executePath, 'manage.py'), 'stop_peer'], function(data) {
		res.render('control', {
			msg: data[0]
		});
	});
};

exports.controlStopLF = function(req, res, next) {
	executeCMD.execute('python', [path.join(executePath, 'manage.py'), 'stop_lf'], function(data) {
		res.render('control', {
			msg: data[0]
		});
	});
};

exports.controlStartLF = function(req, res, next) {
	executeCMD.execute('python', [path.join(executePath, 'leifeng.py'), 'start', '70'], function(data) {
		res.render('control', {
			msg: data[0]
		});
	});
};

exports.controlJoinLF = function(req, res, next) {
	executeCMD.execute('python', [path.join(executePath, 'leifeng.py'), 'join', '70'], function(data) {
		res.render('control', {
			msg: data[0]
		});
	});
};

exports.controlStartPeer = function(req, res, next) {

	var playDuration = req.query.playDuration;

	executeCMD.execute('python', [path.join(executePath, 'fe_play.py'), '-l 1', '-t '+ playDuration, '--lf 70'], function(data) {
		res.render('control', {
			msg: data[0]
		});
	});
};

