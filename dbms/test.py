from cs50 import SQL

db2 = SQL("sqlite:///hospitals.db")

hospitals = db2.execute("select * from hospitals ")

for hospital in hospitals:
    print(hospital['NAME'])