const modal = document.getElementById("create-project-modal");
const openBtn = document.getElementById("new-project-button");
const closeBtn = document.querySelector(".close");

openBtn.onclick = function(){
    modal.style.display = "block";
}

closeBtn.onclick = function(){
    modal.style.display = "none";
}

