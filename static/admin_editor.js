// Inicializa Quill com toolbar personalizada e trata upload de imagens
(function(){
    if (typeof Quill === 'undefined') {
        console.warn('Quill não encontrado. Verifique se o CDN foi incluído.');
        return;
    }

    var toolbarOptions = [
        ['bold', 'italic', 'underline'],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        ['image']
    ];

    var editorEl = document.getElementById('editor');
    if (!editorEl) return; // se não estiver em uma página admin

    var quill = new Quill('#editor', {
        theme: 'snow',
        modules: {
            toolbar: toolbarOptions
        }
    });

    // Se vier conteúdo inicial (em edit), carregar no editor
    if (typeof initialContent !== 'undefined' && initialContent) {
        quill.root.innerHTML = initialContent;
    }

    // Handler customizado para upload de imagens
    var toolbar = quill.getModule('toolbar');
    toolbar.addHandler('image', function() {
        var input = document.createElement('input');
        input.setAttribute('type', 'file');
        input.setAttribute('accept', 'image/*');
        input.onchange = function() {
            var file = input.files[0];
            if (/^image\//.test(file.type)) {
                uploadImage(file);
            } else {
                alert('Arquivo precisa ser uma imagem.');
            }
        };
        input.click();
    });

    function uploadImage(file) {
        var fd = new FormData();
        fd.append('image', file);

        fetch('/admin/upload_image', {
            method: 'POST',
            body: fd
        }).then(function(res){
            return res.json();
        }).then(function(data){
            if (data && data.url) {
                var range = quill.getSelection(true);
                quill.insertEmbed(range.index, 'image', data.url);
            } else {
                alert('Erro no upload da imagem.');
            }
        }).catch(function(err){
            console.error(err);
            alert('Erro no upload da imagem.');
        });
    }

    // Antes do submit, colocar o HTML do editor no campo hidden 'content'
    var form = editorEl.closest('form');
    if (form) {
        form.addEventListener('submit', function(e){
            var hidden = document.getElementById('content');
            if (hidden) {
                // manter quebras e HTML gerado pelo Quill
                hidden.value = quill.root.innerHTML;
            }
        });
    }
})();
