function dateFormat(date) {
    let month = date.getMonth() + 1;
    let day = date.getDate();
    let hour = date.getHours();
    let minute = date.getMinutes();
    let second = date.getSeconds();

    month = month >= 10 ? month : '0' + month;
    day = day >= 10 ? day : '0' + day;
    hour = hour >= 10 ? hour : '0' + hour;
    minute = minute >= 10 ? minute : '0' + minute;
    second = second >= 10 ? second : '0' + second;

    return date.getFullYear().toString().slice(-2) + '' + month + '' + day + '' + hour + '' + minute + '' + second + '' + date.getMilliseconds();
}

getTimestamp = () => {
    var now = new Date();
    return dateFormat(now);
}

getDate = () => {
    var now = new Date();

    year = now.getFullYear();
    month = now.getMonth() + 1;
    date = now.getDate();

    month = month >= 10 ? month : '0' + month;
    date = date >= 10 ? date : '0' + date;

    return year + "-" + month + "-" + date
}

getTime = () => {
    var now = new Date();

    hour = now.getHours();
    minute = now.getMinutes();
    second = now.getSeconds();

    hour = hour >= 10 ? hour : '0' + hour;
    minute = minute >= 10 ? minute : '0' + minute;
    second = second >= 10 ? second : '0' + second;

    return hour + ":" + minute + ":" + second
}