// 点击搜索结果
const labelSearch = document.getElementById("label-search");
labelSearch.onclick = function() {
    // 刷新界面
    location.reload();
}

// 左侧分类点击事件
const allType = document.getElementById("all-type");
const baseModel = document.getElementById("base-model");
const deliverable = document.getElementById("deliverable");
allType.onclick = async function() {
    selfLine = document.querySelector("#all-type > .line");
    selfLine.style.display="block";
    otherLine1 = document.querySelector("#base-model > .line");
    otherLine1.style.display="none";
    otherLine2 = document.querySelector("#deliverable > .line");
    otherLine2.style.display="none";
}
baseModel.onclick = async function() {
    selfLine = document.querySelector("#base-model > .line");
    selfLine.style.display="block";
    otherLine1 = document.querySelector("#all-type > .line");
    otherLine1.style.display="none";
    otherLine2 = document.querySelector("#deliverable > .line");
    otherLine2.style.display="none";
}
deliverable.onclick = async function() {
    selfLine = document.querySelector("#deliverable > .line");
    selfLine.style.display="block";
    otherLine1 = document.querySelector("#all-type > .line");
    otherLine1.style.display="none";
    otherLine2 = document.querySelector("#base-model > .line");
    otherLine2.style.display="none";
}


// 获取参数kw
const url = new URL(location.href);
let kw = url.searchParams.get("kw");
if (kw){
    let relkw = decodeURIComponent(kw);
    const labelSearch = document.getElementById("label-search");
    const searchTtile = document.getElementById("search-title");
    labelSearch.innerHTML = `搜索"${relkw}"`;
    searchTtile.innerHTML = `搜索“${relkw}”`;
}
else {
    const body = document.body;
    body.style.marginTop="50px";
    body.style.display="flex";
    body.style.justifyContent="center";
    body.innerHTML="请确保链接参数正确并重新访问";
    body.style.fontSize="30px";
}