'use strict';

var router = require('express').Router();

var resultQuery = require('../controller/result_query.js');
var upload = require('../controller/upload.js');
var control = require('../controller/control.js');
var envrioment = require('../controller/envrioment.js');
var index = require('../controller/index.js');


router.get('/result_query', resultQuery.renderResultQuery);

router.get('/upload', upload.renderUpload);

router.post('/upload/lf', upload.uploadLF, function(req, res, next) {});

router.post('/upload/peer', upload.uploadPeer, function(req, res, next) {});

router.post('/upload/livepush', upload.uploadLivepush, function(req, res, next) {});

router.get('/control', control.renderControl);

router.get('/control/stop_peer', control.controlStopPeer);

router.get('/control/stop_lf', control.controlStopLF);

router.get('/control/start_peer', control.controlStartPeer);

router.get('/control/start_lf', control.controlStartLF);

router.get('/control/join_lf', control.controlJoinLF);

router.get('/enviroment', envrioment.renderEnvrioment);

router.get('/', index.renderIndex);

module.exports = router;