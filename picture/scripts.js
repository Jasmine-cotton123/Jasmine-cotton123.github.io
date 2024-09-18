document.getElementById("toggleButton").addEventListener("click", function() {
    var imgBox = document.querySelector(".img-box");
    imgBox.classList.toggle("show");
    this.classList.toggle("lighten"); // 切换按钮样式
    if (this.innerHTML === "Darken") {
        this.innerHTML = "Lighten"; // 切换按钮文本
    } else {
        this.innerHTML = "Darken";
    }
});

var imageBoxes = document.querySelectorAll(".img-box:not(.panda)");
imageBoxes.forEach(function(imageBox, index) {
    imageBox.addEventListener("click", function() {
        var selectedImageSrc = this.querySelector("img").src;
        document.getElementById("pandaImg").src = selectedImageSrc;
    });
});

document.getElementById("nextButton").addEventListener("click", function() {
    var currentImageSrc = document.getElementById("pandaImg").src;
    var nextIndex = (parseInt(currentImageSrc.charAt(currentImageSrc.length - 5)) % 4) + 1;
    var nextImageSrc = "熊猫" + nextIndex + ".jpg";
    document.getElementById("pandaImg").src = nextImageSrc;
});

document.getElementById("prevButton").addEventListener("click", function() { // 添加上一张按钮的点击事件监听器
    var currentImageSrc = document.getElementById("pandaImg").src;
    var currentIndex = parseInt(currentImageSrc.charAt(currentImageSrc.length - 5));
    var prevIndex = (currentIndex - 2 + 4) % 4 + 1; // 计算上一张图片的索引，确保索引始终大于等于1
    var prevImageSrc = "熊猫" + prevIndex + ".jpg"; // 根据索引生成上一张图片的src
    document.getElementById("pandaImg").src = prevImageSrc; // 设置上一张图片的src
});
