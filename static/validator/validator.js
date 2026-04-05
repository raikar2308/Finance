import { Rules, isEmpty, toSafeString } from "./rules.js";
import Messages from "./messages.js";

const MAX_INPUT_LENGTH = 1000;

const Validator = {

    validate(value, ruleSet = []) {

        const errors = [];
        const normalized = toSafeString(value);


        if (normalized.length > MAX_INPUT_LENGTH) return ["Input too long"];

        for (const { type, value: ruleValue } of ruleSet) {

            const ruleFn = Rules[type];

            if (!ruleFn) {
                console.warn(`Invalid rule: ${type}`);
                continue;
            }

            // Required first (fail fast)
            if (type === "required" && isEmpty(normalized)) {
                errors.push(Messages.required);
                return errors;
            }

            // Skip other rules if empty
            if (isEmpty(normalized)) continue;

            if (!ruleFn(normalized, ruleValue)) {
                errors.push(
                    typeof Messages[type] === "function"
                        ? Messages[type](ruleValue)
                        : Messages[type] || Messages.generic
                );
            }
        }

        return errors;
    }
};

export default Object.freeze(Validator);