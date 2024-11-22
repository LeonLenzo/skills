import yagmail
yagmail.register('leon.lenzo.1@gmail.com', 'golokpnruqcjmkcn')
yag = yagmail.SMTP('leon.lenzo.1@gmail.com')
yag.send(to='leon.lenzo.1@gmail.com', subject='Test Email', contents='This is a test email.')
