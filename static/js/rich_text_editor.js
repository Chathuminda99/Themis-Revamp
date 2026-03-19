(function () {
    const TOOLBAR_BUTTONS = [
        { command: "bold", icon: "format_bold", label: "Bold" },
        { command: "italic", icon: "format_italic", label: "Italic" },
        { command: "underline", icon: "format_underlined", label: "Underline" },
        { command: "unorderedList", icon: "format_list_bulleted", label: "Bullet List" },
        { command: "orderedList", icon: "format_list_numbered", label: "Numbered List" },
        { command: "clear", icon: "format_clear", label: "Clear Formatting" },
    ];

    function escapeHtml(value) {
        return value
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function looksLikeHtml(value) {
        return /<\/?[a-z][\s\S]*>/i.test(value);
    }

    function plainTextToHtml(value) {
        const normalized = (value || "").replace(/\r\n/g, "\n").replace(/\r/g, "\n").trim();
        if (!normalized) {
            return "";
        }

        return normalized
            .split(/\n\s*\n+/)
            .map((paragraph) => `<p>${paragraph.split("\n").map(escapeHtml).join("<br>")}</p>`)
            .join("");
    }

    function getInitialHtml(textarea) {
        const rawValue = textarea.value || "";
        if (!rawValue.trim()) {
            return "";
        }
        return looksLikeHtml(rawValue) ? rawValue : plainTextToHtml(rawValue);
    }

    function normalizeEditorValue(editor) {
        const text = editor.textContent.replace(/\u00a0/g, " ").trim();
        if (!text) {
            return "";
        }

        let html = editor.innerHTML.trim();
        if (html === "<br>") {
            return "";
        }

        html = html.replace(/<div><br><\/div>/gi, "");
        html = html.replace(/(<br>\s*){3,}/gi, "<br><br>");
        return html.trim();
    }

    function syncEditor(textarea, editor) {
        const nextValue = normalizeEditorValue(editor);
        if (textarea.value === nextValue) {
            return;
        }
        textarea.value = nextValue;
        textarea.dispatchEvent(new Event("input", { bubbles: true }));
    }

    function executeCommand(command, editor, textarea) {
        editor.focus();

        if (command === "unorderedList") {
            document.execCommand("insertUnorderedList", false);
        } else if (command === "orderedList") {
            document.execCommand("insertOrderedList", false);
        } else if (command === "clear") {
            document.execCommand("removeFormat", false);
            document.execCommand("unlink", false);
        } else {
            document.execCommand(command, false);
        }

        syncEditor(textarea, editor);
    }

    function createToolbar(textarea, editor) {
        const toolbar = document.createElement("div");
        toolbar.className = "flex flex-wrap items-center gap-1 rounded-t-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/80 px-2 py-2";

        TOOLBAR_BUTTONS.forEach((buttonConfig) => {
            const button = document.createElement("button");
            button.type = "button";
            button.dataset.richTextCommand = buttonConfig.command;
            button.className = "inline-flex h-9 w-9 items-center justify-center rounded-lg text-slate-600 transition-colors hover:bg-white hover:text-primary focus:outline-none focus:ring-2 focus:ring-primary/30 dark:text-slate-300 dark:hover:bg-slate-800";
            button.title = buttonConfig.label;
            button.setAttribute("aria-label", buttonConfig.label);
            button.innerHTML = `<span class="material-symbols-outlined text-[18px]">${buttonConfig.icon}</span>`;
            button.addEventListener("click", function () {
                executeCommand(buttonConfig.command, editor, textarea);
            });
            toolbar.appendChild(button);
        });

        return toolbar;
    }

    function initializeRichText(textarea) {
        if (!(textarea instanceof HTMLTextAreaElement) || textarea.dataset.richTextInitialized === "true") {
            return;
        }

        textarea.dataset.richTextInitialized = "true";

        const wrapper = document.createElement("div");
        wrapper.className = "rich-text-editor space-y-0";

        const editor = document.createElement("div");
        editor.contentEditable = "true";
        editor.dataset.richTextSurface = "true";
        editor.dataset.placeholder = textarea.getAttribute("placeholder") || "";
        editor.className = "rich-text-surface rounded-b-xl border border-t-0 border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-3 text-sm text-slate-900 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-primary/30";
        editor.style.minHeight = textarea.dataset.richTextMinHeight || "11rem";
        editor.innerHTML = getInitialHtml(textarea);

        const toolbar = createToolbar(textarea, editor);
        wrapper.appendChild(toolbar);
        wrapper.appendChild(editor);
        textarea.insertAdjacentElement("afterend", wrapper);
        textarea.classList.add("hidden");

        editor.addEventListener("input", function () {
            syncEditor(textarea, editor);
        });
        editor.addEventListener("blur", function () {
            syncEditor(textarea, editor);
        });
        editor.addEventListener("paste", function (event) {
            event.preventDefault();
            const text = (event.clipboardData || window.clipboardData).getData("text/plain");
            document.execCommand("insertText", false, text);
        });

        syncEditor(textarea, editor);
    }

    function refreshRichTextEditor(textarea) {
        if (!(textarea instanceof HTMLTextAreaElement)) {
            return;
        }

        const editor = textarea.nextElementSibling?.querySelector("[data-rich-text-surface='true']");
        if (!(editor instanceof HTMLDivElement)) {
            return;
        }

        editor.innerHTML = getInitialHtml(textarea);
    }

    function syncEditorsInForm(form) {
        if (!(form instanceof HTMLFormElement)) {
            return;
        }

        form.querySelectorAll("textarea[data-rich-text='true']").forEach((textarea) => {
            const editor = textarea.nextElementSibling?.querySelector("[data-rich-text-surface='true']");
            if (editor instanceof HTMLDivElement) {
                syncEditor(textarea, editor);
            }
        });
    }

    function initRichTextEditors(root) {
        const scope = root instanceof Element || root instanceof Document ? root : document;
        scope.querySelectorAll("textarea[data-rich-text='true']").forEach((textarea) => {
            initializeRichText(textarea);
        });
    }

    function observeRichTextEditors() {
        if (window.__richTextObserverStarted || !document.body) {
            return;
        }

        window.__richTextObserverStarted = true;
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (!(node instanceof Element)) {
                        return;
                    }
                    if (node.matches("textarea[data-rich-text='true']")) {
                        initializeRichText(node);
                        return;
                    }
                    initRichTextEditors(node);
                });
            });
        });

        observer.observe(document.body, { childList: true, subtree: true });
    }

    document.addEventListener("DOMContentLoaded", function () {
        initRichTextEditors(document);
        observeRichTextEditors();
    });

    document.addEventListener("submit", function (event) {
        const form = event.target instanceof HTMLFormElement ? event.target : event.target?.closest("form");
        if (form) {
            syncEditorsInForm(form);
        }
    }, true);

    document.body.addEventListener("htmx:load", function (event) {
        initRichTextEditors(event.target);
    });

    document.body.addEventListener("htmx:afterSwap", function (event) {
        initRichTextEditors(event.target);
    });

    document.body.addEventListener("htmx:beforeRequest", function (event) {
        const form = event.detail?.elt?.closest("form");
        if (form) {
            syncEditorsInForm(form);
        }
    });

    window.initRichTextEditors = initRichTextEditors;
    window.refreshRichTextEditor = refreshRichTextEditor;
})();
