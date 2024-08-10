$(document).ready(function () {
    const models = [
        {
            name: 'SVC Modeli',
            details: 'Başarı: %91 - Hız: 2800 yorum için 14 sn'
        },
        {
            name: 'Transformance Modeli',
            details: 'Başarı: %95 - Hız: 2800 yorum için 13 dk'
        },
    ];

    const modelSelect = $('#modelSelect');

    models.forEach(function (model, index) {
        modelSelect.append(new Option(model.name, index));
    });

    modelSelect.on('change', function () {
        const selectedIndex = $(this).val();
        if (selectedIndex !== null && selectedIndex !== "") {
            const selectedModel = models[selectedIndex];
            $('#modelName').text(selectedModel.name);
        }
    });
});