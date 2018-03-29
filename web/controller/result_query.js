'use strict';


exports.renderResultQuery = function(req, res, next) {

    // 多久以内的数据
    var hour = req.query.hour;
    if (hour === undefined || hour==="") {
        var diffHour = 24;
    } else {
        var diffHour = hour;
    }
    console.log("diffHour:"+diffHour);

    // 多少雷锋节点
    var leifeng = req.query.leifeng;
    if (leifeng === undefined || leifeng==="") {
        leifeng = 0;
    }
    console.log("leifeng:"+leifeng);

    // 多少播放时间的测试
    var playDuration = req.query.playDuration;
    if (playDuration === undefined || playDuration==="") {
        playDuration = 3600;
    }
    console.log("playDuration:"+playDuration);

    // 排序方法
    var sort = req.query.sort;
    if (sort === undefined || playDuration==="") {
        sort = "buffer_number";
    }
    console.log("sort:"+sort);


    var mysql = require('mysql');
    var conn = mysql.createConnection({
        host: '192.168.1.61',
        user: 'ppc',
        password: 'yunshang2014',
        database:'user_experience',
        port: 3306
    });

    // 获得过滤的起始时间
    var getDate = require('../lib/UXDate').getDate;
    var timeStart = getDate(diffHour);
    console.log(timeStart);

    // var sort = "buffer_number";
    // var sort = "max_buffering_time";

    conn.connect();
    conn.query('select * from ue_performance where case_start_time>' + timeStart
        + ' and play_duration=' + playDuration
        + ' and lf_number='+ leifeng
        + ' ORDER BY ' + sort + ' DESC limit 1000', function(err, rows, fields) {
        if (err) throw err;
        res.render('result_query',
            {
                hour: diffHour,
                leifeng:leifeng,
                playDuration:playDuration,
                sort: sort,
                rows: rows
            });
        conn.end();
    });
};