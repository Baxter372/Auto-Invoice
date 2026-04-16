function switchMainTab(tabId) {
  document.getElementById('main-panel-dashboard').style.display = tabId==='dashboard'?'block':'none';
  document.getElementById('main-panel-history').style.display   = tabId==='history'?'block':'none';
  document.getElementById('main-panel-templates').style.display = tabId==='templates'?'block':'none';
  
  document.getElementById('mtab-dashboard').className = 'main-tab ' + (tabId==='dashboard'?'active':'');
  document.getElementById('mtab-history').className   = 'main-tab ' + (tabId==='history'?'active':'');
  document.getElementById('mtab-templates').className = 'main-tab ' + (tabId==='templates'?'active':'');
  lucide.createIcons();
}
const RATE = 0.049;

// ── State ────────────────────────────────────────────────────────
let curYear = '2026', curSub = 'email', curMode = 'sent', isFiltered = false;
const sortState   = { email:{ col:-1, dir:1 }, sms:{ col:-1, dir:1 } };
window._eRows = []; window._sRows = [];

// ── Master toggle ────────────────────────────────────────────────
let autoBillingState = 'off';
let smsBillingState = 'off';
const scheduleStatus = { email:'paused', sms:'paused' };

function updateConfigureBtn(){
  document.getElementById('configure-btn-wrap').style.display = (autoBillingState === 'on' || smsBillingState === 'on') ? 'block' : 'none';
}
function setAutoBilling(state){
  if(state === 'on' && autoBillingState !== 'on') {
    let m = document.getElementById('auto-bill-modal');
    if(!m) {
      const div = document.createElement('div');
      div.id = 'auto-bill-modal';
      div.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.5); z-index:999999999; display:flex; align-items:center; justify-content:center;';
      div.innerHTML = `
        <div style="width:400px;max-width:95vw;background:#fff;border-radius:10px;box-shadow:0 8px 32px rgba(0,0,0,0.3);overflow:hidden;font-family:Arial,sans-serif;">
          <div style="background:#2c3e8c;color:#fff;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;">
            <h3 style="margin:0;font-size:1.1rem;display:flex;align-items:center;gap:6px;">Enable Auto-Billing</h3>
            <button style="background:transparent;border:none;color:#fff;font-size:1.5rem;cursor:pointer;line-height:1;" onclick="document.getElementById('auto-bill-modal').style.display='none'">✕</button>
          </div>
          <div style="padding:20px;">
            <div style="font-weight:bold;color:#2c3e8c;font-size:1.1rem;margin-bottom:12px;">Approve Feature Addition</div>
            <p style="font-size:0.9rem;color:#444;line-height:1.5;margin:0;">Your monthly invoice will be updated with this additional charge of <strong>$5.00/mo</strong>. Cost will be prorated if turned on during the month.</p>
          </div>
          <div style="background:#f0f3f8;padding:12px 20px;display:flex;justify-content:flex-end;gap:10px;">
            <button style="padding:8px 16px;background:#ddd;border:none;border-radius:6px;cursor:pointer;font-weight:bold;color:#555;" onclick="document.getElementById('auto-bill-modal').style.display='none'">Cancel</button>
            <button style="padding:8px 16px;background:#27ae60;border:none;border-radius:6px;cursor:pointer;font-weight:bold;color:#fff;" onclick="applyAutoBilling('on')">Accept &amp; Enable</button>
          </div>
        </div>
      `;
      document.body.appendChild(div);
    } else {
      m.style.display = 'flex';
    }
    return;
  }
  applyAutoBilling(state);
}

function applyAutoBilling(state){
  autoBillingState = state;
  document.getElementById('ab-off').style.background = state==='off' ? '#e74c3c' : '#555';
  document.getElementById('ab-on').style.background  = state==='on'  ? '#27ae60' : '#555';
  document.getElementById('ab-sub-label').textContent = state==='on' ? 'Active - automated billing emails enabled.' : 'Automatic email notices for collections.';
  updateConfigureBtn();
  document.getElementById('auto-bill-modal').style.display='none';
}

function setSmsBilling(state){
  if(state === 'on' && smsBillingState !== 'on') {
    let m = document.getElementById('sms-bill-modal');
    if(!m) {
      const div = document.createElement('div');
      div.id = 'sms-bill-modal';
      div.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(0,0,0,0.5); z-index:999999999; display:flex; align-items:center; justify-content:center;';
      div.innerHTML = `
        <div style="width:440px;max-width:95vw;background:#fff;border-radius:10px;box-shadow:0 8px 32px rgba(0,0,0,0.3);overflow:hidden;font-family:Arial,sans-serif;">
          <div style="background:#2c3e8c;color:#fff;padding:14px 20px;display:flex;align-items:center;justify-content:space-between;">
            <h3 style="margin:0;font-size:1.1rem;display:flex;align-items:center;gap:6px;">Enable SMS/Text</h3>
            <button style="background:transparent;border:none;color:#fff;font-size:1.5rem;cursor:pointer;line-height:1;" onclick="document.getElementById('sms-bill-modal').style.display='none'">✕</button>
          </div>
          <div style="padding:20px;">
            <div style="font-weight:bold;color:#2c3e8c;font-size:1.1rem;margin-bottom:12px;">Approve Feature Addition</div>
            <p style="font-size:0.9rem;color:#444;line-height:1.5;margin-bottom:14px;">You are enabling the Premium SMS/Text feature. Standard text messages are billed per <strong>message block</strong> at a rate of <strong>$0.05 (5 cents)</strong> each.</p>
            <div style="background:#f9faff;border-left:3px solid #2c3e8c;padding:10px 14px;border-radius:4px;font-size:0.8rem;color:#555;line-height:1.4;">
              <strong>What is a Message Block?</strong><br>
              A standard telecom message block consists of 160 characters. Longer messages or messages containing special characters (like emojis) are automatically split and billed as multiple blocks.<br><br>
              <strong style="color:#2c3e8c;">Note:</strong> Our default Auto-Invoice SMS message is less than 160 characters.
            </div>
          </div>
          <div style="background:#f0f3f8;padding:12px 20px;display:flex;justify-content:flex-end;gap:10px;">
            <button style="padding:8px 16px;background:#ddd;border:none;border-radius:6px;cursor:pointer;font-weight:bold;color:#555;" onclick="document.getElementById('sms-bill-modal').style.display='none'">Cancel</button>
            <button style="padding:8px 16px;background:#27ae60;border:none;border-radius:6px;cursor:pointer;font-weight:bold;color:#fff;" onclick="applySmsBilling('on')">Accept &amp; Enable</button>
          </div>
        </div>
      `;
      document.body.appendChild(div);
    } else {
      m.style.display = 'flex';
    }
    return;
  }
  applySmsBilling(state);
}

function applySmsBilling(state){
  smsBillingState = state;
  document.getElementById('sms-off').style.background = state==='off' ? '#e74c3c' : '#555';
  document.getElementById('sms-on').style.background  = state==='on'  ? '#27ae60' : '#555';
  document.getElementById('sms-sub-label').textContent = state==='on' ? 'Active - targeted SMS enabled.' : 'Targeted SMS messaging to increase recovery.';
  updateConfigureBtn();
  document.getElementById('sms-bill-modal').style.display='none';
}

// ── Schedule Enabled/Paused ───────────────────────────────────────
function setScheduleStatus(type, status){
  scheduleStatus[type] = status;
  const eBtn = document.getElementById('cfg-'+type+'-enabled');
  const pBtn = document.getElementById('cfg-'+type+'-paused');
  const sched = document.getElementById('cfg-'+type+'-schedule');
  eBtn.style.background = status==='enabled' ? '#27ae60' : '#888';
  pBtn.style.background = status==='paused'  ? '#e67e22' : '#888';
  // Grey out schedule fields when paused
  sched.style.opacity      = status==='paused' ? '0.4' : '1';
  sched.style.pointerEvents= status==='paused' ? 'none' : 'auto';
}

// ── Data ─────────────────────────────────────────────────────────
const yearData = {
  '2026': {
    kpi: { total:'1,284', emailTotal:'724', smsTotal:'560', success:'87.4%', revenue:'$14,320', avgpay:'2.4 days', notContacted:'14' },
    cmp: { email:62, sms:74, both:38, ignored:18 },
    chart: { bars:[40,55,48,70,62,80,75,90], labels:['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar'] },
    retry: { first:642, second:213, third:87, noresp:18 },
    emailSent: { customers:'10', open:'60%', openSub:'6 of 10 opened', ctr:'30%', ctrSub:'3 of 10 clicked', bounce:'10%', pending:'1', failed:'2', unsub:'0', avgpay:'2.1 days' },
    smsSent: { segments:15, monthcost:'$0.7350', monthsub:'Mar 2026', yearcost:'$8.8200', yearsub:'2026 YTD', customers:'10', delivrate:'70%', delivSub:'7 of 10 delivered', failed:'1', optout:'1', avgpay:'1.8 days' },
    emailRows: [
      ['03/25/2026','<span class="badge sent">Sent</span>','John Smith<br><small>john.smith@email.com</small>','Subscription Expired','Expiration','<span class="badge opened">Yes</span>','<span class="badge sent">Yes</span>','1'],
      ['03/25/2026','<span class="badge failed">Failed</span>','Linda Garza<br><small>lgarza_old@yahoo.com</small>','Subscription Expired','Expiration','—','—','1'],
      ['03/24/2026','<span class="badge sent">Sent</span>','Mike Torres<br><small>mtorres@gmail.com</small>','Renew Subscription','Renewal','<span class="badge opened">Yes</span>','—','2'],
      ['03/24/2026','<span class="badge sent">Sent</span>','Sara Nguyen<br><small>sara.nguyen@outlook.com</small>','Subscription Expired','Expiration','—','—','1'],
      ['03/23/2026','<span class="badge pending">Pending</span>','DFW Flag Co.<br><small>billing@dfwflag.com</small>','Final Notice','Final','—','—','3'],
      ['03/23/2026','<span class="badge sent">Sent</span>','Carlos Rivera<br><small>crivera@hotmail.com</small>','Renew Subscription','Renewal','<span class="badge opened">Yes</span>','<span class="badge sent">Yes</span>','2'],
      ['03/22/2026','<span class="badge failed">Failed</span>','Lone Star Events<br><small>info@lonestarevents.net</small>','Subscription Expired','Expiration','—','—','1'],
      ['03/22/2026','<span class="badge sent">Sent</span>','Patricia Odom<br><small>podom@gmail.com</small>','Final Notice','Final','<span class="badge opened">Yes</span>','—','3'],
      ['03/21/2026','<span class="badge sent">Sent</span>','Texas Flag Supply<br><small>orders@txflagsupply.com</small>','Subscription Expired','Expiration','<span class="badge opened">Yes</span>','<span class="badge sent">Yes</span>','1'],
      ['03/20/2026','<span class="badge sent">Sent</span>','James Whitfield<br><small>jwhitfield@work.com</small>','Renew Subscription','Renewal','—','—','2'],
    ],
    smsRows: [
      ['03/25/2026','<span class="badge sent">Delivered</span>','John Smith<br><small>(214) 555-0182</small>',1,'1','Dallas Flag Club'],
      ['03/25/2026','<span class="badge failed">Failed</span>','Linda Garza<br><small>(972) 555-0344</small>',1,'1','Plano Flags'],
      ['03/24/2026','<span class="badge sent">Delivered</span>','Mike Torres<br><small>(469) 555-0217</small>',2,'2','Arlington Flags'],
      ['03/24/2026','<span class="badge pending">Pending</span>','Sara Nguyen<br><small>(817) 555-0093</small>',1,'1','Fort Worth Flags'],
      ['03/23/2026','<span class="badge sent">Delivered</span>','Carlos Rivera<br><small>(214) 555-0456</small>',2,'2','Dallas Flag Club'],
      ['03/23/2026','<span class="badge failed">Opted Out</span>','DFW Flag Co.<br><small>(972) 555-0781</small>',1,'3','Plano Flags'],
      ['03/22/2026','<span class="badge sent">Delivered</span>','Patricia Odom<br><small>(469) 555-0329</small>',1,'3','Arlington Flags'],
      ['03/22/2026','<span class="badge sent">Delivered</span>','Texas Flag Supply<br><small>(817) 555-0614</small>',3,'1','Fort Worth Flags'],
      ['03/21/2026','<span class="badge pending">Pending</span>','James Whitfield<br><small>(214) 555-0508</small>',1,'2','Dallas Flag Club'],
      ['03/20/2026','<span class="badge sent">Delivered</span>','Lone Star Events<br><small>(972) 555-0867</small>',2,'1','Plano Flags'],
    ]
  },
  '2025': {
    kpi: { total:'987', emailTotal:'561', smsTotal:'426', success:'81.2%', revenue:'$10,740', avgpay:'3.1 days', notContacted:'22' },
    cmp: { email:54, sms:67, both:29, ignored:24 },
    chart: { bars:[30,42,38,55,50,65,60,72], labels:['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar'] },
    retry: { first:510, second:178, third:94, noresp:24 },
    emailSent: { customers:'8', open:'51%', openSub:'4 of 8 opened', ctr:'25%', ctrSub:'2 of 8 clicked', bounce:'15%', pending:'0', failed:'3', unsub:'1', avgpay:'3.4 days' },
    smsSent: { segments:11, monthcost:'$0.3920', monthsub:'Oct 2025', yearcost:'$5.9290', yearsub:'2025 YTD', customers:'8', delivrate:'62%', delivSub:'5 of 8 delivered', failed:'2', optout:'2', avgpay:'2.6 days' },
    emailRows: [
      ['10/14/2025','<span class="badge sent">Sent</span>','Brian Nguyen<br><small>bnguyen@gmail.com</small>','Subscription Expired','Expiration','<span class="badge opened">Yes</span>','—','1'],
      ['10/12/2025','<span class="badge failed">Failed</span>','Gulf Coast Flags<br><small>info@gulfcoastflags.com</small>','Subscription Expired','Expiration','—','—','1'],
      ['10/10/2025','<span class="badge sent">Sent</span>','Angela Kim<br><small>akim@outlook.com</small>','Renew Subscription','Renewal','<span class="badge opened">Yes</span>','<span class="badge sent">Yes</span>','2'],
      ['10/08/2025','<span class="badge sent">Sent</span>','Heritage Flag Co.<br><small>orders@heritageflag.com</small>','Final Notice','Final','—','—','3'],
      ['10/05/2025','<span class="badge failed">Failed</span>','Roy Duncan<br><small>rduncan@work.net</small>','Subscription Expired','Expiration','—','—','1'],
      ['10/03/2025','<span class="badge sent">Sent</span>','Melody Shaw<br><small>mshaw@gmail.com</small>','Renew Subscription','Renewal','<span class="badge opened">Yes</span>','—','2'],
      ['09/28/2025','<span class="badge sent">Sent</span>','Panhandle Banners<br><small>hello@panhandlebanners.com</small>','Subscription Expired','Expiration','—','—','1'],
      ['09/25/2025','<span class="badge failed">Failed</span>','Travis Cole<br><small>tcole@yahoo.com</small>','Final Notice','Final','—','—','3'],
    ],
    smsRows: [
      ['10/14/2025','<span class="badge sent">Delivered</span>','Brian Nguyen<br><small>(214) 555-0143</small>',1,'1','Dallas Flag Club'],
      ['10/12/2025','<span class="badge failed">Failed</span>','Gulf Coast Flags<br><small>(713) 555-0284</small>',1,'1','Houston Flags'],
      ['10/10/2025','<span class="badge sent">Delivered</span>','Angela Kim<br><small>(972) 555-0319</small>',2,'2','Plano Flags'],
      ['10/08/2025','<span class="badge failed">Opted Out</span>','Heritage Flag Co.<br><small>(817) 555-0452</small>',1,'3','Fort Worth Flags'],
      ['10/05/2025','<span class="badge sent">Delivered</span>','Melody Shaw<br><small>(469) 555-0517</small>',1,'2','Arlington Flags'],
      ['09/28/2025','<span class="badge sent">Delivered</span>','Panhandle Banners<br><small>(806) 555-0628</small>',2,'1','Amarillo Flags'],
      ['09/25/2025','<span class="badge failed">Failed</span>','Travis Cole<br><small>(214) 555-0761</small>',1,'3','Dallas Flag Club'],
    ]
  }
};

const scheduledEmailRows = [
  ['03/30/2026','<span class="badge pending">Scheduled</span>','Robert Chen<br><small>rchen@gmail.com</small>','Subscription Expired','Expiration','—','—','1'],
  ['03/30/2026','<span class="badge pending">Scheduled</span>','Alicia Monroe<br><small>amonroe@outlook.com</small>','Renew Subscription','Renewal','—','—','2'],
  ['03/31/2026','<span class="badge pending">Scheduled</span>','Sunrise Flag Co.<br><small>info@sunriseflag.com</small>','Subscription Expired','Expiration','—','—','1'],
  ['03/31/2026','<span class="badge pending">Scheduled</span>','David Patel<br><small>dpatel@work.com</small>','Final Notice','Final','—','—','3'],
  ['04/01/2026','<span class="badge pending">Scheduled</span>','Maria Castillo<br><small>mcastillo@gmail.com</small>','Subscription Expired','Expiration','—','—','1'],
  ['04/01/2026','<span class="badge pending">Scheduled</span>','TX Banner Supply<br><small>orders@txbanner.com</small>','Renew Subscription','Renewal','—','—','2'],
  ['04/02/2026','<span class="badge pending">Scheduled</span>','Kevin Brooks<br><small>kbrooks@hotmail.com</small>','Final Notice','Final','—','—','3'],
];
const scheduledSmsRows = [
  ['03/30/2026','<span class="badge pending">Scheduled</span>','Robert Chen<br><small>(214) 555-0192</small>',1,'1','Dallas Flag Club'],
  ['03/30/2026','<span class="badge pending">Scheduled</span>','Alicia Monroe<br><small>(972) 555-0417</small>',2,'2','Plano Flags'],
  ['03/31/2026','<span class="badge pending">Scheduled</span>','Sunrise Flag Co.<br><small>(469) 555-0284</small>',1,'1','Arlington Flags'],
  ['03/31/2026','<span class="badge pending">Scheduled</span>','David Patel<br><small>(817) 555-0339</small>',1,'3','Fort Worth Flags'],
  ['04/01/2026','<span class="badge pending">Scheduled</span>','Maria Castillo<br><small>(214) 555-0561</small>',2,'1','Dallas Flag Club'],
  ['04/02/2026','<span class="badge pending">Scheduled</span>','Kevin Brooks<br><small>(972) 555-0748</small>',1,'3','Plano Flags'],
];
const ignoredEmailRows = [
  ['03/10/2026','<span class="badge failed">No Response</span>','Patricia Odom<br><small>podom@gmail.com</small>','Final Notice','Final','—','—','3'],
  ['03/08/2026','<span class="badge failed">No Response</span>','Linda Garza<br><small>lgarza_old@yahoo.com</small>','Final Notice','Final','—','—','3'],
  ['03/06/2026','<span class="badge failed">No Response</span>','DFW Flag Co.<br><small>billing@dfwflag.com</small>','Final Notice','Final','—','—','3'],
];
const ignoredSmsRows = [
  ['03/10/2026','<span class="badge failed">No Response</span>','Patricia Odom<br><small>(469) 555-0329</small>',1,'3','Arlington Flags'],
  ['03/08/2026','<span class="badge failed">No Response</span>','DFW Flag Co.<br><small>(972) 555-0781</small>',1,'3','Plano Flags'],
  ['03/06/2026','<span class="badge failed">No Response</span>','James Whitfield<br><small>(214) 555-0508</small>',1,'3','Dallas Flag Club'],
];

// ── Init ─────────────────────────────────────────────────────────
window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.ai-feature-row[data-tip]').forEach(el => {
    const tip = el.querySelector('.ai-tooltip');
    if(tip) tip.textContent = el.getAttribute('data-tip');
  });
  updateConfigureBtn();
  // Initialize Email & SMS schedules as Paused by default
  setScheduleStatus('email','paused');
  setScheduleStatus('sms','paused');
  renderTables();
});

// ── Render tables ────────────────────────────────────────────────
function renderTables(){
  const d = yearData[curYear];
  window._eRows = curMode==='scheduled' ? scheduledEmailRows : (isFiltered ? ignoredEmailRows : d.emailRows);
  window._sRows = curMode==='scheduled' ? scheduledSmsRows  : (isFiltered ? ignoredSmsRows  : d.smsRows);
  document.getElementById('email-tbody').innerHTML = window._eRows.map((r,i)=>
    `<tr>${r.map(c=>`<td>${c}</td>`).join('')}<td><a href="#" onclick="openEmailPreviewIdx(${i});return false;" style="color:#2c3e8c;font-size:0.78rem;">View</a></td></tr>`
  ).join('');
  document.getElementById('sms-tbody').innerHTML = window._sRows.map((r,i)=>{
    const cost = (r[3]*RATE).toFixed(4);
    return `<tr><td>${r[0]}</td><td>${r[1]}</td><td>${r[2]}</td><td>${r[3]}</td><td>$${cost}</td><td>${r[4]}</td><td>${r[5]}</td><td><a href="#" onclick="openSmsPreviewIdx(${i});return false;" style="color:#2c3e8c;font-size:0.78rem;">View</a></td></tr>`;
  }).join('');
}

// ── Year switch ──────────────────────────────────────────────────
function switchYear(yr){
  curYear = yr;
  const d = yearData[yr];
  document.getElementById('year-badge').textContent = 'Showing: '+yr;
  document.getElementById('ov-total').textContent        = d.kpi.total;
  document.getElementById('ov-email-total').textContent  = d.kpi.emailTotal;
  document.getElementById('ov-sms-total').textContent    = d.kpi.smsTotal;
  document.getElementById('ov-success').textContent      = d.kpi.success;
  document.getElementById('ov-revenue').textContent      = d.kpi.revenue;
  document.getElementById('ov-avgpay').textContent       = d.kpi.avgpay;
  document.getElementById('ov-notcontacted').textContent = d.kpi.notContacted;
  document.getElementById('cmp-email-bar').style.width   = d.cmp.email+'%';
  document.getElementById('cmp-sms-bar').style.width     = d.cmp.sms+'%';
  document.getElementById('cmp-both-bar').style.width    = d.cmp.both+'%';
  document.getElementById('cmp-email-pct').textContent   = d.cmp.email+'%';
  document.getElementById('cmp-sms-pct').textContent     = d.cmp.sms+'%';
  document.getElementById('cmp-both-pct').textContent    = d.cmp.both+'%';
  document.getElementById('cmp-ignored-val').textContent = d.cmp.ignored;
  const em = d.emailSent;
  document.getElementById('me-customers').textContent = em.customers;
  document.getElementById('me-open').textContent      = em.open;
  document.getElementById('me-open-sub').textContent  = em.openSub;
  document.getElementById('me-ctr').textContent       = em.ctr;
  document.getElementById('me-ctr-sub').textContent   = em.ctrSub;
  document.getElementById('me-bounce').textContent    = em.bounce;
  document.getElementById('me-pending').textContent   = em.pending;
  document.getElementById('me-failed').textContent    = em.failed;
  document.getElementById('me-unsub').textContent     = em.unsub;
  document.getElementById('me-avgpay').textContent    = em.avgpay;
  const sm = d.smsSent;
  document.getElementById('ms-cpc').textContent       = '$'+(sm.segments*RATE/parseInt(sm.customers)).toFixed(2);
  document.getElementById('ms-monthcost').textContent = sm.monthcost;
  document.getElementById('ms-monthsub').textContent  = sm.monthsub;
  document.getElementById('ms-yearcost').textContent  = sm.yearcost;
  document.getElementById('ms-yearsub').textContent   = sm.yearsub;
  document.getElementById('ms-segments').textContent  = sm.segments;
  document.getElementById('ms-delivrate').textContent = sm.delivrate;
  document.getElementById('ms-deliv-sub').textContent = sm.delivSub;
  document.getElementById('ms-customers').textContent = sm.customers;
  document.getElementById('ms-avgpay').textContent    = sm.avgpay;
  document.getElementById('ms-failed').textContent    = sm.failed;
  document.getElementById('ms-optout').textContent    = sm.optout;
  const r = d.retry;
  document.getElementById('r-first').textContent      = r.first;
  document.getElementById('r-second').textContent     = r.second;
  document.getElementById('r-third').textContent      = r.third;
  document.getElementById('r-noresp').textContent     = r.noresp;
  document.getElementById('r-second-bar').style.width = Math.round(r.second/r.first*100)+'%';
  document.getElementById('r-third-bar').style.width  = Math.round(r.third/r.first*100)+'%';
  document.querySelectorAll('#trend-chart .mini-bar').forEach((b,i)=>{ b.style.height=d.chart.bars[i]+'%'; });
  document.querySelectorAll('#trend-labels span').forEach((s,i)=>{ s.textContent=d.chart.labels[i]; });
  if(isFiltered) clearIgnoredFilter();
  renderTables();
}

// ── Navigation ───────────────────────────────────────────────────
function switchSub(type){
  curSub = type;
  document.getElementById('panel-email').style.display = type==='email' ? '' : 'none';
  document.getElementById('panel-sms').style.display   = type==='sms'   ? '' : 'none';
  document.getElementById('btn-email').className = 'sub-tab '+(type==='email'?'active':'inactive');
  document.getElementById('btn-sms').className   = 'sub-tab '+(type==='sms'  ?'active':'inactive');
}
function switchListMode(mode){
  curMode = mode;
  const s = mode==='scheduled';
  document.getElementById('me-sent').style.display  = s ? 'none'  : 'block';
  document.getElementById('me-sched').style.display = s ? 'block' : 'none';
  document.getElementById('ms-sent').style.display  = s ? 'none'  : 'block';
  document.getElementById('ms-sched').style.display = s ? 'block' : 'none';
  if(isFiltered) clearIgnoredFilter();
  renderTables();
}
function switchMetric(btn, id){
  document.querySelectorAll('.metric-tab').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.metric-panel').forEach(p=>p.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById(id).classList.add('active');
}

// ── Filter ───────────────────────────────────────────────────────
function filterIgnored(){ isFiltered=true; document.getElementById('filter-banner').style.display='flex'; renderTables(); }
function clearIgnoredFilter(){ isFiltered=false; document.getElementById('filter-banner').style.display='none'; renderTables(); }

// ── Sort / column filter ─────────────────────────────────────────
function getCellText(td){ return td ? td.innerText.trim().toLowerCase() : ''; }
function sortTable(type, col){
  const ss = sortState[type];
  ss.dir = ss.col===col ? ss.dir*-1 : 1; ss.col = col;
  document.querySelectorAll('#'+type+'-table thead tr:first-child th.sortable').forEach((th,i)=>{
    th.classList.remove('sort-asc','sort-desc');
    if(i===col) th.classList.add(ss.dir===1?'sort-asc':'sort-desc');
  });
  applyColFilter(type);
}
function applyColFilter(type){
  const tbody   = document.getElementById(type+'-tbody');
  const rows    = Array.from(tbody.querySelectorAll('tr'));
  const filters = Array.from(document.getElementById(type+'-filter-row').querySelectorAll('input,select')).map(el=>el.value.toLowerCase().trim());
  const ss      = sortState[type];
  rows.forEach(tr=>{
    const cells = Array.from(tr.querySelectorAll('td'));
    tr.style.display = filters.every((f,i)=>!f||getCellText(cells[i]).includes(f)) ? '' : 'none';
  });
  if(ss.col>=0){
    Array.from(tbody.querySelectorAll('tr:not([style*="none"])')).sort((a,b)=>{
      const aT=getCellText(a.querySelectorAll('td')[ss.col]), bT=getCellText(b.querySelectorAll('td')[ss.col]);
      return aT<bT?-ss.dir:aT>bT?ss.dir:0;
    }).forEach(r=>tbody.appendChild(r));
  }
}

// ── Config modal ─────────────────────────────────────────────────
function openConfig()  { document.getElementById('config-modal').style.display='flex'; }
function closeConfig() { document.getElementById('config-modal').style.display='none'; }
function switchCfgTab(tab){
  document.getElementById('cfg-email').style.display = tab==='email'?'block':'none';
  document.getElementById('cfg-sms').style.display   = tab==='sms'  ?'block':'none';
  const eBtn = document.getElementById('cfg-tab-email');
  const sBtn = document.getElementById('cfg-tab-sms');
  eBtn.style.background    = tab==='email' ? '#fff' : '#888';
  eBtn.style.color         = tab==='email' ? '#2c3e8c' : '#fff';
  eBtn.style.borderBottom  = tab==='email' ? '3px solid #fff' : '3px solid transparent';
  sBtn.style.background    = tab==='sms'   ? '#fff' : '#888';
  sBtn.style.color         = tab==='sms'   ? '#2c3e8c' : '#fff';
  sBtn.style.borderBottom  = tab==='sms'   ? '3px solid #fff' : '3px solid transparent';
}

// ── Email preview ────────────────────────────────────────────────
function openEmailPreviewIdx(idx){
  const r = window._eRows[idx];
  const clean = r[2].replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  document.getElementById('preview-recipient').textContent = clean;
  document.getElementById('preview-notice').textContent   = r[7];
  document.getElementById('preview-date').textContent     = r[0];
  document.getElementById('prev-name').textContent        = clean.split(' ').slice(0,2).join(' ');
  document.getElementById('email-preview-modal').style.display='flex';
}
function closeEmailPreview(){ document.getElementById('email-preview-modal').style.display='none'; }

// ── SMS preview ──────────────────────────────────────────────────
function openSmsPreviewIdx(idx){
  const r = window._sRows[idx];
  const segs  = r[3];
  const cost  = (segs*RATE).toFixed(4);
  const clean = r[2].replace(/<[^>]+>/g,' ').replace(/\s+/g,' ').trim();
  const parts = clean.split('  ');
  const name  = (parts[0]||clean).trim();
  const phone = (parts[1]||'').trim();
  const status = r[1].replace(/<[^>]+>/g,'');
  const msg = `Hi ${name}, this is a reminder from HelpingWithFlags.com that your annual Holiday Flag subscription is now due.\n\nAmount Due: $75.00\n\nPay online: https://app.helpingwithflags.com/pay\n\nReply STOP to opt out.`;
  const segCount = Math.ceil(msg.length/160);
  document.getElementById('sms-preview-recipient').textContent = (name+' '+phone).trim();
  document.getElementById('sms-preview-notice').textContent   = r[4];
  document.getElementById('sms-preview-date').textContent     = r[0];
  document.getElementById('sms-preview-timestamp').textContent= r[0]+', 9:41 AM';
  document.getElementById('sms-bubble-text').innerText        = msg;
  document.getElementById('sms-segment-info').textContent     = segCount+' segment'+(segCount>1?'s':'')+' · $'+cost;
  document.getElementById('sms-meta-segments').textContent    = segs;
  document.getElementById('sms-meta-cost').textContent        = '$'+cost;
  const st = document.getElementById('sms-meta-status');
  st.textContent = status;
  st.style.color = status==='Delivered'?'#27ae60':(status==='Pending'||status==='Scheduled')?'#e67e22':'#e74c3c';
  document.getElementById('sms-preview-modal').style.display='flex';
}
function closeSmsPreview(){ document.getElementById('sms-preview-modal').style.display='none'; }
