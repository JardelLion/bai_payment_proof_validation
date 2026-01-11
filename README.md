# Módulo de Upload e Validação de Comprovativos BAI - Odoo Website

## Visão Geral

Este módulo adiciona uma funcionalidade ao **Website Sale** do Odoo permitindo que os clientes:

- Anexem comprovativos de pagamento (PDF) durante o checkout.
- Validem automaticamente pagamentos enviados via **BAI** (Banco Angolano de Investimentos) usando integração com API.
- Recebam feedback visual em tempo real sobre o status do comprovativo.
- Corrijam e reenviem comprovativos inválidos.

O módulo é projetado para fornecer uma experiência **clara, segura e confiável** no processo de pagamento.

---

## Funcionalidades

1. **Upload de Comprovativo**
   - PDF enviado pelo cliente no checkout.
   - Escolha do banco: BAI ou outro banco.
   
2. **Validação Automática**
   - Se o banco selecionado for **BAI**, o sistema verifica se o comprovativo corresponde ao banco via API.
   - Feedback visual baseado no estado do comprovativo:
     - `bai_valid` → Comprovativo validado via API BAI (alerta verde).
     - `other_bank` → Comprovativo recebido de outro banco (alerta verde simples).
     - `not_valid` → Comprovativo inválido ou não pertencente ao BAI (alerta vermelho e permite reenviar).

3. **Mensagens e UX**
   - Ícones Font Awesome centralizados:
     - ✅ Verde para comprovativos válidos
     - ❌ Vermelho para comprovativos inválidos
   - Mensagem clara para reenviar ficheiro quando inválido.
   - Formulário só aparece quando necessário (`not_valid` ou nenhum comprovativo enviado).

4.**Integração Backend**
   - Atualização do estado do pedido (`bai_receipt_state`) no modelo `sale.order`.
   - Criação automática de anexos (`ir.attachment`) com o comprovativo enviado.
   - Estado controlado para impedir reenvio indevido quando comprovativo é válido.

---

## Instalação

1. Copie o módulo para a pasta `addons` do seu Odoo.
2. Atualize a lista de módulos no backend.
3. Instale o módulo via **Apps**.
4. No backend do Odoo, vá para Faturação → Configurações → Métodos de Pagamento e ative os Payment Providers necessários, incluindo Transferência Bancária / Bank Transfer.
---

## Uso

1. Acesse a loja do website.
2. Adicione produtos ao carrinho e finalize o pedido.
3. Na página de **Confirmação do Pedido**:
   - Selecione o banco.
   - Anexe o comprovativo PDF.
   - Clique em **Enviar comprovativo**.
4. Feedback visual:
   - Comprovativo válido → alerta verde.
   - Comprovativo inválido → alerta vermelho + possibilidade de reenviar.
   - Outro banco → alerta verde simples.

---

## Estados do Comprovativo (`bai_receipt_state`)

| Estado       | Significado                                           |
|--------------|-------------------------------------------------------|
| `draft`      | Nenhum comprovativo enviado                           |
| `bai_valid`  | Comprovativo validado via API BAI                     |
| `not_valid`  | Comprovativo inválido ou não do BAI                  |
| `other_bank` | Comprovativo enviado de outro banco                  |

---

## Boas Práticas

- Validar sempre os comprovativos no backend mesmo que a confirmação no frontend permita envio.
- Registrar anexos e estado de pedidos para auditoria financeira.
- Usar mensagens claras para o cliente sobre próximos passos.
- Evitar múltiplos envios de comprovativos válidos.

---

## Contribuição

- Abrir issues no repositório para reportar bugs.
- Sugerir melhorias de UX ou mensagens.
- Contribuir com integração com outros bancos se necessário.

---