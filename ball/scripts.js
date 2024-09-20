//主题烟花
class Fire{
    //构造函数
    constructor(pos){
        this.cont = document.getElementById("container");
        this.x = pos.x;
        this.y = pos.y;
    }

    //创建主题烟花
    create(){
        this.f = document.createElement("div");
        this.f.className = "fire";
        this.f.style.background = randomColor();
        this.cont.appendChild(this.f);
        this.f.style.left = this.x + "px";
        this.fireMove();
    }

    //让主题烟花随机上升到任意的高度
    fireMove(){
        move2(this.f,{
            top:this.y,
        },()=>{
            this.f.remove();
            var randomNum = random(10,20);
            for(var i = 0;i<randomNum;i++){
                var sf = new smallFire({
                    cont:this.cont,
                    x:this.x,
                    y:this.y
                })
                sf.create();
            }
        })
    }
}

//小烟花
class smallFire{
    constructor(obj){
        this.cont = obj.cont;
        this.x = obj.x;
        this.y = obj.y;
    }
    create(){
        this.f = document.createElement("div");
        this.f.className = "small-fire";
        this.f.style.background = randomColor();
        this.cont.appendChild(this.f);
        this.f.style.left = this.x + "px";
        this.f.style.top = this.y + "px";
        this.smallMove();
    }
    smallMove(){
        var speedX = random(-10,10);
        var speedY = random(-20,0);
        this.f.t = setInterval(() => {
            if(this.f.offsetTop > this.cont.offsetHeight){
                clearInterval(this.f.t);
                this.f.remove();
            }else{
                this.f.style.left = this.f.offsetLeft + speedX + "px";
                this.f.style.top = this.f.offsetTop + speedY++ + "px";
            }
        }, 30);
    }
}

//	随机数封装函数	
function random(min, max) {
    return Math.round(Math.random()*(max - min)+min);
}	

//	随机颜色值封装函数	
function randomColor(){
    return `rgb(${random(0,255)},${random(0,255)},${random(0,255)})`;
}

//	运动过程封装函数
function move2(ele,obj,cb){
    clearInterval(ele.t);
    ele.t = setInterval(() => {
        var i = true;
        for(var attr in obj){
            if(attr == "opacity"){
                var iNow = getStyle(ele,attr) * 100;
            }else{
                var iNow = parseInt(getStyle(ele,attr));
            }
            let speed = (obj[attr] - iNow)/10;
            speed = speed < 0 ? Math.floor(speed) : Math.ceil(speed);
            if(iNow !== obj[attr]){
                i = false;
            }
            if(attr == "opacity"){
                ele.style.opacity = (iNow + speed)/100;
            }else{
                ele.style[attr] = iNow + speed + "px";
            }
        }
        if(i){
            clearInterval(ele.t);
            if(cb){
                cb();
            }
        }
    }, 30);
}

//获取样式封装函数
function getStyle(ele,attr){
    if(ele.currentStyle){
        return ele.currentStyle[attr];
    }else{
        return getComputedStyle(ele,false)[attr];
    }
}

// 自动生成烟花的函数
function generateFireworks(){
    var x = random(0, container.clientWidth);
    var y = random(0, container.clientHeight);
    var firework = new Fire({x: x, y: y});
    firework.create();
}

// 设置定时器，每隔一段时间生成烟花
var container = document.getElementById("container");
setInterval(generateFireworks, 1000); // 每隔1秒生成一个烟花
