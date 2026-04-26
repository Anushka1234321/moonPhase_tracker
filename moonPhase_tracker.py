import streamlit as st
from skyfield.api import load
from skyfield import almanac
import calendar
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import math

st.set_page_config(page_title="Moon Phase Tracker", page_icon="🌙", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600&family=Raleway:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'Raleway', sans-serif; background-color: #07090f; color: #e8e0ff; }
.stApp { background: radial-gradient(ellipse at 50% 0%, rgba(100,80,200,0.15), transparent 60%), #07090f; }
h1, h2, h3 { font-family: 'Cinzel', serif !important; color: #d4c9ff !important; }
.moon-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(180,160,255,0.2); border-radius: 20px; padding: 24px; text-align: center; margin: 10px 0; }
.stat-card { background: rgba(255,255,255,0.04); border: 1px solid rgba(180,160,255,0.15); border-radius: 12px; padding: 16px; margin: 6px 0; }
.countdown { font-family: 'Cinzel', serif; font-size: 32px; color: #d4c9ff; text-align: center; margin: 10px 0; }
.tide-info { background: rgba(0,100,180,0.15); border: 1px solid rgba(0,150,255,0.2); border-radius: 12px; padding: 16px; margin: 6px 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("# 🌙 Moon Phase Tracker")
st.markdown("<p style='color:rgba(212,201,255,0.5);margin-top:-12px;font-size:13px;font-family:Cinzel;'>LUNAR OBSERVATORY · PHASE TRACKER · TIDE GUIDE</p>", unsafe_allow_html=True)

@st.cache_resource
def load_ephemeris():
    ts = load.timescale()
    eph = load('de421.bsp')
    return ts, eph

def get_phase_info(phase_angle):
    if phase_angle < 45:    return "New Moon", "🌑", "The moon is not visible. Perfect for stargazing!"
    elif phase_angle < 90:  return "Waxing Crescent", "🌒", "A sliver of moon visible in the west after sunset."
    elif phase_angle < 135: return "First Quarter", "🌓", "Half the moon is lit. Rising around noon."
    elif phase_angle < 180: return "Waxing Gibbous", "🌔", "More than half lit, getting brighter each night."
    elif phase_angle < 220: return "Full Moon", "🌕", "Fully illuminated! Highest tides of the month."
    elif phase_angle < 270: return "Waning Gibbous", "🌖", "Past full moon, slowly getting darker."
    elif phase_angle < 315: return "Last Quarter", "🌗", "Half lit again, rising around midnight."
    else:                   return "Waning Crescent", "🌘", "A thin crescent visible before sunrise."

def get_tide_effect(phase_angle):
    if phase_angle < 20 or phase_angle > 340:
        return "🌊 SPRING TIDE", "Strongest tides! New Moon aligns sun, moon, and Earth.", "#4444ff"
    elif 170 < phase_angle < 210:
        return "🌊 SPRING TIDE", "Strongest tides! Full Moon creates powerful gravitational pull.", "#4444ff"
    elif 80 < phase_angle < 100 or 260 < phase_angle < 280:
        return "🏖️ NEAP TIDE", "Weakest tides. Sun and Moon are at right angles to Earth.", "#44aaff"
    else:
        strength = abs(math.cos(math.radians(phase_angle * 2))) * 100
        return "🌊 MODERATE TIDE", f"Moderate tidal forces. Strength: {strength:.0f}%", "#4488ff"

def days_to_next_full_moon(ts, eph, from_date):
    try:
        t0 = ts.utc(from_date.year, from_date.month, from_date.day)
        t1 = ts.utc(from_date.year, from_date.month, from_date.day + 35)
        times, phases = almanac.find_discrete(t0, t1, almanac.moon_phases(eph))
        for t, phase in zip(times, phases):
            if phase == 2:
                dt = t.utc_datetime().replace(tzinfo=None) - from_date
                return int(dt.days), t.utc_datetime()
    except:
        pass
    return None, None

rise_set_map = {
    "New Moon": ("6:00 AM", "6:00 PM"),
    "Waxing Crescent": ("9:00 AM", "9:00 PM"),
    "First Quarter": ("12:00 PM", "12:00 AM"),
    "Waxing Gibbous": ("3:00 PM", "3:00 AM"),
    "Full Moon": ("6:00 PM", "6:00 AM"),
    "Waning Gibbous": ("9:00 PM", "9:00 AM"),
    "Last Quarter": ("12:00 AM", "12:00 PM"),
    "Waning Crescent": ("3:00 AM", "3:00 PM"),
}

try:
    ts, eph = load_ephemeris()

    with st.sidebar:
        st.markdown("### 📍 Location")
        city = st.text_input("City", "New Delhi")
        lat = st.number_input("Latitude", -90.0, 90.0, 28.6, 0.1)
        lon = st.number_input("Longitude", -180.0, 180.0, 77.2, 0.1)
        st.divider()
        st.markdown("**About**")
        st.markdown("Track moon phases, tides, and lunar events for any date.")

    tab1, tab2, tab3 = st.tabs(["🌙 Today's Moon", "📅 Monthly Calendar", "🌊 Tide Guide"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Select Date", value=datetime.today())
        with col2:
            hour = st.slider("Hour (UTC)", 0, 23, 12)

        if st.button("🔍 Analyse Moon", use_container_width=True):
            t = ts.utc(date.year, date.month, date.day, hour, 0)
            phase_angle = almanac.moon_phase(eph, t).degrees
            illumination = almanac.fraction_illuminated(eph, 'moon', t) * 100
            phase, symbol, description = get_phase_info(phase_angle)
            tide_name, tide_desc, tide_color = get_tide_effect(phase_angle)
            days_left, full_moon_date = days_to_next_full_moon(ts, eph, datetime(date.year, date.month, date.day))
            rise_time, set_time = rise_set_map.get(phase, ("N/A", "N/A"))

            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"""
                <div class="moon-card">
                    <div style="font-size:80px">{symbol}</div>
                    <div style="font-family:Cinzel;font-size:20px;color:#d4c9ff;margin:8px 0">{phase}</div>
                    <div style="font-size:13px;color:rgba(232,224,255,0.6)">{description}</div>
                </div>""", unsafe_allow_html=True)

            with c2:
                st.markdown(f"""
                <div class="stat-card">
                    <div style="font-size:12px;color:rgba(212,201,255,0.6);font-family:Cinzel">ILLUMINATION</div>
                    <div style="font-size:36px;font-family:Cinzel;color:#d4c9ff">{illumination:.1f}%</div>
                </div>
                <div class="stat-card">
                    <div style="font-size:12px;color:rgba(212,201,255,0.6);font-family:Cinzel">🌙 MOONRISE</div>
                    <div style="font-size:22px;font-family:Cinzel;color:#d4c9ff">{rise_time}</div>
                </div>
                <div class="stat-card">
                    <div style="font-size:12px;color:rgba(212,201,255,0.6);font-family:Cinzel">🌑 MOONSET</div>
                    <div style="font-size:22px;font-family:Cinzel;color:#d4c9ff">{set_time}</div>
                </div>""", unsafe_allow_html=True)

            with c3:
                if days_left is not None:
                    st.markdown(f"""
                    <div class="stat-card" style="text-align:center">
                        <div style="font-size:12px;color:rgba(212,201,255,0.6);font-family:Cinzel">NEXT FULL MOON</div>
                        <div class="countdown">{days_left} days</div>
                        <div style="font-size:12px;color:rgba(232,224,255,0.4)">{full_moon_date.strftime('%B %d, %Y') if full_moon_date else ''}</div>
                    </div>""", unsafe_allow_html=True)
                st.markdown(f"""
                <div class="tide-info">
                    <div style="font-size:13px;color:{tide_color};font-family:Cinzel;font-weight:600">{tide_name}</div>
                    <div style="font-size:12px;color:rgba(232,224,255,0.7);margin-top:4px">{tide_desc}</div>
                </div>""", unsafe_allow_html=True)

            st.divider()
            graph_range = st.slider("Days range for graph", 3, 15, 7)
            selected_dt = datetime(date.year, date.month, date.day)
            days_list, illum_list, major = [], [], []
            for i in range(-graph_range, graph_range+1):
                d = selected_dt + timedelta(days=i)
                tg = ts.utc(d.year, d.month, d.day)
                pa = almanac.moon_phase(eph, tg).degrees
                il = almanac.fraction_illuminated(eph, 'moon', tg) * 100
                p, sym, _ = get_phase_info(pa)
                days_list.append(d.strftime("%b %d"))
                illum_list.append(il)
                if p in ["New Moon","First Quarter","Full Moon","Last Quarter"]:
                    major.append((len(days_list)-1, il, sym))

            fig, ax = plt.subplots(figsize=(10,3))
            fig.patch.set_facecolor('#07090f')
            ax.set_facecolor('#0d0f1a')
            ax.fill_between(range(len(days_list)), illum_list, alpha=0.2, color='#a78bfa')
            ax.plot(range(len(days_list)), illum_list, color='#a78bfa', linewidth=2, marker='o', markersize=4)
            ax.axvline(graph_range, linestyle='--', color='#f472b6', linewidth=1.5, label='Selected Date')
            for idx, il, sym in major:
                ax.text(idx, il+3, sym, fontsize=14, ha='center')
            ax.set_xticks(range(len(days_list)))
            ax.set_xticklabels(days_list, rotation=45, color='#a09ac0', fontsize=8)
            ax.tick_params(colors='#a09ac0')
            ax.set_ylabel("Illumination (%)", color='#a09ac0')
            ax.set_ylim(0, 115)
            ax.grid(True, alpha=0.1, color='#4040a0')
            for spine in ax.spines.values():
                spine.set_edgecolor('#2a2050')
            ax.legend(facecolor='#0d0f1a', labelcolor='#d4c9ff')
            plt.tight_layout()
            st.pyplot(fig)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            year = st.number_input("Year", 1900, 2100, datetime.today().year)
        with c2:
            month = st.selectbox("Month", range(1,13), format_func=lambda x: calendar.month_name[x], index=datetime.today().month-1)

        if st.button("📅 Show Calendar", use_container_width=True):
            days_in_month = calendar.monthrange(year, month)[1]
            rows, days_list, illum_list, major = [], [], [], []
            for day in range(1, days_in_month+1):
                t = ts.utc(year, month, day)
                pa = almanac.moon_phase(eph, t).degrees
                il = almanac.fraction_illuminated(eph, 'moon', t) * 100
                phase, sym, _ = get_phase_info(pa)
                days_list.append(day)
                illum_list.append(il)
                rows.append({"Date": f"{year}-{month:02d}-{day:02d}", "Phase": f"{sym} {phase}", "Illumination": f"{il:.1f}%"})
                if phase in ["New Moon","First Quarter","Full Moon","Last Quarter"]:
                    major.append((day-1, il, sym))

            st.dataframe(rows, use_container_width=True, height=300)
            fig, ax = plt.subplots(figsize=(10,4))
            fig.patch.set_facecolor('#07090f')
            ax.set_facecolor('#0d0f1a')
            ax.fill_between(days_list, illum_list, alpha=0.2, color='#a78bfa')
            ax.plot(days_list, illum_list, color='#a78bfa', linewidth=2, marker='o', markersize=4)
            for idx, il, sym in major:
                ax.text(days_list[idx], il+3, sym, fontsize=14, ha='center')
            ax.set_title(f"Moon — {calendar.month_name[month]} {year}", color='#d4c9ff', fontsize=13)
            ax.set_xlabel("Day", color='#a09ac0')
            ax.set_ylabel("Illumination (%)", color='#a09ac0')
            ax.tick_params(colors='#a09ac0')
            ax.set_ylim(0, 115)
            ax.grid(True, alpha=0.1, color='#4040a0')
            for spine in ax.spines.values():
                spine.set_edgecolor('#2a2050')
            plt.tight_layout()
            st.pyplot(fig)

    with tab3:
        st.markdown("### 🌊 Moon & Tides Guide")
        st.markdown("""<div class="tide-info">
            <h4 style="color:#4488ff;font-family:Cinzel">How the Moon Controls Tides</h4>
            <p>The Moon's gravity pulls Earth's oceans, creating tidal bulges. As Earth rotates, coastlines pass through these bulges — causing high and low tides twice daily.</p>
        </div>""", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("""<div class="stat-card">
                <h4 style="color:#4444ff;font-family:Cinzel">🌊 Spring Tides</h4>
                <p style="font-size:13px">At <b>New Moon</b> and <b>Full Moon</b> — Sun, Moon, and Earth align creating the strongest tides. Up to 20% stronger than average.</p>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("""<div class="stat-card">
                <h4 style="color:#44aaff;font-family:Cinzel">🏖️ Neap Tides</h4>
                <p style="font-size:13px">At <b>First</b> and <b>Last Quarter</b> — Sun and Moon at right angles creating the weakest tides. About 20% weaker than average.</p>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### 📊 Monthly Tide Strength Chart")
        date_t = st.date_input("Month", datetime.today(), key="tide_date")
        if st.button("🌊 Show Tide Chart", use_container_width=True):
            days_in_month = calendar.monthrange(date_t.year, date_t.month)[1]
            days_t, tide_strength = [], []
            for day in range(1, days_in_month+1):
                t = ts.utc(date_t.year, date_t.month, day)
                pa = almanac.moon_phase(eph, t).degrees
                strength = abs(math.cos(math.radians(pa))) * 100
                days_t.append(day)
                tide_strength.append(strength)

            fig, ax = plt.subplots(figsize=(10,3))
            fig.patch.set_facecolor('#07090f')
            ax.set_facecolor('#0d0f1a')
            ax.fill_between(days_t, tide_strength, alpha=0.3, color='#4488ff')
            ax.plot(days_t, tide_strength, color='#4488ff', linewidth=2)
            ax.set_title(f"Tide Strength — {calendar.month_name[date_t.month]} {date_t.year}", color='#d4c9ff')
            ax.set_xlabel("Day", color='#a09ac0')
            ax.set_ylabel("Tide Strength (%)", color='#a09ac0')
            ax.tick_params(colors='#a09ac0')
            ax.grid(True, alpha=0.1, color='#4040a0')
            for spine in ax.spines.values():
                spine.set_edgecolor('#2a2050')
            plt.tight_layout()
            st.pyplot(fig)

except Exception as e:
    st.error(f"Error: {str(e)}")
