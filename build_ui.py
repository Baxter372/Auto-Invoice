import re

def generate_list_view(section_id, active_label):
    rows = []
    
    mock_data = [
        {
           'name': 'This Years Pending Payment Subscribers',
           'date': 'Apr 30, 2026',
           'adv_filter': 'No',
           'schedule': 'Recurring Every 7 Days',
           'count': '212'
        },
        {
           'name': 'Last Years Pending Payment Subscribers',
           'date': 'Jun 15, 2026',
           'adv_filter': 'No',
           'schedule': 'Recurring Every 7 Days',
           'count': '22'
        },
        {
           'name': 'Expired Credit Card',
           'date': 'Jul 01, 2026',
           'adv_filter': 'No',
           'schedule': 'Custom',
           'count': '15'
        }
    ]
    
    for row in mock_data:
        
        row_html = f"""
        <tr style="border-bottom:1px solid #eee; transition: background 0.2s;" onmouseenter="this.style.background='#f8faff'" onmouseleave="this.style.background='transparent'">
            <td style="padding:16px 12px; text-align:center;">
                <div style="width:16px; height:16px; background:#2ecc71; border-radius:50%; margin:0 auto; box-shadow:0 1px 3px rgba(46,204,113,0.4);"></div>
            </td>
            <td style="padding:16px 12px; font-weight:bold; color:#111; font-size:0.85rem; max-width:200px; white-space:normal; text-align:left;">{row['name']}</td>
            <td style="padding:16px 12px; color:#555; font-size:0.85rem; text-align:center;">{row['date']}</td>
            <td style="padding:16px 12px; color:#555; font-size:0.85rem; text-align:center;">{row['adv_filter']}</td>
            <td style="padding:16px 12px; color:#555; font-size:0.85rem; max-width:140px; white-space:normal; text-align:left;">{row['schedule']}</td>
            <td style="padding:16px 12px; color:#111; font-weight:bold; font-size:0.9rem; text-align:center;">{row['count']}</td>
            <td style="padding:16px 12px; text-align:center; min-width:80px;">
                <i data-lucide="edit" style="width:18px; height:18px; color:#3f51b5; cursor:pointer; margin-right:8px;" onclick="document.getElementById('schedule-edit-modal').style.display='flex'"></i>
                <i data-lucide="trash-2" style="width:18px; height:18px; color:#e74c3c; cursor:pointer;"></i>
            </td>
        </tr>
        """
        rows.append(row_html)
        
    tbody_content = "".join(rows)

    html = f"""
    <div id="{section_id}" style="padding:20px; background:#fff; { "display:none;" if section_id == "cfg-sms" else ""}">
        <div style="border:1px solid #eee; border-radius:4px; box-shadow:0 1px 4px rgba(0,0,0,0.02); overflow-x:auto;">
            <table style="width:100%; border-collapse:collapse; text-align:left;">
                <thead>
                    <tr style="border-bottom:2px solid #f0f0f0; color:#111; font-size:0.85rem;">
                        <th style="padding:16px 12px; text-align:center; width:60px;">Status</th>
                        <th style="padding:16px 12px; text-align:left;">Schedule Name:</th>
                        <th style="padding:16px 12px; text-align:center;">Next Sch. Date</th>
                        <th style="padding:16px 12px; text-align:center;">ADV Filter</th>
                        <th style="padding:16px 12px; text-align:left;">Schedule</th>
                        <th style="padding:16px 12px; text-align:center;">Audience Count</th>
                        <th style="padding:16px 12px; text-align:center;">Action</th>
                    </tr>
                </thead>
                <tbody>
                    {tbody_content}
                </tbody>
            </table>
        </div>
    </div>
    """
    return html

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

email_layout = generate_list_view("cfg-email", "Email")
sms_layout = generate_list_view("cfg-sms", "SMS")

start_marker = '<div id="cfg-email"'
end_marker = '</div> <!-- closes main-left-col -->'

if start_marker in content:
    pre = content.split(start_marker)[0]
    post = content.split(end_marker, 1)[1]
    
    new_content = pre + email_layout + "\n" + sms_layout + "\n</div> <!-- /#main-panel-config -->\n</div></div>\n" + end_marker + post
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("SUCCESS")
else:
    print("FAILED TO FIND MARKER")
