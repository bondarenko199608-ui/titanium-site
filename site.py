import streamlit as st
import streamlit.components.v1 as components
import os

# ==========================================
# ЗАЩИТА (F12, Ctrl+U, контекстное меню)
# ==========================================
components.html("""
<script>
    document.addEventListener('contextmenu', function(e) { e.preventDefault(); });
    document.addEventListener('keydown', function(e) {
        if (e.key === 'F12' || e.keyCode === 123) { e.preventDefault(); return false; }
        if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'J' || e.key === 'C')) { e.preventDefault(); return false; }
        if (e.ctrlKey && (e.key === 'u' || e.key === 's')) { e.preventDefault(); return false; }
    });
    document.addEventListener('selectstart', function(e) { e.preventDefault(); });
    document.addEventListener('dragstart', function(e) { e.preventDefault(); });
</script>
""", height=0)

# ==========================================
# НАСТРОЙКА
# ==========================================
st.set_page_config(
    page_title="Titanium Toolkit",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# МЕГА-СТИЛЬ (Тёмный Премиум + 3D)
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;600;800&display=swap');
    
    /* Глобальный стиль */
    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
        color: #E2E8F0;
    }
    
    /* Очень темный фон с мягким свечением */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #1E1B4B 0%, #0F0F15 50%, #050505 100%);
        background-attachment: fixed;
    }

    /* Кастомный скроллбар */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: #0F0F15; }
    ::-webkit-scrollbar-thumb { background: #3B3B4A; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #0066FF; }

    /* Сайдбар */
    [data-testid="stSidebar"] {
        background: rgba(15, 15, 21, 0.95);
        border-right: 1px solid rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }
    [data-testid="stSidebar"] * { color: #E2E8F0 !important; }

    /* Скрываем хедер Streamlit */
    header {visibility: hidden;}
    footer {visibility: hidden;}

    /* Заголовки с градиентом */
    h1 {
        font-weight: 800;
        font-size: 4rem !important;
        background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        line-height: 1.1;
        margin-bottom: 20px;
    }
    h2 { font-weight: 700; color: #F8FAFC !important; margin-top: 40px; letter-spacing: -0.5px; }
    h3 { font-weight: 600; color: #CBD5E1 !important; }

    /* Кнопки */
    .stButton>button, .stDownloadButton>button {
        background: linear-gradient(135deg, #0066FF 0%, #0044CC 100%) !important;
        color: white !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        padding: 14px 32px !important;
        border: none !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(0, 102, 255, 0.3) !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 14px !important;
    }
    .stButton>button:hover, .stDownloadButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 10px 30px rgba(0, 102, 255, 0.5) !important;
    }

    /* 3D КАРТОЧКИ */
    .premium-card {
        background: linear-gradient(135deg, rgba(30, 30, 40, 0.8) 0%, rgba(20, 20, 30, 0.8) 100%);
        border-radius: 20px;
        padding: 35px;
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    .premium-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(0,102,255,0.1), transparent);
        opacity: 0;
        transition: opacity 0.4s;
        pointer-events: none;
    }
    .premium-card:hover {
        transform: translateY(-8px) rotateX(2deg);
        border-color: rgba(0,102,255,0.4);
        box-shadow: 0 20px 40px rgba(0, 102, 255, 0.15);
    }
    .premium-card:hover::before { opacity: 1; }
    
    .premium-card .icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, rgba(0,102,255,0.2), rgba(0,102,255,0.05));
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
        border: 1px solid rgba(0,102,255,0.3);
    }
    .premium-card h4 {
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 12px;
        color: #F8FAFC;
    }
    .premium-card p {
        color: #94A3B8;
        font-size: 15px;
        line-height: 1.7;
    }

    /* Метрики */
    .metric-box {
        background: rgba(255,255,255,0.03);
        border-radius: 16px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(255,255,255,0.08);
        transition: all 0.3s;
    }
    .metric-box:hover {
        border-color: rgba(0,102,255,0.5);
        background: rgba(0,102,255,0.05);
    }
    .metric-box .value {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF, #94A3B8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-box .label {
        font-size: 13px;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        margin-top: 8px;
    }

    /* Красивые экспандеры (FAQ) */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        color: #F8FAFC !important;
        padding: 15px 20px !important;
    }
    .streamlit-expanderContent {
        background: transparent !important;
        color: #94A3B8 !important;
    }
    
    /* Запрет выделения */
    * { user-select: none; -webkit-user-select: none; }
    img { pointer-events: none; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# SVG ИКОНКИ
# ==========================================
ICON_MOUSE = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="7"></rect><path d="M12 6v4"></path></svg>'
ICON_CLEAN = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"></path><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>'
ICON_CHART = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>'
ICON_VIDEO = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>'
ICON_LOCK = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>'
ICON_CPU = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="20" y1="14" x2="23" y2="14"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="1" y1="14" x2="4" y2="14"></line></svg>'
ICON_SHIELD = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
ICON_DIAMOND = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 3h12l4 6-10 13L2 9z"></path></svg>'
ICON_LIGHTNING = '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#60A5FA" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>'

# ==========================================
# СТРАНИЦА: ГЛАВНАЯ
# ==========================================
def home_page():
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.1, 1])
    
    with col1:
        st.markdown('<div style="color: #60A5FA; font-weight: 700; font-size: 13px; margin-bottom: 15px; letter-spacing: 2px;">NEW RELEASE V1.0</div>', unsafe_allow_html=True)
        st.title("Твой арсенал для побед")
        st.markdown('<p style="font-size: 22px; color: #94A3B8; margin-bottom: 40px; line-height: 1.5;">33 профессиональных инструмента в одном окне. Кликай, оптимизируй, записывай.</p>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; gap: 20px; margin-bottom: 40px;">
            <div class="metric-box">
                <div class="value">33</div>
                <div class="label">Модуля</div>
            </div>
            <div class="metric-box">
                <div class="value">1.2K+</div>
                <div class="label">Игроков</div>
            </div>
            <div class="metric-box">
                <div class="value">100%</div>
                <div class="label">Free</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("Перейди в раздел **«Скачать»** в левом меню, чтобы получить установщик.")

    with col2:
        if os.path.exists("screenshot.png"):
            st.markdown("""<div style="background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.02)); padding: 15px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 30px 60px rgba(0,0,0,0.5);">""", unsafe_allow_html=True)
            st.image("screenshot.png", use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Скриншот не найден. Добавь `screenshot.png` в папку.")

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    st.subheader("Почему именно Titanium?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_LIGHTNING}</div><h4>Молниеносно</h4><p>Написан на Python с оптимизацией под Windows. Ноль лагов, минимум потребления RAM.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_DIAMOND}</div><h4>Премиум-дизайн</h4><p>Тёмная тема, плавные анимации и удобный интерфейс без визуального шума.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_SHIELD}</div><h4>Полная безопасность</h4><p>Открытый исходный код. Никаких вирусов, майнеров и скрытых процессов.</p></div>', unsafe_allow_html=True)

# ==========================================
# СТРАНИЦА: ВОЗМОЖНОСТИ
# ==========================================
def features_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Возможности")
    st.markdown('<p style="font-size: 20px; color: #94A3B8; margin-bottom: 40px;">Швейцарский нож для настоящего геймера.</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_MOUSE}</div><h4>Авто-кликер</h4><p>До 1000 CPS, рандомизация интервала, двойной клик. Идеально для фарма.</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_CLEAN}</div><h4>Оптимизатор</h4><p>Очистка RAM, кэша, корзины и временных файлов. Ускорь свой ПК за секунду.</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_CHART}</div><h4>FPS & Пинг</h4><p>Мониторинг пинга в реальном времени, красивые графики и проверка скорости.</p></div>', unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_VIDEO}</div><h4>Запись экрана</h4><p>Встроенный рекордер с настройкой FPS и быстрой записью в MP4.</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_LOCK}</div><h4>Инструменты</h4><p>Генератор паролей, хеши (MD5, SHA256), конвертер цветов и заметки.</p></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="premium-card"><div class="icon">{ICON_CPU}</div><h4>Система</h4><p>Мониторинг CPU/RAM/Дисков, управление автозагрузкой и громкостью.</p></div>', unsafe_allow_html=True)

# ==========================================
# СТРАНИЦА: СКАЧАТЬ
# ==========================================
def download_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Скачать Titanium")
    st.markdown('<p style="font-size: 20px; color: #94A3B8;">Бесплатно. Без рекламы. Без подписок.</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(30,30,40,0.8), rgba(20,20,30,0.8)); border-radius: 24px; padding: 50px; text-align: center; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 20px 50px rgba(0,0,0,0.3); backdrop-filter: blur(20px);">
        <h3 style="margin-bottom: 10px; color: #F8FAFC; font-size: 28px;">Titanium Toolkit v1.0</h3>
        <p style="color: #94A3B8; margin-bottom: 30px; font-size: 16px;">Windows 10/11 • ~120 MB • x64</p>
    </div>
    """, unsafe_allow_html=True)

    exe_path = "Titanium_Setup.exe"
    
    if os.path.exists(exe_path):
        with open(exe_path, "rb") as f:
            st.download_button(
                label="Скачать установщик",
                data=f,
                file_name="Titanium_Setup.exe",
                mime="application/octet-stream",
                use_container_width=True
            )
        st.success("Файл готов к скачиванию!")
    else:
        st.error(f"Файл `{exe_path}` не найден в папке с сайтом.")
        
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    st.subheader("Как установить?")
    st.markdown("""
    <ol style="color: #94A3B8; font-size: 16px; line-height: 2.5;">
        <li>Скачай <b style="color:#F8FAFC">Titanium_Setup.exe</b></li>
        <li>Запусти установщик</li>
        <li>Следуй инструкциям на экране</li>
        <li>Запусти Titanium с рабочего стола</li>
    </ol>
    """, unsafe_allow_html=True)

# ==========================================
# СТРАНИЦА: FAQ
# ==========================================
def faq_page():
    st.markdown("<br>", unsafe_allow_html=True)
    st.title("Частые вопросы")
    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("Это безопасно?"):
        st.write("Да. Программа написана на Python с открытым исходным кодом. Антивирус может ругаться на PyInstaller — это ложное срабатывание.")
    with st.expander("Нужен ли Python?"):
        st.write("Нет. Установщик содержит готовый EXE-файл со всеми зависимостями.")
    with st.expander("Работает ли кликер в играх?"):
        st.write("В одиночных играх — да. В онлайн-играх с античитами (Valorant, CS2) — на свой страх и риск, возможен бан.")
    with st.expander("Можно ли использовать на нескольких ПК?"):
        st.write("Да, просто перенеси установщик на другой компьютер и установи.")

# ==========================================
# МЕНЮ (Сайдбар)
# ==========================================
with st.sidebar:
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 30px;">
        <div style="background: linear-gradient(135deg, #0066FF, #0044CC); color: white; padding: 10px 14px; border-radius: 12px; font-weight: 800; font-size: 20px; box-shadow: 0 4px 15px rgba(0,102,255,0.4);">T</div>
        <div>
            <div style="font-weight: 800; font-size: 18px; color: #F8FAFC;">Titanium</div>
            <div style="font-size: 12px; color: #64748B;">v1.0 Toolkit</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.1); margin-bottom: 20px;'>", unsafe_allow_html=True)

# ==========================================
# НАВИГАЦИЯ
# ==========================================
pg = st.navigation([
    st.Page(home_page, title="Главная", icon="🏠", default=True),
    st.Page(features_page, title="Возможности", icon="✨"),
    st.Page(download_page, title="Скачать", icon="📥"),
    st.Page(faq_page, title="FAQ", icon="❓"),
])

pg.run()
