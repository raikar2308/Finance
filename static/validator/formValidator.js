import Validator from "./validator.js";
import ApiValidator from "./apiValidator.js";
import debounce from "./debounce.js";
import Messages from "./messages.js";

const FormValidator = {

    form: null,
    config: {},
    state: {},

    init(form, config) {
        this.form = form;
        this.config = config;
        this.state = {};
        this.initRealtime();
    },

    initRealtime() {
        Object.keys(this.config).forEach(field => {
            const input = this.form.querySelector(`[name="${field}"]`);
            if (!input) return;

            const rules = this.config[field];

            input.addEventListener(
                "input",
                debounce(() => this.validateField(input, rules), 300)
            );
        });
    },

    async validateField(input, rules) {

        if (!input) return false;

        const value = (input.value ?? "").toString().trim();
        input._lastValidatedValue = value;

        let errors = Validator.validate(value, rules.rules);

        if (!errors.length && rules.rules) {
            const asyncErrors = await this.runAsyncValidators(value, rules.rules);


            if (input._lastValidatedValue !== value) return false;

            errors = [...errors, ...asyncErrors];
        }

        this.state[input.name] = {
            value,
            valid: !errors.length,
            errors
        };

        this.showError(input, errors);

        return !errors.length;
    },

    async runAsyncValidators(value, rules) {

        const errors = [];

        for (const rule of rules) {

            if (rule.async === "emailAvailable") {


    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
        return [];
    }

    if (window.originalEmail && value === window.originalEmail) {
        return [];
    }

    const { available, error } =
        await ApiValidator.isEmailAvailable(value) || {};

    if (error) errors.push(Messages.apiError);
    else if (!available) errors.push("Email already exists");
}
        }

        return errors;
    },

    showError(input, errors) {
        const el = document.getElementById(input.getAttribute("data-error"));
        if (el) el.innerText = errors[0] || "";
    }
};

export default FormValidator;