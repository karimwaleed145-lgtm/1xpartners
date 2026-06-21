# All user-facing text in 4 languages. Telegram renders color emojis fine.
DEFAULT_LANG = "en"
LANGS = [("ar", "العربية"), ("fr", "Français"), ("en", "English"), ("fa", "فارسی"), ("es", "Español")]

CHOOSE_LANG = (
    "🌍 اختر لغتك\n"
    "Choose your language\n"
    "Choisis ta langue\n"
    "زبان خود را انتخاب کنید\n"
    "Elige tu idioma"
)

TEXTS = {
"en": {
 "welcome": "👋 Welcome to <b>1xBet Partners</b>!\n\nTurn your audience into real monthly income — no investment, no risk.\n\nTap a button to start 👇",
 "btn_register": "🚀 Become a partner",
 "btn_commission": "💸 Commission",
 "btn_withdraw": "💵 Withdrawal",
 "btn_banners": "🎨 Free designs",
 "btn_about": "ℹ️ How it works",
 "btn_lang": "🌍 Language",
 "btn_back": "⬅️ Back to menu",
 "btn_confirm": "✅ Confirm & send",
 "btn_restart": "🔄 Start over",
 "ask_name": "📝 Let's set you up.\n\nWhat's your <b>full name</b>? (first and last)",
 "ask_email": "📧 Your <b>email address</b>?",
 "ask_promocode": "🎟 The <b>promo code</b> you'd like to use?",
 "ask_phone": "📞 Your <b>phone number</b>? (with country code, e.g. +20…)",
 "invalid_name": "Please send your full name (at least 3 characters).",
 "invalid_email": "That doesn't look like a valid email. Please try again. 📧",
 "invalid_phone": "Please send a valid phone number with country code. 📞",
 "confirm": "Please check your details:\n\n👤 <b>{name}</b>\n📧 {email}\n🎟 {promocode}\n📞 {phone}\n\nIs everything correct?",
 "saved": "✅ <b>Done!</b> We've received your details.\nOur team will contact you very soon. 🚀",
 "commission": "💸 <b>Commission</b>\n\nYou start as a partner at <b>25%</b>, and your rate climbs automatically with your monthly first-time deposits (FTD):\n\n• 0–500 FTD → <b>25%</b>\n• 501–799 FTD → <b>30%</b>\n• 800–1200 FTD → <b>35%</b>\n• 1200+ FTD → <b>40%</b>\n\nThe more you bring, the higher your rate — for life.",
 "withdraw": "💵 <b>Withdrawal</b>\n\nTo withdraw your earnings, two simple conditions apply:\n\n1️⃣ Balance available for withdrawal: <b>$30 or more</b>\n2️⃣ <b>30 registrations</b> with deposits\n\nYour manager will explain the rest privately.",
 "banners": "🎨 <b>Free professional designs</b>\n\nAs our partner you get ready-made match banners, channel avatars and posts — in your language, with your code.\n\nBecome a partner and we'll send your kit. 🚀",
 "about": "ℹ️ <b>How it works</b>\n\n1️⃣ Register as a partner (free)\n2️⃣ Get your personal promo code\n3️⃣ Share it with your audience\n4️⃣ Earn lifetime commission on every deposit\n\nNo investment. No risk. Tap <b>Become a partner</b> to start.",
},
"ar": {
 "welcome": "👋 مرحبًا بك في <b>1xBet Partners</b>!\n\nحوّل جمهورك إلى دخل شهري حقيقي — بلا استثمار وبلا مخاطرة.\n\nاختر من الأزرار للبدء 👇",
 "btn_register": "🚀 ابدأ كشريك",
 "btn_commission": "💸 العمولة",
 "btn_withdraw": "💵 السحب",
 "btn_banners": "🎨 تصاميم مجانية",
 "btn_about": "ℹ️ كيف يعمل",
 "btn_lang": "🌍 اللغة",
 "btn_back": "⬅️ رجوع للقائمة",
 "btn_confirm": "✅ تأكيد وإرسال",
 "btn_restart": "🔄 البدء من جديد",
 "ask_name": "📝 لنبدأ التسجيل.\n\nما هو <b>اسمك الكامل</b>؟ (الاسم الأول واسم العائلة)",
 "ask_email": "📧 ما هو <b>بريدك الإلكتروني</b>؟",
 "ask_promocode": "🎟 ما هو <b>الكود الترويجي</b> الذي ترغب في استخدامه؟",
 "ask_phone": "📞 ما هو <b>رقم هاتفك</b>؟ (مع رمز الدولة، مثال: ‎+213…)",
 "invalid_name": "من فضلك أرسل اسمك الكامل (3 أحرف على الأقل).",
 "invalid_email": "هذا البريد غير صالح. حاول مرة أخرى. 📧",
 "invalid_phone": "من فضلك أرسل رقم هاتف صحيح مع رمز الدولة. 📞",
 "confirm": "يرجى مراجعة بياناتك:\n\n👤 <b>{name}</b>\n📧 {email}\n🎟 {promocode}\n📞 {phone}\n\nهل كل شيء صحيح؟",
 "saved": "✅ <b>تم!</b> استلمنا بياناتك.\nسيتواصل معك فريقنا في أقرب وقت. 🚀",
 "commission": "💸 <b>العمولة</b>\n\nتبدأ كشريك بنسبة <b>25%</b>، وترتفع نسبتك تلقائيًا حسب عدد الإيداعات الأولى (FTD) شهريًا:\n\n• 0–500 ➜ <b>25%</b>\n• 501–799 ➜ <b>30%</b>\n• 800–1200 ➜ <b>35%</b>\n• 1200+ ➜ <b>40%</b>\n\nكلما زاد عدد لاعبيك، ارتفعت نسبتك — مدى الحياة.",
 "withdraw": "💵 <b>السحب</b>\n\nلسحب أرباحك، هناك شرطان بسيطان:\n\n1️⃣ الرصيد المتاح للسحب: <b>30$ أو أكثر</b>\n2️⃣ <b>30 تسجيلًا</b> مع إيداع\n\nسيشرح لك المدير بقية التفاصيل في الخاص.",
 "banners": "🎨 <b>تصاميم احترافية مجانية</b>\n\nكشريك معنا تحصل على بانرات للمباريات، صور قنوات ومنشورات جاهزة — بلغتك وبكودك.\n\nانضم كشريك وسنرسل لك المجموعة. 🚀",
 "about": "ℹ️ <b>كيف يعمل</b>\n\n1️⃣ سجّل كشريك (مجانًا)\n2️⃣ احصل على كودك الترويجي الخاص\n3️⃣ شاركه مع جمهورك\n4️⃣ اربح عمولة مدى الحياة على كل إيداع\n\nبلا استثمار. بلا مخاطرة. اضغط <b>ابدأ كشريك</b>.",
},
"fr": {
 "welcome": "👋 Bienvenue chez <b>1xBet Partners</b> !\n\nTransforme ton audience en revenu mensuel réel — sans investissement, sans risque.\n\nChoisis un bouton pour commencer 👇",
 "btn_register": "🚀 Devenir partenaire",
 "btn_commission": "💸 Commission",
 "btn_withdraw": "💵 Retrait",
 "btn_banners": "🎨 Visuels gratuits",
 "btn_about": "ℹ️ Comment ça marche",
 "btn_lang": "🌍 Langue",
 "btn_back": "⬅️ Retour au menu",
 "btn_confirm": "✅ Confirmer et envoyer",
 "btn_restart": "🔄 Recommencer",
 "ask_name": "📝 On commence ton inscription.\n\nQuel est ton <b>nom complet</b> ? (prénom et nom)",
 "ask_email": "📧 Ton <b>adresse e-mail</b> ?",
 "ask_promocode": "🎟 Le <b>code promo</b> que tu veux utiliser ?",
 "ask_phone": "📞 Ton <b>numéro de téléphone</b> ? (avec indicatif, ex : +213…)",
 "invalid_name": "Merci d'envoyer ton nom complet (au moins 3 caractères).",
 "invalid_email": "Cet e-mail ne semble pas valide. Réessaie. 📧",
 "invalid_phone": "Merci d'envoyer un numéro valide avec l'indicatif. 📞",
 "confirm": "Vérifie tes informations :\n\n👤 <b>{name}</b>\n📧 {email}\n🎟 {promocode}\n📞 {phone}\n\nTout est correct ?",
 "saved": "✅ <b>C'est fait !</b> Nous avons reçu tes informations.\nNotre équipe te contactera très vite. 🚀",
 "commission": "💸 <b>Commission</b>\n\nTu démarres comme partenaire à <b>25%</b>, et ton taux monte automatiquement selon tes premiers dépôts (FTD) mensuels :\n\n• 0–500 ➜ <b>25%</b>\n• 501–799 ➜ <b>30%</b>\n• 800–1200 ➜ <b>35%</b>\n• 1200+ ➜ <b>40%</b>\n\nPlus tu apportes, plus ton taux monte — à vie.",
 "withdraw": "💵 <b>Retrait</b>\n\nPour retirer tes gains, deux conditions simples :\n\n1️⃣ Solde disponible : <b>30$ ou plus</b>\n2️⃣ <b>30 inscriptions</b> avec dépôt\n\nTon manager t'expliquera le reste en privé.",
 "banners": "🎨 <b>Visuels professionnels gratuits</b>\n\nEn tant que partenaire, tu reçois des bannières de matchs, des avatars et des posts prêts — dans ta langue, avec ton code.\n\nDeviens partenaire et on t'envoie le kit. 🚀",
 "about": "ℹ️ <b>Comment ça marche</b>\n\n1️⃣ Inscris-toi comme partenaire (gratuit)\n2️⃣ Reçois ton code promo personnel\n3️⃣ Partage-le avec ton audience\n4️⃣ Gagne une commission à vie sur chaque dépôt\n\nSans investissement. Sans risque. Appuie sur <b>Devenir partenaire</b>.",
},
"fa": {
 "welcome": "👋 به <b>1xBet Partners</b> خوش آمدید!\n\nمخاطبان خود را به درآمد ماهانه واقعی تبدیل کنید — بدون سرمایه و بدون ریسک.\n\nبرای شروع یک دکمه را انتخاب کنید 👇",
 "btn_register": "🚀 شریک شوید",
 "btn_commission": "💸 کمیسیون",
 "btn_withdraw": "💵 برداشت",
 "btn_banners": "🎨 طرح‌های رایگان",
 "btn_about": "ℹ️ نحوه کار",
 "btn_lang": "🌍 زبان",
 "btn_back": "⬅️ بازگشت به منو",
 "btn_confirm": "✅ تأیید و ارسال",
 "btn_restart": "🔄 شروع دوباره",
 "ask_name": "📝 بیایید ثبت‌نام کنیم.\n\n<b>نام کامل</b> شما چیست؟ (نام و نام خانوادگی)",
 "ask_email": "📧 <b>ایمیل</b> شما؟",
 "ask_promocode": "🎟 <b>کد پرومو</b> که می‌خواهید استفاده کنید؟",
 "ask_phone": "📞 <b>شماره تلفن</b> شما؟ (با کد کشور، مثال: ‎+93…)",
 "invalid_name": "لطفاً نام کامل خود را بفرستید (حداقل ۳ حرف).",
 "invalid_email": "این ایمیل معتبر نیست. دوباره تلاش کنید. 📧",
 "invalid_phone": "لطفاً شماره معتبر با کد کشور بفرستید. 📞",
 "confirm": "لطفاً اطلاعات خود را بررسی کنید:\n\n👤 <b>{name}</b>\n📧 {email}\n🎟 {promocode}\n📞 {phone}\n\nهمه چیز درست است؟",
 "saved": "✅ <b>انجام شد!</b> اطلاعات شما را دریافت کردیم.\nتیم ما خیلی زود با شما تماس می‌گیرد. 🚀",
 "commission": "💸 <b>کمیسیون</b>\n\nشما به‌عنوان شریک از <b>۲۵٪</b> شروع می‌کنید و نرخ شما به‌طور خودکار بر اساس اولین واریزی‌ها (FTD) در ماه افزایش می‌یابد:\n\n• 0–500 ➜ <b>25%</b>\n• 501–799 ➜ <b>30%</b>\n• 800–1200 ➜ <b>35%</b>\n• 1200+ ➜ <b>40%</b>\n\nهرچه بیشتر بیاورید، نرخ شما بالاتر می‌رود — برای همیشه.",
 "withdraw": "💵 <b>برداشت</b>\n\nبرای برداشت سود، دو شرط ساده وجود دارد:\n\n1️⃣ موجودی قابل برداشت: <b>۳۰ دلار یا بیشتر</b>\n2️⃣ <b>۳۰ ثبت‌نام</b> همراه با واریزی\n\nمدیر بقیه را در پیام خصوصی توضیح می‌دهد.",
 "banners": "🎨 <b>طرح‌های حرفه‌ای رایگان</b>\n\nبه‌عنوان شریک، بنرهای مسابقات، آواتار کانال و پست‌های آماده دریافت می‌کنید — به زبان شما و با کد شما.\n\nشریک شوید تا کیت را برایتان بفرستیم. 🚀",
 "about": "ℹ️ <b>نحوه کار</b>\n\n1️⃣ به‌عنوان شریک ثبت‌نام کنید (رایگان)\n2️⃣ کد پرومو شخصی خود را بگیرید\n3️⃣ آن را با مخاطبان خود به اشتراک بگذارید\n4️⃣ روی هر واریزی کمیسیون مادام‌العمر بگیرید\n\nبدون سرمایه. بدون ریسک. روی <b>شریک شوید</b> بزنید.",
},
"es": {
 "welcome": "👋 ¡Bienvenido a <b>1xBet Partners</b>!\n\nConvierte tu audiencia en ingresos mensuales reales — sin inversión, sin riesgo.\n\nToca un botón para empezar 👇",
 "btn_register": "🚀 Hazte socio",
 "btn_commission": "💸 Comisión",
 "btn_withdraw": "💵 Retiro",
 "btn_banners": "🎨 Diseños gratis",
 "btn_about": "ℹ️ Cómo funciona",
 "btn_lang": "🌍 Idioma",
 "btn_back": "⬅️ Volver al menú",
 "btn_confirm": "✅ Confirmar y enviar",
 "btn_restart": "🔄 Empezar de nuevo",
 "ask_name": "📝 Vamos a registrarte.\n\n¿Cuál es tu <b>nombre completo</b>? (nombre y apellido)",
 "ask_email": "📧 ¿Tu <b>correo electrónico</b>?",
 "ask_promocode": "🎟 ¿El <b>código promocional</b> que quieres usar?",
 "ask_phone": "📞 ¿Tu <b>número de teléfono</b>? (con código de país, ej: +57…)",
 "invalid_name": "Por favor envía tu nombre completo (al menos 3 caracteres).",
 "invalid_email": "Ese correo no parece válido. Inténtalo de nuevo. 📧",
 "invalid_phone": "Por favor envía un número válido con código de país. 📞",
 "confirm": "Revisa tus datos:\n\n👤 <b>{name}</b>\n📧 {email}\n🎟 {promocode}\n📞 {phone}\n\n¿Está todo correcto?",
 "saved": "✅ <b>¡Listo!</b> Recibimos tus datos.\nNuestro equipo te contactará muy pronto. 🚀",
 "commission": "💸 <b>Comisión</b>\n\nEmpiezas como socio con <b>25%</b>, y tu tasa sube automáticamente según tus primeros depósitos (FTD) mensuales:\n\n• 0–500 ➜ <b>25%</b>\n• 501–799 ➜ <b>30%</b>\n• 800–1200 ➜ <b>35%</b>\n• 1200+ ➜ <b>40%</b>\n\nCuantos más traigas, mayor será tu tasa — de por vida.",
 "withdraw": "💵 <b>Retiro</b>\n\nPara retirar tus ganancias, hay dos condiciones simples:\n\n1️⃣ Saldo disponible para retiro: <b>$30 o más</b>\n2️⃣ <b>30 registros</b> con depósitos\n\nTu mánager te explicará el resto en privado.",
 "banners": "🎨 <b>Diseños profesionales gratis</b>\n\nComo socio recibes banners de partidos, avatares de canal y publicaciones listas — en tu idioma, con tu código.\n\nHazte socio y te enviamos el kit. 🚀",
 "about": "ℹ️ <b>Cómo funciona</b>\n\n1️⃣ Regístrate como socio (gratis)\n2️⃣ Recibe tu código promocional personal\n3️⃣ Compártelo con tu audiencia\n4️⃣ Gana comisión de por vida en cada depósito\n\nSin inversión. Sin riesgo. Toca <b>Hazte socio</b>.",
},
}


# ===================== FAQ =====================
FAQ_ORDER = ["free", "start", "earn", "website", "withdraw_opts", "designs", "demo"]

FAQ = {
"en": {
 "btn": "❓ FAQ",
 "intro": "❓ <b>FAQ</b>\nPick a question 👇",
 "back": "⬅️ All questions",
 "items": {
  "free": ("💰 Is it free?", "Yes — joining is completely free. No investment, no risk."),
  "start": ("🚀 How do I start?", "Register as a partner (free), then send <b>all your details in one message</b> — full name, email, the promo code you want, and your phone number. The manager will set you up.\n\nTip: tap 🚀 <b>Become a partner</b> and the bot collects it step by step."),
  "earn": ("📈 How much can I earn?", "Lifetime revenue share: you start at <b>25%</b> and climb up to <b>40%</b> based on your monthly results. No cap on what you can earn."),
  "website": ("🌐 Need a website?", "No. A Telegram channel, Facebook page, TikTok or any active audience works — even a small, engaged community is enough to start."),
  "withdraw_opts": ("💵 Withdrawal options", "You can withdraw from <b>$30</b>. Your <b>first 3 withdrawals</b> go to your 1xBet account; after that you can withdraw to <b>Binance or any wallet</b>.\n\nThe 1xBet account must be <b>new and clean</b> — no prior deposits or withdrawals — and registered with the <b>same details as your ID</b>."),
  "designs": ("🎨 Where are the designs?", "As our partner you get ready-made designs <b>free</b> — match banners, channel avatars and posts, in your language with your code. We send your kit after you register."),
  "demo": ("🎮 Demo account?", "A practice balance you unlock by bringing 20 registrations with deposits; rechargeable with 20 more + a 1-week wait (needs a fresh 1xBet account). The manager walks you through it."),
 },
},
"ar": {
 "btn": "❓ الأسئلة الشائعة",
 "intro": "❓ <b>الأسئلة الشائعة</b>\nاختر سؤالًا 👇",
 "back": "⬅️ كل الأسئلة",
 "items": {
  "free": ("💰 هل الاشتراك مجاني؟", "نعم — الاشتراك مجاني تمامًا. بلا استثمار وبلا مخاطرة."),
  "start": ("🚀 كيف أبدأ؟", "سجّل كشريك (مجانًا)، ثم أرسل <b>كل بياناتك في رسالة واحدة</b> — الاسم الكامل، البريد الإلكتروني، الكود الترويجي الذي تريده، ورقم الهاتف. وسيتولى المدير إعدادك.\n\nنصيحة: اضغط 🚀 <b>ابدأ كشريك</b> وسيجمعها البوت خطوة بخطوة."),
  "earn": ("📈 كم يمكنني أن أربح؟", "عمولة مدى الحياة: تبدأ بنسبة <b>25%</b> وترتفع حتى <b>40%</b> حسب نتائجك الشهرية. لا حد أقصى للأرباح."),
  "website": ("🌐 هل أحتاج موقعًا؟", "لا. قناة تيليجرام، صفحة فيسبوك، تيك توك أو أي جمهور نشط يكفي — حتى مجتمع صغير ومتفاعل يكفي للبدء."),
  "withdraw_opts": ("💵 خيارات السحب", "يمكنك السحب من <b>30$</b>. أول <b>3 عمليات سحب</b> تكون على حساب 1xBet؛ بعدها يمكنك السحب إلى <b>Binance أو أي محفظة</b>.\n\nيجب أن يكون حساب 1xBet <b>جديدًا ونظيفًا</b> — بدون أي إيداعات أو سحوبات سابقة — ومسجّلًا <b>بنفس بيانات هويتك</b>."),
  "designs": ("🎨 أين التصاميم؟", "كشريك معنا تحصل على تصاميم جاهزة <b>مجانًا</b> — بانرات مباريات، صور قنوات ومنشورات، بلغتك وبكودك. نرسل لك المجموعة بعد التسجيل."),
  "demo": ("🎮 الحساب التجريبي؟", "رصيد تجريبي تفتحه بإحضار 20 تسجيلًا مع إيداع؛ ويُعاد شحنه بـ20 تسجيلًا جديدًا + الانتظار أسبوعًا (يتطلب حساب 1xBet جديدًا). يشرحه لك المدير."),
 },
},
"fr": {
 "btn": "❓ FAQ",
 "intro": "❓ <b>FAQ</b>\nChoisis une question 👇",
 "back": "⬅️ Toutes les questions",
 "items": {
  "free": ("💰 C'est gratuit ?", "Oui — l'inscription est totalement gratuite. Sans investissement, sans risque."),
  "start": ("🚀 Comment commencer ?", "Inscris-toi comme partenaire (gratuit), puis envoie <b>toutes tes infos en un seul message</b> — nom complet, e-mail, le code promo que tu veux, et ton numéro. Le manager s'occupe du reste.\n\nAstuce : appuie sur 🚀 <b>Devenir partenaire</b> et le bot collecte tout étape par étape."),
  "earn": ("📈 Combien je peux gagner ?", "Revenu à vie : tu démarres à <b>25%</b> et tu montes jusqu'à <b>40%</b> selon tes résultats mensuels. Aucun plafond."),
  "website": ("🌐 Besoin d'un site ?", "Non. Une chaîne Telegram, une page Facebook, TikTok ou toute audience active suffit — même une petite communauté engagée suffit pour démarrer."),
  "withdraw_opts": ("💵 Options de retrait", "Tu peux retirer à partir de <b>30$</b>. Tes <b>3 premiers retraits</b> se font sur le compte 1xBet ; ensuite tu peux retirer vers <b>Binance ou n'importe quel wallet</b>.\n\nLe compte 1xBet doit être <b>neuf et propre</b> — sans dépôts ni retraits antérieurs — et enregistré avec les <b>mêmes informations que ta pièce d'identité</b>."),
  "designs": ("🎨 Où sont les visuels ?", "En tant que partenaire, tu reçois des visuels prêts <b>gratuits</b> — bannières de matchs, avatars, posts, dans ta langue avec ton code. On envoie ton kit après l'inscription."),
  "demo": ("🎮 Compte démo ?", "Un solde d'entraînement débloqué en apportant 20 inscriptions avec dépôt ; rechargeable avec 20 de plus + 1 semaine d'attente (nécessite un nouveau compte 1xBet). Le manager t'explique."),
 },
},
"fa": {
 "btn": "❓ سؤالات متداول",
 "intro": "❓ <b>سؤالات متداول</b>\nیک سؤال را انتخاب کنید 👇",
 "back": "⬅️ همه سؤالات",
 "items": {
  "free": ("💰 رایگان است؟", "بله — عضویت کاملاً رایگان است. بدون سرمایه و بدون ریسک."),
  "start": ("🚀 چطور شروع کنم؟", "به‌عنوان شریک ثبت‌نام کنید (رایگان)، سپس <b>همه اطلاعات خود را در یک پیام</b> بفرستید — نام کامل، ایمیل، کد پرومو مورد نظر و شماره تلفن. مدیر شما را راه‌اندازی می‌کند.\n\nنکته: روی 🚀 <b>شریک شوید</b> بزنید تا ربات مرحله‌به‌مرحله جمع‌آوری کند."),
  "earn": ("📈 چقدر می‌توانم درآمد داشته باشم؟", "درآمد مادام‌العمر: از <b>۲۵٪</b> شروع می‌کنید و تا <b>۴۰٪</b> بر اساس نتایج ماهانه بالا می‌روید. بدون سقف درآمد."),
  "website": ("🌐 به وب‌سایت نیاز دارم؟", "نه. یک کانال تلگرام، صفحه فیسبوک، تیک‌تاک یا هر مخاطب فعال کافی است — حتی یک جامعه کوچک و فعال برای شروع کافی است."),
  "withdraw_opts": ("💵 گزینه‌های برداشت", "می‌توانید از <b>۳۰ دلار</b> برداشت کنید. <b>۳ برداشت اول</b> به حساب 1xBet است؛ پس از آن می‌توانید به <b>Binance یا هر کیف پولی</b> برداشت کنید.\n\nحساب 1xBet باید <b>جدید و تمیز</b> باشد — بدون واریز یا برداشت قبلی — و با <b>همان اطلاعات کارت شناسایی شما</b> ثبت شده باشد."),
  "designs": ("🎨 طرح‌ها کجا هستند؟", "به‌عنوان شریک، طرح‌های آماده <b>رایگان</b> می‌گیرید — بنر مسابقات، آواتار کانال و پست‌ها، به زبان شما و با کد شما. کیت را پس از ثبت‌نام می‌فرستیم."),
  "demo": ("🎮 حساب دمو؟", "یک موجودی آزمایشی که با آوردن ۲۰ ثبت‌نام همراه با واریزی باز می‌شود؛ با ۲۰ ثبت‌نام جدید + یک هفته صبر دوباره شارژ می‌شود (به حساب 1xBet جدید نیاز دارد). مدیر توضیح می‌دهد."),
 },
},
"es": {
 "btn": "❓ Preguntas",
 "intro": "❓ <b>Preguntas frecuentes</b>\nElige una pregunta 👇",
 "back": "⬅️ Todas las preguntas",
 "items": {
  "free": ("💰 ¿Es gratis?", "Sí — unirse es totalmente gratis. Sin inversión, sin riesgo."),
  "start": ("🚀 ¿Cómo empiezo?", "Regístrate como socio (gratis) y envía <b>todos tus datos en un solo mensaje</b> — nombre completo, correo, el código promocional que quieres y tu teléfono. El mánager te configura.\n\nConsejo: toca 🚀 <b>Hazte socio</b> y el bot lo recoge paso a paso."),
  "earn": ("📈 ¿Cuánto puedo ganar?", "Ingresos de por vida: empiezas con <b>25%</b> y subes hasta <b>40%</b> según tus resultados mensuales. Sin límite."),
  "website": ("🌐 ¿Necesito web?", "No. Un canal de Telegram, página de Facebook, TikTok o cualquier audiencia activa sirve — incluso una comunidad pequeña y activa basta para empezar."),
  "withdraw_opts": ("💵 Opciones de retiro", "Puedes retirar desde <b>$30</b>. Tus <b>3 primeros retiros</b> van a la cuenta 1xBet; después puedes retirar a <b>Binance o cualquier wallet</b>.\n\nLa cuenta 1xBet debe ser <b>nueva y limpia</b> — sin depósitos ni retiros previos — y registrada con los <b>mismos datos que tu identificación</b>."),
  "designs": ("🎨 ¿Dónde están los diseños?", "Como socio recibes diseños listos <b>gratis</b> — banners de partidos, avatares y publicaciones, en tu idioma con tu código. Enviamos tu kit tras el registro."),
  "demo": ("🎮 ¿Cuenta demo?", "Un saldo de práctica que desbloqueas trayendo 20 registros con depósito; recargable con 20 más + 1 semana de espera (requiere una cuenta 1xBet nueva). El mánager te guía."),
 },
},
}


# ---------------- FAQ ----------------
BTN_FAQ = {"en": "❓ FAQ", "ar": "❓ الأسئلة الشائعة", "fr": "❓ FAQ", "fa": "❓ سوالات متداول", "es": "❓ Preguntas frecuentes"}
BTN_FAQ_BACK = {"en": "⬅️ Back to questions", "ar": "⬅️ رجوع للأسئلة", "fr": "⬅️ Retour aux questions", "fa": "⬅️ بازگشت به سوالات", "es": "⬅️ Volver a preguntas"}
FAQ_INTRO = {
 "en": "❓ <b>Frequently Asked Questions</b>\n\nTap a question:",
 "ar": "❓ <b>الأسئلة الشائعة</b>\n\nاختر سؤالًا:",
 "fr": "❓ <b>Questions fréquentes</b>\n\nChoisis une question :",
 "fa": "❓ <b>سوالات متداول</b>\n\nیک سوال را انتخاب کنید:",
 "es": "❓ <b>Preguntas frecuentes</b>\n\nElige una pregunta:",
}

# each item: (button_label, answer_html)
FAQ = {
"en": [
 ("💰 Is it free to join?", "💰 <b>Is it free to join?</b>\n\nYes — joining as a partner is 100% free. No investment, no risk."),
 ("🚀 How do I start?", "🚀 <b>How do I start?</b>\n\nRegister as a partner (free), then send all your details in one message — full name, email, the promo code you want, and your phone number — and the manager sets you up.\n\nTip: just tap «Become a partner» here and the bot collects it step by step."),
 ("📈 How much can I earn?", "📈 <b>How much can I earn?</b>\n\nLifetime revenue share — you start at 25% and climb up to 40% based on your monthly results. No cap on total earnings."),
 ("🌐 Do I need a website?", "🌐 <b>Do I need a website?</b>\n\nNo. A Telegram channel, Facebook page, TikTok or any active audience works — even a small, engaged community is enough to start."),
 ("💵 Withdrawal options", "💵 <b>Withdrawal options</b>\n\nYou can withdraw from $30.\n\n• Your first 3 withdrawals go to your 1xBet account.\n• After that, you can withdraw to Binance or any wallet.\n\nThe 1xBet account must be new and clean (no prior deposits or withdrawals) and registered with the same information as your ID. The manager explains the full setup."),
 ("🎨 Where are the designs?", "🎨 <b>Where do I get banners/designs?</b>\n\nAs our partner you get ready-made designs free — match banners, channel avatars and posts, in your language with your code. We send your kit after you register."),
 ("🔗 Multiple channels?", "🔗 <b>Can I promote on more than one channel?</b>\n\nYes — you can promote with your code across several platforms and channels."),
 ("🎮 What's the demo account?", "🎮 <b>What's the demo account?</b>\n\nA practice balance you unlock by bringing 20 registrations with deposits; rechargeable with 20 more + a 1-week wait (needs a fresh 1xBet account). The manager walks you through it."),
 ("💬 Still have a question?", "💬 <b>Still have a question?</b>\n\nTap «Become a partner» to register, or message our manager directly — we reply fast. 🚀"),
],
"ar": [
 ("💰 هل الانضمام مجاني؟", "💰 <b>هل الانضمام مجاني؟</b>\n\nنعم — الانضمام كشريك مجاني 100%. بلا استثمار وبلا مخاطرة."),
 ("🚀 كيف أبدأ؟", "🚀 <b>كيف أبدأ؟</b>\n\nسجّل كشريك (مجانًا)، ثم أرسل كل بياناتك في رسالة واحدة — الاسم الكامل، البريد الإلكتروني، الكود الترويجي الذي تريده، ورقم الهاتف — وسيقوم المدير بإعدادك.\n\nنصيحة: اضغط «ابدأ كشريك» هنا وسيجمع البوت بياناتك خطوة بخطوة."),
 ("📈 كم يمكنني أن أربح؟", "📈 <b>كم يمكنني أن أربح؟</b>\n\nعمولة مدى الحياة — تبدأ بنسبة 25% وترتفع حتى 40% حسب نتائجك الشهرية. لا حد أقصى للأرباح."),
 ("🌐 هل أحتاج إلى موقع؟", "🌐 <b>هل أحتاج إلى موقع إلكتروني؟</b>\n\nلا. قناة تيليجرام، صفحة فيسبوك، تيك توك أو أي جمهور نشط يكفي — حتى مجتمع صغير ومتفاعل يكفي للبدء."),
 ("💵 خيارات السحب", "💵 <b>خيارات السحب</b>\n\nيمكنك السحب من 30$.\n\n• أول 3 عمليات سحب تكون على حساب 1xBet.\n• بعد ذلك يمكنك السحب إلى Binance أو أي محفظة.\n\nيجب أن يكون حساب 1xBet جديدًا ونظيفًا (بدون إيداعات أو سحوبات سابقة) ومسجلًا بنفس بيانات هويتك. يشرح لك المدير الإعداد كاملًا."),
 ("🎨 أين التصاميم؟", "🎨 <b>من أين أحصل على التصاميم؟</b>\n\nكشريك معنا تحصل على تصاميم جاهزة مجانًا — بانرات للمباريات، صور قنوات ومنشورات، بلغتك وبكودك. نرسل لك المجموعة بعد التسجيل."),
 ("🔗 أكثر من قناة؟", "🔗 <b>هل أستطيع الترويج في أكثر من قناة؟</b>\n\nنعم — يمكنك الترويج بكودك عبر عدة منصات وقنوات."),
 ("🎮 ما هو الحساب التجريبي؟", "🎮 <b>ما هو الحساب التجريبي؟</b>\n\nرصيد تدريبي تفتحه بإحضار 20 تسجيلًا مع إيداع؛ ويُعاد شحنه بـ20 تسجيلًا جديدًا + انتظار أسبوع (يتطلب حساب 1xBet جديد). يشرح لك المدير التفاصيل."),
 ("💬 لا يزال لديك سؤال؟", "💬 <b>لا يزال لديك سؤال؟</b>\n\nاضغط «ابدأ كشريك» للتسجيل، أو راسل المدير مباشرة — نرد بسرعة. 🚀"),
],
"fr": [
 ("💰 C'est gratuit ?", "💰 <b>C'est gratuit ?</b>\n\nOui — devenir partenaire est 100% gratuit. Sans investissement, sans risque."),
 ("🚀 Comment commencer ?", "🚀 <b>Comment commencer ?</b>\n\nInscris-toi comme partenaire (gratuit), puis envoie toutes tes infos en un seul message — nom complet, e-mail, le code promo que tu veux, et ton numéro — et le manager s'occupe de toi.\n\nAstuce : appuie sur «Devenir partenaire» ici et le bot collecte tout étape par étape."),
 ("📈 Combien puis-je gagner ?", "📈 <b>Combien puis-je gagner ?</b>\n\nRevenu à vie — tu démarres à 25% et montes jusqu'à 40% selon tes résultats mensuels. Aucun plafond."),
 ("🌐 Faut-il un site web ?", "🌐 <b>Faut-il un site web ?</b>\n\nNon. Une chaîne Telegram, une page Facebook, TikTok ou toute audience active suffit — même une petite communauté engagée."),
 ("💵 Options de retrait", "💵 <b>Options de retrait</b>\n\nTu peux retirer à partir de 30$.\n\n• Tes 3 premiers retraits se font sur ton compte 1xBet.\n• Ensuite, tu peux retirer vers Binance ou n'importe quel wallet.\n\nLe compte 1xBet doit être nouveau et propre (sans dépôts ni retraits) et enregistré avec les mêmes informations que ta pièce d'identité. Le manager explique tout."),
 ("🎨 Où sont les visuels ?", "🎨 <b>Où sont les visuels ?</b>\n\nEn tant que partenaire, tu reçois des visuels prêts gratuitement — bannières de matchs, avatars, posts, dans ta langue avec ton code. On t'envoie le kit après ton inscription."),
 ("🔗 Plusieurs canaux ?", "🔗 <b>Plusieurs canaux ?</b>\n\nOui — tu peux promouvoir avec ton code sur plusieurs plateformes."),
 ("🎮 Le compte démo ?", "🎮 <b>Le compte démo ?</b>\n\nUn solde d'entraînement débloqué en apportant 20 inscriptions avec dépôt ; rechargeable avec 20 de plus + 1 semaine d'attente (nécessite un nouveau compte 1xBet). Le manager t'explique."),
 ("💬 Encore une question ?", "💬 <b>Encore une question ?</b>\n\nAppuie sur «Devenir partenaire» pour t'inscrire, ou écris au manager — on répond vite. 🚀"),
],
"fa": [
 ("💰 آیا رایگان است؟", "💰 <b>آیا رایگان است؟</b>\n\nبله — عضویت به‌عنوان شریک ۱۰۰٪ رایگان است. بدون سرمایه و بدون ریسک."),
 ("🚀 چطور شروع کنم؟", "🚀 <b>چطور شروع کنم؟</b>\n\nبه‌عنوان شریک ثبت‌نام کنید (رایگان)، سپس همه اطلاعات خود را در یک پیام بفرستید — نام کامل، ایمیل، کد پرومو دلخواه و شماره تلفن — و مدیر شما را راه‌اندازی می‌کند.\n\nنکته: روی «شریک شوید» بزنید تا ربات مرحله‌به‌مرحله جمع‌آوری کند."),
 ("📈 چقدر درآمد دارم؟", "📈 <b>چقدر می‌توانم درآمد داشته باشم؟</b>\n\nدرآمد مادام‌العمر — از ۲۵٪ شروع می‌کنید و تا ۴۰٪ بر اساس نتایج ماهانه بالا می‌روید. بدون سقف."),
 ("🌐 به وب‌سایت نیاز دارم؟", "🌐 <b>به وب‌سایت نیاز دارم؟</b>\n\nنه. یک کانال تلگرام، صفحه فیسبوک، تیک‌تاک یا هر مخاطب فعال کافی است — حتی یک جامعه کوچک و فعال."),
 ("💵 گزینه‌های برداشت", "💵 <b>گزینه‌های برداشت</b>\n\nمی‌توانید از ۳۰ دلار برداشت کنید.\n\n• ۳ برداشت اول شما به حساب 1xBet انجام می‌شود.\n• پس از آن می‌توانید به Binance یا هر کیف پول برداشت کنید.\n\nحساب 1xBet باید جدید و تمیز باشد (بدون واریز یا برداشت قبلی) و با همان اطلاعات مدرک شناسایی شما ثبت شده باشد. مدیر تنظیمات کامل را توضیح می‌دهد."),
 ("🎨 طرح‌ها کجا هستند؟", "🎨 <b>طرح‌ها کجا هستند؟</b>\n\nبه‌عنوان شریک، طرح‌های آماده رایگان دریافت می‌کنید — بنر مسابقات، آواتار و پست، به زبان شما و با کد شما. کیت را پس از ثبت‌نام می‌فرستیم."),
 ("🔗 چند کانال؟", "🔗 <b>چند کانال؟</b>\n\nبله — می‌توانید با کد خود در چند پلتفرم تبلیغ کنید."),
 ("🎮 حساب دمو چیست؟", "🎮 <b>حساب دمو چیست؟</b>\n\nموجودی تمرینی که با آوردن ۲۰ ثبت‌نام همراه واریزی باز می‌شود؛ با ۲۰ ثبت‌نام جدید + یک هفته صبر دوباره شارژ می‌شود (به حساب جدید 1xBet نیاز دارد). مدیر توضیح می‌دهد."),
 ("💬 هنوز سوال دارید؟", "💬 <b>هنوز سوال دارید؟</b>\n\nبرای ثبت‌نام روی «شریک شوید» بزنید یا مستقیم به مدیر پیام دهید — سریع پاسخ می‌دهیم. 🚀"),
],
"es": [
 ("💰 ¿Es gratis?", "💰 <b>¿Es gratis unirse?</b>\n\nSí — unirte como socio es 100% gratis. Sin inversión, sin riesgo."),
 ("🚀 ¿Cómo empiezo?", "🚀 <b>¿Cómo empiezo?</b>\n\nRegístrate como socio (gratis), luego envía todos tus datos en un solo mensaje — nombre completo, correo, el código promocional que quieres y tu teléfono — y el mánager te configura.\n\nConsejo: toca «Hazte socio» aquí y el bot lo recoge paso a paso."),
 ("📈 ¿Cuánto puedo ganar?", "📈 <b>¿Cuánto puedo ganar?</b>\n\nComisión de por vida — empiezas con 25% y subes hasta 40% según tus resultados mensuales. Sin límite."),
 ("🌐 ¿Necesito web?", "🌐 <b>¿Necesito un sitio web?</b>\n\nNo. Un canal de Telegram, página de Facebook, TikTok o cualquier audiencia activa sirve — incluso una comunidad pequeña y activa."),
 ("💵 Opciones de retiro", "💵 <b>Opciones de retiro</b>\n\nPuedes retirar desde $30.\n\n• Tus primeros 3 retiros van a tu cuenta 1xBet.\n• Después puedes retirar a Binance o cualquier wallet.\n\nLa cuenta 1xBet debe ser nueva y limpia (sin depósitos ni retiros previos) y registrada con los mismos datos de tu identificación. El mánager explica todo."),
 ("🎨 ¿Dónde están los diseños?", "🎨 <b>¿Dónde están los diseños?</b>\n\nComo socio recibes diseños listos gratis — banners de partidos, avatares y publicaciones, en tu idioma con tu código. Enviamos el kit tras tu registro."),
 ("🔗 ¿Varios canales?", "🔗 <b>¿Varios canales?</b>\n\nSí — puedes promocionar con tu código en varias plataformas."),
 ("🎮 ¿Qué es la cuenta demo?", "🎮 <b>¿Qué es la cuenta demo?</b>\n\nUn saldo de práctica que desbloqueas trayendo 20 registros con depósito; recargable con 20 más + 1 semana de espera (requiere una cuenta 1xBet nueva). El mánager te explica."),
 ("💬 ¿Aún tienes dudas?", "💬 <b>¿Aún tienes dudas?</b>\n\nToca «Hazte socio» para registrarte, o escribe al mánager — respondemos rápido. 🚀"),
],
}


# ---------------- Referral / Sub-manager (Ref 3%) ----------------
BTN_REFER = {"en": "🤝 Refer & earn 3%", "ar": "🤝 كن مديرًا فرعيًا (3%)", "fr": "🤝 Parraine & gagne 3%", "fa": "🤝 مدیر فرعی شوید (۳٪)", "es": "🤝 Refiere y gana 3%"}

REFER_TEXT = {
"en": "🤝 <b>Become a sub-manager — earn 3%</b>\n\nRefer other affiliates with your personal referral link and earn from their results too.\n\n<b>Your tasks as a sub-manager:</b>\n✅ Register anyone who wants a promo code through your referral link\n✅ Help your sub-affiliate link their account and support them when needed\n\n<b>Your earnings:</b>\n💰 <b>RS 25%</b> — from players' profit\n💜 <b>Ref 3%</b> — from your sub-affiliates' profit\n(Base commission + a share from every sub-affiliate.)\n\n📹 Here's how to get your personal referral link from your 1x.partners account:",
"ar": "🤝 <b>كن مديرًا فرعيًا — اربح 3%</b>\n\nأحِل وكلاء آخرين عبر رابط الإحالة الخاص بك واربح من نتائجهم أيضًا.\n\n<b>مهامك كمدير فرعي:</b>\n✅ تسجيل أي شخص يريد الحصول على بروموكود عبر رابط الإحالة الخاص بك\n✅ مساعدة الوكيل الفرعي في ربط حسابه وتقديم الدعم عند الحاجة\n\n<b>أرباحك:</b>\n💰 <b>RS 25%</b> — من أرباح اللاعبين\n💜 <b>Ref 3%</b> — من أرباح الوكلاء الفرعيين\n(العمولة الأساسية + نسبة من كل وكيل فرعي.)\n\n📹 إليك كيفية الحصول على رابط الإحالة الخاص بك من حساب 1x.partners:",
"fr": "🤝 <b>Deviens sous-manager — gagne 3%</b>\n\nParraine d'autres affiliés avec ton lien personnel et gagne aussi sur leurs résultats.\n\n<b>Tes tâches en tant que sous-manager :</b>\n✅ Inscrire toute personne voulant un code promo via ton lien de parrainage\n✅ Aider ton sous-affilié à lier son compte et le soutenir si besoin\n\n<b>Tes gains :</b>\n💰 <b>RS 25%</b> — sur les profits des joueurs\n💜 <b>Ref 3%</b> — sur les profits de tes sous-affiliés\n(Commission de base + une part de chaque sous-affilié.)\n\n📹 Voici comment obtenir ton lien de parrainage depuis ton compte 1x.partners :",
"fa": "🤝 <b>مدیر فرعی شوید — ۳٪ درآمد</b>\n\nنمایندگان دیگر را با لینک دعوت شخصی خود معرفی کنید و از نتایج آن‌ها هم درآمد داشته باشید.\n\n<b>وظایف شما به‌عنوان مدیر فرعی:</b>\n✅ ثبت هر کسی که کد پرومو می‌خواهد از طریق لینک دعوت شما\n✅ کمک به نماینده فرعی برای اتصال حساب و پشتیبانی در صورت نیاز\n\n<b>درآمد شما:</b>\n💰 <b>RS 25%</b> — از سود بازیکنان\n💜 <b>Ref 3%</b> — از سود نمایندگان فرعی\n(کمیسیون پایه + سهمی از هر نماینده فرعی.)\n\n📹 نحوه دریافت لینک دعوت شخصی از حساب 1x.partners:",
"es": "🤝 <b>Conviértete en submánager — gana 3%</b>\n\nRefiere a otros afiliados con tu enlace personal y gana también de sus resultados.\n\n<b>Tus tareas como submánager:</b>\n✅ Registrar a cualquiera que quiera un código promocional con tu enlace de referido\n✅ Ayudar a tu subafiliado a vincular su cuenta y darle soporte cuando lo necesite\n\n<b>Tus ganancias:</b>\n💰 <b>RS 25%</b> — del beneficio de los jugadores\n💜 <b>Ref 3%</b> — del beneficio de tus subafiliados\n(Comisión base + una parte de cada subafiliado.)\n\n📹 Así obtienes tu enlace de referido desde tu cuenta 1x.partners:",
}
