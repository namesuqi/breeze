// 获得制定的小时数之前的时间戳字符串
// 格式如下：20170808154126
// 精确到秒，和数据库里面存储的格式一致
exports.getDate = function (diffHour) {

    Date.prototype.Format = function (fmt) { //author: meizz
        var o = {
            "M+": this.getMonth() + 1, //月份
            "d+": this.getDate(), //日
            "h+": this.getHours(), //小时
            "m+": this.getMinutes(), //分
            "s+": this.getSeconds(), //秒
            "q+": Math.floor((this.getMonth() + 3) / 3), //季度
            "S": this.getMilliseconds() //毫秒
        };
        if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
        for (var k in o)
            if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        return fmt;
    }

    var order = "buffer_number";
    // var order = "max_buffering_time";
    var lf_number = "=";


    // 多少个小时以前，新方案
    var timeNow = Date.parse(new Date());
    var timeAgo = timeNow - 3600*1000*(diffHour);
    var timeStart = (new Date(timeAgo)).Format("yyyyMMddhhmmss");
    return timeStart;

}

