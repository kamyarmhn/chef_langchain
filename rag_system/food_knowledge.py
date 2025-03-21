"""
Food knowledge base for the RAG system.
"""
from langchain.schema import Document
from rag_system.persian_recipes import PERSIAN_RECIPES

FOOD_KNOWLEDGE = PERSIAN_RECIPES + [
    Document(
        page_content="""
        پیتزا مارگاریتا
        
        مواد لازم:
        - خمیر پیتزا: ۱ عدد
        - گوجه فرنگی سان مارزانو: ۴۰۰ گرم
        - موزارلا تازه: ۲۰۰ گرم
        - ریحان تازه: ۱۰-۱۲ برگ
        - روغن زیتون: ۲ قاشق غذاخوری
        - نمک و فلفل: به مقدار لازم
        
        دستور پخت:
        ۱. فر را روی ۲۶۰ درجه سانتیگراد گرم کنید
        ۲. خمیر را پهن کنید
        ۳. گوجه‌های له شده را پخش کنید
        ۴. موزارلا را روی آن قرار دهید
        ۵. به مدت ۱۰-۱۲ دقیقه در فر بپزید
        ۶. ریحان تازه و روغن زیتون را اضافه کنید
        
        ارزش غذایی (در هر ۱۰۰ گرم):
        - کالری: ۲۶۶
        - پروتئین: ۱۱ گرم
        - کربوهیدرات: ۳۳ گرم
        - چربی: ۱۲ گرم
        """,
        metadata={"source": "دستورات بین‌المللی", "category": "Main Dish"}
    ),
    Document(
        page_content="""
        سوشی کلاسیک
        
        مواد لازم:
        - برنج سوشی: ۲ پیمانه
        - جلبک نوری: ۴ برگ
        - ماهی تن تازه: ۲۰۰ گرم
        - آووکادو: ۱ عدد
        - خیار: ۱ عدد
        - سس سویا: برای سرو
        - واسابی: برای سرو
        
        دستور پخت:
        ۱. برنج سوشی را بپزید
        ۲. جلبک را روی حصیر بامبو قرار دهید
        ۳. برنج را روی جلبک پخش کنید
        ۴. ماهی و سبزیجات را اضافه کنید
        ۵. محکم رول کنید
        ۶. به قطعات کوچک برش دهید
        
        ارزش غذایی (در هر ۱۰۰ گرم):
        - کالری: ۱۵۰
        - پروتئین: ۵ گرم
        - کربوهیدرات: ۳۰ گرم
        - چربی: ۲ گرم
        """,
        metadata={"source": "دستورات بین‌المللی", "category": "Main Dish"}
    ),
    Document(
        page_content="""
        نکات مهم تغذیه سالم
        
        ۱. رژیم متعادل:
        - مصرف همه گروه‌های غذایی
        - تنوع در غذاها
        - کنترل اندازه وعده‌ها
        
        ۲. روش‌های پخت:
        - کباب کردن
        - بخارپز کردن
        - پخت در فر
        - تفت دادن
        
        ۳. نکات تغذیه‌ای:
        - مصرف بیشتر سبزیجات
        - انتخاب غلات کامل
        - محدود کردن غذاهای فرآوری شده
        - نوشیدن آب کافی
        
        ۴. برنامه‌ریزی غذایی:
        - برنامه‌ریزی از قبل
        - پخت در حجم زیاد
        - نگهداری صحیح
        - استفاده از مواد تازه
        """,
        metadata={"source": "راهنمای سلامت", "category": "Tips"}
    ),
    Document(
        page_content="""
        راهنمای روش‌های پخت
        
        ۱. روش‌های حرارت خشک:
        - کباب کردن
        - بریان کردن
        - پخت در فر
        - تفت دادن
        
        ۲. روش‌های حرارت مرطوب:
        - جوشاندن
        - بخارپز کردن
        - پخت ملایم
        - خورشتی کردن
        
        ۳. روش‌های ترکیبی:
        - خورشتی کردن
        - خورش
        - پخت در قابلمه
        
        ۴. روش‌های خاص:
        - سرخ کردن عمیق
        - تفت دادن سریع
        - دودی کردن
        - پخت در خلاء
        """,
        metadata={"source": "راهنمای آشپزی", "category": "Techniques"}
    ),
    Document(
        page_content="""
        پاستا کاربونارا
        
        مواد لازم:
        - اسپاگتی: ۴۰۰ گرم
        - گوشت خوک نمک‌سود: ۲۰۰ گرم
        - تخم مرغ: ۴ عدد
        - پنیر پکورینو: ۱۰۰ گرم
        - فلفل سیاه: به مقدار لازم
        - نمک: به مقدار لازم
        
        دستور پخت:
        ۱. پاستا را در آب نمک بپزید
        ۲. گوشت را تا ترد شدن تفت دهید
        ۳. تخم مرغ و پنیر را مخلوط کنید
        ۴. همه مواد را ترکیب کنید
        ۵. در صورت نیاز آب پاستا را اضافه کنید
        
        ارزش غذایی (در هر ۱۰۰ گرم):
        - کالری: ۴۵۰
        - پروتئین: ۱۵ گرم
        - کربوهیدرات: ۴۵ گرم
        - چربی: ۲۵ گرم
        """,
        metadata={"source": "دستورات بین‌المللی", "category": "Main Dish"}
    )
] 