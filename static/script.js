document.addEventListener("DOMContentLoaded", function() {
	const nav = document.querySelector('.main-nav');
	const main = document.getElementById('main-content');

	function setActive(link) {
		document.querySelectorAll('.main-nav a').forEach(a => a.classList.remove('active'));
		if (link) link.classList.add('active');
	}

	async function loadPage(name, linkEl) {
		try {
			const res = await fetch(`/page/${name}`);
			if (!res.ok) throw new Error('Erro ao carregar página');
			const text = await res.text();

			// Se a resposta contém uma tag <main>, extrai seu conteúdo; senão usa o texto todo
			let content = text;
			try {
				const parser = new DOMParser();
				const doc = parser.parseFromString(text, 'text/html');
				const m = doc.querySelector('main');
				if (m) content = m.innerHTML;
			} catch (e) {
				// fallback: usar text
			}

			main.innerHTML = content;
			setActive(linkEl);
			window.scrollTo(0,0);
		} catch (err) {
			main.innerHTML = '<p>Não foi possível carregar a página.</p>';
			console.error(err);
		}
	}

	if (nav) {
		nav.addEventListener('click', function(e) {
			const a = e.target.closest('a[data-page]');
			if (!a) return;
			e.preventDefault();
			const page = a.dataset.page;
			loadPage(page, a);
		});
	}

	// opcional: carregar a página inicial via AJAX ao abrir
	const initial = document.querySelector('.main-nav a[data-page="index"]');
	if (initial) loadPage('index', initial);
});
