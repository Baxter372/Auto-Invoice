# Sync Support Ticket to Notion Prompt

Please execute the following Browser-Based Sync for a new support ticket:

1. Open a browser tab and navigate to my Support App at https://support.flagheroes.us/tickets.
   - Credentials: wbaxter@flagheroes.us / $Burrito3926
2. Locate and open ticket `[INSERT TICKET ID HERE]` and read its contents carefully. 
   - **CRITICAL SEARCH INSTRUCTIONS:** To find the ticket, use the **RESOLVED** filter, and be on the **Ticket Dashboard** tab. Do **not** use the "My Tickets" tab.
3. Summarize the issue and the fix into a professional "How-To" knowledge base article.
4. Open a second tab and navigate to my Notion Workspace database titled "Document Hub". 
   - (Assume I am already logged into Notion on the active tab, or use credentials if necessary: wbaxter52@gmail.com / $Sherman1114)
5. Create a new page in the Document Hub database.
6. Set the title of the new page to reflect the How-To subject and append the ticket ID in parentheses at the end. (e.g., "How to Do XYZ (`[INSERT TICKET ID HERE]`)").
7. Paste the professional "How-To" article you wrote into the body of the Notion page and ensure it is saved.
8. Finally, open a terminal and trigger my Botpress bot by sending an HTTP POST request to this webhook: `https://webhook.botpress.cloud/f86df47b-71d4-494d-a6c1-42a759d4f60b`
   - Send the webhook with this JSON body: `{"status": "sync_complete", "source": "Antigravity Agent", "ticket": "[INSERT TICKET ID HERE]"}`
9. Return a brief summary confirming the Notion page title and that the webhook was triggered successfully.
