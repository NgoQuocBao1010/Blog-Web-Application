let searchIcon = document.querySelector("#search-icon");
let searchForm = document.querySelector(".search-form");

searchIcon.onclick = () => {
    searchIcon.classList.toggle("fa-times");
    searchForm.classList.toggle("active");

    document.getElementById("search-box").focus(); // focus on input
};
