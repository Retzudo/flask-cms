(function () {
    tinymce.init({
        selector: '.edit-text',
        inline: true,
        plugins: 'save autosave',
        menubar: false,
        toolbar: 'save | undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | bullist numlist outdent indent blockquote',
        save_enablewhendirty: true,
        save_onsavecallback: function () {
            var fileName = $('.edit-text').data('filename');
            $.post('/update-text', {
                file_name: fileName,
                content: this.getContent()
            });
        }
    });
})();
