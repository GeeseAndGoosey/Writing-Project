document.addEventListener("DOMContentLoaded", function() {
    if (typeof Quill === "undefined") {
        console.error("Quill is not loaded yet!");
        return;
    }

    const quill = new Quill('#editor', {
        theme: 'snow',
        placeholder: 'Start typing here...'
    });

    const wordCountDisplay = document.getElementById('wordCount');
    function countWords(text) {
        return text.trim().split(/\s+/).filter(Boolean).length;
    }

    quill.on('text-change', () => {
        const text = quill.getText();
        wordCountDisplay.textContent = countWords(text);
    });
});