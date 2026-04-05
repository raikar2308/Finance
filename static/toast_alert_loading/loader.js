const Loader = {

    show() {
        let loader = document.getElementById("global-loader");

        if (!loader) {
            loader = document.createElement("div");
            loader.id = "global-loader";
            loader.innerHTML = `<div class="spinner"></div>`;
            document.body.appendChild(loader);
        }

        loader.style.display = "flex";
    },

    hide() {
        const loader = document.getElementById("global-loader");
        if (loader) loader.style.display = "none";
    }
};

export default Loader;