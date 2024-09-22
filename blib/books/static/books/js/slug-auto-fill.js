document.addEventListener("DOMContentLoaded", function() {
    if (typeof slugify !== "undefined") {
        const titleField = document.querySelector('input[name="title"]');
        const slugField = document.querySelector('input[name="slug"]');

        if (titleField && slugField) {
            titleField.addEventListener("input", function() {
                const slugified = slugify(titleField.value, { lower: true });
                slugField.value = slugified;
            });
        }
    } else {
        console.error("Slugify is not loaded");
    }
});
