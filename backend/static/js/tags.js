const urlSearchParams = new URLSearchParams(window.location.search);
const params = Object.fromEntries(urlSearchParams.entries());

const tagsContainer = document.getElementById("tags");
const tags = tagsContainer.querySelectorAll(".tag");

// Reload page when click delete icon of a tag
tags.forEach((tag) => {
    const delIcon = tag.querySelector("i");
    const queryField = tag.getAttribute("data-query");

    delIcon.addEventListener("click", () => {
        urlSearchParams.delete(queryField);
        window.location.search = urlSearchParams;
    });
});
