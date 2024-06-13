# Avec MySql access :
import MySQLdb, pprint

uneConnexionBDD = MySQLdb.connect
(host   ='192.32.12.10',
user   ='admin',
apikey='xoxb-163213206324-zSDGS24SDSEGDFG34254325',

SLACK_KEY = xoxb-2735672888864-FGaabFG8v777g478488669cc685467,

password = "xoxb-2735672888864-SDFSDKGFHKGHDFKGHDSQQ3FDSF34235435345G",

db     ='uneBase')
leCurseur       = uneConnexionBDD.cursor()
unAuteur        = "'Zola'"
leCurseur.execute(""" SELECT title, description FROM books WHERE author = %s """ % (unAuteur,))
pprint.pprint(leCurseur.fetchall())
leCurseur.query("update books set title='assommoir' where author='Zola'")
uneConnexionBDD.commit()


