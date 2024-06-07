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
                showComments('negative');
                $('.filter-btn').removeClass('btn-primary').addClass('btn-secondary');
                $('.filter-btn[data-filter="negative"]').removeClass('btn-secondary').addClass('btn-primary');
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
});

function showComments(filter) {
    let resultsDiv = $('#results');
    resultsDiv.empty();

    const commentCategories = {
        'negative': 'negative_comments',
        'criticism': 'criticism_comments',
        'donation': 'donation_comments',
        'positive': 'positive_comments',
        'neutral': 'neutral_comments',
        'all': 'all_comments'
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

function getBadgeColor(category) {
    switch (category) {
        case 'negative': return 'bg-danger';
        case 'criticism': return 'bg-warning';
        case 'donation': return 'bg-info';
        case 'positive': return 'bg-success';
        case 'neutral': return 'bg-secondary';
        default: return 'bg-secondary'; // Tanınmayan kategoriler için varsayılan renk
    }
}

function getType(category) {
    switch (category) {
        case 'negative': return 4;
        case 'criticism': return 2;
        case 'donation': return 3;
        case 'positive': return 1;
        case 'neutral': return 0;
        default: return 0; // Tanınmayan kategoriler için varsayılan renk
    }
}

function getBadgeText(category) {
    switch (category) {
        case 'negative': return 'Olumsuz';
        case 'criticism': return 'Eleştiri/Soru';
        case 'donation': return 'Bağış';
        case 'positive': return 'Olumlu';
        case 'neutral': return 'Normal';
        default: return 'Normal'; // Tanınmayan kategoriler için varsayılan metin
    }
}

function getTextByType(type) {
    switch (type) {
        case 4: return 'Olumsuz';
        case 2: return 'Eleştiri/Soru';
        case 3: return 'Bağış';
        case 1: return 'Olumlu';
        case 0: return 'Normal';
        default: return 'Normal'; // Tanınmayan kategoriler için varsayılan metin
    }
}