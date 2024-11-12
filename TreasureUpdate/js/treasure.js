let data = null;
async function getData() {
  data = await fetch("data.txt").then((res) => res.text());
}
getData();
setTimeout(() => {
  let  text = data.split("-");
  let arr1 = text[0].split(",");
  let arr2 = text[1].split(",");
  let arr3 = text[2].split(",");
  // 模拟宝藏地图API
  window.TreasureMap = class {
    static getInitialClue(type) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(
            `在${arr1[type]}找到了第一个线索...`
          );
        }, 1000);
      });
    }

    static decodeAncientScript(clue, type) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          if (!clue) {
            reject("没有线索可以解码!");
          }
          resolve(
            `解码成功!宝藏在${
              arr2[type]
            }中...`
          );
        }, 1500);
      });
    }

    static searchTemple(type) {
      return new Promise((resolve, reject) => {
        setTimeout(() => {
          const random = Math.random();
          if (random < 0.5) {
            reject(
              `糟糕!遇到了${arr3[type]}!`
            );
          }
          resolve("找到了一个神秘的箱子...");
        }, 2000);
      });
    }

    static openTreasureBox() {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve("恭喜!你找到了传说中的宝藏!");
        }, 1000);
      });
    }
  }
}, 500);

