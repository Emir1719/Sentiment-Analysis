$(document).ready(function () {
    $('.progress').hide(); // Progress bar başlangıçta gizli

    $('#commentForm').on('submit', function (event) {
        event.preventDefault();
        let resultsDiv = $('#results');
        resultsDiv.empty();
        $('.progress').show(); // Progress bar'ı göster

        $.ajax({
            url: '/analyze',
            method: 'POST',
            data: $(this).serialize(),
            success: function (response) {
                $('.progress').hide();
                // Yorumları kaydet
                window.comments = response;

                // Başlangıçta olumsuzlar gösterilsin
                showComments('criticism');
                $('.filter-btn').removeClass('btn-primary').addClass('btn-secondary');
                $('.filter-btn[data-filter="criticism"]').removeClass('btn-secondary').addClass('btn-primary');
            },
            error: function () {
                $('.progress').hide(); // Hata durumunda progress bar'ı gizle
                alert("Yorumlar yüklenirken bir hata oluştu.");
            }
        });
    });

    // Filtreleme butonları için olay dinleyicileri
    $('.filter-btn').on('click', function () {
        $('.filter-btn').removeClass('btn-primary').addClass('btn-secondary');
        $(this).removeClass('btn-secondary').addClass('btn-primary');
        let filter = $(this).data('filter');
        showComments(filter);
    });

    // Kopyalama butonu için olay dinleyicisi
    $('#copyButton').on('click', function () {
        let filter = $('.filter-btn.btn-primary').data('filter');
        copyComments(filter);
    });
});

function showComments(filter) {
    let resultsDiv = $('#results');
    resultsDiv.empty();

    const commentCategories = {
        'criticism': 'criticism_comments',
        'donation': 'donation_comments',
        'positive': 'positive_comments',
    };

    let commentsToShow = commentCategories[filter] ? window.comments[commentCategories[filter]] : window.comments['all_comments'];
    $('#commentCount').text(`Yorum Sayısı: ${commentsToShow.length}`);

    commentsToShow.forEach(comment => {
        let badgeColor = getBadgeColor(filter);
        let badgeText = getBadgeText(filter);
        resultsDiv.append(`
            <div class="card mb-3">
                <div class="card-body">
                    <p class="card-text">${comment.text}</p>
                    <span class="badge ${badgeColor}">${badgeText}</span>
                    <a href="${comment.link}" target="_blank"><span class="badge bg-primary">Link</span></a>
                </div>
            </div>
        `);
    });
}

function copyComments(filter) {
    const commentCategories = {
        'criticism': 'criticism_comments',
        'donation': 'donation_comments',
        'positive': 'positive_comments',
        'all': 'all_comments'
    };

    let commentsToCopy = commentCategories[filter] ? window.comments[commentCategories[filter]] : window.comments['all_comments'];
    let textToCopy = commentsToCopy.map(comment => comment.text).join('\n');

    // Text'i kopyalama
    navigator.clipboard.writeText(textToCopy).then(() => {
        alert('Yorumlar kopyalandı.');
    }).catch(err => {
        alert('Yorumlar kopyalanırken bir hata oluştu.');
    });
}

function getBadgeColor(category) {
    switch (category) {
        case 'criticism': return 'bg-danger';
        case 'donation': return 'bg-info';
        case 'positive': return 'bg-success';
        default: return 'bg-success'; // Tanınmayan kategoriler için varsayılan renk
    }
}

function getType(category) {
    switch (category) {
        case 'criticism': return 2;
        case 'donation': return 3;
        case 'positive': return 1;
        default: return 1; // Tanınmayan kategoriler için varsayılan renk
    }
}

function getBadgeText(category) {
    switch (category) {
        case 'criticism': return 'Olumsuz/Soru';
        case 'donation': return 'Bağış';
        case 'positive': return 'Olumlu';
        default: return 'Olumlu'; // Tanınmayan kategoriler için varsayılan metin
    }
}

function getTextByType(type) {
    switch (type) {
        case 2: return 'Olumsuz/Soru';
        case 3: return 'Bağış';
        case 1: return 'Olumlu';
        default: return 'Olumlu'; // Tanınmayan kategoriler için varsayılan metin
    }
}