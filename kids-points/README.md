# כוכבים בבית

אפליקציית נקודות להורים: כוכבים על מעשים טובים, סימנים על התנהגות לא בסדר, חנות פרסים, סולם תוצאות והדרכה להורה ברגע המתאים.

קובץ אחד (`index.html`), בלי בנייה. שלושה מצבי שמירה, לפי מה שזמין:

1. **Firebase** (מומלץ לשני הורים): אם קיים `firebase-config.js`, האפליקציה דורשת התחברות Google ושומרת ב-Firestore. הגישה מוגבלת לכתובות המייל שב-`firestore.rules`.
2. **Artifact ב-claude.ai** עם יכולת `db`: שיתוף בין משתמשים מחוברים באותו חשבון.
3. **מקומי**: שמירה בדפדפן של המכשיר, עם גיבוי/שחזור בהגדרות.

## הקמה עם Netlify + Firebase (כ-20 דקות, חינם)

### א. Firebase
1. נכנסים ל-https://console.firebase.google.com ויוצרים פרויקט (אפשר לכבות Analytics).
2. **Authentication → Sign-in method → Google → Enable.** שומרים.
3. **Firestore Database → Create database → Production mode.** בוחרים אזור (למשל `europe-west1`).
4. **Firestore → Rules:** מדביקים את התוכן של `firestore.rules`, מחליפים את שתי הכתובות לכתובות ה-Google של שני ההורים, ולוחצים Publish.
5. **Project settings (גלגל שיניים) → Your apps → Web (</>) → רושמים אפליקציה.** מעתיקים את אובייקט ה-`firebaseConfig`.
6. יוצרים בתיקייה הזאת קובץ `firebase-config.js` לפי `firebase-config.example.js` ומדביקים בו את ההגדרות. הקובץ הזה נשמר ב-git (ה-apiKey של Firebase לא סודי; ההגנה היא ב-Rules).

### ב. Netlify
1. נכנסים ל-https://app.netlify.com → **Add new site → Import an existing project → GitHub** ובוחרים את הרפו הזה.
2. **Base directory:** `kids-points`. **Publish directory:** `kids-points` (או `.` יחסית ל-base). **Build command:** ריק.
3. Deploy. מקבלים כתובת כמו `https://something.netlify.app` (אפשר לשנות שם ב-Site settings → Change site name).

### ג. לחבר ביניהם
1. חוזרים ל-Firebase → **Authentication → Settings → Authorized domains → Add domain** ומוסיפים את הדומיין של Netlify (בלי https://).
2. פותחים את הכתובת בטלפון, מתחברים עם Google. מי שלא ברשימה יראה "אין גישה לחשבון הזה".
3. בטלפון: "הוספה למסך הבית" כדי שזה ייראה כמו אפליקציה.

## פרטיות
- הנתונים יושבים בפרויקט Firebase שלכם בלבד, ורק שתי כתובות המייל שהגדרתם יכולות לקרוא או לכתוב.
- אין אנליטיקס, אין צד שלישי. הגופנים נטענים מ-Google Fonts; הספריות של Firebase מ-Google.
- הקוד ברפו לא מכיל שמות או רישומים.
