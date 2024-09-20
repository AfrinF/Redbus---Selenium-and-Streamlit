# importing neccessary libraries
import pandas as pd
import pymysql
import streamlit as slt
from streamlit_option_menu import option_menu
import plotly.express as px
import time
from datetime import datetime

# Kerala bus
keralaList=[]
df_k=pd.read_csv("df_k.csv")
for i,r in df_k.iterrows():
    keralaList.append(r["Route_name"])

#Andhra Pradesh bus
andhraList=[]
df_A=pd.read_csv("df_A.csv")
for i,r in df_A.iterrows():
    andhraList.append(r["Route_name"])

#Telungana bus
TelanganaList=[]
df_T=pd.read_csv("df_T.csv")
for i,r in df_T.iterrows():
    TelanganaList.append(r["Route_name"])

#Goa bus
GoaList=[]
df_G=pd.read_csv("df_G.csv")
for i,r in df_G.iterrows():
    GoaList.append(r["Route_name"])

#Rajastan bus
RajasthanList=[]
df_R=pd.read_csv("df_R.csv")
for i,r in df_R.iterrows():
    RajasthanList.append(r["Route_name"])


# South Bengal bus 
sbengalList=[]
df_SB=pd.read_csv("df_SB.csv")
for i,r in df_SB.iterrows():
    sbengalList.append(r["Route_name"])

# Haryana bus
HaryanaList=[]
df_H=pd.read_csv("df_H.csv")
for i,r in df_H.iterrows():
    HaryanaList.append(r["Route_name"])

#Assam bus
assamList=[]
df_AS=pd.read_csv("df_AS.csv")
for i,r in df_AS.iterrows():
    assamList.append(r["Route_name"])

#Uttar Pradesh bus
uttarList=[]
df_UP=pd.read_csv("df_UP.csv")
for i,r in df_UP.iterrows():
    uttarList.append(r["Route_name"])

#West bengal bus
westList=[]
df_WB=pd.read_csv("df_WB.csv")
for i,r in df_WB.iterrows():
    westList.append(r["Route_name"])

#setting up streamlit page
slt.set_page_config(layout="wide")

web=option_menu(menu_title="🚌OnlineBus",
                options=["📍States and Routes"],
                orientation="horizontal"
                )

# States and Routes page setting
if web == "📍States and Routes":
    S = slt.selectbox("Lists of States", ["Adhra Pradesh" , "Assam" , "Goa" , "Haryana" , "Kerala" , "Rajastan" , 
                                           "South Bengal" , "Telugana" , "Uttar Pradesh" , "West Bengal"])
    
    col1,col2,col3=slt.columns(3)
    with col1:
        select_type = slt.radio("Choose bus type", ("sleeper", "semi-sleeper", "others"))
    with col2:
        select_fare = slt.radio("Choose bus fare range", ("50-1000", "1000-2000", "2000 and above"))
    with col3:
        select_actype = slt.radio("Choose ac or non-ac", ("AC", "Non-AC"))

    # TIME=slt.time_input("Select the time")

    # Kerala bus fare filtering
    if S == "Kerala":
        K = slt.selectbox("List of routes",keralaList)

        def type_and_fare(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  # assuming a high max value for "2000 and above"

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {bus_type_condition} 
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)
            
            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{K}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price,Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare(select_type, select_fare,select_actype)
        slt.dataframe(df_result)

    # Adhra Pradesh bus fare filtering
    if S=="Adhra Pradesh":
        A=slt.selectbox("list of routes",andhraList)

        def type_and_fare_A(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{A}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_A(select_type, select_fare,select_actype)
        slt.dataframe(df_result)
          

    # Telugana bus fare filtering
    if S=="Telugana":
        T=slt.selectbox("list of routes",TelanganaList)

        def type_and_fare_T(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{T}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{T}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_T(select_type, select_fare,select_actype)
        slt.dataframe(df_result)

    # Goa bus fare filtering
    if S=="Goa":
        G=slt.selectbox("list of routes",GoaList)

        def type_and_fare_G(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{G}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{G}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_G(select_type, select_fare,select_actype)
        slt.dataframe(df_result)

    # Rajastan bus fare filtering
    if S=="Rajastan":
        R=slt.selectbox("list of routes",RajasthanList)

        def type_and_fare_R(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{R}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{R}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_R(select_type, select_fare,select_actype)
        slt.dataframe(df_result)
          

    # South Bengal bus fare filtering       
    if S=="South Bengal":
        SB=slt.selectbox("list of rotes",sbengalList)

        def type_and_fare_SB(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{SB}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{SB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_SB(select_type, select_fare,select_actype)
        slt.dataframe(df_result)
    
    # Haryana bus fare filtering
    if S=="Haryana":
        H=slt.selectbox("list of rotes",HaryanaList)

        def type_and_fare_H(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{H}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{H}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()
            
            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_H(select_type, select_fare,select_actype)
        slt.dataframe(df_result)


    # Assam bus fare filtering
    if S=="Assam":
        AS=slt.selectbox("list of rotes",assamList)

        def type_and_fare_AS(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AS}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{AS}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_AS(select_type, select_fare,select_actype)
        slt.dataframe(df_result)

    # Utrra Pradesh bus fare filtering
    if S=="Utrra Pradesh":
        UP=slt.selectbox("list of rotes",uttarList)

        def type_and_fare_UP(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{UP}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{UP}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_UP(select_type, select_fare,select_actype)
        slt.dataframe(df_result)

    # West Bengal bus fare filtering
    if S=="West Bengal":
        WB=slt.selectbox("list of rotes",westList)

        def type_and_fare_WB(bus_type, fare_range,ac_type):
            conn = pymysql.connect(
                host="localhost",
                user="root",
                password="Sky1234",
                database="Red_Bus_Details"
            )
            my_cursor = conn.cursor()
            # Define fare range based on selection
            if fare_range == "50-1000":
                fare_min, fare_max = 50, 1000
            elif fare_range == "1000-2000":
                fare_min, fare_max = 1000, 2000
            else:
                fare_min, fare_max = 2000, 100000  

            # Define bus type condition
            if bus_type == "sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND ( Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "semi-sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Semi Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "sleeper" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type LIKE '%Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"
            elif bus_type == "others" and ac_type == "AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%AC%' OR Bus_type LIKE '%A/C%')"
            elif bus_type == "others" and ac_type == "Non-AC":
                bus_type_condition = "Bus_type NOT LIKE '%Sleeper%' AND Bus_type NOT LIKE '%Semi-Sleeper%' AND (Bus_type LIKE '%NON AC%' OR Bus_type LIKE '%NON A/C%')"

            query1 = f'''
                SELECT Start_time FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{WB}"
                AND {bus_type_condition}
            '''
            my_cursor.execute(query1)
            out = my_cursor.fetchall()
            available_times_dt = [datetime.strptime(time[0], "%H:%M").time() for time in out]
            TIME=slt.selectbox("Select the time", available_times_dt)

            query = f'''
                SELECT * FROM bus_details 
                WHERE Price BETWEEN {fare_min} AND {fare_max}
                AND Route_name = "{WB}"
                AND {bus_type_condition} AND Start_time>='{TIME}'
                ORDER BY Price and Start_time  DESC
            '''
            my_cursor.execute(query)
            out = my_cursor.fetchall()
            conn.close()

            df = pd.DataFrame(out, columns=[
                "ID", "Bus_name", "Bus_type", "Start_time", "End_time", "Total_duration",
                "Price", "Seats_Available", "Ratings", "Route_link", "Route_name"
            ])
            return df

        df_result = type_and_fare_WB(select_type, select_fare,select_actype)
        slt.dataframe(df_result)



