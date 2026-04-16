import re
import sys

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Shared fields block to inject inside cards
def get_fields(type_str, card_num=0):
    val_name = "New Placeholder Schedule"
    chk_pay_this_year = ""
    chk_pay_last_year = ""
    chk_attach_yes = ""
    chk_attach_no = "checked"
    
    if card_num == 1:
        val_name = "This Year's Renewal Customers"
        chk_pay_this_year = "checked"
        chk_attach_yes = "checked"
        chk_attach_no = ""
    elif card_num == 2:
        val_name = "Last Year's Renewal Customers"
        chk_pay_last_year = "checked"
        chk_attach_yes = "checked"
        chk_attach_no = ""

    return f"""
      <div style="margin-bottom:16px;">
         <div style="font-weight:bold; font-size:0.9rem; color:#111; margin-bottom:4px; display:flex; align-items:flex-end;">Schedule Name: <input type="text" value="{val_name}" style="border:none; border-bottom:1px solid #b3d9f5; color:#0277bd; font-size:1.05rem; flex:1; outline:none; font-weight:bold; padding-bottom:2px; margin-left:8px;"/></div>
      </div>
      
      <!-- Payment Status -->
      <div style="margin-bottom:14px; border:1px solid #eee; padding:12px; border-radius:4px;">
         <div style="font-weight:bold; font-size:0.85rem; color:#111; margin-bottom:8px;">Payment Status</div>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#555; margin-bottom:6px; cursor:pointer;">
            <input type="checkbox" {chk_pay_this_year} style="transform:scale(1.2); accent-color:#3f51b5;"/> Customers with active Invoices (this year)
         </label>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#555; cursor:pointer;">
            <input type="checkbox" {chk_pay_last_year} style="transform:scale(1.2); accent-color:#3f51b5;"/> Customers with active Invoices (past years)
         </label>
      </div>

      <!-- Auto-Pay Filters -->
      <div style="margin-bottom:14px; border:1px solid #eee; padding:12px; border-radius:4px;">
         <div style="font-weight:bold; font-size:0.85rem; color:#111; margin-bottom:8px; display:flex; align-items:center; gap:6px;">Auto-Pay Filters <span style="font-weight:normal; color:#888; font-size:0.75rem;">(Send to customers with)</span> <a href="javascript:void(0)" onclick="resetRadio('autopay_{type_str}')" style="color:#0277bd; font-size:0.75rem; text-decoration:underline;">Reset</a></div>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#555; margin-bottom:4px; cursor:pointer;"><input type="radio" name="autopay_{type_str}" style="transform:scale(1.2); accent-color:#3f51b5;"/> Failed Auto-Pay Payments</label>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#555; margin-bottom:4px; cursor:pointer;"><input type="radio" name="autopay_{type_str}" style="transform:scale(1.2); accent-color:#3f51b5;"/> Card Expired <span style="color:#aaa; font-size:0.75rem;">(Customers who's stored Card has expired)</span></label>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#555; margin-bottom:4px; cursor:pointer;"><input type="radio" name="autopay_{type_str}" style="transform:scale(1.2); accent-color:#3f51b5;"/> All Auto-Pay Customers</label>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#111; font-weight:bold; cursor:pointer;"><input type="radio" name="autopay_{type_str}" checked style="transform:scale(1.2); accent-color:#3f51b5;"/> Exclude Auto-Pay Customers</label>
      </div>

      <!-- Email/Phone Addresses -->
      <div style="margin-bottom:14px; border:1px solid #eee; padding:12px; border-radius:4px;">
         <div style="font-weight:bold; font-size:0.85rem; color:#111; margin-bottom:8px; display:flex; align-items:center; gap:6px;">Target Addresses <span style="font-weight:normal; color:#888; font-size:0.75rem;">(Selecting type of address will not affect Customer count)</span> <a href="javascript:void(0)" onclick="resetRadio('addr_{type_str}')" style="color:#0277bd; font-size:0.75rem; text-decoration:underline;">Reset</a></div>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#111; font-weight:bold; margin-bottom:4px; cursor:pointer;"><input type="radio" name="addr_{type_str}" checked style="transform:scale(1.2); accent-color:#3f51b5;"/> Billing Address and Contact Address</label>
         <label style="display:flex; align-items:center; gap:8px; font-size:0.85rem; color:#555; cursor:pointer;"><input type="radio" name="addr_{type_str}" style="transform:scale(1.2); accent-color:#3f51b5;"/> Customer Login Only</label>
      </div>

      <!-- Advanced Filters -->
      <div style="margin-bottom:14px; border:1px solid #eee; padding:12px; border-radius:4px; color:#3f51b5; font-size:0.85rem; cursor:pointer;">
         Advanced Filters <i data-lucide="chevron-down" style="width:14px; height:14px; vertical-align:middle;"></i>
      </div>

      <!-- Attach Invoice -->
      <div style="margin-bottom:20px; border:1px solid #eee; padding:12px; border-radius:4px;">
         <div style="font-weight:bold; font-size:0.85rem; color:#111; margin-bottom:8px;">Attach Invoice to each Customer's Notice?</div>
         <div style="display:flex; gap:16px;">
            <label style="display:flex; align-items:center; gap:6px; font-size:0.85rem; color:#555; cursor:pointer;"><input type="radio" name="attach_{type_str}" {chk_attach_yes} style="transform:scale(1.2); accent-color:#3f51b5;"/> Yes</label>
            <label style="display:flex; align-items:center; gap:6px; font-size:0.85rem; color:#111; font-weight:bold; cursor:pointer;"><input type="radio" name="attach_{type_str}" {chk_attach_no} style="transform:scale(1.2); accent-color:#3f51b5;"/> No</label>
         </div>
      </div>

      <!-- Schedule Details -->
      <h3 style="font-size:1.1rem; color:#111; margin:0 0 16px 0;">Schedule Details</h3>
      <div style="margin-bottom:24px;">
         <div style="display:flex; gap:20px; margin-bottom:16px;">
            <label style="display:flex; align-items:center; gap:6px; font-size:0.8rem; cursor:pointer;"><input name="sched-date-{type_str}" type="radio" value="custom" style="transform:scale(1.2); accent-color:#3f51b5;"/> Custom Date</label>
            <label style="display:flex; align-items:center; gap:6px; font-size:0.8rem; cursor:pointer; font-weight:bold;"><input checked="" name="sched-date-{type_str}" type="radio" value="invoice" style="transform:scale(1.2); accent-color:#3f51b5;"/> Invoice Creation Date <span style="color:#888;font-weight:normal;">(2026-11-12)</span></label>
         </div>
         
         <div style="display:flex; gap:24px; margin-bottom:16px;">
            <label style="display:flex; align-items:center; gap:6px; font-size:0.8rem; cursor:pointer;"><input name="sched-recur-{type_str}" type="radio" value="recurring" style="transform:scale(1.2); accent-color:#3f51b5;"/> Recurring Reminder Schedule</label>
            <label style="display:flex; align-items:center; gap:6px; font-size:0.8rem; cursor:pointer; font-weight:bold;"><input name="sched-recur-{type_str}" type="radio" checked value="granular" style="transform:scale(1.2); accent-color:#3f51b5;"/> Granular Reminder Schedule</label>
         </div>
         
         <table style="width:100%; border-collapse:collapse; font-size:0.8rem; text-align:left;">
            <thead style="background:#eef2ff;">
               <tr>
               <th style="padding:10px; color:#2c3e8c;">SCHEDULE</th>
               <th style="padding:10px; color:#2c3e8c;">SEND DATE</th>
               <th style="padding:10px; color:#2c3e8c;">SELECT TEMPLATE</th>
               <th style="padding:10px; text-align:right;"><button onclick="addScheduleRow(this)" style="background:#3f51b5; color:#fff; border:none; padding:6px 12px; font-weight:bold; cursor:pointer; font-size:0.75rem; border-radius:2px;">ADD SCHEDULE</button></th>
               </tr>
            </thead>
            <tbody>
               <tr style="border-bottom:1px solid #eee;">
               <td style="padding:10px; color:#555;">1. Blast</td>
               <td style="padding:10px;"><input type="date" value="2026-04-16" style="padding:6px; border:1px solid #ccc; outline:none; border-radius:2px; color:#555; width:100%; box-sizing:border-box;"/></td>
               <td style="padding:10px;">
                  <select style="padding:6px; border:1px solid #ccc; outline:none; border-radius:2px; width:100%; color:#555; box-sizing:border-box;">
                     <option>2025 renewals</option>
                  </select>
               </td>
               <td style="padding:10px; text-align:right;"><button onclick="deleteScheduleRow(this)" style="background:#e74c3c; color:#fff; border:none; padding:6px 12px; cursor:pointer; font-size:0.75rem; border-radius:2px;">Delete</button></td>
               </tr>
               <tr>
               <td style="padding:10px; color:#555;">2. Blast</td>
               <td style="padding:10px;"><input type="date" value="2026-04-21" style="padding:6px; border:1px solid #ccc; outline:none; border-radius:2px; color:#555; width:100%; box-sizing:border-box;"/></td>
               <td style="padding:10px;">
                  <select style="padding:6px; border:1px solid #ccc; outline:none; border-radius:2px; width:100%; color:#555; box-sizing:border-box;">
                     <option>Home & Business Flag Sub...</option>
                  </select>
               </td>
               <td style="padding:10px; text-align:right;"><button onclick="deleteScheduleRow(this)" style="background:#e74c3c; color:#fff; border:none; padding:6px 12px; cursor:pointer; font-size:0.75rem; border-radius:2px;">Delete</button></td>
               </tr>
            </tbody>
         </table>
      </div>

      <div style="background:#e8f4fd;border:1px solid #b3d9f5;padding:10px 14px;font-size:0.75rem;color:#1a6e9e;">
         <div style="display:flex;align-items:center;gap:6px;"><i data-lucide="info" style="width: 14px; height: 14px; flex-shrink: 0;"></i> <span>The Administrator will be notified by {type_str} 24 hours prior to the start of the Auto-Invoicing process.</span></div>
      </div>
"""

def generate_layout(section_id, active_label, count=4):
    cards_html = ""
    for i in range(1, count + 1):
        if i in [1, 2]:
            # Active Card
            card = f"""
    <!-- Card {i} -->
    <div id="{section_id}-c{i}" class="schedule-card" onmouseenter="setCardFocus('{section_id}', '{section_id}-c{i}')" style="border:1px solid #2c3e8c; border-top:4px solid #27ae60; border-radius:4px; padding:12px; background:#fff; box-shadow:0 1px 4px rgba(0,0,0,0.05); max-height:510px; overflow-y:auto; font-size:0.8rem; transition: transform 0.2s, box-shadow 0.2s, border-top 0.2s;">
      <div style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid #2c3e8c; padding-bottom:8px; margin-bottom:12px;">
        <h2 style="margin:0; font-size:1.1rem; color:#111; font-weight:bold;">Auto-Send ({active_label}) Schedule</h2>
        <div style="display:flex; align-items:center; gap:6px;">
          <span style="font-size:0.75rem; color:#333;">Status</span>
          <div style="display:flex; border-radius:2px; overflow:hidden;">
            <button onclick="toggleCardStatus(this, 'off')" style="background:#f0f0f0; color:#888; border:none; padding:4px 8px; font-size:0.65rem; font-weight:bold; cursor:pointer;">OFF</button>
            <button onclick="toggleCardStatus(this, 'on')" style="background:#27ae60; color:#fff; border:none; padding:4px 8px; font-size:0.65rem; font-weight:bold; cursor:pointer;">ON</button>
          </div>
        </div>
      </div>
      {get_fields(active_label + f"_c{i}")}
    </div>
            """
        else:
            # Placeholder Card
            card = f"""
    <!-- Card {i} -->
    <div id="{section_id}-c{i}" class="schedule-card" onmouseenter="setCardFocus('{section_id}', '{section_id}-c{i}')" style="border:1px solid #2c3e8c; border-top:4px solid #ccc; border-radius:4px; padding:12px; background:#fff; position:relative; box-shadow:0 1px 4px rgba(0,0,0,0.05); min-height:510px; max-height:510px; overflow-y:auto; display:flex; flex-direction:column; font-size:0.8rem; transition: transform 0.2s, box-shadow 0.2s, border-top 0.2s;">
      <div id="{section_id}-c{i}-header" style="display:flex; justify-content:space-between; align-items:flex-end; border-bottom:2px solid #2c3e8c; padding-bottom:8px; margin-bottom:12px;">
        <h2 style="margin:0; font-size:1.1rem; color:#111; font-weight:bold;">Auto-Send ({active_label}) Schedule</h2>
        <div style="display:flex; align-items:center; gap:6px;">
          <span style="font-size:0.75rem; color:#333;">Status</span>
          <div style="display:flex; border-radius:2px; overflow:hidden;">
            <button onclick="toggleCardStatus(this, 'off')" style="background:#e74c3c; color:#fff; border:none; padding:4px 8px; font-size:0.65rem; font-weight:bold; cursor:pointer;">OFF</button>
            <button onclick="toggleCardStatus(this, 'on')" style="background:#f0f0f0; color:#888; border:none; padding:4px 8px; font-size:0.65rem; font-weight:bold; cursor:pointer;">ON</button>
          </div>
        </div>
      </div>

      <!-- State 1: Placeholder/Collapsed -->
      <div id="{section_id}-c{i}-placeholder" style="flex:1; display:flex; flex-direction:column; align-items:center; padding-top:60px; cursor:pointer;" onclick="expandCard('{section_id}-c{i}')">
         <div style="display:flex; align-items:center; gap:10px; font-size:1rem; color:#111; font-weight:bold;">
            <i data-lucide="plus-circle" style="width:24px; height:24px; color:#3f51b5;"></i>
            Add Another Schedule
         </div>
      </div>

      <!-- State 2: Expanded Fields -->
      <div id="{section_id}-c{i}-full" style="display:none; flex:1; flex-direction:column;">
         <div style="margin-bottom:12px; border-bottom:1px solid #ddd; padding-bottom:8px;">
            <span style="font-size:0.75rem; color:#888; display:flex; align-items:center; justify-content:space-between;">
               <span style="display:flex; align-items:center; gap:4px;"><i data-lucide="plus-circle" style="width:12px; height:12px; color:#3f51b5;"></i> Add Another Schedule</span>
               <a href="javascript:void(0)" onclick="revertCard('{section_id}-c{i}')" style="color:#0277bd; text-decoration:underline;">Revert to no Schedule</a>
            </span>
         </div>
         {get_fields(active_label + f"_c{i}", i)}
      </div>
    </div>
            """
        cards_html += card

    audience_html = f"""
    <div style="flex:1;">
       <div style="position:sticky; top:20px; border:1px solid #c9d8ff; border-radius:4px; padding:16px; background:#fff; box-shadow:0 1px 6px rgba(0,0,0,0.05); min-height:600px;">
          <h2 style="margin:0 0 8px 0; font-size:1.2rem; color:#2c3e8c;">Audience Selector</h2>
          <p style="font-size:0.8rem; color:#666; margin-bottom:16px;">
             Previewing targeted audience for: <br/>
             <strong id="{section_id}-audience-target" style="color:#111; font-size:0.95rem; display:inline-block; margin-top:4px;">Auto-Send ({active_label}) Schedule</strong>
          </p>
          
          <div style="border:1px solid #e1e8f5; border-radius:4px; overflow:hidden;">
              <table style="width:100%; border-collapse:collapse; font-size:0.75rem;">
                <thead>
                    <tr style="background:#e8efff; color:#2c3e8c; font-weight:bold; text-align:left;">
                       <th style="padding:10px 8px;"><input type="checkbox" checked style="accent-color:#0277bd;" /> ALL</th>
                       <th style="padding:10px 8px;">FULL NAME</th>
                       <th style="padding:10px 8px;">BILLING ADDRESS</th>
                       <th style="padding:10px 8px;">EMAIL</th>
                    </tr>
                </thead>
                <tbody id="{section_id}-audience-tbody" style="color:#e74c3c;">
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
                    </tr>
                </tbody>
              </table>
          </div>
       </div>
    </div>
    """

    return f"""
<div id="{section_id}" style="padding:16px; display:flex; gap:24px; align-items:flex-start; { "display:none;" if section_id == "cfg-sms" else ""}">
    <div style="flex:2.2; display:grid; grid-template-columns:1fr 1fr; gap:16px;">
        {cards_html}
    </div>
    {audience_html}
</div>"""


email_layout = generate_layout("cfg-email", "Email", 4)
sms_layout = generate_layout("cfg-sms", "SMS", 4)

js_functions = """
// ── Schedule N-Card Expansion Logic ──────────────────────────────
function expandCard(cardId) {
    document.getElementById(cardId+'-placeholder').style.display = 'none';
    document.getElementById(cardId+'-full').style.display = 'flex';
    document.getElementById(cardId).style.borderTop = '4px solid #e74c3c';
}
function revertCard(cardId) {
    document.getElementById(cardId+'-full').style.display = 'none';
    document.getElementById(cardId+'-placeholder').style.display = 'flex';
    document.getElementById(cardId).style.borderTop = '4px solid #ccc';
    
    // Automatically sever 'ON' state gracefully if the user abandons via reversion
    const headerBtns = document.getElementById(cardId+'-header').querySelectorAll('button');
    if(headerBtns.length >= 2) {
        headerBtns[0].style.background = '#e74c3c';
        headerBtns[0].style.color = '#fff';
        headerBtns[1].style.background = '#f0f0f0';
        headerBtns[1].style.color = '#888';
    }
}
function resetRadio(groupName) {
    let radios = document.querySelectorAll(`input[name="${groupName}"]`);
    radios.forEach(r => r.checked = false);
}
// ── Schedule ON/OFF Interaction ──────────────────────────────
function toggleCardStatus(btn, state) {
    const btnContainer = btn.parentElement; 
    const headerRow = btnContainer.parentElement.parentElement;
    const cardWrapper = headerRow.parentElement;
    
    const cardId = cardWrapper.id;
    if (state === 'on' && cardId) {
        const placeholder = document.getElementById(cardId + '-placeholder');
        if (placeholder && placeholder.style.display !== 'none') {
            alert("Please click 'Add Another Schedule' before enabling this campaign.");
            return;
        }
    }
    
    const offBtn = btnContainer.children[0];
    const onBtn = btnContainer.children[1];
    
    if (state === 'on') {
        offBtn.style.background = '#f0f0f0';
        offBtn.style.color = '#888';
        onBtn.style.background = '#27ae60';
        onBtn.style.color = '#fff';
        cardWrapper.style.borderTop = '4px solid #27ae60';
    } else {
        offBtn.style.background = '#e74c3c';
        offBtn.style.color = '#fff';
        onBtn.style.background = '#f0f0f0';
        onBtn.style.color = '#888';
        // Reset card top layer
        cardWrapper.style.borderTop = '4px solid transparent'; 
        // Note: For active Card 1, returning to transparent might lose its blue top edge if it was generic, but our transparent border preserves layout shift
    }
}
// Dynamic Add/Delete Row Logic
function addScheduleRow(btn) {
    const tbody = btn.closest('table').querySelector('tbody');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td style="padding:10px; color:#555;">New Blast</td>
        <td style="padding:10px;"><input type="date" style="padding:6px; border:1px solid #ccc; outline:none; border-radius:2px; color:#555; width:100%; box-sizing:border-box;"/></td>
        <td style="padding:10px;">
           <select style="padding:6px; border:1px solid #ccc; outline:none; border-radius:2px; width:100%; color:#555; box-sizing:border-box;">
               <option>-- Select Template --</option>
               <option>2025 renewals</option>
               <option>Auto-Invoice</option>
               <option>Final Expiration Notice</option>
           </select>
        </td>
        <td style="padding:10px; text-align:right;"><button onclick="deleteScheduleRow(this)" style="background:#e74c3c; color:#fff; border:none; padding:6px 12px; cursor:pointer; font-size:0.75rem; border-radius:2px;">Delete</button></td>
    `;
    tbody.appendChild(newRow);
}
function deleteScheduleRow(btn) {
    btn.closest('tr').remove();
}
"""

start_marker = '<div id="cfg-email"'
end_marker = '</div> <!-- closes main-left-col -->'

# Extract the block
if start_marker in content:
    pre = content.split(start_marker)[0]
    post = content.split(end_marker, 1)[1]
    
    # inject the new layouts
    new_content = pre + email_layout + "\n" + sms_layout + "\n</div> <!-- /#main-panel-config -->\n</div></div>\n" + end_marker + post
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED TO FIND MARKER")
