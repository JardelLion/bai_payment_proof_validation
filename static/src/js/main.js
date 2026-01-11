/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.BaiUploadWidget = publicWidget.Widget.extend({

    selector: ".js_bai_upload_form",

    events: {
        "change .js_bank_select": "_onBankChange",
    },

    start() {
        this._toggle(false);
        return this._super.apply(this, arguments);
    },

    _onBankChange(ev) {
        const value = ev.currentTarget.value;
        this._toggle(!!value);
    },

    _toggle(show) {
        this.$(".js_pdf_block").toggleClass("d-none", !show);
        this.$(".js_submit_btn").toggleClass("d-none", !show);

        // tornar obrigatório apenas quando visível
        this.$('input[name="attachment"]').prop("required", show);
    },
});
