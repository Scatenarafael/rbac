from __future__ import annotations

import hashlib


class SessionFingerprintService:
    def build_fingerprint(self, *, user_agent: str | None, ip_address: str | None) -> str:
        normalized_user_agent = (user_agent or "").strip().lower()
        normalized_ip_address = (ip_address or "").strip().lower()
        raw_fingerprint = f"{normalized_user_agent}|{normalized_ip_address}"
        return hashlib.sha256(raw_fingerprint.encode("utf-8")).hexdigest()
