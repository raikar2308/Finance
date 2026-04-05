const AlertBox = {

    show(message, type = "info") {
        const container = document.getElementById("alert-container");

        if (!container) return;

        container.innerHTML = `
            <div class="alert alert-${type}">
                ${message}
            </div>
        `;
    },

    clear() {
        const container = document.getElementById("alert-container");
        if (container) container.innerHTML = "";
    }
};

export default AlertBox;