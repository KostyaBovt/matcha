import smtplib

# conn = psycopg2.connect("dbname=matcha user=vagrant");
# cur = conn.cursor()
# print conn
# print cur
# cur.execute("CREATE TABLE test2 (id serial PRIMARY KEY, num integer, data varchar);")
# conn.commit()
# print 'success'

from email.mime.text import MIMEText

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
# fp = open(textfile, 'rb')
# Create a text/plain message
# msg = MIMEText(fp.read())
msg = MIMEText("hello friend! this is your letter")
# fp.close()
 
me = 'no-reply@camagram.net'
you = 'kostya.bovt@gmail.com'
msg['Subject'] = 'topic'
msg['From'] = me
msg['To'] = you

# Send the message via our own SMTP server, but don't include the
# envelope header.
s = smtplib.SMTP(host='localhost', port=1025)
ret = s.sendmail(me, [you], msg.as_string())
print ret
s.quit()