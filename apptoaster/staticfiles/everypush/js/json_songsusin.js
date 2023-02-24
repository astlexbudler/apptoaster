isModal = false;
isUi = true;

// getCookie/쿠키데이터 호출
getCookie = (name) => {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// csrfToken/CSRF 토큰 생성
csrfToken = getCookie('csrftoken');

// asyncRequest/비동기적 api 요청 송신(테스트중..)
asyncRequest = (requestUrl, jsonData) => {
    if (jsonData == "") {
        jsonData = '{"data": "null"}';
    }
    fetch(requestUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        body: jsonData,
    }).then((response) => {
        try {
            resultJson = response.json();
            console.log("asyncRequest(); 비동기적 api 요청\n주소: " + requestUrl + "\n데이터: " + jsonData + "처리 완료.\n응답: " + resultJson);
            return resultJson;
        } catch {
            console.warn("asyncRequest(); 비동기적 api 요청\n주소: " + requestUrl + "\n데이터: " + jsonData + "처리 중 응답이 json 형식이 아닙니다.\n응답: " + response);
            return response;
        }
    });
}

// syncRequest/동기적 api 요청 송신
syncRequest = (requestUrl, jsonData) => {
    if (jsonData == "") {
        jsonData = '{"data": "null"}';
    }
    httpRequest = new XMLHttpRequest();
    httpRequest.open("POST", requestUrl, false);
    httpRequest.setRequestHeader("X-CSRFToken", csrfToken);
    httpRequest.send(jsonData);
    try {
        resultJson = JSON.parse(httpRequest.responseText);
        console.log("syncRequest(); 동기적 api 요청.\nurl: " + requestUrl + "\ndata: " + jsonData + " 처리 완료.\nresponse: " + httpRequest.responseText);
        return resultJson
    } catch {
        console.warn("syncRequest(); 동기적 api 요청.\nurl: " + requestUrl + "\ndata: " + jsonData + " 처리 중 응답이 json 형식이 아닙니다.\nresponse: " + httpRequest.responseText);
        return httpRequest.responseText;
    }
}

// getDate/며칠 후의 시간 구하기
getDate = (dateIndex) => {
    today = new Date();
    today.setDate(today.getDate() + dateIndex);
    timestamp = today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
    console.log("getDate();\n현재 날짜에서 " + dateIndex + "일 만큼 이동한 날짜.\ntimestamp: " + timestamp);
    return timestamp;
}

// toggleModal/해당되는 모달의 활성화 상태를 토글
toggleModal = (modalId) => {
    modal = document.querySelector("#" + modalId);
    style = modal.getAttribute("style");
    if (style.indexOf("display: none;") != -1) {
        console.log("toggleModal();\n" + modalId + " 모달 활성화");
        modal.setAttribute("style", "");
    } else {
        console.log("toggleModal();\n" + modalId + " 모달 비활성화");
        modal.setAttribute("style", "display: none;");
    }
}

// toggleUi/UI 활성화 상태를 토글
toggleUi = (status) => {
    if (status && isUi) {
        return
    }

    if (status == "") {
        isUi = !isUi;
    } else {
        isUi = status;
    }

    uiElements = document.querySelectorAll(".uiElements");
    if (isUi) {
        console.log("toggleUi();\nUI 활성화");
        for (element of uiElements) {
            defaultStyle = element.getAttribute("style");
            element.setAttribute("style", defaultStyle.replace("display: none;", ""));
        }
    } else {
        console.log("toggleUi();\nUI 비활성화");
        for (element of uiElements) {
            defaultStyle = element.getAttribute("style");
            element.setAttribute("style", defaultStyle + "display: none;");
        }
    }
}

// getJsonStringData/통신 전 제이슨 형식의 String Data 전처리.
getJsonStringData = (dataArray) => {
    var startMustache = "{"
    var innerComma = ",";
    var endMustache = "}";
    var wq = "\"";//double qoutation mark
    var dd = ":";
    var JsonStringData = "";
    JsonStringData += startMustache;
    for (var idx in dataArray) {//dataArray..[["",""],["",""],...]
        var key = dataArray[idx][0];
        var value = dataArray[idx][1];
        JsonStringData += wq;// \"
        JsonStringData += key;// pastorId
        JsonStringData += wq;// \"
        JsonStringData += dd;// :
        JsonStringData += wq;// \"
        JsonStringData += value;// value
        JsonStringData += wq;// \"
        JsonStringData += innerComma;// ,
        }
    var newJsonStringData = JsonStringData.slice(0, -1);
    newJsonStringData += endMustache;
    return newJsonStringData;
    }

//어디론가 이동
goTo = (gourl) => {
    window.location.href = gourl
}

//기본모달 및 기능(OnOff) 정의
modalOn = (modalElement) => {
    modalElement.style.display = "flex"
}

isModalOn = (modalElement) => {
return modalElement.style.display === "flex";
}

modalOff = (modalElement) => {
modalElement.style.display = "none";
}

//기본모달의 표준세팅(닫기 기능+)
modalSetting = (modalElement) => {
	const closeBtn = modalElement.querySelector(".modal-close-area")
	closeBtn.addEventListener("click", e => {
		modalOff(modalElement)
	})
    const closeBtn2 = modalElement.querySelector(".modal-btnModal_sub_gray")
    closeBtn2.addEventListener("click", e => {
    modalOff(modalElement)
    })
	modalElement.addEventListener("click", e => {
	const evTarget = e.target
	if(evTarget.classList.contains("modal-overlay")) {
		modalOff(modalElement)
	}
	})}

//로그아웃 동기 요청
signoutSyncRequest = () => {
    var data;
    url = 'data/try_signout'
    syncRequest(url, data);
    goTo('/');
}

//랜덤문자열생성8자.
getRandomString8 = () => {
    ranstr = Math.random().toString(36).substring(2, 10);
    return ranstr;
}