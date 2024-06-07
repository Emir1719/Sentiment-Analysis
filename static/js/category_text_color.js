function getBadgeColor(category) {
    switch (category) {
        case 'negative_comments': return 'bg-danger';
        case 'criticism_comments': return 'bg-warning';
        case 'donation_comments': return 'bg-dark';
        case 'positive_comments': return 'bg-success';
        case 'neutral_comments': return 'bg-secondary';
        default: return 'bg-secondary'; // Tanınmayan kategoriler için varsayılan renk
    }
}

function getBadgeText(category) {
    switch (category) {
        case 'negative_comments': return 'Olumsuz';
        case 'criticism_comments': return 'Eleştiri/Soru';
        case 'donation_comments': return 'Bağış';
        case 'positive_comments': return 'Olumlu';
        case 'neutral_comments': return 'Normal';
        default: return 'Yorum'; // Tanınmayan kategoriler için varsayılan metin
    }
}