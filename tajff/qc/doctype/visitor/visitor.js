frappe.ready(function() {
    // إضافة تأثيرات تفاعلية للحقول
    $('.form-field input, .form-field textarea, .form-field select').focus(function() {
        $(this).closest('.form-field').addClass('field-focused');
    }).blur(function() {
        $(this).closest('.form-field').removeClass('field-focused');
    });
    
    // إضافة رسالة تأكيد قبل الإرسال
    $('form').on('submit', function(e) {
        if (!confirm('هل أنت متأكد من صحة المعلومات المدخلة؟')) {
            e.preventDefault();
        }
    });
    
    // إضافة تأثيرات للأسئلة الصحية
    $('.question-item').click(function() {
        $(this).toggleClass('question-selected');
        $(this).find('input[type="checkbox"]').prop('checked', 
            $(this).hasClass('question-selected'));
    });
    
    // تحسين ظهور/اختفاء الحقول المشروطة
    $('input[data-fieldname="ill"]').change(function() {
        const isChecked = $(this).prop('checked');
        $('.conditional-section').slideToggle(isChecked);
    }).trigger('change');
    
    // إضافة شعار أو صورة للصفحة
    $('.registration-header').prepend(
        '<div class="logo-container" style="text-align: center; margin-bottom: 20px;">' +
        '<img src="/assets/custom_app/images/visitor-logo.png" alt="Visitor Registration" style="height: 80px;">' +
        '</div>'
    );
});