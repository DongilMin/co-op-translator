<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "0788d7ebe4876c9be89132f48e09b26d",
  "translation_date": "2025-06-12T12:22:35+00:00",
  "source_file": "getting_started/troubleshooting.md",
  "language_code": "ar"
}
-->
# دليل استكشاف أخطاء مترجم Microsoft Co-op وإصلاحها

## نظرة عامة  
يُعد مترجم Microsoft Co-Op أداة قوية لترجمة مستندات Markdown بسلاسة. سيساعدك هذا الدليل في حل المشكلات الشائعة التي قد تواجهها عند استخدام الأداة.

## المشكلات الشائعة والحلول

### 1. مشكلة في علامة Markdown  
**المشكلة:** يتضمن مستند Markdown المترجم علامة `markdown` في الأعلى، مما يسبب مشاكل في العرض.

**الحل:** لحل هذه المشكلة، ببساطة احذف علامة `markdown` الموجودة في أعلى الملف. هذا سيسمح بعرض ملف Markdown بشكل صحيح.

**الخطوات:**  
1. افتح ملف Markdown المترجم (`.md`).  
2. حدد موقع علامة `markdown` في أعلى المستند.  
3. احذف علامة `markdown`.  
4. احفظ التغييرات في الملف.  
5. أعد فتح الملف للتأكد من عرضه بشكل صحيح.

### 2. مشكلة روابط الصور المضمنة  
**المشكلة:** روابط الصور المضمنة لا تتطابق مع لغة المستند، مما يؤدي إلى ظهور الصور بشكل غير صحيح أو عدم ظهورها.

**الحل:** تحقق من روابط الصور المضمنة وتأكد من تطابقها مع لغة المستند. جميع الصور موجودة في مجلد `translated_images` وكل صورة تحتوي على علامة لغة في اسم ملف الصورة.

**الخطوات:**  
1. افتح مستند Markdown المترجم.  
2. حدد الصور المضمنة وروابطها.  
3. تحقق من تطابق علامة اللغة في اسم ملف الصورة مع لغة المستند.  
4. حدّث الروابط إذا لزم الأمر.  
5. احفظ التغييرات وأعد فتح المستند للتأكد من عرض الصور بشكل صحيح.

### 3. دقة الترجمة  
**المشكلة:** المحتوى المترجم غير دقيق أو يحتاج إلى تحرير إضافي.

**الحل:** راجع المستند المترجم وقم بإجراء التعديلات اللازمة لتحسين الدقة وسهولة القراءة.

**الخطوات:**  
1. افتح المستند المترجم.  
2. راجع المحتوى بعناية.  
3. أجرِ التعديلات اللازمة لتحسين دقة الترجمة.  
4. احفظ التغييرات.

### 4. مشاكل تنسيق الملف  
**المشكلة:** تنسيق المستند المترجم غير صحيح. قد تحدث هذه المشكلة في الجداول، وهنا سيعالج ``` are added.

**Solution:** Adjust the formatting of the document to match the original structure. Simply deleting the ``` مشاكل الجداول.

**الخطوات:**  
1. افتح المستند المترجم.  
2. قارن بينه وبين المستند الأصلي لتحديد مشاكل التنسيق.  
3. عدّل التنسيق ليطابق المستند الأصلي.  
4. احفظ التغييرات.

**تنويه**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الرسمي والمعتمد. بالنسبة للمعلومات الحساسة أو الهامة، يُنصح بالاعتماد على الترجمة الاحترافية البشرية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.