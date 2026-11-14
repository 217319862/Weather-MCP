# Weather MCP Server

שרת MCP פשוט שנותן ל-Claude כלי אחד, `get_weather`, שמחזיר מזג אוויר נוכחי לפי שם עיר.
הנתונים מגיעים מ-[Open-Meteo](https://open-meteo.com/) (חינמי, ללא מפתח API).

## מה זה עושה

1. המשתמש שואל את Claude על מזג האוויר בעיר מסוימת.
2. Claude קורא לכלי `get_weather` בשרת המקומי.
3. השרת ממיר את שם העיר לקואורדינטות (Geocoding API), מביא את מזג האוויר הנוכחי (Forecast API) ומחזיר טמפרטורה ומהירות רוח.
4. Claude מנסח מהנתונים תשובה בשפה טבעית.

```
משתמש  ->  Claude Desktop  ->  שרת MCP (weather_server.py)  ->  Open-Meteo API
                  <-------------------- תשובה --------------------
```

## מבנה הפרויקט

```
MCP_Weather/
├── weather_server.py   # השרת והכלי get_weather
├── requirements.txt    # התלויות להתקנה
├── .gitignore          # קבצים שלא עולים ל-Git
├── README.md           # הקובץ הזה
└── .venv/              # הסביבה הווירטואלית (לא עולה ל-Git)
```

## דרישות

- Python 3.10 ומעלה
- Claude Desktop

## התקנה

```bash
git clone https://github.com/<שם-המשתמש>/weather-mcp.git
cd weather-mcp
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

(החליפי את `<שם-המשתמש>` בשם המשתמש שלך ב-GitHub.)

> הערה: הקוד כתוב עבור `mcp` גרסה 1.x (`FastMCP`). בגרסה 2.x השם שונה ל-`MCPServer`, ולכן מצמצמים ל-`<2`.

## בדיקה שהשרת עולה

```bash
python weather_server.py
```

השרת אמור "להיתקע" וללא פלט, כי הוא ממתין ללקוח. עוצרים עם `Ctrl+C`.

## חיבור ל-Claude Desktop

1. ב-Claude Desktop: **Settings ← Extensions ← Local MCP servers ← Edit config**.
2. מוסיפים בקובץ `claude_desktop_config.json`, בתוך אובייקט ה-JSON הראשי, את הבלוק:

```json
"mcpServers": {
  "weather": {
    "command": "C:\\Users\\1\\Desktop\\MCP_Weather\\.venv\\Scripts\\python.exe",
    "args": ["C:\\Users\\1\\Desktop\\MCP_Weather\\weather_server.py"]
  }
},
```

   - **הנתיבים למעלה הם הדוגמה מהמחשב שבו נבנה הפרויקט.** יש להחליף אותם בנתיב המלא של `python.exe` שבתוך `.venv` ושל `weather_server.py` במחשב שלך. כדי להעתיק נתיב ב-PyCharm: קליק ימני על הקובץ ← Copy Path/Reference ← Absolute Path.
   - ב-JSON יש לכתוב `\\` כפול בנתיבי Windows.
   - אם יש כבר תוכן בקובץ, משאירים אותו ומוסיפים את הבלוק בצמוד, עם פסיק.
3. סוגרים את Claude Desktop לגמרי (גם מאזור ההתראות) ופותחים מחדש.
4. ב-**Settings ← Extensions ← Local MCP servers** אמור להופיע `weather` במצב **Running**.

## שימוש

בשיחה חדשה:

```
תפעיל את הכלי get_weather מהשרת weather עם city=Tel Aviv
```

אם הכלי הופעל, תופיע בצ'אט השורה **"used weather integration"** (אפשר ללחוץ עליה להרחבה ולראות את הקריאה והתוצאה).

טיפ: אם Claude עונה מכרטיס מזג אוויר מובנה ("Weather data from Google") במקום מהכלי, מבטלים את **Web search** בתפריט ה-`+` ומנסחים את הבקשה עם שם הכלי.

## איך הקוד בנוי

- `FastMCP("weather")` יוצר את השרת.
- `@mcp.tool()` רושם את הפונקציה כ"כלי". השם, ה-docstring וטיפוסי הפרמטרים הם מה ש-Claude רואה כדי להחליט מתי ואיך להשתמש בו.
- הפונקציה עטופה ב-`try/except` ובקריאות יש `timeout`, כך ששגיאת רשת מוחזרת כהודעה ברורה ולא קורסת את השרת.
- `mcp.run()` מריץ את השרת בתקשורת `stdio`: Claude Desktop מפעיל את התהליך ומדבר איתו דרך הקלט והפלט הסטנדרטיים.

## פתרון תקלות

| בעיה | פתרון |
|------|--------|
| `No module named 'mcp.server.fastmcp'` | הותקנה גרסה 2.x. להריץ `pip install "mcp[cli]<2"` |
| `weather` לא מופיע ב-Local MCP servers | הקובץ `claude_desktop_config.json` לא נמצא במקום שהאפליקציה קוראת, או שהסיומת `.json.txt`. לפתוח דרך **Edit config** |
| `Couldn't load app settings` | ה-JSON לא תקין (למשל הודבק בו קוד פייתון, או חסר פסיק) |
| Claude עונה מגוגל במקום מהכלי | לבטל Web search ולנסח עם שם הכלי |
| לוגים | **Settings ← Extensions ← Local MCP servers ← weather ← View logs** |

## הרחבות אפשריות

- כלי `get_forecast` לתחזית של כמה ימים.
- בחירת יחידות (צלזיוס או פרנהייט).
