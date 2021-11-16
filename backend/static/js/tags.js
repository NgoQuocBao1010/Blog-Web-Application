// const urlSearchParams = new URLSearchParams(window.location.search);
// const params = Object.fromEntries(urlSearchParams.entries());

const tagsContainer = document.getElementById("tags");
const tags = tagsContainer.querySelectorAll(".tag");

// Reload page when click delete icon of a tag
tags.forEach((tag) => {
    const delIcon = tag.querySelector("i");
    delIcon.addEventListener("click", () => {
        history.pushState({}, null, location.href.split("?")[0]);
        location.reload();
    });
});
