
let like = document.querySelectorAll(".like-btn");
let likeCount  = document.querySelectorAll("#count");
let count = 0;



like.forEach((btn) => {
  btn.addEventListener("click", () => {
    if (btn.style.color === "rgb(254, 79, 112)") {
      btn.style.color = "";
      count--;
      likeCount.innerText = count;
    } else {
      btn.style.color = "#fe4f70";
      count++;
      likeCount.innerText = count;
    }
  });
});

let logIn = document.querySelector("#log-in");
logIn.addEventListener("click", ()=>{
  logIn.innerText= "Log in";
});


let editBtn = document.querySelector("#edit");
editBtn.addEventListener("click", ()=>{
   window.location.href = "/onboarding/";
})
