class Links {
    constructor(sources = []) {
        if (!Array.isArray(sources) || !sources.length) {
            this.sources = [];
            console.error('Object is not array type, or is empty!');
        } else {
            this.sources = sources
        }
    }

    #createLink(src, src_type = "") {
        const link = document.createElement('link');
        if (src_type !== "") {
            link.rel = src_type;
        }
        link.href = src;
        document.head.appendChild(link);
    }

    #getSource(value) {
        const src = {
            main  : 'static/css/main.css',
            index : 'static/css/index.css'
        }

        return src[value];
    }

    generate() {
        if (!Array.isArray(this.sources) || !this.sources.length) {
            console.error('Sources reference is null or empty');
        }

        document.addEventListener('DOMContentLoaded', () => {
            this.sources.forEach((source) => {
                this.#createLink(this.#getSource(source), "stylesheet");
            });
            
            // Non-css links
            this.#createLink("https://fonts.googleapis.com/css?family=Montserrat:700,400|Inter:700,400");
        });

        // Prevent FOUC
        window.onload = () => {
            document.documentElement.style.visibility = 'visible';
        }
    }
}