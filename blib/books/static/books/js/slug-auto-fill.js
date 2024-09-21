document.addEventListener("DOMContentLoaded", function() {
    const titleField = document.querySelector('input[name="title"]');
    const slugField = document.querySelector('input[name="slug"]');

    if (titleField && slugField) {
        titleField.addEventListener("input", function() {
            const slugified = slugify(titleField.value, { lower: true });
            slugField.value = slugified;
        });
    }
});
console.log("Script is loaded")
