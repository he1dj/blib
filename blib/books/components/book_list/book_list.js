document.addEventListener("htmx:beforeSwap", (event) => {
    if (event.detail.target.id === "book-list") {
    window.scrollTo({ top: 0, behavior: "smooth" });
    }
});
