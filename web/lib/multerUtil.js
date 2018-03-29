'use strict';

// var path = require('path');
var multer = require('multer');

// var storage = multer.diskStorage({
// 	destination: function(req, file, cb) {
// 		cb(null, path.join(__dirname ,'/../' , '/uploads/'))
// 	},
// 	filename: function(req, file, cb) {
// 		cb(null, file.originalname)
// 	}
// })

// var upload = multer({
// 	storage: storage
// })


// module.exports = upload;

exports.upload = function(path) {
	var storage = multer.diskStorage({
		destination: function(req, file, cb) {
			cb(null, path)
		},
		filename: function(req, file, cb) {
			cb(null, file.originalname)
		}
	});

	var upload = multer({
		storage: storage
	});

	return upload;
};