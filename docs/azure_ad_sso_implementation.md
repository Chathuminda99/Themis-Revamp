# Azure AD SSO Implementation Notes

## The Core Problem: Login → Dashboard vs Direct → Dashboard

The "flicker" (callback → login page → dashboard) happens in other apps because the callback
route is intercepted by auth middleware before the session cookie is set. Here is how this
implementation avoids it.

---

## Why This Implementation Goes Directly to Dashboard

### 1. Auth Middleware Does NOT Guard the Callback Route

In `app/middleware/auth.py`, the middleware only **reads** the session cookie and injects
`request.state.user`. It never redirects — it just sets `user = None` if there is no valid session:

```python
# auth.py middleware
request.state.user = user        # None if no session — but does NOT redirect
return await call_next(request)  # always passes through
```

Route handlers are responsible for redirecting unauthenticated users. The callback route
`/auth/azure/callback` does not require an authenticated user, so the middleware does nothing.

**The anti-pattern in other apps:** Middleware that redirects to `/login` when no session
cookie exists will intercept the callback request (which has no session cookie yet), redirect
to login, and only after the login page loads does the cookie get set. Result: login flash.

---

### 2. The Session Cookie Is Set in the Same Response That Redirects to Dashboard

In `app/routes/auth.py`, the callback handler does both in one response:

```python
response = RedirectResponse(url="/dashboard", status_code=302)
response.set_cookie(key=settings.session_cookie_name, value=token, ...)
response.delete_cookie("az_oauth_state")
return response
```

The browser receives a single 302 with `Set-Cookie` + `Location: /dashboard`. It sets the
cookie and follows the redirect in one step — the login page is never visited.

**The anti-pattern in other apps:** Setting the cookie via JavaScript or via a separate
redirect-to-self step before going to the dashboard. This adds an extra round trip and can
cause the login page to flash.

---

### 3. The Azure App Registration Must Be a Confidential Client (Web Platform)

In Azure Portal → App registrations → Authentication, the redirect URI must be registered
under the **Web** platform, not "Single-page application" (SPA).

- **Web** = confidential client = sends `client_secret` during token exchange ✓
- **SPA** = public client = PKCE only, no `client_secret` — MSAL's
  `ConfidentialClientApplication` will be rejected with `AADSTS700025`

---

## Full Flow (Step by Step)

```
Browser                    Server                         Azure AD
  |                          |                               |
  |-- GET /auth/azure/login ->|                               |
  |                          | initiate_auth_code_flow()     |
  |                          | (generates PKCE code_verifier |
  |                          |  + code_challenge internally) |
  |                          | signs flow dict into cookie   |
  |<-- 302 to Azure + Set-Cookie: az_oauth_state ------------|
  |                                                          |
  |-- GET login.microsoftonline.com/... -------------------->|
  |<-- Microsoft login UI -----------------------------------|
  |-- POST credentials -------------------------------------->|
  |<-- 302 /auth/azure/callback?code=...&state=... ----------|
  |                          |                               |
  |-- GET /auth/azure/callback?code=...&state=... ---------->|
  |                          | decode az_oauth_state cookie  |
  |                          | acquire_token_by_auth_code_flow()
  |                          | (MSAL verifies state + nonce, |
  |                          |  sends code_verifier to Azure)|
  |                          | get_or_create_azure_user()    |
  |                          | create_session_token(user)    |
  |<-- 302 /dashboard + Set-Cookie: session + Del az_oauth_state
  |                          |                               |
  |-- GET /dashboard ------->|                               |
  |  (session cookie present, user authenticated)            |
```

---

## PKCE: Why initiate_auth_code_flow, Not get_authorization_request_url

MSAL Python's `get_authorization_request_url` is **deprecated** and its `**kwargs` are silently
dropped — passing `code_challenge` does nothing. Azure AD tenants with the policy
`AADSTS9002325` (PKCE required for cross-origin redemption) will reject the token exchange.

Use `initiate_auth_code_flow` instead. It generates the PKCE pair internally, embeds
`code_challenge` in the auth URL, and stores `code_verifier` in the returned flow dict.
Pass the flow dict to `acquire_token_by_auth_code_flow` on callback.

```python
# Correct approach
flow = msal_app.initiate_auth_code_flow(scopes=[...], redirect_uri=...)
# flow["auth_uri"]       → redirect the browser here
# flow["code_verifier"]  → MSAL stores this, sent automatically on token exchange

result = msal_app.acquire_token_by_auth_code_flow(flow, auth_response)
claims = result.get("id_token_claims")
```

The flow dict must survive between the login request and the callback. Since servers can
restart (losing in-memory state), serialize it to JSON, sign it with `itsdangerous`, and
store it in an HTTP-only cookie (`az_oauth_state`, max_age=600s).

---

## Scopes: Avoid Reserved Words

MSAL automatically adds `openid`, `profile`, and `offline_access` to every request.
Passing them explicitly raises `ValueError: You cannot use any scope value that is reserved`.

```python
# Wrong
scopes = ["openid", "email", "profile"]

# Correct — just the Graph API scope you need
scopes = ["User.Read"]
```

Filter any reserved words before passing to MSAL:

```python
RESERVED = {"openid", "profile", "offline_access", "email"}
scopes = [s for s in configured_scopes if s not in RESERVED]
```

---

## State Cookie Expiry (600s)

The `az_oauth_state` cookie has `max_age=600` (10 minutes). This is the window the user has
to complete the Microsoft login. If they take longer, the cookie expires, and the callback
returns "Session expired" with a redirect to login. Adjust if needed.

---

## User Provisioning on First Login

New Azure AD users are created with `is_active=False` and redirected to `/auth/pending`.
An admin must approve them at `/admin/users` before they can access the app.

On subsequent logins, `get_or_create_azure_user` looks up by `azure_oid` (stable object ID
from the token claims) and skips creation entirely.

---

## Checklist for Other Apps Adopting This Pattern

- [ ] Auth middleware must NOT redirect on missing session — only inject `user = None`
- [ ] Set session cookie and redirect to dashboard in the **same** `RedirectResponse`
- [ ] Register redirect URI as **Web** platform in Azure Portal (not SPA)
- [ ] Use `initiate_auth_code_flow` + `acquire_token_by_auth_code_flow` (not the deprecated method)
- [ ] Store the MSAL flow dict server-side between login and callback (signed cookie or cache)
- [ ] Filter reserved scopes (`openid`, `profile`, `offline_access`) before passing to MSAL
- [ ] Pass all callback query params as `auth_response` dict to `acquire_token_by_auth_code_flow`
- [ ] `AZURE_AD_CLIENT_SECRET` must be the **Value**, not the Secret ID (UUID)
