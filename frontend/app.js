async function generateDockerfile() {

    const language = document.getElementById("language").value;

    const response = await fetch("http://localhost:5000/generate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            language: language
        })

    });

    const data = await response.json();

    document.getElementById("output").textContent = data.dockerfile;

}