'use strict';

var fs = require('fs');
var path = require('path');
var multer = require('../lib/multerUtil.js');

// var upload = multer.single('upload-file');


exports.renderUpload = function(req, res, next) {
	res.render('upload', {
		msg: null
	});
};

// exports.uploadLF = function(req, res, next) {
// 	upload(req, res, function(err) {
// 		if (err) {
// 			return console.log(req.body, err);
// 		}

// 		console.log(req.file.originalname);
// 		var msg = req.file.originalname + " upload successful";
// 		res.render('upload', {
// 			msg: msg
// 		});
// 	});
// };


exports.uploadLF = function(req, res, next) {

	var upload = multer.upload(path.join(__dirname, '/../', '/uploads/', '/lf/'))
		.single('upload-file');
	commomUpload(req, res, upload);
};

exports.uploadPeer = function(req, res, next) {

	var upload = multer.upload(path.join(__dirname, '/../', '/uploads/', '/peer/'))
		.single('upload-file');
	commomUpload(req, res, upload);
};

exports.uploadLivepush = function(req, res, next) {

	var upload = multer.upload(path.join(__dirname, '/../', '/uploads/', '/livepush/'))
		.single('upload-file');
	commomUpload(req, res, upload);
};

function commomUpload(req, res, obj) {
	obj(req, res, function(err) {
		if (err) {
			return console.log(req.body, err);
		}

		console.log(req.file.originalname);
		var msg = req.file.originalname + " upload successful";
		res.render('upload', {
			msg: msg
		});
	});
};