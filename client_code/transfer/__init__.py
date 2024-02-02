from ._anvil_designer import transferTemplate
from anvil import *
#import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime

class transfer(transferTemplate):
  
    def __init__(self, user=None, **properties):
        # self.user = user
        # self.init_components(**properties)
        # self.label_1.text = f"Welcome to Green Gate Financial, {user['username']}"
        # Initialize self.user as a dictionary 
        self.init_components(**properties) 
        self.user = user
        # Set Form properties and Data Bindings.
        username = anvil.server.call('get_username', self.user['phone'])
        self.label_1.text = f"Welcome to Green Gate Financial, {username}"
        #currencies=anvil.server.call('get_user_currency',self.user['phone'])
        self.drop_down_2.items= ["INR","USD","EUR","GBP"]
        self.display()
        # Any code you write here will run before the form opens.

    def drop_down_1_change(self, **event_args):
      self.display()

    def display(self, **event_args):
      acc = self.drop_down_2.selected_value

    def button_1_click(self, **event_args):
        current_datetime = datetime.now()
        entered_phone_number = self.text_box_2.text
        transfer_amount = self.text_box_3.text
        cur=self.drop_down_2.selected_value
        
        # Use the phone number of the depositor to identify their account
        depositor_phone_number = self.user['phone']
        depositor_balance = anvil.server.call('get_accounts_emoney_using_phone_number', depositor_phone_number, self.drop_down_2.selected_value)

        # Use the entered phone number to identify the receiver's account
        receiver_balance = anvil.server.call('get_accounts_emoney_using_phone_number', entered_phone_number, self.drop_down_2.selected_value)

        # Check if 'e_money' is not None and not an empty string
        if receiver_balance['balance'] is not None:
            recieve = float(receiver_balance['balance'])
        else:
            recieve = 0.0  # or set a default value based on your application logic

        if receiver_balance['balance'] is None:
            anvil.server.call('update_rows_emoney_trasaction', entered_phone_number, str(0))
        
        if (transfer_amount < 5) or (transfer_amount > 50000):
            app_tables.wallet_users_transaction.add_row(
                  phone=depositor_phone_number,
                  fund=money_value,
                  date=current_datetime,
                  transaction_type="Debit",
                  transaction_status="Transfer",
                  receiver_phone=entered_phone_number
            )
            self.label_4.text = "Transfer amount should be between 5 and 50000 for a transfer Funds." 
        else:
            if float(depositor_balance['balance']) < transfer_amount:
                self.label_4.text = "Insufficient Funds in E-Wallet."
            else: 
                # calculating the money to be added in the receiver's end
                transfer_final_receive_amount = recieve + transfer_amount
                # calculating the money to be deducted in the depositor's end
                transfer_depositor_amount_final = float(depositor_balance['balance']) - transfer_amount
                # setting the value
                anvil.server.call('update_rows_emoney_trasaction', depositor_phone_number, str(transfer_depositor_amount_final))
                anvil.server.call('update_rows_emoney_trasaction', entered_phone_number, str(transfer_final_receive_amount))
                # Updating the daily limit
                # answer = float(self.user['limit']) - transfer_amount
                # anvil.server.call('update_daily_limit', self.user['username'], str(answer))
                self.label_4.text = "Money transferred successfully"

                app_tables.wallet_users_transaction.add_row(
                  phone=depositor_phone_number,
                  fund=money_value,
                  date=current_datetime,
                  transaction_type="Debit",
                  transaction_status="Transfer",
                  receiver_phone=entered_phone_number
                     
                )


    # def button_1_click(self, **event_args):
    #     current_datetime = datetime.now()
    #     #depoitor = self.text_box_1.text
    #     entered_phone_number = self.text_box_2.text
    #     transfer_amount = self.text_box_3.text
        
    #     depositor_wallet_id= anvil.server.call('generate_unique_id', self.user['username'], self.user['phone'])
    #     #getting the depositor's details
    #     fore_money_depositor = anvil.server.call('get_accounts_emoney_using_wallet_id', depositor_wallet_id)
    #     #getting the reciever's details
    #     fore_money_sent = anvil.server.call('get_accounts_emoney_using_wallet_id',wallet_id)
    #     # Check if 'e_money' is not None and not an empty string
    #     if fore_money_sent['e_money'] is not None and fore_money_sent['e_money'].strip() != '':
    #         recieve = float(fore_money_sent['e_money'])
    #     else:
    #         recieve = 0.0  # or set a default value based on your application logic

    #     if(fore_money_sent['e_money']== None):
    #       anvil.server.call('update_rows_emoney_trasaction',wallet_id, str(0))
    #     if (transfer_amount < 5) or (transfer_amount > 50000):
    #        app_tables.transactions.add_row(
    #              user=self.user['username'],
    #              e_wallet=f"{depositor_wallet_id} to {wallet_id}",
    #              money=f"₹-{transfer_amount}",
    #              date=current_datetime,
    #              transaction_type="E-wallet to E-wallet",
    #              proof="failed"
    #            )
    #        self.label_4.text = "Transfer amount should be between 5 and 50000 for a transfer Funds." 
    #     else:
    #        if float(fore_money_depositor['e_money']) < transfer_amount:
    #          self.label_4.text = "Insufficient Funds in E-Wallet."
    #        else: 
    #          #calculating the money to be added in the recieve's end
    #          transfer_fianl_sent_amount= recieve + transfer_amount
    #          #calculating the money to be deducted in the depositor's end
    #          transfer_amount_final = float(fore_money_depositor['e_money'])-transfer_amount
    #          #setting the value
    #          anvil.server.call('update_rows_emoney_trasaction',depositor_wallet_id, str(transfer_amount_final))
    #          anvil.server.call('update_rows_emoney_trasaction',wallet_id, str(transfer_fianl_sent_amount))
    #          #Updating the daily limit
    #          answer = float(self.user['limit'])- transfer_amount
    #          anvil.server.call('update_daily_limit', self.user['username'], str(answer))
    #          self.label_4.text = "Money transferred successfully"

    #          app_tables.transactions.add_row(
    #              user=self.user['username'],
    #              e_wallet=f"{depositor_wallet_id} to {wallet_id}",
    #              money=f"₹-{transfer_amount}",
    #              date=current_datetime,
    #              transaction_type="E-wallet to E-wallet",
    #              proof="success"
    #            )
    #     if self.user['top_up'] is not None and self.user['top_up']== True:
    #       for_emoney = anvil.server.call('get_accounts_emoney_with_user',self.user['username'])
    #       money_in_emoney= for_emoney['e_money']
    #       threshold =2000
    #       if float(money_in_emoney)< threshold:
    #         final= str(float(money_in_emoney) + 5000)
    #         print("hi there")
    #         if self.validate()== True:
    #           print("hi I'm sending user value")
    #           self.deduct_currencies(final)
    #           anvil.server.call('update_all_rows',self.user['username'], final)
    #         else:
    #           self.label_4.text = "Insufficient Funds put money in your casa account"
    #       else:
    #         return f"E-wallet balance ({money_in_emoney}) is above the threshold. No top-up needed."

    
            
          
    # def validate(self):
    #   currencies_table = app_tables.currencies.get(user=self.user['username'])
    #   conversion_usd = float(currencies_table['money_usd'])*80
    #   conversion_euro = float(currencies_table['money_euro'])*85
    #   conversion_swis = float(currencies_table['money_swis']) * 90
    #   conversion_inr = float(currencies_table['money_inr']) * 1
    #   if conversion_usd > 5000:
    #     return True
    #   elif conversion_euro  > 5000:
    #     return True
    #   elif conversion_swis > 5000:
    #     return True
    #   elif conversion_inr > 5000:
    #     return True
    #   else:
    #      return False
      
    # def deduct_currencies(self, amount):
    #   currencies_table = app_tables.currencies.get(user=self.user['username'])
    #   conversion_usd = float(currencies_table['money_usd'])*80
    #   conversion_euro = float(currencies_table['money_euro'])*85
    #   conversion_swis = float(currencies_table['money_swis']) * 90
    #   conversion_inr = float(currencies_table['money_inr']) * 1 
    #   if conversion_usd > 5000:
    #     currencies_table['money_usd'] = str((conversion_usd- 5000)/80)
    #     currencies_table.update()
    #   elif conversion_euro  > 5000:
    #     currencies_table['money_euro'] = str((conversion_euro- 5000)/85)
    #     currencies_table.update()
    #   elif conversion_swis > 5000:
    #     currencies_table['money_swis'] = str((conversion_swis - 5000) / 90)
    #     currencies_table.update()
    #   elif conversion_inr > 5000:
    #     currencies_table['money_inr'] = str((conversion_inr - 5000) / 1)
    #     currencies_table.update()
    #   else:
    #     self.label_4.text = "Insufficient funds"

    def link_8_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("service",user=self.user)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("deposit",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("transfer",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("withdraw",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("service",user=self.user)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home")





# from ._anvil_designer import transferTemplate
# from anvil import *
# import anvil.server
# import anvil.tables as tables
# import anvil.tables.query as q
# from anvil.tables import app_tables

# class transfer(transferTemplate):
#   def __init__(self, **properties):
#     # Set Form properties and Data Bindings.
#     self.init_components(**properties)

#     # Any code you write here will run before the form opens.
