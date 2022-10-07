(function () {
    const second = 1000,
        minute = second * 60,
        hour = minute * 60,
        day = hour * 24;

    let birthday = "JAN 07, 2022 00:00:00",
        countDown = new Date().getTime(),
        //x = setInterval(function () {

            now = new Date().getTime(),
                distance = countDown - now;

            document.getElementById("days").innerText = Math.floor(distance / (day)),
                document.getElementById("hours").innerText = Math.floor((distance % (day)) / (hour)),
                document.getElementById("minutes").innerText = Math.floor((distance % (hour)) / (minute)),
                document.getElementById("seconds").innerText = Math.floor((distance % (minute)) / second);

            //do something later when date is reached
            if (distance < 0) {
                document.getElementById("countdown").innerText = "00:00:00";
                //clearInterval(x);
            }
            //seconds
        //}, 0)
    //document.getElementById("countdown").innerText = "00:00:00";
}());