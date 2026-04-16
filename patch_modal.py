import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

modal_html = """<!-- ── SCHEDULE EDIT MODAL ── -->
<div id="schedule-edit-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9999; align-items:center; justify-content:center; backdrop-filter:blur(2px);">
   <div style="background:#fff; border-radius:4px; box-shadow:0 12px 40px rgba(0,0,0,0.2); width:800px; height:750px; max-height:90vh; border:1px solid #ddd; display:flex; flex-direction:column; overflow:hidden; font-family:Arial, sans-serif;">
      
      <!-- HEADER -->
      <div style="background:#fff; padding:16px 20px 0 20px; border-bottom:1px solid #ddd; flex-shrink:0;">
         <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
            <h2 style="margin:0; font-size:1.3rem; font-weight:normal; color:#3f51b5;">Pending Payment Customers</h2>
            <i data-lucide="x" style="width:24px; height:24px; cursor:pointer; color:#888;" onclick="document.getElementById('schedule-edit-modal').style.display='none'"></i>
         </div>
         
         <!-- TABS -->
         <div style="display:flex; gap:24px;">
            <div id="modal-tab-head-filter" onclick="switchModalTab('filter')" style="padding-bottom:12px; border-bottom:2px solid #3f51b5; color:#3f51b5; font-size:1.1rem; cursor:pointer;">Filter</div>
            <div id="modal-tab-head-schedule" onclick="switchModalTab('schedule')" style="padding-bottom:12px; border-bottom:2px solid transparent; color:#111; font-size:1.1rem; cursor:pointer;">Schedule</div>
            <div id="modal-tab-head-results" onclick="switchModalTab('results')" style="padding-bottom:12px; border-bottom:2px solid transparent; color:#111; font-size:1.1rem; cursor:pointer;">Results (<span style="color:#3f51b5;">212</span>)</div>
         </div>
      </div>

      <!-- BODY CONTAINERS -->
      <div style="flex:1; overflow-y:auto; background:#fff; padding:20px;">
         
         <!-- BODY: FILTER -->
         <div id="modal-body-filter" style="display:block;">
            <div style="background:#fff; border:1px solid #eee; padding:16px; margin-bottom:16px; border-radius:4px;">
               <div style="font-weight:bold; margin-bottom:8px; color:#111; font-size:0.95rem;">Payment Status</div>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#555; margin-bottom:6px;"><input type="checkbox" checked style="accent-color:#3f51b5;"/> Customers with active Invoices (this year)</label>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#888;"><input type="checkbox" style="accent-color:#3f51b5;"/> Customers with active Invoices (past years)</label>
            </div>

            <div style="background:#fff; border:1px solid #eee; padding:16px; margin-bottom:16px; border-radius:4px;">
               <div style="font-weight:bold; margin-bottom:10px; color:#111; font-size:0.95rem;">Auto-Pay Filters <span style="font-weight:normal; color:#888; font-size:0.85rem;">(Send to customers with)</span> <a href="#" style="color:#0277bd; text-decoration:underline; font-size:0.85rem; margin-left:6px; font-weight:normal;">Reset</a></div>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#888; margin-bottom:4px;"><input type="radio" name="modal-autopay"/> Failed Auto-Pay Payments</label>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#888; margin-bottom:4px;"><input type="radio" name="modal-autopay"/> Card Expired <span style="font-size:0.85rem; color:#aaa;">(Customers who's stored Card has expired)</span></label>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#888; margin-bottom:4px;"><input type="radio" name="modal-autopay"/> All Auto-Pay Customers</label>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#111; font-weight:bold;"><input type="radio" name="modal-autopay" checked style="accent-color:#3f51b5;"/> Exclude Auto-Pay Customers</label>
            </div>

            <div style="background:#fff; border:1px solid #eee; padding:16px; margin-bottom:16px; border-radius:4px;">
               <div style="font-weight:bold; margin-bottom:10px; color:#111; font-size:0.95rem;">Target Addresses <span style="font-weight:normal; color:#888; font-size:0.85rem;">(Selecting type of address will not affect Customer count)</span> <a href="#" style="color:#0277bd; text-decoration:underline; font-size:0.85rem; margin-left:6px; font-weight:normal;">Reset</a></div>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#111; font-weight:bold; margin-bottom:8px;"><input type="radio" name="modal-address" checked style="accent-color:#3f51b5;"/> Billing Address and Contact Address</label>
               <label style="display:flex; align-items:center; gap:8px; font-size:0.95rem; color:#888;"><input type="radio" name="modal-address"/> Customer Login Only</label>
            </div>

            <div style="background:#fff; border:1px solid #eee; padding:16px; border-radius:4px; color:#3f51b5; display:flex; align-items:center; gap:6px; cursor:pointer;">
               Advanced Filters <i data-lucide="chevron-down" style="width:16px; height:16px;"></i>
            </div>
         </div>

         <!-- BODY: SCHEDULE -->
         <div id="modal-body-schedule" style="display:none;">
            <div style="background:#fff; border:1px solid #eee; padding:16px; margin-bottom:24px; border-radius:4px;">
                <div style="font-weight:bold; font-size:0.95rem; color:#111; margin-bottom:12px;">Attach Invoice to each Customer's Notice?</div>
                <div style="display:flex; gap:16px;">
                   <label style="display:flex; align-items:center; gap:6px; font-size:0.95rem; color:#888;"><input type="radio" name="modal-attach"/> Yes</label>
                   <label style="display:flex; align-items:center; gap:6px; font-size:0.95rem; color:#111; font-weight:bold;"><input type="radio" name="modal-attach" checked style="accent-color:#3f51b5;"/> No</label>
                </div>
            </div>

            <div style="font-weight:bold; font-size:1.1rem; color:#111; margin-bottom:16px;">Schedule Details</div>
            
            <div style="display:flex; gap:20px; margin-bottom:16px;">
                <label style="display:flex; align-items:center; gap:6px; font-size:0.95rem; color:#555;"><input type="radio" name="modal-schedule-type"/> Custom Date</label>
                <label style="display:flex; align-items:center; gap:6px; font-size:0.95rem; color:#3f51b5; font-weight:bold;"><input type="radio" name="modal-schedule-type" checked style="accent-color:#3f51b5;"/> Invoice Creation Date <span style="font-weight:normal; color:#888;">(2026-11-12)</span></label>
            </div>
            <div style="display:flex; gap:20px; margin-bottom:24px;">
                <label style="display:flex; align-items:center; gap:6px; font-size:0.95rem; color:#555;"><input type="radio" name="modal-schedule-type-2"/> Recurring Reminder Schedule</label>
                <label style="display:flex; align-items:center; gap:6px; font-size:0.95rem; color:#3f51b5; font-weight:bold;"><input type="radio" name="modal-schedule-type-2" checked style="accent-color:#3f51b5;"/> Granular Reminder Schedule</label>
            </div>

            <div style="background:#f4f7ff; margin-bottom:24px;">
               <table style="width:100%; border-collapse:collapse; text-align:left;">
                  <thead style="color:#3f51b5; font-size:0.85rem;">
                     <tr>
                        <th style="padding:16px;">SCHEDULE</th>
                        <th style="padding:16px;">SEND DATE</th>
                        <th style="padding:16px;">SELECT TEMPLATE</th>
                        <th style="padding:10px; text-align:right;">
                           <button style="background:#3f51b5; color:#fff; border:none; padding:10px 16px; border-radius:2px; font-weight:bold; cursor:pointer; font-size:0.8rem;">ADD SCHEDULE</button>
                        </th>
                     </tr>
                  </thead>
                  <tbody style="background:#fff; border-top:1px solid #e1e8f5;">
                     <tr style="border-bottom:1px solid #f0f0f0;">
                        <td style="padding:16px; color:#555; font-size:0.95rem;">1. Blast</td>
                        <td style="padding:16px;"><input type="date" value="2026-04-16" style="padding:8px; border:1px solid #ccc; border-radius:4px; color:#555; outline:none;"/></td>
                        <td style="padding:16px;">
                           <select style="padding:8px; border:1px solid #ccc; border-radius:4px; color:#555; outline:none; width:100%;">
                              <option>2025 renewal</option>
                              <option>Final Expiration Notice</option>
                           </select>
                        </td>
                        <td style="padding:16px; text-align:right;">
                           <button style="background:#e74c3c; color:#fff; border:none; padding:6px 12px; border-radius:2px; cursor:pointer; font-size:0.8rem;">Delete</button>
                        </td>
                     </tr>
                     <tr>
                        <td style="padding:16px; color:#555; font-size:0.95rem;">2. Blast</td>
                        <td style="padding:16px;"><input type="date" value="2026-04-21" style="padding:8px; border:1px solid #ccc; border-radius:4px; color:#555; outline:none;"/></td>
                        <td style="padding:16px;">
                           <select style="padding:8px; border:1px solid #ccc; border-radius:4px; color:#555; outline:none; width:100%;">
                              <option>Home & Busi...</option>
                           </select>
                        </td>
                        <td style="padding:16px; text-align:right;">
                           <button style="background:#e74c3c; color:#fff; border:none; padding:6px 12px; border-radius:2px; cursor:pointer; font-size:0.8rem;">Delete</button>
                        </td>
                     </tr>
                  </tbody>
               </table>
            </div>

            <div style="background:#e3f2fd; border:1px solid #bbdefb; padding:16px; border-radius:2px; display:flex; gap:12px; align-items:flex-start; color:#0277bd; font-size:0.85rem;">
               <i data-lucide="info" style="width:16px; height:16px; flex-shrink:0; margin-top:2px;"></i>
               <div>The Administrator will be notified by Email_c1 24 hours prior to the start of the Auto-Invoicing process.</div>
            </div>
         </div>

         <!-- BODY: RESULTS -->
         <div id="modal-body-results" style="display:none;">
            <div style="font-size:1.1rem; color:#111; margin-bottom:16px;">Total Email Count: <span style="color:#3f51b5; font-weight:bold;">212</span></div>
            
            <div style="border:1px solid #e1e8f5; border-radius:4px; overflow:hidden;">
                 <table style="width:100%; border-collapse:collapse; font-size:0.85rem;">
                   <thead>
                       <tr style="background:#eef2fa; color:#3f51b5; font-weight:bold; text-align:left;">
                          <th style="padding:12px; width:60px; text-align:center;"><input type="checkbox" checked style="accent-color:#0277bd;" /><br/>ALL</th>
                          <th style="padding:12px;">FULL NAME</th>
                          <th style="padding:12px;">BILLING ADDRESS</th>
                          <th style="padding:12px;">EMAIL</th>
                       </tr>
                   </thead>
                   <tbody style="color:#e74c3c;">
                       <tr style="border-bottom:1px solid #f0f0f0;">
                          <td style="padding:12px; text-align:center;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                          <td style="padding:12px;">Demooo Demooo</td>
                          <td style="padding:12px;">890 Mountain Ave</td>
                          <td style="padding:12px;">test@webcodegenie.net</td>
                       </tr>
                       <tr style="border-bottom:1px solid #f0f0f0;">
                          <td style="padding:12px; text-align:center;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                          <td style="padding:12px;">Webcodegenie</td>
                          <td style="padding:12px;">676 N St Clair St</td>
                          <td style="padding:12px;">sakshi.b@webcodegenie.com</td>
                       </tr>
                       <tr style="border-bottom:1px solid #f0f0f0;">
                          <td style="padding:12px; text-align:center;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                          <td style="padding:12px;">Multi Tier Product Test</td>
                          <td style="padding:12px;">3456 Shadeland Ave</td>
                          <td style="padding:12px;">tier@webcodegenie.net</td>
                       </tr>
                       <tr>
                          <td style="padding:12px; text-align:center;"><input type="checkbox" checked style="accent-color:#0277bd;" /></td>
                          <td style="padding:12px;">Demo Testing</td>
                          <td style="padding:12px;">5465 Windward Pkwy</td>
                          <td style="padding:12px;">Demo.test@webcodegenie.net</td>
                       </tr>
                   </tbody>
                 </table>
             </div>
         </div>
         
      </div>

      <!-- FOOTER -->
      <div style="padding:16px 20px; background:#fff; border-top:1px solid #ddd; display:flex; justify-content:flex-end; gap:12px; flex-shrink:0;">
         <button style="padding:10px 24px; background:#fff; border:1px solid #ccc; border-radius:4px; font-size:0.9rem; color:#555; cursor:pointer;" onclick="document.getElementById('schedule-edit-modal').style.display='none'">Cancel</button>
         <button style="padding:10px 32px; background:#3f51b5; border:none; border-radius:4px; font-size:0.9rem; color:#fff; font-weight:bold; cursor:pointer;" onclick="document.getElementById('schedule-edit-modal').style.display='none'">Save</button>
      </div>
   </div>
</div>

<script>
function switchModalTab(tab) {
    // Hide all bodies
    document.getElementById('modal-body-filter').style.display = 'none';
    document.getElementById('modal-body-schedule').style.display = 'none';
    document.getElementById('modal-body-results').style.display = 'none';
    
    // Reset all headers
    ['filter', 'schedule', 'results'].forEach(t => {
        let el = document.getElementById('modal-tab-head-' + t);
        el.style.borderBottom = '2px solid transparent';
        el.style.color = '#111';
    });
    
    // Show active body & style Header
    document.getElementById('modal-body-' + tab).style.display = 'block';
    let head = document.getElementById('modal-tab-head-' + tab);
    head.style.borderBottom = '2px solid #3f51b5';
    head.style.color = '#3f51b5';
}
</script>
</body>"""

pattern = re.compile(r'<!-- ── SCHEDULE EDIT MODAL ── -->.*?</body>', re.DOTALL)
new_html = pattern.sub(modal_html, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("success")
