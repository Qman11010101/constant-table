function setTableWidth() {
    const tableWidth = document.getElementById("table_width");
    let bodywrap = document.getElementById("bodywrap");
    bodywrap.style.width = String(parseInt(tableWidth.value) * 112) + "px"; // image 108px (100px + 4px border) + margin 2px * 2
}

function toggleDispTitle() {
    const dispTitleElm = document.getElementById("disp_title");
    const titles = document.getElementsByClassName("titleblock");
    for (let i = 0; i < titles.length; i++) {
        if (dispTitleElm.checked) {
            titles[i].style.display = "block";
        } else {
            titles[i].style.display = "none";
        }
    }
}

function toggleDispUnderExp() {
    const dispUnderExpElm = document.getElementById("disp_under_exp");
    const musics = document.getElementsByClassName("items");
    for (let i = 0; i < musics.length; i++) {
        if (musics[i].getElementsByTagName("div")[0].className === "levconst") continue;
        const imgClass = musics[i].getElementsByTagName("img")[0]
        if (imgClass.className !== "mas" && imgClass.className !== "ult" && imgClass.className !== "lun") {
            if (dispUnderExpElm.checked) {
                musics[i].style.display = "block";
            } else {
                musics[i].style.display = "none";
            }
        }
    }

    const blocks = document.getElementsByClassName("levblock");
    if (dispUnderExpElm.checked) {
        for (let i = 0; i < blocks.length; i++) {
            blocks[i].style.display = "flex";
        }
    } else {
        for (let i = 0; i < blocks.length; i++) {
            const items = blocks[i].getElementsByClassName("items");
            let exists = false;
            for (let j = 1; j < items.length; j++) {
                if (items[j].style.display !== "none") {
                    exists = true;
                    break;
                }
            }
            if (!exists) blocks[i].style.display = "none";
        }
    }
}

function init(fn, elementID) {
    fn()
    const element = document.getElementById(elementID);
    element.addEventListener("change", fn);
}

document.addEventListener("DOMContentLoaded", function () {
    init(setTableWidth, "table_width");
    init(toggleDispTitle, "disp_title");
    init(toggleDispUnderExp, "disp_under_exp");
});