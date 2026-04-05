const REGEX = Object.freeze({
    email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    phone: /^[6-9]\d{9}$/,
    pincode: /^[1-9][0-9]{5}$/,
    password: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/,
    number: /^[0-9]+(\.[0-9]+)?$/
});

const isEmpty = (v) =>
    v === null ||
    v === undefined ||
    (typeof v === "string" && v.trim() === '');

const toSafeString = (v) =>
    typeof v === "string" ? v.trim() : String(v ?? '');

// 🔹 Helper to ensure string-based validation safely
const isValidString = (v) => typeof v === "string";

const Rules = Object.freeze({

    required: (v) => !isEmpty(v),

    minLength: (v, len) =>
        isValidString(v) && v.length >= len,

    maxLength: (v, len) =>
        isValidString(v) && v.length <= len,

    email: (v) =>
        isValidString(v) && REGEX.email.test(v),

    phone: (v) =>
        isValidString(v) && REGEX.phone.test(v),

    pincode: (v) =>
        isValidString(v) && REGEX.pincode.test(v),

    password: (v) =>
        isValidString(v) && REGEX.password.test(v),

    number: (v) =>
        isValidString(v) && REGEX.number.test(v)
});

export { Rules, isEmpty, toSafeString };