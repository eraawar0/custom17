/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { patch } from "@web/core/utils/patch";
import { ajax } from "@web/core/ajax/ajax";

/**
 * Pengelola CSRF Token yang Aman
 * Menyimpan token di sessionStorage dan menambahkannya ke header permintaan
 */
export const csrfTokenManager = {
    start() {
        this.token = null;
        this.fetchToken();
        
        // Patch fungsi ajax untuk selalu menyertakan CSRF token
        patch(ajax, "csrf_token_patch", {
            jsonrpc(route, params = {}, settings = {}) {
                if (!settings.headers) {
                    settings.headers = {};
                }
                
                // Tambahkan CSRF token ke header jika tersedia
                if (this.token) {
                    settings.headers["X-CSRFToken"] = this.token;
                } else if (browser.sessionStorage.getItem("csrf_token")) {
                    settings.headers["X-CSRFToken"] = browser.sessionStorage.getItem("csrf_token");
                }
                
                return this._super(route, params, settings);
            }
        });
    },
    
    async fetchToken() {
        try {
            const result = await ajax.jsonrpc("/web/csrf/token", "call", {});
            this.token = result.token;
            
            // Simpan token di sessionStorage (lebih aman daripada localStorage)
            if (browser.sessionStorage) {
                browser.sessionStorage.setItem("csrf_token", this.token);
            }
            
            return this.token;
        } catch (error) {
            console.error("Gagal mengambil CSRF token:", error);
            return null;
        }
    },
    
    getToken() {
        if (this.token) {
            return this.token;
        }
        
        if (browser.sessionStorage && browser.sessionStorage.getItem("csrf_token")) {
            this.token = browser.sessionStorage.getItem("csrf_token");
            return this.token;
        }
        
        return this.fetchToken();
    }
};

// Daftarkan sebagai layanan
registry.category("services").add("csrf_token_manager", csrfTokenManager);