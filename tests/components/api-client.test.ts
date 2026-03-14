import { apiFetch, getFriendlyError } from "@/lib/api-client";

describe("api-client error handling", () => {
  const originalFetch = global.fetch;

  afterEach(() => {
    global.fetch = originalFetch;
    jest.restoreAllMocks();
  });

  it("maps network failures to user-friendly errors", async () => {
    global.fetch = jest.fn().mockRejectedValue(new TypeError("Failed to fetch")) as typeof fetch;

    await expect(apiFetch("/api/test")).rejects.toThrow(
      "Unable to connect to the server. Please check your internet connection."
    );
  });

  it("maps HTTP errors to user-friendly messages", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: false,
      status: 500,
      headers: new Headers(),
    }) as typeof fetch;

    await expect(apiFetch("/api/test")).rejects.toThrow(
      "The server encountered an error. Please try again later."
    );
  });

  it("rejects invalid non-JSON responses", async () => {
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      headers: new Headers({ "content-type": "text/plain" }),
      text: async () => "ok",
    }) as typeof fetch;

    await expect(apiFetch("/api/test")).rejects.toThrow(
      "Received an unexpected response from the server."
    );
  });

  it("prevents raw backend-like messages from leaking to UI", () => {
    const backendLikeError =
      "Traceback (most recent call last): RuntimeError: DB connection refused";

    const message = getFriendlyError(backendLikeError);

    expect(message).toBe("Something went wrong. Please try again.");
    expect(message).not.toContain("Traceback");
    expect(message).not.toContain("DB connection refused");
  });
});
