// 首页搜索功能
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const searchBtn = document.getElementById('search-btn');
    const statusFilter = document.getElementById('status-filter');
    const dateFilter = document.getElementById('date-filter');
    const logisticsCards = document.querySelectorAll('.logistics-card');
    const noResults = document.getElementById('no-results');

    function filterCards() {
        const searchTerm = searchInput.value.toLowerCase();
        const status = statusFilter.value;
        const date = dateFilter.value;
        let visibleCount = 0;

        logisticsCards.forEach(card => {
            const trackingId = card.dataset.trackingId.toLowerCase();
            const cardStatus = card.dataset.status;
            let showCard = true;

            // 搜索过滤
            if (searchTerm && !trackingId.includes(searchTerm)) {
                showCard = false;
            }

            // 状态过滤
            if (status && cardStatus !== status) {
                showCard = false;
            }

            // 日期过滤（简化逻辑，实际应根据数据中的日期处理）
            if (date) {
                // 这里需要根据实际数据中的日期字段进行过滤
                showCard = false; // 简化处理，实际项目中需要完善
            }

            card.style.display = showCard ? 'block' : 'none';
            if (showCard) visibleCount++;
        });

        // 显示/隐藏无结果提示
        noResults.classList.toggle('hidden', visibleCount > 0);
    }

    searchInput.addEventListener('input', filterCards);
    searchBtn.addEventListener('click', filterCards);
    statusFilter.addEventListener('change', filterCards);
    dateFilter.addEventListener('change', filterCards);

    // 按Enter键搜索
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            filterCards();
        }
    });

    // 详情页返回顶部功能
    if (window.location.pathname !== 'index.html') {
        const timelineContainer = document.querySelector('.timeline-container');
        if (timelineContainer) {
            const backToTopBtn = document.createElement('button');
            backToTopBtn.className = 'back-to-top';
            backToTopBtn.innerHTML = '<i class="fa fa-arrow-up" aria-hidden="true"></i> 回到顶部';
            backToTopBtn.style.position = 'fixed';
            backToTopBtn.style.bottom = '20px';
            backToTopBtn.style.right = '20px';
            backToTopBtn.style.padding = '10px 15px';
            backToTopBtn.style.background = '#1976d2';
            backToTopBtn.style.color = 'white';
            backToTopBtn.style.border = 'none';
            backToTopBtn.style.borderRadius = '4px';
            backToTopBtn.style.cursor = 'pointer';
            backToTopBtn.style.display = 'none';
            backToTopBtn.style.zIndex = '100';
            
            document.body.appendChild(backToTopBtn);
            
            window.addEventListener('scroll', function() {
                if (window.pageYOffset > 300) {
                    backToTopBtn.style.display = 'block';
                } else {
                    backToTopBtn.style.display = 'none';
                }
            });
            
            backToTopBtn.addEventListener('click', function() {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }
});