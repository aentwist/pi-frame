import upload from "./upload.js";

const fileInput = document.getElementById("fileInput");
const fileSelect = document.getElementById("fileSelect");
const fileSubmit = document.getElementById("fileSubmit");
const uploadStatus = document.getElementById("uploadStatus");

fileSelect.addEventListener("click", () => {
    if (fileInput) fileInput.click();
});
// fileInput.addEventListener("change", validate);
fileSubmit.addEventListener("click", () => {
    const statuses = [];
    (async () => {
        for (const file of fileInput.files) {
            uploadStatus.innerText = "Uploading " + file.name + "...";
            const response = await upload(file, fileInput.name, fileSubmit.href);
            const json = await response.json();
            statuses.push(response.status);
            if (!response.ok) alert("File " + file.name + ": " + json.message);
        }
    })().then(() => {
        if (statuses.some(status => status === 200)) location.reload();
    });
});
