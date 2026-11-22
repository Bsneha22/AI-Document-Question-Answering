
const fileInput = document.getElementById("fileInput");

const dropArea = document.getElementById("dropArea");

const fileName = document.getElementById("fileName");


dropArea.addEventListener("click", function() {
    fileInput.click();
});


fileInput.addEventListener("change", function() {

    if (fileInput.files.length > 0) {

        fileName.textContent =
            "Selected: " + fileInput.files[0].name;

    }

});


dropArea.addEventListener("dragover", function(event) {

    event.preventDefault();

    dropArea.classList.add("dragover");

});


dropArea.addEventListener("dragleave", function() {

    dropArea.classList.remove("dragover");

});


dropArea.addEventListener("drop", function(event) {

    event.preventDefault();

    dropArea.classList.remove("dragover");

    const files = event.dataTransfer.files;

    if (files.length > 0) {

        const file = files[0];

        const allowed =
            file.name.toLowerCase().endsWith(".pdf") ||
            file.name.toLowerCase().endsWith(".txt");

        if (!allowed) {

            fileName.textContent =
                "Please select a PDF or TXT file.";

            return;

        }

        fileInput.files = files;

        fileName.textContent =
            "Selected: " + file.name;

    }

});
