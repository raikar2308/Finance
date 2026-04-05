const Messages = Object.freeze({
    required: "This field is required",
    email: "Invalid email format",
    phone: "Invalid phone number",
    pincode: "Invalid pincode",
    password: "Password must be strong",
    number: "Only numbers allowed",
    minLength: (len) => `Minimum ${len} characters required`,
    maxLength: (len) => `Maximum ${len} characters allowed`,
    generic: "Invalid value",
    apiError: "Validation failed. Please try again."
});

export default Messages;