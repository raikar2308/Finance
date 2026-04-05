import Messages from "./messages.js";

const ApiValidator = {

    cache: new Map(),

    async request(url) {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 5000);

        try {
            const res = await fetch(url, { signal: controller.signal });
            if (!res.ok) throw new Error("API error");
            return await res.json();
        } catch (err) {
            console.error("API validation error:", err);
            return null;
        } finally {
            clearTimeout(timeout);
        }
    },

    async isEmailAvailable(email) {

        if (this.cache.has(email)) return this.cache.get(email);

        const data = await this.request(
            `/admin/users/api/check-email?email=${encodeURIComponent(email)}`
        );

        if (!data) return { error: true };

        const result = { available: data?.available ?? false };

        if (this.cache.size > 500) this.cache.clear();

        this.cache.set(email, result);

        return result;
    }
};

export default Object.freeze(ApiValidator);