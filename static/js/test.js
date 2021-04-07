let card = document.querySelector(".card");
let count = document.querySelector(".count");
let avatarPic = document.getElementById("avatar");
let cir = 2 * Math.PI * 10;

let data = {
  "design": document.getElementById("design-score").innerHTML,
  "usability" : document.getElementById("usability-score").innerHTML,
  "contentScore": document.getElementById("content-score").innerHTML,
}
function populateCard(data) {

  for(let item in data) {
    if(item === "design" || item === "usability" || item === "contentScore") {
      createCircle(item, data[item], card.querySelector(`.${item}`));
    }

    else if(card.querySelector(`.${item}`) !== null) {
      let current = card.querySelector(`.${item}`);
      current.innerHTML = data[item];
    } 
  }
}

function createCircle(content, val, parent) {
  let div = document.createElement("div");
  let p = document.createElement("p");
  let title = document.createElement("div");
  let frag = document.createDocumentFragment();
  let markup = `<svg viewBox="0 0 40 30" xmlns="http://www.w3.org/2000/svg">
<linearGradient id="gradient" x1="0" y1="1" x2="1" y2="0">
<stop offset="6%" stop-color="#FFE53B" stop-opacity="0.5"></stop>
<stop offset="100%" stop-color="#FF2525"></stop>
</linearGradient>
<circle class="inner-circle"></circle>
<circle class="outer-circle circle-${content}" id="circle" stroke="url(#gradient)" stroke-dashoffset=${cir}></circle>
</svg>`;
  div.innerHTML = markup;
  div.className = "svg-wrapper";
  p.innerHTML = val;
  title.innerHTML = content;
  parent.innerHTML = markup;
  frag.appendChild(p);
  frag.appendChild(title);
  parent.appendChild(frag);
}

let circles = ["design" ,"usability", "contentScore"];

function animateStrokes() {
  circles.forEach((circle) => {
    console.log(data[circle]);
    let val = data[circle];
    val = ( val * 100)/ 5
    // if(val < 100) {
    //   val = val / 200;
    // }
    let current = document.querySelector(`.circle-${circle}`);
    current.setAttribute("stroke-dashoffset", val);
  })
}

function init() {
  populateCard(data);
  setTimeout(() => {
    animateStrokes()
  }, 1000);
}

init();