const Toast = {

    show(message, type = "info") {

        const container = document.getElementById("toast-container") || this.createContainer();

        const toast = document.createElement("div");
        toast.className = `toast toast-${type}`;
        toast.innerText = message;

        container.appendChild(toast);

        setTimeout(() => {
            toast.classList.add("show");
        }, 100);

        setTimeout(() => {
            toast.classList.remove("show");
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    },

    createContainer() {
        const container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
        return container;
    }
};

export default Toast;