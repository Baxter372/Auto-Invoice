import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

modal_html = """<!-- ── SCHEDULE EDIT MODAL ── -->
<div id="schedule-edit-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9999; align-items:center; justify-content:center; backdrop-filter:blur(2px);">
   <div style="background:#fff; border-radius:4px; box-shadow:0 12px 40px rgba(0,0,0,0.2); width:800px; height:750px; max-height:90vh; border:1px solid #ddd; display:flex; flex-direction:column; overflow:hidden; font-family:Arial, sans-serif;">
      
      <!-- HEADER -->
      <div style="background:#fff; padding:16px 20px 0 20px; border-bottom:1px solid #ddd; flex-shrink:0;">
         <div style="display:flex; justify-content:space-between; align-items:center; margin:-16px -20px 16px -20px; padding:16px 20px; background:#f4f6f8; border-bottom:1px solid #eee;">
            <input type="text" value="Pending Payment Customers" style="margin:0; font-size:1.3rem; font-weight:bold; color:#555; background:transparent; border:none; outline:none; border-bottom:1px solid transparent; transition:border 0.2s; width:60%;" onfocus="this.style.borderBottom='1px solid #3f51b5'" onblur="this.style.borderBottom='1px solid transparent'"/>
            <i data-lucide="x" style="width:24px; height:24px; cursor:pointer; color:#888;" onclick="document.getElementById('schedule-edit-modal').style.display='none'"></i>
         </div>
         
         <!-- TABS -->
         <div style="display:flex; gap:24px;">
            <div id="modal-tab-head-filter" onclick="switchModalTab('filter')" style="padding-bottom:12px; border-bottom:2px solid #3f51b5; color:#3f51b5; font-size:1.1rem; cursor:pointer;">Filter</div>
            <div id="modal-tab-head-schedule" onclick="switchModalTab('schedule')" style="padding-bottom:12px; border-bottom:2px solid transparent; color:#111; font-size:1.1rem; cursor:pointer;">Schedule</div>
            <div id="modal-tab-head-results" onclick="switchModalTab('results')" style="padding-bottom:12px; border-bottom:2px solid transparent; color:#111; font-size:1.1rem; cursor:pointer;">Audience (<span style="color:#3f51b5;">212</span>)</div>
            <div id="modal-tab-head-activate" onclick="switchModalTab('activate')" style="padding-bottom:12px; border-bottom:2px solid transparent; color:#111; font-size:1.1rem; cursor:pointer;">Test & Activate</div>
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
                        <th style="padding:16px; text-align:left;">SCHEDULE</th>
                        <th style="padding:16px; text-align:center;">SEND DATE</th>
                        <th style="padding:16px; text-align:center;">SELECT TEMPLATE</th>
                        <th style="padding:10px; text-align:right;">
                           <button onclick="addScheduleRow(this)" style="background:#3f51b5; color:#fff; border:none; padding:8px 16px; border-radius:2px; font-weight:bold; cursor:pointer; font-size:0.8rem; display:inline-flex; align-items:center; gap:6px;"><i data-lucide="plus" style="width:14px; height:14px;"></i> ADD SCHEDULE</button>
                        </th>
                     </tr>
                  </thead>
                  <tbody style="background:#fff; border-top:1px solid #e1e8f5;">
                     <tr style="border-bottom:1px solid #f0f0f0;">
                        <td style="padding:16px; color:#555; font-size:0.95rem; text-align:left;">1. Blast</td>
                        <td style="padding:16px; text-align:center;"><input type="date" value="2026-04-16" style="padding:8px; border:1px solid #ccc; border-radius:4px; color:#555; outline:none;"/></td>
                        <td style="padding:16px; text-align:center;">
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
                        <td style="padding:16px; color:#555; font-size:0.95rem; text-align:left;">2. Blast</td>
                        <td style="padding:16px; text-align:center;"><input type="date" value="2026-04-21" style="padding:8px; border:1px solid #ccc; border-radius:4px; color:#555; outline:none;"/></td>
                        <td style="padding:16px; text-align:center;">
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
         
         <!-- BODY: ACTIVATE -->
         <div id="modal-body-activate" style="display:none;">
            <div style="font-weight:bold; font-size:1.15rem; color:#111; margin-bottom:16px;">Test & Activate Configuration</div>
            
            <!-- Send Test -->
            <div style="background:#fff; border:1px solid #eee; padding:24px; margin-bottom:24px; border-radius:4px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
               <div style="font-weight:bold; font-size:1.05rem; color:#111; margin-bottom:8px;">1. Send Test Notification</div>
               <div style="color:#666; font-size:0.9rem; margin-bottom:16px;">Send a sample notification to your admin email address to verify the template configuration.</div>
               <div style="display:flex; gap:12px; align-items:center;">
                  <input type="email" placeholder="Enter admin email address..." style="flex:1; padding:10px 12px; border:1px solid #ccc; border-radius:4px; font-size:0.95rem; outline:none;" value="admin@helpingwithflags.com" />
                  <button style="background:#3f51b5; color:#fff; border:none; padding:11px 24px; border-radius:4px; font-size:0.95rem; font-weight:bold; cursor:pointer;" onclick="alert('Success! Test notification successfully simulated to admin email address.')">Send Test Notification</button>
               </div>
            </div>

            <!-- Activation Panel -->
            <div style="background:#fff; border:1px solid #eee; padding:24px; border-radius:4px; box-shadow:0 1px 3px rgba(0,0,0,0.02);">
               <div style="display:flex; justify-content:space-between; align-items:center;">
                  <div>
                     <div style="font-weight:bold; font-size:1.05rem; color:#111; margin-bottom:4px;">2. Schedule Activation</div>
                     <div style="color:#666; font-size:0.9rem;">Turn this configuration ON to begin automatically processing elements inside the bounded audience matrix.</div>
                  </div>
                  <!-- Native iOS-Style Toggle -->
                  <label style="position:relative; display:inline-block; width:52px; height:28px;">
                     <input type="checkbox" id="modal-activate-slider" checked style="opacity:0; width:0; height:0;" onchange="toggleScheduleActiveState(this.checked)" />
                     <span class="slider-bg" style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; transition:.4s; border-radius:28px;">
                        <span class="slider-dot" style="position:absolute; content:''; height:20px; width:20px; left:4px; bottom:4px; background-color:white; transition:.4s; border-radius:50%; box-shadow:0 1px 3px rgba(0,0,0,0.2);"></span>
                     </span>
                  </label>
               </div>
               <style>
                  .slider-bg { background-color: #ccc; }
                  #modal-activate-slider:checked + .slider-bg { background-color: #2ecc71 !important; }
                  #modal-activate-slider:checked + .slider-bg .slider-dot { transform: translateX(24px); }
               </style>
            </div>
         </div>
         
      </div>

      <!-- FOOTER -->
      <div style="padding:16px 20px; background:#fff; border-top:1px solid #ddd; display:flex; justify-content:flex-end; gap:12px; flex-shrink:0;">
         <button style="padding:10px 24px; background:#fff; border:1px solid #ccc; border-radius:4px; font-size:0.9rem; color:#555; cursor:pointer;" onclick="document.getElementById('schedule-edit-modal').style.display='none'">Cancel</button>
         <button id="modal-primary-action-btn" style="padding:10px 32px; background:#3f51b5; border:none; border-radius:4px; font-size:0.9rem; color:#fff; font-weight:bold; cursor:pointer;">Save & Next</button>
      </div>
   </div>
</div>

<!-- ── SCHEDULE SELECT MODAL ── -->
<div id="schedule-select-modal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:99999; align-items:center; justify-content:center; backdrop-filter:blur(2px);">
   <div style="background:#fff; border-radius:4px; box-shadow:0 12px 40px rgba(0,0,0,0.2); width:450px; border:1px solid #ddd; display:flex; flex-direction:column; overflow:hidden; font-family:Arial, sans-serif;">
      <!-- HEADER -->
      <div style="background:#f4f6f8; color:#555; padding:14px 20px; display:flex; align-items:center; justify-content:space-between; border-bottom:1px solid #eee;">
         <div style="margin:0; font-size:1.1rem; font-weight:bold; display:flex; align-items:center; gap:6px;">Choose a List</div>
         <i data-lucide="x" style="width:20px; height:20px; cursor:pointer; color:#888;" onclick="document.getElementById('schedule-select-modal').style.display='none'"></i>
      </div>
      <!-- BODY -->
      <div style="padding:24px; text-align:center;">
         <div style="font-size:1.05rem; color:#444; margin-bottom:24px; line-height:1.5;">Would you like to add a new schedule to the Email list or SMS/Text list?</div>
         <div style="display:flex; justify-content:center; gap:16px;">
            <button style="flex:1; padding:12px; background:#fff; border:2px solid #3f51b5; color:#3f51b5; border-radius:4px; font-weight:bold; cursor:pointer; font-size:0.95rem; display:flex; align-items:center; justify-content:center; gap:8px;" onclick="document.getElementById('schedule-select-modal').style.display='none'; document.getElementById('schedule-edit-modal').style.display='flex'; switchModalTab('filter');">
               <i data-lucide="mail" style="width:18px; height:18px;"></i> Email List
            </button>
            <button style="flex:1; padding:12px; background:#fff; border:2px solid #27ae60; color:#27ae60; border-radius:4px; font-weight:bold; cursor:pointer; font-size:0.95rem; display:flex; align-items:center; justify-content:center; gap:8px;" onclick="document.getElementById('schedule-select-modal').style.display='none'; document.getElementById('schedule-edit-modal').style.display='flex'; switchModalTab('filter');">
               <i data-lucide="message-square" style="width:18px; height:18px;"></i> SMS/Text
            </button>
         </div>
      </div>
   </div>
</div>

<script>
function switchModalTab(tab) {
    // Hide all bodies
    document.getElementById('modal-body-filter').style.display = 'none';
    document.getElementById('modal-body-schedule').style.display = 'none';
    document.getElementById('modal-body-results').style.display = 'none';
    document.getElementById('modal-body-activate').style.display = 'none';
    
    // Reset all headers
    ['filter', 'schedule', 'results', 'activate'].forEach(t => {
        let el = document.getElementById('modal-tab-head-' + t);
        el.style.borderBottom = '2px solid transparent';
        el.style.color = '#111';
    });
    
    // Show active body & style Header
    document.getElementById('modal-body-' + tab).style.display = 'block';
    let head = document.getElementById('modal-tab-head-' + tab);
    head.style.borderBottom = '2px solid #3f51b5';
    head.style.color = '#3f51b5';
    
    // Dynamic Action Button Logic
    let actionBtn = document.getElementById('modal-primary-action-btn');
    if (tab === 'activate') {
        actionBtn.innerText = 'Save Configuration';
        actionBtn.onclick = function() { document.getElementById('schedule-edit-modal').style.display='none'; };
    } else {
        actionBtn.innerText = 'Save & Next';
        let nextTab = tab === 'filter' ? 'schedule' : (tab === 'schedule' ? 'results' : 'activate');
        actionBtn.onclick = function() { switchModalTab(nextTab); };
    }
}

function toggleScheduleActiveState(isActive) {
    // Lookup the first green status indicator dot on the main schedule grid
    const dot = document.querySelector('#cfg-email tbody tr td div');
    if (dot) {
        dot.style.background = isActive ? '#2ecc71' : '#ccc';
        dot.style.boxShadow = isActive ? '0 1px 3px rgba(46,204,113,0.4)' : 'none';
    }
}

// Initialize Modal state machine arrays natively overriding static DOM HTML constraints
document.addEventListener('DOMContentLoaded', () => switchModalTab('filter'));
</script>
</body>"""

pattern = re.compile(r'<!-- ── SCHEDULE EDIT MODAL ── -->.*?</body>', re.DOTALL)
new_html = pattern.sub(modal_html, html)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(new_html)

print("success")
