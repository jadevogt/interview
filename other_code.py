 def get_asset_active_tickets(self, asset_id, subject_filter='', problem_filter=''):
    url=f'https://{self.host}/Asset/{asset_id}/Ticket'
    headers = {'Content-Type': 'application/json'}
    response = get(url, headers=headers, auth=(self.username, self.password))
    if response.ok:
      ticket_list = []
      ticket_status_exclusions = ['Resolved', 'Closed']
      asset_data = response.json()
      if asset_data['payload'] != []:        
        for ticket_item in asset_data['payload']:
          if subject_filter != '' and problem_filter != '' and ticket_item['status'] not in ticket_status_exclusions and subject_filter in ticket_item['subject'] and problem_filter in ticket_item['problem']:            
            ticket_list.append(ticket_item)
          elif subject_filter == '' and problem_filter != '' and ticket_item['status'] not in ticket_status_exclusions and problem_filter in ticket_item['problem']:            
            ticket_list.append(ticket_item)
          elif subject_filter != '' and problem_filter == '' and ticket_item['status'] not in ticket_status_exclusions and subject_filter in ticket_item['subject']:            
            ticket_list.append(ticket_item)
          elif subject_filter == '' and problem_filter == '' and ticket_item['status'] not in ticket_status_exclusions:
            ticket_list.append(ticket_item)
          else:
            pass
        return ticket_list
      else:
        return ticket_list
    else:
      asset_response = response.content
      result = f'Error: {asset_response}'
      return result
