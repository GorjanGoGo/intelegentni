import json
import streamlit as st

# LOAD DATA
def load_data():
    with open("database.json", "r", encoding="utf-8") as f:
        return json.load(f)["people"]

people = load_data()

# SAFE GET
def get(p, key):
    return p.get(key, False)

# INIT SESSION
if "pool" not in st.session_state:
    st.session_state.pool = people

if "asked" not in st.session_state:
    st.session_state.asked = set()

if "stage" not in st.session_state:
    st.session_state.stage = "role"

# BEST QUESTION
def best_question(pool):
    keys = set()

    for p in pool:
        for k, v in p.items():
            if isinstance(v, bool):
                keys.add(k)

    if any("gender" in p for p in pool):
        keys.add("gender")

    if any("elective_subject" in p for p in pool):
        keys.add("elective_subject")

    best_key = None
    best_score = -1

    for k in keys:
        if k in st.session_state.asked:
            continue

        if k == "gender":
            yes = sum(1 for p in pool if p.get("gender") == "male")
            no = sum(1 for p in pool if p.get("gender") == "female")

        elif k == "elective_subject":
            yes = sum(1 for p in pool if p.get("elective_subject") == "advanced_programming")
            no = sum(1 for p in pool if p.get("elective_subject") == "graphs")

        else:
            yes = sum(1 for p in pool if p.get(k) is True)
            no = sum(1 for p in pool if p.get(k) is False)

        if yes == 0 and no == 0:
            continue

        score = min(yes, no)

        if score > best_score:
            best_score = score
            best_key = k

    return best_key

# AREA GUESS
def area_guess(pool):
    areas = sorted({p.get("area") for p in pool if p.get("area")})

    if len(pool) > 3 or len(areas) == 0:
        return None

    for area in areas:
        if area in st.session_state.asked:
            continue
        return area

    return None


def make_area_question(area):
    mapping = {
        "Aerodrom": "Дали е од Аеродром?",
        "Kisela Voda": "Дали е од Кисела Вода?",
        "Centar": "Дали е од Центар?",
        "Karposh": "Дали е од Карпош?",
        "Madjari": "Дали е од Маџари?"
    }
    return mapping.get(area, f"Дали е од {area}?")

# CITY GUESS
def city_guess(pool):
    cities = sorted({p.get("city") for p in pool if p.get("city")})

    if len(pool) > 4 or len(cities) <= 1:
        return None

    for c in cities:
        if c in st.session_state.asked:
            continue
        return c

    return None


def make_city_question(city):
    mapping = {
        "Skopje": "Дали е од Скопје?",
        "Kichevo": "Дали е од Кичево?",
        "Sveti Nikole": "Дали е од Свети Николе?",
        "Delchevo": "Дали е од Делчево?",
        "Prilep": "Дали е од Прилеп?",
        "Kavadarci": "Дали е од Кавадарци?",
        "Makedonska Kamenica": "Дали е од Македонска Каменица?"
    }
    return mapping.get(city, f"Дали е од {city}?")


# QUESTION TEXTS
def make_question(key):
    q = {
        "role": "Дали е ученик?",
        "glasses": "Дали носи очила?",
        "sports": "Дали се занимава со спорт?",
        "gym": "Дали оди во теретана?",
        "beard": "Дали има брада?",
        "cycling": "Дали вози велосипед?",
        "kickboxing": "Дали тренира кикбокс?",
        "motorcycle": "Дали вози мотор?",
        "tattoo": "Дали има тетоважа?",
        "volleyball": "Дали игра одбојка?",
        "karate": "Дали тренира карате?",
        "dexiverse_founder": "Дали е основач на Dexiverse?",
        "jarvis_ai": "Дали има Jarvis AI?",
        "competition_subject": "Дали се натпреварува во предмети?",
        "boarding_school": "Дали престојува во интернатот?",
        "gender": "Дали е машко?",
        "elective_subject": "Дали има избрано напредно програмирање?",
        "band_member": "Дали е дел од бенд?",
        "talkative": "Дали многу збори?",
        "calisthenics": "Дали тренира калестетика?",
        "likes_vanja": "Дали го сака Вања?",
        "youtuber": "Дали е youtuber?",
        "beautiful": "Дали е убава?",
        'class_teacher': "Дали е класен раководител?",
        "drinks_matcha": "Дали пије мача?",
        "attractive_friends": "Дали има убава другарка?",
        "uses_discord": "Дали користи discord?",
        "uses_linux": "Дали користи linux?",
        "deceased": "Дали е починат?",
        "loud_voice": "Дали многу вика?",
        "tall": "Дали е висок?",
        "boring_personality": "Дали е досаден?",
        "long_hair": "Дали има долга коса?",
        "bald": "Дали нема коса?",
        "injured": "Дали е повреден?",
        "teeth_missing": "Дали му фалат заби?",
        "strict_personality": "Дали е строг?",
        "flies_helicopters": "Дали лета хелихоптери?",
        "pilot": "Дали е пилот?"

    }
    return q.get(key, f"Дали има карактеристика: {key}?")

# UI
st.title("🧠 MIGinator AI")
st.write(f"Останати: {len(st.session_state.pool)}")

pool = st.session_state.pool

# WIN
if len(pool) == 1:
    st.success(f"🎯 Погодив: {pool[0]['name']}")

    if st.button("🔄 Restart"):
        st.session_state.pool = people
        st.session_state.asked = set()
        st.session_state.stage = "role"
        st.rerun()

    st.stop()


# DEBUG
st.sidebar.title("DEBUG")
st.sidebar.write("Remaining:", len(st.session_state.pool))
st.sidebar.write("Asked:", list(st.session_state.asked))

for p in st.session_state.pool:
    st.sidebar.write("•", p["name"])

# ROLE
if st.session_state.stage == "role":

    st.subheader("Дали е ученик?")

    c1, c2 = st.columns(2)

    if c1.button("Да"):
        st.session_state.pool = [p for p in pool if p.get("role") == "student"]
        st.session_state.stage = "dynamic"
        st.rerun()

    if c2.button("Не"):
        st.session_state.pool = [p for p in pool if p.get("role") != "student"]
        st.session_state.stage = "dynamic"
        st.rerun()

# DYNAMIC
else:

    # 1. AREA (small groups)
    area = area_guess(pool)
    if area:
        st.subheader(make_area_question(area))

        c1, c2 = st.columns(2)

        if c1.button("Да"):
            st.session_state.pool = [p for p in pool if p.get("area") == area]
            st.session_state.asked.add(area)
            st.rerun()

        if c2.button("Не"):
            st.session_state.pool = [p for p in pool if p.get("area") != area]
            st.session_state.asked.add(area)
            st.rerun()

    else:

        # 2. CITY
        city = city_guess(pool)

        if city:
            st.subheader(make_city_question(city))

            c1, c2 = st.columns(2)

            if c1.button("Да"):
                st.session_state.pool = [p for p in pool if p.get("city") == city]
                st.session_state.asked.add(city)
                st.rerun()

            if c2.button("Не"):
                st.session_state.pool = [p for p in pool if p.get("city") != city]
                st.session_state.asked.add(city)
                st.rerun()

        else:
            key = best_question(pool)

            if not key:
                st.warning("Нема повеќе прашања.")
                st.stop()

            st.subheader(make_question(key))

            c1, c2, c3 = st.columns(3)

            if c1.button("Да"):
                if key == "gender":
                    st.session_state.pool = [p for p in pool if p.get("gender") == "male"]
                elif key == "elective_subject":
                    st.session_state.pool = [p for p in pool if p.get("elective_subject") == "advanced_programming"]
                else:
                    st.session_state.pool = [p for p in pool if p.get(key, False) is True]

                st.session_state.asked.add(key)
                st.rerun()

            if c2.button("Не"):
                if key == "gender":
                    st.session_state.pool = [p for p in pool if p.get("gender") == "female"]
                elif key == "elective_subject":
                    st.session_state.pool = [p for p in pool if p.get("elective_subject") == "graphs"]
                else:
                    st.session_state.pool = [p for p in pool if p.get(key, False) is False]

                st.session_state.asked.add(key)
                st.rerun()

            if c3.button("Не знам"):
                st.session_state.asked.add(key)
                st.rerun()