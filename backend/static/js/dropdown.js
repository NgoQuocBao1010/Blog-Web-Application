let searchIcon = document.querySelector("#search-icon");
let searchForm = document.querySelector(".search-form");

searchIcon.onclick = () => {
    searchIcon.classList.toggle("fa-times");
    searchForm.classList.toggle("active");

    document.getElementById("search-box").focus(); // focus on input
};

searchForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const searchVal = document.getElementById("search-box").value;

    const urlSearchParams = new URLSearchParams(window.location.search);
    urlSearchParams.set("search", searchVal);
    window.location.search = urlSearchParams;
});
