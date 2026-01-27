function enviar() {
    const url = document.getElementById("url").value;
    const resultado = document.getElementById("resultado");

    resultado.textContent = "Baixando, aguarde...";

    fetch("http://127.0.0.1:5000/download", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            const link = `http://127.0.0.1:5000/file/${data.file}`;
            resultado.innerHTML = `<a href="${link}">Clique para baixar o vídeo</a>`;
        } else {
            resultado.textContent = "Erro: " + data.message;
        }
    })
    .catch(() => {
        resultado.textContent = "Erro na requisição";
    });
}
