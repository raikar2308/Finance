import Toast from "./toast.js";
import AlertBox from "./alertBox.js";

const MessageService = {

    success(msg) {
        Toast.show(msg, "success");
    },

    error(msg) {
        Toast.show(msg, "error");
    },

    warning(msg) {
        Toast.show(msg, "warning");
    },

    info(msg) {
        Toast.show(msg, "info");
    },

    alert(msg, type = "info") {
        AlertBox.show(msg, type);
    }

};

export default MessageService;