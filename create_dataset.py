import csv
import random

random.seed(42)

sentences = [
    "السلام عليكم ورحمة الله وبركاته",
    "أحب تعلم البرمجة وتطوير البرامج",
    "جامعة الإمام الأعظم تضم أقساماً علمية",
    "علوم الحاسبات مجال واسع وممتع",
    "أدرس الذكاء الاصطناعي وتعلم الآلة",
    "اللغة العربية لغة جميلة وغنية",
    "أعمل على تطوير مشروع تخرج جديد",
    "أهمية الأمن الرقمي تزداد كل يوم",
    "تساعد الحاسبة في معالجة البيانات",
    "تحليل النصوص يساعد على اكتشاف الأنماط",
    "التكنولوجيا تسهل التواصل بين الناس",
    "أتعلم لغة بايثون في هذا الفصل",
    "البيانات مهمة في بناء النماذج الذكية",
    "يستخدم الباحثون الحاسوب لتحليل المعلومات",
    "أحب قراءة الكتب العلمية المفيدة",
    "الشبكات تربط الأجهزة لتبادل المعلومات",
    "التعلم المستمر يساعد على النجاح",
    "أدرس قواعد البيانات في الجامعة",
    "تطوير البرمجيات يحتاج إلى تخطيط",
    "الأمن السيبراني يحمي المعلومات الرقمية",
    "تساعد الخوارزميات على حل المشكلات",
    "الذكاء الاصطناعي من التقنيات الحديثة",
    "النص العربي يحتوي على حروف متنوعة",
    "تحليل البيانات يساعد في اتخاذ القرارات",
    "أستخدم بايثون لتنفيذ التجارب البرمجية",
    "يحتاج المشروع إلى اختبار وتقييم",
    "تساعد البرمجة على التفكير المنطقي",
    "إخفاء البيانات موضوع مهم في الأمن",
    "أعمل على تحليل النصوص العربية",
    "التجارب العملية توضح نتائج البحث"
]


def add_tatweel(text):
    chars = list(text)

    for i, char in enumerate(chars):
        if "\u0600" <= char <= "\u06ff" and char.isalpha():
            chars.insert(i + 1, "ـ")
            return "".join(chars)

    return text


def add_zero_width(text):
    middle = len(text) // 2
    return text[:middle] + "\u200b" + text[middle:]


rows = []

for index, sentence in enumerate(sentences):
    rows.append({
        "text": sentence,
        "label": 0,
        "technique": "normal",
        "base_id": index
    })

    rows.append({
        "text": add_tatweel(sentence),
        "label": 1,
        "technique": "tatweel",
        "base_id": index
    })

    rows.append({
        "text": add_zero_width(sentence),
        "label": 1,
        "technique": "zero_width",
        "base_id": index
    })


random.shuffle(rows)

with open("arabic_dataset.csv", "w", encoding="utf-8-sig", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["text", "label", "technique", "base_id"]
    )
    writer.writeheader()
    writer.writerows(rows)

print("Dataset created successfully!")
print("Total samples:", len(rows))
print("Normal samples:", sum(row["label"] == 0 for row in rows))
print("Suspicious samples:", sum(row["label"] == 1 for row in rows))
