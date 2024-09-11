

window.addEventListener("DOMContentLoaded", function () {  
    var wrapper = document.querySelector(".wrapper");
    var prev = document.querySelector(".prev");
    var next = document.querySelector(".next");
    var img_wrapper = document.querySelector(".img_wrapper");
    var circle = document.querySelector(".circle");
    //flag是用来判断上一个动画是否已经完成，完成才能进行下一个动画（这里的动画指图片左右滑动的动画）
    var flag = true;  
    var num = 0;  //num用于判断是第几张图片
    var timerA = setInterval(() => {  //这个定时器实现自动播放下一张图片的效果
      next.click();  //自动播放下一张不是直接改变这个盒子的位移，而是通过点击next按钮
    }, 1500);
    
    //利用for循环生成circle
    for (var i = 0; i < img_wrapper.children.length; i++) {
      var li = document.createElement("li");
      circle.appendChild(li);
      //使用setAttribute给小圆圈添加index这个自定义属性，并且赋值，以便后续通过index获取当前是第几张图片
      li.setAttribute("index", i);
      li.addEventListener("click", function () {
        for (let j = 0; j < circle.children.length; j++) {
          circle.children[j].className = "";
        }
        this.className = "current";  //每次点击小圆圈则该小圆圈变成白色，其余颜色变为透明（排他思想）
        
        num = this.getAttribute("index");
        animate(  //实现点击小圆圈也可以切换图片
          img_wrapper,
          -img_wrapper.parentElement.offsetWidth * this.getAttribute("index")
        );
      });
    }
    
  //由于播放到最后一张图片后再点击下一张图片动画会返回第一张，并且画面非常不好看，要实现无缝切换图片即需将第一张图片复制放到最后面。由于添加小圆圈的代码是在复制第一张图片之前执行的，因此小圆圈的数量不会受影响。
  
    var firstImg = img_wrapper.children[0].cloneNode(true);//创建节点
    img_wrapper.appendChild(firstImg);//添加节点
    var circleLis = circle.querySelectorAll("li");//将所有小圆圈添加到数组里
    circleLis[0].className = "current";//默认第一个小圆圈为当前状态
    
    //由于在css中left是50%，因此不是居中的状态，当我们把圆圈添加后获取整个盒子的长度，使marginLeft等于负的盒子的一半即可实现居中效果
    circle.style.marginLeft = -(circle.offsetWidth / 2) + "px";
  
  //当我们鼠标不在图片的盒子中时，不显示切换图片的两个按钮，这里实现鼠标在盒子上方时按钮显示，并且暂停自动播放图片的功能
    wrapper.addEventListener("mouseenter", function () {
      prev.style.display = "block";
      next.style.display = "block";
      clearInterval(timerA);  //清除定时器，暂停自动播放的功能
      timerA = null;
    });
    
    //鼠标离开盒子上方，按钮隐藏，开始自动播放的功能
    wrapper.addEventListener("mouseleave", function () {
      prev.style.display = "none";
      next.style.display = "none"; 
      timerA = setInterval(() => {  //添加定时器，开始自动播放的功能
        next.click();
      }, 1500);
    });
  
    next.addEventListener("click", function () {
      if (flag) {  //flag判断是否上一个动画已完成
        flag = false;//当开始这一次的动画（切换图片）时，使flag为false，这样再点击按钮就不会开始下一个动画
        //判断是否是最后一张图片，最后一张图片与第一张图片一样，如果已经是最后一张图片了，使图片盒子的left值立即回到0，即初始位置，这样在切换下一张图片时就会切换到第二张图片
        if (num == img_wrapper.children.length - 1) {
          img_wrapper.style.left = 0 + "px";
          num = 0;
        }
        num++;
  
        animate(
          img_wrapper,
          -num * img_wrapper.parentElement.offsetWidth,
          function () {
            flag = true;
          }
          
          //动画结束，使flag=true
        );
          //这里改变小圆圈的背景颜色，使小圆圈的背景颜色随着图片的切换而改变
        for (let i = 0; i < circleLis.length; i++) {
          circleLis[i].className = "";
  
          if (num == img_wrapper.children.length - 1) {  
          //当图片是最后一张时，第一个小圆圈改变背景颜色
            circleLis[0].className = "current";
          } else {
            circleLis[num].className = "current";
          }
        }
      }
    });
  //上一张图片的按钮代码与下一张的相似
    prev.addEventListener("click", function () {
      if (flag) {
        if (num == 0) {
          num = img_wrapper.children.length - 1;
          img_wrapper.style.left =
            -num * img_wrapper.parentElement.offsetWidth + "px";
        }
        num--;
        animate(
          img_wrapper,
          -num * img_wrapper.parentElement.offsetWidth,
          function () {
            flag = true;
          }
        );
  
        for (let i = 0; i < circleLis.length; i++) {
          circleLis[i].className = "";
          circleLis[num].className = "current";
        }
      }
    });
  //切换图片的动画
  //obj:目标盒子，target：需要移动的距离
    function animate(obj, target, callback) {
      clearInterval(obj.timer);//首先先清除定时器，防止过多定时器的叠加
      
      obj.timer = setInterval(() => {
        if (obj.offsetLeft == target) {//当目标盒子的left值等于目标距离时清除定时器
          clearInterval(obj.timer);
          // if (callback) {
          //   callback();
          // }相当于：
          callback && callback();
        } else {
          obj.step = (target - obj.offsetLeft) / 10;  //这行代码可以实现变速的移动，不懂的自己代入数值计算
          if (obj.step >= 0) {
            obj.step = Math.ceil(obj.step);
          } else {
            obj.step = Math.floor(obj.step);
          }
  
          obj.style.left = obj.offsetLeft + obj.step + "px";
        }
      }, 15);
    }
  });