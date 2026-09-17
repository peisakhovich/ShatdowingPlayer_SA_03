function renderMermaid() {
    const blocks = document.querySelectorAll("pre code.language-mermaid");

    blocks.forEach(function (block) {
        const container = document.createElement("div");

        container.className = "mermaid";
        container.textContent = block.textContent;

        block.parentElement.replaceWith(container);
    });

    mermaid.initialize({
        startOnLoad: false,

        theme: "default",

        themeVariables: {
            fontSize: "18px"
        },

        flowchart: {
            useMaxWidth: true,
            wrappingWidth: 180,
            nodeSpacing: 35,
            rankSpacing: 55,
            padding: 15
        }
    });

    mermaid.run();
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderMermaid);
} else {
    renderMermaid();
}