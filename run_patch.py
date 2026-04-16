import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

correct = '''function setCardFocus(sectionId, cardId) {
    const section = document.getElementById(sectionId);
    if (!section) return;
    
    const cards = section.querySelectorAll('.schedule-card');
    cards.forEach(c => {
        c.style.transform = 'scale(1)';
        c.style.boxShadow = '0 1px 4px rgba(0,0,0,0.05)';
        c.style.borderColor = '#2c3e8c';
    });

    const targetCard = document.getElementById(cardId);
    if(targetCard) {
        const tColor = targetCard.getAttribute('data-color') || '#2c3e8c';
        targetCard.style.transform = 'scale(1.02)';
        targetCard.style.boxShadow = `0 8px 24px ${tColor}40`;
        targetCard.style.borderColor = tColor;
        
        let name = "New Placeholder Schedule";
        const nameInput = targetCard.querySelector('input[type="text"]');
        if (nameInput && nameInput.value) {
            name = nameInput.value;
        } else {
            const header = targetCard.querySelector('h2');
            if (header) name = header.innerText;
        }
        
        const audienceHeader = document.getElementById(sectionId + '-audience-target');
        if (audienceHeader) audienceHeader.innerText = name;
        
        const panel = document.getElementById(sectionId + '-audience-panel');
        if(panel) {
            panel.style.borderTop = `4px solid ${tColor}`;
        }
        
        const tbody = document.getElementById(sectionId + '-audience-tbody');
        if(tbody) {
             const dataBlock1 = `
                <tr style="border-bottom:1px solid #f0f0f0;">
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Demooo Demooo</td>
                   <td style="padding:8px;">890 Mountain Ave</td>
                   <td style="padding:8px;">test@webcodegenie.net</td>
                </tr>
                <tr style="border-bottom:1px solid #f0f0f0;">
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Webcodegenie</td>
                   <td style="padding:8px;">676 N St Clair St</td>
                   <td style="padding:8px;">sakshi.b@webcodegenie.com</td>
                </tr>
                <tr style="border-bottom:1px solid #f0f0f0;">
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Multi Tier Product Test</td>
                   <td style="padding:8px;">3456 Shadeland Ave</td>
                   <td style="padding:8px;">tier@webcodegenie.net</td>
                </tr>
                <tr>
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Demo Testing</td>
                   <td style="padding:8px;">5465 Windward Pkwy</td>
                   <td style="padding:8px;">Demo.test@webcodegenie.net</td>
                </tr>`;
             
             const dataBlock2 = `
                <tr style="border-bottom:1px solid #f0f0f0;">
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Acme Logistics Corp</td>
                   <td style="padding:8px;">123 Business Loop, NY</td>
                   <td style="padding:8px;">accounts@acmelogistics.com</td>
                </tr>
                <tr style="border-bottom:1px solid #f0f0f0;">
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Jane Smith Enterprises</td>
                   <td style="padding:8px;">42 North Avenue, Suite B</td>
                   <td style="padding:8px;">jane.smith@gmail.com</td>
                </tr>
                <tr>
                   <td style="padding:8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                   <td style="padding:8px;">Global Dynamics Inc.</td>
                   <td style="padding:8px;">900 Tech Park Way</td>
                   <td style="padding:8px;">billing@globaldynamics.org</td>
                </tr>`;
             
             const emptyData = `
                <tr><td colspan="4" style="padding:24px; text-align:center; color:#888;">No audience targeted by this filter configuration yet.</td></tr>`;
                
             if (cardId.endsWith('-c1')) {
                 tbody.innerHTML = dataBlock1;
             } else if (cardId.endsWith('-c2')) {
                 tbody.innerHTML = dataBlock2;
             } else {
                 tbody.innerHTML = emptyData;
             }
        }
    }
}'''

new_text = re.sub(r'function setCardFocus\(sectionId, cardId\) \{.*?(?=^// ── Schedule ON/OFF Interaction)', correct + '\n', text, flags=re.MULTILINE|re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("success")
