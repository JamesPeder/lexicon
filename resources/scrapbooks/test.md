<textarea id="md" rows="6"># Hello Markdown</textarea>
<div id="preview"></div>

<script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
<script>
const md = document.getElementById("md");
const preview = document.getElementById("preview");

md.addEventListener("input", () => {
    preview.innerHTML = marked(md.value);
});
</script>
