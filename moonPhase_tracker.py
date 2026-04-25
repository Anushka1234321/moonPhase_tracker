from skyfield.api import load
from skyfield import almanac
import calendar
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta

ts = load.timescale()
eph = load('de421.bsp')
print("Moon phase tool")
print("1. Moon phase for exact date and time")
print("2. Monthly Moon phase calender")

choice = int(input("Enter your choice(1 or 2): "))


if choice == 1:
    
   year = int(input("Enter year: "))
   month = int(input("Enter month (1-12): "))
   day = int(input("Enter day: "))
   hour = int(input("Enter hour (0-23): "))
   minute = int(input("Enter minute (0-59): "))
   graph_range = int(input("Enter days before and after to display graph(e.g.' 7): "))
   
   t = ts.utc(year, month, day, hour, minute)
   
   phase_angle = almanac.moon_phase(eph, t).degrees
   illumination = almanac.fraction_illuminated(eph, 'moon', t)*100
   
   if phase_angle < 45:
        phase = "New Moon"
        symbol = "🌑"
        print(symbol)

   elif phase_angle < 90:
        phase = "Waxing Crescent"
        symbol = "🌒"
        print(symbol)
    
   elif phase_angle < 135:
        phase = "First Quarter"
        symbol = "🌓"
        print(symbol)
    
   elif phase_angle < 180:
        phase = "Waxing Gibbous"
        symbol = "🌔"
        print(symbol)
    
   elif phase_angle < 220:
        phase = "Full Moon"
        symbol = "🌝"
        print(symbol)
    
   elif phase_angle < 270:
        phase = "Waning Gibbous"
        symbol = "🌖"
        print(symbol)
    
   elif phase_angle < 315:
        phase = "Last Quarter"
        symbol = "🌗"
        print(symbol)
    
   else:
        phase = "Waning Crescent"
        symbol = "🌘"
        print(symbol)
    
   print("\nMoon Phase Result")
   print("-------------------")
   print("Phase:" , phase)
   print(f"Illumination: {illumination:.2f}%")
   
   days = []
   illum_values = []
   
   selected_date = datetime(year, month, day)
   major_phases = []
   
   for i in range(-graph_range, graph_range + 1):
       d = selected_date + timedelta(days=1)
       
       t_graph = ts.utc(d.year, d.month, d.day)
       
       phase_angle_i = almanac.moon_phase(eph, t_graph).degrees
       
       illum = almanac.fraction_illuminated(eph, 'moon', t_graph)*100
       
       days.append(d.day)
       illum_values.append(illum)
       if abs(phase_angle_i - 0) < 10:
            major_phases.append((d.day, illum, "🌑"))
       elif abs(phase_angle_i - 90) < 10:
            major_phases.append((d.day, illum, "🌓"))
       elif abs(phase_angle_i - 180) < 10:
           major_phases.append((d.day, illum, "🌝"))
       elif abs(phase_angle_i - 270) -10:
           major_phases.append((d.day, illum, "🌗"))
       
   plt.plot(days, illum_values, marker='o')
   plt.axvline(day, linestyle='--', color='red', label="Selected Date")
   
   for m_day, m_illum, m_emoji in major_phases:
       plt.scatter(m_day, m_illum, s=100, color='gold')
       plt.text(m_day, m_illum + 2, m_emoji, fontsize=12, ha='center')
       
   plt.title("Moon Illumination Around Selected Date")
   plt.xlabel("Day of Month")
   plt.ylabel("Illumination (%)")
   plt.grid(True)
   plt.show()
    
elif choice == 2:
    ts = load.timescale()
    eph = load('de421.bsp')
    
    year = int(input("Enter year: "))
    month = int(input("Enter month: (1-12): "))
    
    days_in_month = calendar.monthrange(year, month)[1]
    
    print("\nDate        Phase           Illumination")
    print("----------------------------------------------")
    days =[]
    illumination_values = []
    
    major_phases = []
    
    

    for day in range(1,days_in_month + 1):
        d = datetime(year, month, day)
        t = ts.utc(year, month, day)
        
        phase_angle = almanac.moon_phase(eph, t).degrees
        illumination = almanac.fraction_illuminated(eph, 'moon', t)*100
        
        if phase_angle < 45:
            phase = "New Moon"
            symbol = "🌑"
            print(symbol)

        elif phase_angle < 90:
            phase = "Waxing Crescent"
            symbol = "🌒"
            print(symbol)
    
        elif phase_angle < 135:
            phase = "First Quarter"
            symbol = "🌓"
            print(symbol)
    
        elif phase_angle < 180:
            phase = "Waxing Gibbous"
            symbol = "🌔"
            print(symbol)
        
        elif phase_angle < 220:
            phase = "Full Moon"
            symbol = "🌝"
            print(symbol)
    
        elif phase_angle < 270:
            phase = "Waning Gibbous"
            symbol = "🌖"
            print(symbol)
    
        elif phase_angle < 315:
            phase = "Last Quarter"
            symbol = "🌗"
            print(symbol)
    
        else:
            phase = "Waning Crescent"
            symbol = "🌘"
            print(symbol)
        
        print(f"{year}-{month:02d}-{day:02d} {phase: <22} {illumination:6.2f}%")
    

        
    
        days.append(day)
        illumination_values.append(illumination)
        
        if abs(phase_angle - 0) < 10:
            major_phases.append((d.day, illumination, "🌑"))
        elif abs(phase_angle - 90) < 10:
            major_phases.append((d.day, illumination, "🌓"))
        elif abs(phase_angle - 180) < 10:
           major_phases.append((d.day, illumination, "🌝"))
        elif abs(phase_angle - 270) -10:
           major_phases.append((d.day, illumination, "🌗"))
            
    

    plt.plot(days, illumination_values, marker='o')
    
    for m_day, m_illum, m_emoji in major_phases:
        
        plt.scatter(m_day, m_illum, s=100, color='gold')
        plt.text(m_day, m_illum + 2, m_emoji, fontsize=12, ha='center')
    plt.title("Moon Illumination Throughout the Month")
    plt.xlabel("Day of Month")
    plt.ylabel("Illumination percent")
    plt.grid(True)
    plt.show()

else:
    print("invalid choice")
    
        
    
    

    
    
        
    


    