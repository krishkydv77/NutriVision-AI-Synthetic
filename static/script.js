document.addEventListener("DOMContentLoaded", () => {
    const dropZone = document.getElementById("dropZone");
    const imageInput = document.getElementById("imageInput");
    const imagePreview = document.getElementById("imagePreview");
    const dropZoneText = dropZone.querySelector(".drop-zone-text");
    const uploadForm = document.getElementById("uploadForm");

    const loader = document.getElementById("loader");
    const results = document.getElementById("results");
    const placeholderText = document.getElementById("placeholderText");

    // Click to select file
    dropZone.addEventListener("click", () => imageInput.click());

    // File change preview
    imageInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreview.classList.remove("hidden");
                dropZoneText.classList.add("hidden");
            };
            reader.readAsDataURL(file);
        }
    });

    // Handle Form Submit
    uploadForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (!imageInput.files[0]) {
            alert("Please select an image first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", imageInput.files[0]);

        // UI States
        placeholderText.classList.add("hidden");
        results.classList.add("hidden");
        loader.classList.remove("hidden");

        try {
            const response = await fetch("/api/predict", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                document.getElementById("foodName").innerText = data.food;
                document.getElementById("confidence").innerText = `${data.confidence}% Match`;
                document.getElementById("healthScore").innerText = `${data.health_score} / 10`;
                
                document.getElementById("calories").innerText = `${data.nutrition.calories} kcal`;
                document.getElementById("protein").innerText = `${data.nutrition.protein} g`;
                document.getElementById("carbs").innerText = `${data.nutrition.carbs} g`;
                document.getElementById("fat").innerText = `${data.nutrition.fat} g`;

                loader.classList.add("hidden");
                results.classList.remove("hidden");
            } else {
                alert("Error: " + data.detail);
                loader.classList.add("hidden");
                placeholderText.classList.remove("hidden");
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred while connecting to server.");
            loader.classList.add("hidden");
            placeholderText.classList.remove("hidden");
        }
    });
});