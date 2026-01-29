function extrairVideoID(url) {
    const regex = /(?:v=|\/)([0-9A-Za-z_-]{11})/;
    const match = url.match(regex);
    return match ? match[1] : null;
}

function abrir() {
    const url = document.getElementById("url").value;
    const player = document.getElementById("player");

    const videoId = extrairVideoID(url);

    if (!videoId) {
        player.innerHTML = "Link inválido";
        return;
    }

    player.innerHTML = `
        <iframe width="560" height="315"
        src="https://www.youtube.com/embed/${videoId}"
        frameborder="0"
        allowfullscreen></iframe>
    `;
}
