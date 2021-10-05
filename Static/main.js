const submit = $("<input id='finish' type = 'submit' value = 'Submit and Finish' /> ")
const next = $("<input id='next' type='submit' value='Continue'/>")
var timer = null

$(document).ready(function () {
    checkCookie()
    $("#question").fadeOut(1) // Do quick fadeout to set state properly
    $("#begin").click(function () {
        $("#top").fadeOut(500)
        getQuestion(500)
    })
})

$(window).on('unload', function () {
    if (timer != null) {
        sendAnswer()
    }
})

// Gets the next question for the user
// If the question is valid, use variableName.propertyName to get values
function getQuestion(timeout) {
    response = null
    $.ajax({
        url: "/send",
        type: "POST",
        async: false,
        dataType: "JSON",
        success: function (response) {
            occupyQuestionField(response)
            setTimeout(function () { $("#question").fadeIn(500) }, timeout)
            // This will only go off once per method call
            timer = setInterval(function () {
                finish()
            }, 30000)
        },
        error: function (response) {
            console.log("error" + response)
        }
    })
}

// Fills appropriate areas in question field with data from backend
function occupyQuestionField(question) {
    $("#prompt").append(question.prompt)

    // You might be able to use this later if you add questions with more or less than 4 answers
    // instead of the four lines below that aren't in comments. Would need to change something with 
    // getting specific question values

    /*var checked = false;
    for (var i = 1; i < Object.keys(question).length; i++) {
        if (!checked) {
            checked = true
            $("#answers").append("<input type='radio' name='ans' value='ans" +
                i + "' checked=true/>" + question.i + "<br/>")
        }
        else {
            $("#answers").append("<input type='radio' name='ans' value='ans" +
                i + "'>" + question.i + "<br/>")
        }
    }*/

    $("#answers").append("<input type='radio' name='ans' checked=true value='" + question.ans1 + "'>" + question.ans1 + "</input><br/> ")
    $("#answers").append("<input type='radio' name='ans' value='" + question.ans2 + "'>" + question.ans2 + "</input><br/> ")
    $("#answers").append("<input type='radio' name='ans' value='" + question.ans3 + "'>" + question.ans3 + "</input><br/> ")
    $("#answers").append("<input type='radio' name='ans' value='" + question.ans4 + "'>" + question.ans4 + "</input><br/> ")

    $("#answers").append(next)
    $("#answers").append(submit)
    submit.click(function () { console.log('finish button clicked'); finish() })
    next.click(function () { console.log('next button clicked'); nextQuestion() })
}

/*// Displays the next question
function displayQuestion(timeout) {
    question = getQuestion()
    console.log(question)
    if (question == null) {
        console.log("Server failed to send question")
    }

}*/
function clearQuestion() {
    $("#question").fadeOut(500)
    $("#prompt").html("")
    $("#answers").remove(next)
    $("#answers").remove(submit)
    $("#answers").html("")
}

function nextQuestion() {
    clearInterval(timer)
    timer = null
    sendAnswer()
    clearQuestion()
    getQuestion(500)
}

function sendAnswer() {
    $.ajax({
        url: "/receive",
        type: "POST",
        data: {
            'answer-choice': $('input[name="ans"]:checked').val()
        },
        async: false
    })
}

function finish() {
    clearInterval(timer)
    timer = null
    sendAnswer()
    reset()
}

function reset() {
    $("#question").fadeOut(500)
    clearQuestion()
    $("#top").fadeIn(500)
}

//Code from https://www.w3schools.com/js/js_cookies.asp

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    //Add cookie to database here using php
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function checkCookie() {
    var username = getCookie("username");
    if (username == "") {
        username = prompt("Please enter your name:", "");
        if (username != "" && username != null) {
            setCookie("username", username, 365);
        }
    }
}

//Code from https://www.w3schools.com/js/js_cookies.asp