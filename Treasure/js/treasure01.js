// 模拟宝藏地图API
class TreasureMap {
  static getInitialClue(type) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(`在${['森林入口','神庙入口', '洞穴入口'][type]}找到了第一个线索...`);
      }, 1000);
    });
  }

  static decodeAncientScript(clue, type) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (!clue) {
          reject("没有线索可以解码!");
        }
        resolve(`解码成功!宝藏在${['森林东方的沼泽里','神庙的深处', '洞穴深处'][type]}中...`);
      }, 1500);
    });
  }

  static searchTemple(type) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const random = Math.random();
        if (random < 0.5) {
          reject(`糟糕!遇到了${['森林树精','神庙守卫', '洞穴大蜘蛛'][type]}!`);
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

async function findTreasureWithPromises(type, dom, btnBox) {
  try {
    let clue = await TreasureMap.getInitialClue(type)
    dom.innerHTML += `<div>${clue}</div>`;
    let location = await TreasureMap.decodeAncientScript(clue, type);
    dom.innerHTML += `<div>${location}</div>`;
    let box = await TreasureMap.searchTemple(location, type);
    dom.innerHTML += `<div>${box}</div>`;
    let treasure = await TreasureMap.openTreasureBox();
    dom.innerHTML += `<div>${treasure}</div>`;
    btnBox.style.display = 'flex';
  } catch (error) {
    dom.innerHTML += `<div>${error}</div>`;
    btnBox.style.display = 'flex';
  }
}
