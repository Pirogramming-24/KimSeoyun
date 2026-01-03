// =======================
//  정렬 Select
// =======================
const sortSelect = document.getElementById('sortSelect');
if (sortSelect){
    sortSelect.addEventListener('change', function() {
        const sortValue = this.value;
        const url = new URL(window.location.href);

        if(sortValue){
            url.searchParams.set('sort', sortValue);
        } else {
            url.searchParams.delete('sort');
        }

        url.searchParams.set('page', 1); 
        window.location.href = url.toString();
    });
}


// =======================
//  관심도 (+ / -)
// =======================
document.querySelectorAll('.interest-btn').forEach(button => {
    button.addEventListener('click', function(event){
        event.preventDefault();

        const action = this.getAttribute('data-action');
        const li = this.closest('li[data-idea-id]');
        if(!li) return;

        const ideaId = li.getAttribute('data-idea-id');
        const interestValueSpan = li.querySelector('.interest-value');

        fetch(`${ideaId}/change_interest/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `action=${action}`
        })
        .then(response => response.json())
        .then(data => {
            if(data.interest !== undefined){
                interestValueSpan.textContent = data.interest;
            } else if(data.error){
                alert(data.error);
            }
        })
        .catch(err => {
            alert('오류가 발생했습니다.');
            console.error(err);
        });
    });
});


// =======================
//  ⭐ 리스트 & 디테일 공통 별 토글
// =======================
document.querySelectorAll('.star-btn').forEach(button => {

    button.addEventListener('click', function(event){
        event.preventDefault();
        event.stopPropagation();

        const btn = this;
        const url = this.dataset.url;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(res => res.json())
        .then(data => {
            if(data.starred){
                btn.classList.add('starred');
            } else {
                btn.classList.remove('starred');
            }
        })
        .catch(() => alert("별 업데이트 실패"));
    });

});



// =======================
//  CSRF
// =======================
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i=0; i<cookies.length; i++){
            const cookie = cookies[i].trim();
            if(cookie.startsWith(name + '=')){
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
