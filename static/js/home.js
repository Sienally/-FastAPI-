// -*- coding: utf-8 -*-
// 搜索功能
const searchBtn = document.getElementById("searchBtn");
searchBtn.onclick = async function() {
    const value = document.getElementById("input").value;
    if(!value) {
        alert("输入不能为空!");
    }
    else {
        // 当前页面跳转
        location.href = "/api/subpages/search?kw=" + value;

        // // get请求方法
        // const res = await fetch("/api/subpages/search?kw=" + value);
        // const result = await res.json();
        // alert(JSON.stringify(result));
        // window.open("/api/subpages/search?kw=" + value);

        // post请求方法

        // // 封装请求信息
        // const data = {
        //     kw: value
        // };
        // // 发送请求
        // const res = await fetch("/api/subpages/search", {
        //     method: "POST",
        //     headers: {
        //         "Content-Type": "application/json"  // 告诉后端请求body是json格式
        //     },
        //     body: JSON.stringify(data)  // 把JS对象转成JSON字符串, 放进请求体
        // })
        // const result = await res.json();
        // alert(JSON.stringify(result));
    }
}

// 监听输入框是否按下回车键, 视同点击搜索
const input = document.getElementById("input");
input.addEventListener("keydown", function(e) {
    if(e.key == "Enter") {
        e.preventDefault();
        searchBtn.click();
    }
})





/* 轮播图 */

// 写一个数组，原来存放图片路径
var picList = new Array();
picList[0] = document.getElementById("banner-pic-01");
picList[1] = document.getElementById("banner-pic-02");
picList[2] = document.getElementById("banner-pic-03");
var timer;
var index = 1;
function sliderBanner() {
    if (picList.length - index == 2) {
        document.getElementById("banner-pic-01").style.display="block";
        document.getElementById("banner-pic-02").style.display="none";
        document.getElementById("banner-pic-03").style.display="none";
    }
    else if(picList.length - index == 1) {
        document.getElementById("banner-pic-01").style.display="none";
        document.getElementById("banner-pic-02").style.display="block";
        document.getElementById("banner-pic-03").style.display="none";
    }
    else {
        document.getElementById("banner-pic-01").style.display="none";
        document.getElementById("banner-pic-02").style.display="none";
        document.getElementById("banner-pic-03").style.display="block";
    }
    if (index < picList.length) {
        index++;
    }
    else {
        index = 1;
    }
    timer = setTimeout(sliderBanner, 2000);
};





/* 登录界面的iframe */
const login = document.getElementById("login");
const cancel = document.querySelector("#iframe-login > button");
const iframeBox = document.getElementById("iframe-login");
const iframe = document.querySelector("#iframe-login > iframe");
const loginMask = document.getElementById("login-mask");


// 登录函数
function loading() {
    // 手机端暂不可用
    let w = window.innerWidth;
    if (w < 450) {
        alert("手机端暂未开放登录功能喵!");
    }
    else {
        loginMask.style.display="block";
        iframeBox.style.display="block";
    }
}

// 取消登录函数
function loadingCancel() {
    loginMask.style.display="none";
    iframeBox.style.display="none";
    // 清空表单残留数据
    iframe.contentDocument.querySelector("#account > input").value = "";
    iframe.contentDocument.querySelector("#password > input").value = "";
    iframe.contentDocument.querySelector("#account > .input-underline").style.background="#899FF6";
    iframe.contentDocument.querySelector("#password > .input-underline").style.background="#899FF6";
    iframe.contentDocument.querySelector("#account > p").style.display="none";
    iframe.contentDocument.querySelector("#password > p").style.display="none";
    return 0;
}

// 按键绑定
login.onclick = loading;
cancel.onclick = loadingCancel;



// 页面加载完成后执行函数
window.onload=function() {
    sliderBanner();
    let w = window.innerWidth;

    // 只有PC端会10秒后自动弹出登录
    if (w > 450) {
        let timer;
        timer = setTimeout(loading, 10000);
    }
}