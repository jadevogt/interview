    if request.method == 'POST':
        #translate vrops alert severity to smc ticket severity. default to 2 medium
        smcticketseverity = 2
        if vrops_alert_object['alertcriticality'] == 'ALERT_CRITICALITY_LEVEL_CRITICAL':
            smcticketseverity = 3
        elif vrops_alert_object['alertcriticality'] == 'ALERT_CRITICALITY_LEVEL_IMMEDIATE':
            smcticketseverity = 3
        elif vrops_alert_object['alertcriticality'] == 'ALERT_CRITICALITY_LEVEL_WARNING':
            smcticketseverity = 2
        elif vrops_alert_object['alertcriticality'] == 'ALERT_CRITICALITY_LEVEL_INFORMATION':
            smcticketseverity = 1
        else:
            smcticketseverity = 2
        ticket_problem = 247
        new_ticket = Ticket_notes(asset_name, 'vrops', vrops_alert_object, None, alert_payload['status'])
        ticket_body = new_ticket.initial_ticket_note()
        if 'Error: No matching alert type' in ticket_body:
          return 'pong'
        assets = [asset_id]
        asset_active_tickets = smc_conn.get_asset_active_tickets(asset_id, ticket_subject)
        if asset_active_tickets == []:
            assets = [asset_id]
            response = smc_conn.create_ticket(customer_id, ticket_subject, ticket_problem, ticket_body, 'OSC', smcticketseverity, asset_list=assets)
            if response.ok:
                ticket_response = response.json()   
                ticket_id = ticket_response['payload'][0]['id']
                note_body = new_ticket.new_ticket_note()
                response = smc_conn.create_ticket_note(ticket_id, note_body, 2)
                return response.content
            else:
                return response.content
        else:
            return 'pong'
    else:
        return 'pong'
